
from .emulated_disk import EmulatedDisk
from .open_file_table import OFT
from .directory import Directory
from .exceptions import Exceptions
from .buffer import Buffer

class FileSystem:
    def __init__(self):
        self.ED     = EmulatedDisk(64, 512)
        self.OFT    = OFT()
        self.DIR    = Directory()
        self.B      = Buffer(512)

        self.current_OFT_entry = -1
        print("system initialized")


    def create(self, name: str) -> None:

        try:
            self.DIR.search_directory_if_not_exists(name) 
            free_entry = self.ED.search_for_free_file_descriptor()
            self.ED.set_size_field_to_empty(free_entry)
            free_directory = self.DIR.search_free_directory()
            self.DIR.add_to_directory(name, free_entry, free_directory)
            print(f"{name} created")
        except Exceptions.FileExists:
            print("error")
        except Exceptions.TooManyFiles:
            print("error")
        except Exceptions.NoFreeDirectory:
            print("error")


    def destroy(self, name: str) -> None:

        try:
            index = self.DIR.search_directory_if_exists(name)
            descriptor_index = self.DIR.get_file_descriptor_index(index)
            self.ED.reset_bitmap_with_block_numbers(descriptor_index)
            self.ED.reset_file_descriptor(descriptor_index)
            self.ED.set_size_field_to_free(descriptor_index)
            self.DIR.remove_from_directory(index)
            print(f"{name} destroyed")
        except Exceptions.FileDoesNotExist:
            print("error")


    def open(self, name: str) -> None:
        try:
            open_directory_index = self.DIR.search_directory_if_exists(name)
            file_descriptor_index = self.DIR.get_file_descriptor_index(open_directory_index)
            self.OFT.check_if_file_is_open(file_descriptor_index)
            
            self.current_OFT_entry = self.OFT.search_for_free_oft()
            self.OFT.set_current_position(self.current_OFT_entry, 0)

            # file_descriptor_index = self.DIR.get_file_descriptor_index(open_directory_index)
            file_descriptor_size = self.ED.get_size_from_file_descriptor(file_descriptor_index)
            self.OFT.set_file_size(self.current_OFT_entry, file_descriptor_size)

            self.OFT.set_file_descriptor_index(self.current_OFT_entry, file_descriptor_index)
            
            if file_descriptor_size == 0:
                free_bitmap = self.ED.search_bitmap_for_free_entry()
                self.ED.add_block_index_to_file_descriptor(file_descriptor_index, 1, free_bitmap)
            else:
                first_block_index = self.ED.get_block_index(file_descriptor_index, 0)
                self.OFT.set_read_write_buffer(self.current_OFT_entry, self.ED.D[first_block_index])
            print(f"{name} opened {self.current_OFT_entry}")

        except Exceptions.FileDoesNotExist:
            print("error")
        except Exceptions.TooManyFilesOpen:
            print("error")
        except Exceptions.FileOpenAlready:
            print("error")


    def close(self, file_descriptor_index: int) -> None:
        try:
            self.OFT.check_if_file_can_be_closed(file_descriptor_index)
            oft_entry = self.OFT.find_file_descriptor_index(file_descriptor_index)
            block_number = self.OFT.get_current_position(oft_entry) // 512
            # file_descriptor_index = self.OFT.get_file_descriptor_index(self.current_OFT_entry)
            block_index = self.ED.get_block_index(file_descriptor_index, block_number)

            self.ED.write_to_block(block_index, self.OFT.get_read_write_buffer(oft_entry))
            self.ED.set_size_field(file_descriptor_index, self.OFT.get_file_size(oft_entry))
            self.OFT.reset_read_write_buffer(oft_entry)
            self.OFT.set_current_position(oft_entry, -1)
            self.OFT.set_file_descriptor_index(oft_entry, -1)
            self.OFT.set_file_size(oft_entry, -1)
            print(f"{file_descriptor_index} closed")
        except Exceptions.FileNotOpen:
            print("error")


    def read(self, open_file_i: int, location_m: int, n_bytes: int) -> None:
        try:
            if self.OFT.get_current_position(open_file_i) == -1:
                raise Exceptions.FileNotOpen
            file_descriptor_index = self.OFT.get_file_descriptor_index(open_file_i)
            current_position = self.OFT.get_current_position(open_file_i)
            buffer = ""
            bytes_read = 0
            counter = 0

            while True:
                block = bytes_read // 512
                position = bytes_read % 512

                if bytes_read == n_bytes or bytes_read + current_position == 512 * 3:
                    self.OFT.set_current_position(open_file_i, (block * 512) + position)
                    print(f"{counter} bytes read from {open_file_i}")
                    break
                elif bytes_read + current_position == 512:
                    # Copy the r/w buffer into the appropriate block on disk
                    read_write_buffer = self.OFT.get_read_write_buffer(open_file_i)
                    block_index = self.ED.get_block_index(file_descriptor_index, block - 1)
                    self.ED.write_to_block(block_index, read_write_buffer)

                    # Copy the sequentially next block from the disk into the r/w buffer
                    block_index = self.ED.get_block_index(file_descriptor_index, block)
                    buffer = self.ED.read_from_block(block)
                    self.OFT.set_read_write_buffer(open_file_i, buffer)

                #Continue copying bytes from the r/w buffer into memory until again one of the above events occurs
                buffer = self.OFT.get_read_write_buffer(open_file_i)[current_position + bytes_read]
                if buffer != '':
                    counter += 1
                self.B.write_to_M(buffer, location_m)
                location_m += 1
                bytes_read += 1
        except Exceptions.FileNotOpen:
            print("error")
        


    def write(self, open_file_i: int, location_m: int, n_bytes: int) -> None:

        file_descriptor_index = self.OFT.get_file_descriptor_index(open_file_i)
        current_position = self.OFT.get_current_position(open_file_i)
        temp_current_position = current_position
        size = self.OFT.get_file_size(open_file_i)
        bytes_read = 0
        counter = 0

        while True:
            block = bytes_read // 512
            position = bytes_read % 512
            
            if bytes_read == n_bytes or bytes_read + current_position == 512 * 3:
                if current_position + bytes_read > size:
                    self.OFT.set_file_size(open_file_i, counter + self.OFT.get_file_size(open_file_i))
                    self.OFT.set_current_position(open_file_i, counter + current_position)
                    self.ED.set_size_field(file_descriptor_index, counter + self.ED.get_size_from_file_descriptor(file_descriptor_index))
                print(f"{counter} bytes written to {open_file_i}")
                break
            elif bytes_read + current_position == 512:
                # Copy the r/w buffer into the appropriate block on disk
                read_write_buffer = self.OFT.get_read_write_buffer(open_file_i)
                block_index = self.ED.get_block_index(file_descriptor_index, block - 1)
                self.ED.write_to_block(block_index, read_write_buffer)

                # Copy the sequentially next block from the disk into the r/w buffer
                if block != 0:
                    block_index = self.ED.get_block_index(file_descriptor_index, block)
                    buffer = self.ED.read_from_block(block)
                    self.OFT.set_read_write_buffer(open_file_i, buffer)
                else:
                    free_bitmap_index = self.ED.search_bitmap_for_free_entry()
                    self.ED.add_block_index_to_file_descriptor(file_descriptor_index, block, free_bitmap_index)
                    self.ED.set_bitmap_entry_to_occupied(free_bitmap_index)


            if self.B.read_block(location_m) == '':
                pass
            else:
                self.OFT.set_read_write_buffer_with_position(open_file_i, temp_current_position + bytes_read, self.B.read_block(location_m))
                counter += 1
            bytes_read += 1
            location_m += 1


    def seek(self, oft_index: int, position: int) -> None:
        try:
            if position > self.OFT.get_file_size(oft_index):
                raise Exceptions.CurrentPositionPastEOF
            
            file_descriptor = self.OFT.get_file_descriptor_index(oft_index)
            current_position = self.OFT.get_current_position(oft_index) // 512
            new_position = position // 512

            if current_position != new_position:
                current_block = self.ED.get_block_index(file_descriptor, current_position)
                self.ED.write_to_block(current_block, self.OFT.get_read_write_buffer(oft_index))
                new_block = self.ED.get.get_block_index(file_descriptor, new_position)
                self.OFT.set_read_write_buffer(oft_index, self.ED.read_from_block(new_block))

            self.OFT.set_current_position(oft_index, position)
            print(f"position is {position}")
        except Exceptions.CurrentPositionPastEOF:
            print("error")


    def directory(self) -> None:

        for i in range(192):
            file_name = self.DIR.get_file_name(i)
            descriptor_index = self.DIR.get_file_descriptor_index(i)
            file_size = self.ED.get_size_from_file_descriptor(descriptor_index)
            if file_name != 0:
                print(f"{file_name} {file_size} ", end='')
        print()


    def read_memeory(self, m_position: int, n_bytes: int) -> None:

        for i in range(m_position, m_position + n_bytes):
            print(self.B.read_block(i), end='')
        print()


    def write_memory(self, m_position: int, s: str) -> None:

        for char in s:
            self.B.write_to_M(char, m_position)
            m_position += 1
        print(f"{m_position} bytes written to M")



if __name__ == "__main__":
    FS = FileSystem()
    # print(FS.OFT.OFT[1])
    # FS.create("test")
    # FS.create("test2")
    # FS.open("test")
    # FS.read(1, 0, 50)
    # FS.seek(1, 0)
    # FS.directory()

    FS.write_memory(0, "abcdefghij")
    FS.create("foo")
    FS.open("foo")
    FS.write(1, 0, 5)
    FS.write(1, 5, 2)
    FS.directory()
    FS.seek(1, 0)
    FS.read(1, 10, 3)
    FS.read_memeory(0, 20)
    FS.close(1)
    FS.directory()
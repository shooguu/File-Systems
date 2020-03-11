from .exceptions import Exceptions
from .directory import Directory

class EmulatedDisk:
    def __init__(self, blocks: int, block_size: int):
        self._num_of_blocks         = blocks
        self._block_size            = block_size
        self._file_descriptor_size  = 6 
        self._file_descriptors      = int(block_size / 16)   # 512 / 16 = 32

        self.D = [['' for _ in range(block_size)] for _ in range(blocks)]
        self._initialize_bitmap()
        self._initialize_file_descriptors()
        self._initialize_directory()

        self.current_file_descriptor = 1


    def _initialize_bitmap(self):
        '''
        Array of B bits (64 bits)
        '''
        self.D[0] = [0 for _ in range(self._num_of_blocks)]

        for i in range(8):
            self.D[0][i] = 1


    def _initialize_file_descriptors(self):
        '''
        -1 indicates that the size field is free.
        [file size, 3 disk block numbers...]
        '''
        for index in range(self._file_descriptor_size):
            self.D[index + 1] = [[-1, 0, 0, 0] for _ in range(self._file_descriptors)]

        self.D[1][0] = [0, 0, 0, 0]


    def _initialize_directory(self):
        '''
        Index 7 is for the directory
        '''
        self.D[7] = "directory"

    
    def _convert_to_row_col(self, i: int) -> (int, int):
        '''
        Converts the given index to row and col form.
        We add 1 because file descriptor index 0 is taken
        for the directory
        '''
        row = (i // 32) + 1
        col = i % 32
        return row, col

    
    def reset_file_descriptor(self, i: int) -> None:
        
        row, col = self._convert_to_row_col(i)
        self.D[row][col] = [-1, 0, 0, 0]


    def reset_bitmap_with_block_numbers(self, i: int) -> None:

        row, col = self._convert_to_row_col(i)
        for index in range(1, 4):
            self.set_bitmap_entry_to_free(self.D[row][col][index])


    def search_for_free_file_descriptor(self) -> (int, int):
        '''
        Searches for the first free size field in the
        file descriptor and returns the index.
        -1 (Free)
        '''
        for i in range(self._file_descriptor_size):
            for j in range(self._file_descriptors):
                if self.D[i + 1][j][0] == -1:
                    return (i * 32) + j
        raise Exceptions.TooManyFiles


    def get_size_from_file_descriptor(self, i: int):
        '''
        Returns the size field of the index i in the file descriptor
        '''
        row, col = self._convert_to_row_col(i)
        return self.D[row][col][0]


    def set_size_field(self, i: int, size: int) -> None:
        row, col = self._convert_to_row_col(i)
        self.D[row][col][0] = size


    def set_size_field_to_empty(self, i: int) -> None:
        '''
        If the file descriptor size field has a free entry,
        change that size field to 0 (empty file)
        '''
        row, col = self._convert_to_row_col(i)
        self.D[row][col][0] = 0


    def set_size_field_to_free(self, i: int) -> None:
        '''
        This sets the file descriptor size to -1 (free)
        '''
        row, col = self._convert_to_row_col(i)
        self.D[row][col][0] = -1


    def search_bitmap_for_free_entry(self) -> int:
        '''
        This function searches for a free block 
        using the bitmap.
        The function returns the index if found
        '''
        for index in range(self._num_of_blocks):
            if self.D[0][index] == 0:
                return index
        raise Exceptions.BitmapFull

    
    def set_bitmap_entry_to_occupied(self, index: int) -> None:
        '''
        This function sets an index in the bitmap to 1 (occupied)
        '''
        self.D[0][index] = 1


    def set_bitmap_entry_to_free(self, index: int) -> None:

        self.D[0][index] = 0


    def add_directory(self, index: int) -> None:
        '''
        Because I created another data structure for the directory, a string
        called directory will take it's place
        '''
        self.D[index] = "directory"


    def add_block_index_to_file_descriptor(self, index: int, block_number: int, block_index: int) -> None:
        '''
        Given an index, the block number in the file
        descriptor will be updated
        '''
        row, col = self._convert_to_row_col(index)
        self.D[row][col][block_number] = block_index


    def get_block_index(self, index: int, block_number: int) -> str:
        '''
        This function returns the first block of the 
        file descriptor given an index
        '''
        row, col = self._convert_to_row_col(index)
        return self.D[row][col][block_number + 1]


    def write_to_block(self, index: int, buffer: str) -> str:
        '''
        This function takes an index and writes the buffer
        to that index block
        '''
        self.D[index] = buffer


    def read_from_block(self, index: int) -> str:
        '''
        Given a index, the function returns the information
        inside the disk
        '''
        return self.D[index]


if __name__ == "__main__":
    # disk = EmulatedDisk(64, 512, 6)
    disk = EmulatedDisk(64, 512)
    print(disk.D[0])
    print(disk.D[7])

    # i, j = disk.search_for_free_entry()
    # disk.set_size_field_to_empty(i, j)
    # print(disk.D[i])
    
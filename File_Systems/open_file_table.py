from .exceptions import Exceptions

class OFT:
    def __init__(self):
        '''
        Creates an Open File Table fixed size array
        [read/write buffer, current position, file size, file descriptor index]
        '''
        self._read_write_buffer     = 0
        self._current_position      = 1
        self._file_size             = 2
        self._file_descriptor_index = 3
        self._buffer_size           = 512

        self.OFT = [[['' for _ in range(self._buffer_size)], -1, -1, -1] for _ in range(4)]
        self.OFT[0] = [0, 0, 0, 0]


    def get_read_write_buffer_with_position(self, index: int, start: int, end: int) -> str:
        '''
        Given a start and end position, the function will return the r/w buffer
        between the start and end
        '''
        return self.OFT[index][self._read_write_buffer][start:end]


    def get_read_write_buffer(self, index: int):
        '''
        Returns index 0 - read/write buffer - of the open file

        ** This is an area of 512 bytes, used to hold the 
        currently accessed block
        '''
        return self.OFT[index][self._read_write_buffer]

    
    def set_read_write_buffer_with_position(self, index: int, position: int, char: str) -> None:

        self.OFT[index][self._read_write_buffer][position] = char


    def set_read_write_buffer(self, index: int, buffer: str) -> None:
        '''
        Given an OFT index, it sets the r/w buffer with the 
        given buffer
        '''
        self.OFT[index][self._read_write_buffer] = buffer


    def reset_read_write_buffer(self, index: int) -> None:
        '''
        Given an OFT index, is resets the r/w buffer to -1
        '''
        self.OFT[index][self._read_write_buffer] = ['' for _ in range(self._buffer_size)]


    def get_current_position(self, index: int):
        '''
        Returns index 1 - current position - of the open file

        ** This maintains the current position within the file and 
        is used by sequential read and write operations; with a 
        maximum file size of 3 blocks, the current position ranges 
        from 0 to 1536.
        ** −1 is used to mark the corresponding OFT entry as free
        '''
        return self.OFT[index][self._current_position]


    def set_current_position(self, index: int, position: int):
        '''
        Sets the current position with the given value
        '''
        self.OFT[index][self._current_position] = position


    def get_file_size(self, index: int):
        '''
        Returns index 2 - file size - of the open file

        ** This is the current size of the file, in bytes; initially, 
        the value is copied from the file descriptor but may 
        increase with each write operation
        '''
        return self.OFT[index][self._file_size]


    def set_file_size(self, index: int, size: int):
        '''
        Sets the current file size with the given value
        '''
        self.OFT[index][self._file_size] = size


    def get_file_descriptor_index(self, index: int):
        '''
        Returns index 3 - file descriptor index - of the open file

        ** This is the index of the file descriptor located on one of 
        the disk blocks D[1] through D[k−1]
        '''
        return self.OFT[index][self._file_descriptor_index]


    def set_file_descriptor_index(self, index: int, file_descriptor_index: int):
        '''
        Sets the file descriptor index with the given value
        '''
        self.OFT[index][self._file_descriptor_index] = file_descriptor_index


    def search_for_free_oft(self):
        '''
        Checks for an open OFT entry. An open OFT is defined as if the 
        position (index 1) is -1
        '''
        for array_index in range(len(self.OFT)):
            if self.OFT[array_index][self._current_position] == -1:
                return array_index
        raise Exceptions.TooManyFilesOpen


    def check_if_file_is_open(self, file_descriptor: int) -> None:

        for oft in self.OFT:
            if oft[self._file_descriptor_index] == file_descriptor:
                raise Exceptions.FileOpenAlready
    

    def check_if_file_can_be_closed(self, file_descriptor: int) -> None:
        flag = False
        for oft in self.OFT:
            if oft[self._file_descriptor_index] == file_descriptor:
                flag = True
        if flag == False:
            raise Exceptions.FileNotOpen


    def find_file_descriptor_index(self, file_descriptor: int) -> None:

        for i in range(len(self.OFT)):
            if self.OFT[i][self._file_descriptor_index] == file_descriptor:
                return i


if __name__ == "__main__":
    oft = OFT()
    print(oft.OFT) 
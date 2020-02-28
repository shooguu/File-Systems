from exceptions import Exceptions

class EmulatedDisk:
    def __init__(self, blocks: int, block_size: int, file_descriptor_size: int):
        self._num_of_blocks         = blocks
        self._block_size            = block_size
        self._file_descriptor_size  = file_descriptor_size

        self.D = [[0 for _ in range(block_size)] for _ in range(blocks)]
        self._initialize_bitmap()
        self._initialize_file_descriptors()

        self.current_file_descriptor = 1


    def _initialize_bitmap(self):
        '''
        Array of B bits (64 bits)
        '''
        self.D[0] = [0 for _ in range(self._num_of_blocks)]


    def _initialize_file_descriptors(self):
        '''
        -1 indicates that the size field is free.
        [file size, 3 disk block numbers...]
        '''
        for index in range(self._file_descriptor_size):
            self.D[index + 1] = [-1, 0, 0, 0]

    def get_file_descriptor_size(self):

        return self.D[self.current_file_descriptor][0]

    def search_for_free_entry(self):
        '''
        Searches for the first free size field in the
        file descriptor and changes the size field from 
        -1 to 0, indicating that the new file is empty.
        Return -1 means there are too many files in the descriptor,
        return 1 means it has successfully found available space.
        '''
        for index in range(self._file_descriptor_size):
            if self.D[index + 1][0] == -1:
                self._set_size_field_to_empty(index + 1)
        raise Exceptions.TooManyFiles

    def _set_size_field_to_empty(self, index: int):
        '''
        If the file descriptor size field has a free entry,
        change that size field to 0 (empty file).
        '''
        self.D[index][0] = 0

if __name__ == "__main__":
    disk = EmulatedDisk(64, 512, 6)
    print(disk.D[1])
    print(disk.search_for_free_entry())

class EmulatedDisk:
    def __init__(self, blocks, block_size):
        self.D = [[0 for _ in range(block_size)] for _ in range(blocks)]
        self._initialize_bitmap(blocks)
        self._initialize_file_descriptors()


    def _initialize_bitmap(self, blocks):
        '''
        Array of B bits (64 bits)
        '''
        self.D[0] = [0 for _ in range(blocks)]


    def _initialize_file_descriptors(self):
        '''
        -1 indicates that the size field is free.
        '''
        for index in range(6):
            self.D[index + 1] = [-1, 0, 0, 0]

    def search_for_free_entry(self):
        '''
        Searches for the first free size field in the
        file descriptor and returns the index.
        '''
        for index in range(6):
            if self.D[index + 1][0] == -1:
                self._set_size_field_to_empty(index + 1)
                return 1
        return -1

    def _set_size_field_to_empty(self, index):
        '''
        If the file descriptor size field has a free entry,
        change that size field to 1 (empty file).
        '''
        self.D[index][0] = 1

if __name__ == "__main__":
    disk = EmulatedDisk(64, 512)
    print(disk.D[1])
    print(disk.search_for_free_entry())
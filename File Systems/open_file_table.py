from exceptions import Exceptions

class OFT:
    def __init__(self):
        '''
        Creates an Open File Table fixed size array
        [read/write buffer, current position, file size, file descriptor index]
        '''
        self.OFT = [[-1, -1, -1, -1] for _ in range(4)]
        self.OFT[0] = [0, 0, 0, 0]

    def get_read_write_buffer(self, index: int):
        '''
        Returns index 0 - read/write buffer - of the open file

        ** This is an area of 512 bytes, used to hold the 
        currently accessed block
        '''
        return self.OFT[index][0]

    def get_current_position(self):
        '''
        Returns index 1 - current position - of the open file

        ** This maintains the current position within the file and 
        is used by sequential read and write operations; with a 
        maximum file size of 3 blocks, the current position ranges 
        from 0 to 1536.
        ** −1 is used to mark the corresponding OFT entry as free
        '''
        return self.OFT[1]

    def set_current_position(self, index: int, position: int):
        '''
        Sets the current position with the given value
        '''
        self.OFT[index][1] = position

    def get_file_size(self, index: int):
        '''
        Returns index 2 - file size - of the open file

        ** This is the current size of the file, in bytes; initially, 
        the value is copied from the file descriptor but may 
        increase with each write operation
        '''
        return self.OFT[index][2]

    def set_file_size(self, index: int, size: int):
        '''
        Sets the current file size with the given value
        '''
        self.OFT[index][2] = size

    def get_file_descriptor_index(self, index: int):
        '''
        Returns index 3 - file descriptor index - of the open file

        ** This is the index of the file descriptor located on one of 
        the disk blocks D[1] through D[k−1]
        '''
        return self.OFT[index][3]

    def set_file_descriptor_index(self, index: int, file_descriptor_index: int):

        self.OFT[index][3] = file_descriptor_index

    def search_for_free_oft(self):
    
        for array_index in range(len(self.OFT)):
            if self.OFT[array_index][1] == -1:
                return array_index
        raise Exceptions.TooManyFilesOpen


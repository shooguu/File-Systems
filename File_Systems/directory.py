from .exceptions import Exceptions

class Directory:

    def __init__(self):
        '''
        (int, int) -> (name, file_descriptor_index)
        '''
        self.dir = [[(0, 0) for _ in range(64)] for _ in range(3)]
        self.block_allocated = 1


    def _convert_to_row_col(self, index: int) -> (int, int):
        '''
        Given an index, it will automatically convert the number
        to a a 2d array index
        '''
        row = index // 64
        col = index % 64
        return row, col

    
    def get_directory_blocks_allocated(self) -> int:
        '''
        Returns the number of directory blocks allocated.
        Maximum is 3 blocks
        '''
        return self.block_allocated


    def add_to_directory(self, symbolic_file_name: str, file_index: int, index: int) -> None:
        '''
        Given a directory index, a tuple with the file_name and file_index will be made.
        The function also updates how many blocks of the file descriptor has be allocated
        '''
        row, col = self._convert_to_row_col(index)
        self.dir[row][col] = (symbolic_file_name, file_index)

        if self.block_allocated <= row + 1:
            self.block_allocated = row + 1


    def get_file_name(self, index: int) -> str:

        row, col = self._convert_to_row_col(index)
        return self.dir[row][col][0]


    def get_file_descriptor_index(self, index: int) -> int:
        '''
        Returns index 1 of the tuple (index of file descriptor)
        '''
        row, col = self._convert_to_row_col(index)
        return self.dir[row][col][1]


    def remove_from_directory(self, index: int) -> None:
        '''
        Given an index, it will set the directory to (0, 0)
        meaning it is not used
        '''
        row, col = self._convert_to_row_col(index)
        self.dir[row][col] = (0, 0)


    def search_free_directory(self) -> int:
        '''
        Return an index of a free directory
        If the directory is full, it will raise a 
        NoFreeDirectory exception
        '''
        for i in range(len(self.dir) * len(self.dir[0])):
            row, col = self._convert_to_row_col(i)
            if self.dir[row][col][0] == 0:
                return i
        raise Exceptions.NoFreeDirectory


    def search_directory_if_exists(self, symbolic_file_name: str) -> int:
        '''
        This function searches for a file name inside a directory.
        If not found, it will raise a FileDoesNotExist exception
        '''
        for i in range(len(self.dir) * len(self.dir[0])):
            row, col = self._convert_to_row_col(i)
            name, index = self.dir[row][col]
            if symbolic_file_name == name:
                return i
        raise Exceptions.FileDoesNotExist


    def search_directory_if_not_exists(self, symbolic_file_name: str) -> None:
        '''
        This function raises an exception if the file
        name matches a one in the directory
        '''
        for i in range(len(self.dir) * len(self.dir[0])):
            row, col = self._convert_to_row_col(i)
            name, index = self.dir[row][col]
            if symbolic_file_name == name:
                raise Exceptions.FileExists


    def get_directory(self, index: int) -> (str, int):
        '''
        Given a index, it will return the tuple
        '''
        row, col = self._convert_to_row_col(index)
        return self.dir[row][col]



if __name__ == "__main__":
    d = Directory()
    print(d.dir)
    # d.search_directory("hello")
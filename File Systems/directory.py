from exceptions import Exceptions

class Directory:

    def __init__(self):
        self.dir = [(0, 0)]
        self.dir_size = 0

    def add_to_directory(self, symbolic_file_name: str, file_index: int):

        self.dir.append((symbolic_file_name, file_index))
        self._increase_directory_size()

    def remove_from_directory(self):

        self._decrease_directory_size()

    def search_directory(self, symbolic_file_name: str):

        for name, index in self.dir:
            if symbolic_file_name == name:
                pass
        raise Exceptions.FileDoesNotExist

    def _increase_directory_size(self):

        self.dir_size += 8

    def _decrease_directory_size(self):

        self.dir_size -= 8

    def get_directory(self):

        return self.dir

from emulated_disk import EmulatedDisk
from open_file_table import OFT
from directory import Directory
from exceptions import Exceptions

class FileSystem:
    def __init__(self):
        self.ED = EmulatedDisk(64, 512, 16)
        self.OFT = OFT()
        self.DIR = Directory()

        self.current_OFT_entry = -1

    def create(self):
        try:
            # Check if file already exists
            output = self.ED.search_for_free_entry()
            # Search for a free entry in the directory 
        except Exceptions.TooManyFiles:
            print("Too Many Files")

    def destroy(self, name: str):
        pass

    def open(self, name: str):
        try:
            self.DIR.search_directory(name)
            self.current_OFT_entry = self.OFT.search_for_free_oft()
            self.OFT.set_current_position(self.current_OFT_entry, 0)
            self.OFT.set_file_size(self.current_OFT_entry, self.ED.get_file_descriptor_size())
            self.OFT.set_file_descriptor_index(self.current_OFT_entry, self.ED.file_descriptor_index)
            if self.ED.get_file_descriptor_size() == 0:
                # use the bitmap to find a free block and record the block number in the file descriptor
                pass
            else:
                # Otherwise, copy the first block of the file into the r/w buffer of entry j
                pass

        except Exceptions.FileDoesNotExist:
            print("File Does Not Exist")
        except Exceptions.TooManyFilesOpen:
            print("Too Many Files Open")

if __name__ == "__main__":
    FS = FileSystem()
    FS.create()
    FS.open("test")
    
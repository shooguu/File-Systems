
from emulated_disk import EmulatedDisk

class FileSystem:
    def __init__(self):
        self.e = EmulatedDisk(64, 512)

    def create(self):
        # Check if file already exists
        output = self.e.search_for_free_entry()



if __name__ == "__main__":
    FS = FileSystem()
    FS.create()
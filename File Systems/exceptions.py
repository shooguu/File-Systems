class Exceptions:

    class FileDoesNotExist(BaseException):
        pass

    class TooManyFilesOpen(BaseException):
        pass

    class TooManyFiles(BaseException):
        pass
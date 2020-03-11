class Exceptions:

    class FileDoesNotExist(BaseException):
        pass

    class FileExists(BaseException):
        pass

    class TooManyFilesOpen(BaseException):
        pass

    class TooManyFiles(BaseException):
        pass

    class BitmapFull(BaseException):
        pass

    class NoFreeDirectory(BaseException):
        pass

    class CurrentPositionPastEOF(BaseException):
        pass

    class FileOpenAlready(BaseException):
        pass

    class FileNotOpen(BaseException):
        pass
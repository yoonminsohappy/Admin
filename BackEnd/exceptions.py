class NonPrimaryImageError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message

class NonImageFilenameError(Exception):
    def __init__(self, code, message):
        super().__init__()
        self.message = message

class ValidationError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message

class OneOfDatesAreNoneError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message

class ProductIdListEmptyError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message

class InvalidDownloadTypeError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message
class UglyNameError(Exception):
    """custom class to raise an Exception for ugly names"""
    def __init__(self, name, message):
        self.name = name
        self.message = message
        super().__init__(message)

raise UglyNameError(name='welf', message="that's not a valid name bro")

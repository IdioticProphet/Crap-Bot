class SoundNotFound(Exception):
    def __init__(self, message):
        self.message = message

class NotInVoice(Exception):
    def __init__(self, message):
        self.message = message

class NotAudioException(Exception):
    def __init__(self, message="Filetype was not audio."):
        self.message = message

class ExistsError(Exception):
    def __init__(self, message="Object didnt exist"):
        self.message = message

class InvalidLink(Exception):
    def __init__(self, message="Link Was not valid."):
        self.message = message

class InvalidName(Exception):
    def __init__(self, message="Name was incorrect"):
        self.message = message

class InvalidArguments(Exception):
    def __init__(self, message="You used an invalid argument"):
        self.message = message


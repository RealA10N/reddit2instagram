class Reddit2InstagramException(Exception):
    pass


class InvalidConfigFileType(Reddit2InstagramException, TypeError):
    pass

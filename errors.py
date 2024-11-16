"""Program Exception Definitions"""


class AlreadyImportedError(Exception):
    """Exception to raise when CSV file already imported"""

    pass  # pylint:disable=W0107

class DatabaseImportError(Exception):
    """Exception to raise when the database file has already been created"""

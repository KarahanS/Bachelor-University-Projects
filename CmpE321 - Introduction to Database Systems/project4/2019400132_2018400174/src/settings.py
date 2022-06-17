import os

"""
DB Settings
"""

class Settings:
    """
    All size settings are in bytes
    """
    FILE_SIZE = 1073741824
    PAGE_SIZE = 2048
    MAX_PAGE_INDEX = FILE_SIZE // PAGE_SIZE

    MAX_TYPE_NAME_LENGTH = 12
    MAX_FIELD_NAME_LENGTH = 12
    MAX_N_OFF_FIELDS = 12
    MAX_STR_LENGTH = 20
    
    LOGFILE_NAME = "horadrimLog.csv"
    CATALOG_TYPE = "_catalog"
    __TREE_FOLDER = "Trees"
    __FILE_FOLDER = "Files"

    DIRECTORY_PATH   = os.path.join("2019400132_2018400174", "src")
    TREE_FOLDER_PATH = os.path.join(DIRECTORY_PATH, __TREE_FOLDER)
    FILE_FOLDER_PATH = os.path.join(DIRECTORY_PATH, __FILE_FOLDER)

    """
    Page Structure
    """
    __IS_AVAILABLE = 1
    __N_RECORD_SLOTS = 4
    HEADER_SIZE = __IS_AVAILABLE + __N_RECORD_SLOTS
    BODY_SIZE   = PAGE_SIZE - HEADER_SIZE
    
settings = Settings()
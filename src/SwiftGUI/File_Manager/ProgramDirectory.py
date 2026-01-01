from os import PathLike
from pathlib import Path

_PROGRAM_DIRECTORY: Path | None = None

def set_program_directory(
        path: str | PathLike,
        *,
        parent: str | PathLike | None = Path.home(),
        ignore_parent: bool = False,
) -> Path:
    """
    Define a program-directory that can be used to store configuration, save-files, etc.

    First argument should be the name of the program.

    :param ignore_parent: True, if the parent should be ignored. Useful for debug-starts
    :param path: Ideally the name of the program.
    :param parent:
    :return: Path-object to the new directory
    """
    global _PROGRAM_DIRECTORY
    if ignore_parent or not parent:
        _PROGRAM_DIRECTORY = Path(path)
    else:
        _PROGRAM_DIRECTORY = Path(parent) / Path(path)

    _PROGRAM_DIRECTORY.mkdir(parents= True, exist_ok= True) # Create the folder if it doesn't exist already
    return _PROGRAM_DIRECTORY

def program_path(relative_path: str | PathLike = None) -> Path:
    """
    Return a file-path inside the program's directory.
    Leave it empty to return the program directory

    :param relative_path:
    :return:
    """
    assert _PROGRAM_DIRECTORY is not None, "No program-directory isn't defined.\nUse .set_program_directory(...) to define it"

    if relative_path:
        return _PROGRAM_DIRECTORY / Path(relative_path)
    else:
        return _PROGRAM_DIRECTORY



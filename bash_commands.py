import os


def ls():
    """
    List the contents of a folder.
    """
    return os.system("ls")


def cd(folder):
    """
    Change the current folder.
    """
    os.chdir(folder)


def cat(file):
    """
    Open a file and read its contents.
    """
    os.system(f"cat {file}")


def sed(file, start, end):
    """
    Read the lines from start to end in a file.
    """
    os.system(f"sed -n '{start},{end}p' {file}")



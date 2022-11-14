import os
import platform
import zipfile

def all_files(path):
    files = [item.path for item in scan_tree(path) if item.is_file()]
    # Windows has maximum path length of 260 - ignore any files that are longer
    if platform.system() == 'Windows':
        files = [f for f in files if len(f) <= 260]
    return files

def _unzip_files(path, status):
    """
    Unzip any zipped files in a directory.
    
    Checking for zipped files is slow so this only searches the top folder.

    Returns : a list with unzipped files
    """
    files = [entry.path for entry in os.scandir(path) if entry.is_file()]
    zipfiles = []
    for i, file in enumerate(files):
        status.progress(i, len(files), message='Searching for zipped folders..')
        if zipfile.is_zipfile(file):
            zipfiles.append(file)
    if zipfiles == []:
        return
    for i, file in enumerate(zipfiles): # unzip any zip files and delete the original zip
        status.progress(i, len(zipfiles), 'Unzipping file ' + file)
        with zipfile.ZipFile(file, 'r') as zip_folder:
            path = ''.join(file.split('.')[:-1]) # remove file extension
            if not os.path.isdir(path): 
                os.mkdir(path)
            zip_folder.extractall(path)
        os.remove(file)


def scan_tree(directory):
    """Helper function: yield DirEntry objects for the directory."""

    for entry in os.scandir(directory):
        if entry.is_dir(follow_symlinks=False):
            yield from scan_tree(entry.path)
        else:
            yield entry
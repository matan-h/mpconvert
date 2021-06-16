import os

import filetype as filetype
import win32com.client.gencache


def get_file_metadata(path, filename, metadata_l) -> dict:
    """
    get file metadata
    Args:
        path: folder of the file
        filename: filename of the file
        metadata_l: metadata list

    Returns:dictionary of file metadata

    """
    # Path shouldn't end with backslash, i.e. "E:\Images\Paris"
    # filename must include extension, i.e. "PID manual.pdf"
    # Returns dictionary containing all file metadata.
    sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
    ns = sh.NameSpace(path)
    if ns is None:
        print(f"cant find NameSpace '{path}' returning")
        return {}

    # Enumeration is necessary because ns.GetDetailsOf only accepts an integer as 2nd argument
    file_metadata = dict()
    item = ns.ParseName(str(filename))
    for ind, attribute in enumerate(metadata_l):
        attr_value = ns.GetDetailsOf(item, ind)
        if attr_value:
            file_metadata[attribute] = attr_value

    return file_metadata


metadata_list = ['Name', 'Size', 'Item type', 'Date modified', 'Date created', 'Date accessed', 'Attributes',
                 'Offline status', 'Availability', 'Perceived type', 'Owner', 'Kind', 'Date taken',
                 'Contributing artists', 'Album', 'Year', 'Genre', 'Conductors', 'Tags', 'Rating', 'Authors', 'Title',
                 'Subject', 'Categories', 'Comments', 'Copyright', '#', 'Length', 'Bit rate', 'Protected',
                 'Camera model', 'Dimensions', 'Camera maker', 'Company', 'File description', 'Masters keywords',
                 'Masters keywords', "xa"]


def metadata(file):
    """
    split file to folder, filename and pass them to get_file_metadata()
    Args:
        file: full path of the file

    Returns:dictionary of file metadata

    """
    folder, filename = os.path.dirname(file), os.path.basename(file)
    # return
    return get_file_metadata(folder, filename, metadata_list)


def info_by_contact(file):
    """
    guss type of file by contact

    Args:
        file: the file

    Returns:guss types

    """
    kind = filetype.guess(file)
    extension = 'Could Not guess file type'
    mime = 'Could Not guess file type'
    if kind is not None:
        extension = kind.extension
        mime = kind.mime
    return {'guess-extension': extension, 'guess-mime': mime}

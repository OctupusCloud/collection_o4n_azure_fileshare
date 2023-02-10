import re

def right_path(_path):
    _path = re.sub(r"^\/", "", _path)
    _path = re.sub(r"\/$", "", _path)

    if not _path:
        print_path = "/"
    else:
        print_path = _path

    return _path, print_path
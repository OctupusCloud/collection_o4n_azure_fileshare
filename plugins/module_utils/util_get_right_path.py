import re

def right_path(_path):
    _path = re.sub(r"^\/", "", _path)
    _path = re.sub(r"\/$", "", _path)

    return _path
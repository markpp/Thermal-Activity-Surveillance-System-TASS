

def check_path(path):
    # check if path ends with a "/" and remove it

    if path.endswith("/"):
        return path[:-1]
    else:
        return path
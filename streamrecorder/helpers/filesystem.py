import os


class Filesystem:
    def __init__(self):
        self.directory = ''

    def create_directory(self, path, directory):
        self.directory = os.path.join(os.path.abspath(path), directory)

        if os.path.isdir(self.directory) is False:
            os.makedirs(self.directory)

    def create_file(self, name, extension):
        filename = "".join(x for x in name if x.isalnum() or x in ["-", "_", "."])
        filename += '.' + extension
        filename = os.path.join(self.directory, filename)
        return filename

import os


class Filesystem:
    def __init__(self):
        self.directory = ''
        self.filename = ''
        self.filepath = ''

    def get_directory(self):
        return self.directory

    def get_filename(self):
        return self.filename

    def get_filepath(self):
        return self.filepath

    def create_directory(self, path, directory):
        self.directory = os.path.join(os.path.abspath(path), directory)

        if os.path.isdir(self.directory) is False:
            os.makedirs(self.directory)

    def create_file(self, name, extension):
        self.filename = "".join(x for x in name if x.isalnum() or x in ["-", "_", "."])
        self.filename += '.' + extension
        return self.filename

    def create_filepath(self, directory, filename):
        filepath = os.path.join(directory, filename)
        return filepath

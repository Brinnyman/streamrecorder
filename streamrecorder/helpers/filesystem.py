import os


class Filesystem:
    def __init__(self, directory, filename):
        self.directory = directory
        self.filename = filename

    def get_directory(self):
        return self.directory

    def get_filename(self):
        return self.filename

    def create_directory(self):
        self.directory = os.path.join(os.path.abspath(self.directory), self.filename)

        if os.path.isdir(self.directory) is False:
            os.makedirs(self.directory)

    def create_file(self, date):
        filename = self.filename + '_' + date
        filename = "".join(x for x in filename if x.isalnum() or x in ["-", "_", "."])
        filename = os.path.join(self.get_directory(), filename)
        return filename

import os
import datetime


class Filesystem:
    def __init__(self):
        self.directory = ''
        self.filename = ''

    # create directory
    def create_directory(self, path, name):
        # TODO: check if path is empty, set default path to the path of the main directory
        # create directory with at the specified path
        self.directory = os.path.join(os.path.abspath(path), name)

        if(os.path.isdir(self.directory) is False):
            os.makedirs(self.directory)

    # get directory
    def get_directory(self):
        # return directory
        return self.directory

    # create file
    def create_file(self, name, date):
        # create file with specified name
        self.filename = name + '_' + date
        self.filename = "".join(x for x in self.filename if x.isalnum()
                           or x in ["-", "_", "."])
        self.filename = os.path.join(self.get_directory(), self.filename)
        return self.filename

    # get filename
    def get_filename(self):
        # return filename
        return self.filename
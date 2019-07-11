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

    # get list of files in directory
    def get_files_in_directory(self, directory):
        files = []
        for dirpath,_,filenames in os.walk(directory):
            for f in filenames:
                file = os.path.abspath(os.path.join(dirpath, f))
                files.append(file)
            
        return files

    def add_file_extension(self, file, extension):
        file += extension
        
        return file

    def remove_file_extension(self, file):
        return os.path.splitext(file)[0]

    def filtered_files(self, directory, extension):
        files = self.get_files_in_directory(directory)
        export = []
        filtered_list = []

        for f in files:
            x = self.remove_file_extension(f)
            x += extension
            filtered_list.append(x)

        first = set(self.get_files_in_directory(directory))
        second = [item for item in filtered_list if item not in first]

        for s in second:
            x = self.remove_file_extension(s)
            export.append(x)

        return export

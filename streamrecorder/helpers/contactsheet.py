import subprocess
import sys
import os


class ContactSheet:
    def __init__(self, vcsi_path):
        self.vcsi_path = vcsi_path

    def create_contact_sheet(self, filename):
        process = None
        try:
            name =  os.path.splitext(filename)[0]
            vcsi = [self.vcsi_path, filename, '-t', '-w', '850', '-g', ' 3x5', '-o', name + '.png']
            process = subprocess.Popen(vcsi, stdout=subprocess.PIPE, stderr=None)
            process.communicate()

        except OSError:
            print(
                'An error has occurred while trying to use vcsi. Is it installed? Do you have Python in your PATH variable?')
            sys.exit(1)

        return process.stdout

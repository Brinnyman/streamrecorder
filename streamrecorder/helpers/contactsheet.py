import configparser
import os
import subprocess
import sys

class ContactSheet:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config.ini'))
        self.contact_sheet_extension = config['VCSI']['CONTACT_SHEET_EXTENSION']

    def create_contact_sheet(self, recorded_file):
        process = None
        try:
            vcsi = [self.contact_sheet_extension, recorded_file + '.mkv', '-t', '-w', '850', '-g', ' 3x5', '-o', recorded_file + '.png']
            process = subprocess.Popen(vcsi, stdout=subprocess.PIPE, stderr=None)
            process.communicate()

        except OSError:
            print(
                'An error has occurred while trying to use vcsi. Is it installed? Do you have Python in your PATH variable?')
            sys.exit(1)

        return process.stdout
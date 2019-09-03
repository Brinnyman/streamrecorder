import subprocess
import sys


class ContactSheet:
    def create_contact_sheet(self, recorded_file, *args):
        process = None
        try:
            vcsi = ['vcsi', recorded_file + '.mp4', '-t', '-w', '850', '-g', ' 3x5', '-o', recorded_file + '.png']
            process = subprocess.Popen(vcsi, stdout=subprocess.PIPE, stderr=None)

            print('start vcsi')
            process.communicate()

        except OSError:
            print(
                'An error has occurred while trying to use vcsi. Is it installed? Do you have Python in your PATH variable?')
            sys.exit(1)

        return process.stdout

    def bulk_contact_sheet(self, files):
        for f in files:
            print(f)
            self.create_contact_sheet(f)

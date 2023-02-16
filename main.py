import subprocess
import shutil
import logging
from datetime import datetime
import os

# Run a program
# Capture exit code and log success/failure
# If success, we check the output of the folders it creates and validates that the
# proper structure exists (with addl size validation) (log properly)
# Once everything is good to go, we zip up the contents into a zip file with the current date
# (YYYYMMDD.zip) and copy that zip file to an outbox folder

logging.basicConfig(filename='py_zip_file.log', encoding='utf-8', level=logging.DEBUG)


def main(args, input_directory):
    try:
        child = subprocess.check_call(args, stdout=subprocess.PIPE)
        logging.debug(f"Process call to '{' '.join(args)}' was successful -- {datetime.now()}")
        folder_check = ['foo', 'bar', 'baz', 'bam']
        # check to see that folder exists within the directory
        check = all(folder in folder_check for folder in os.listdir(input_directory))
        if not check:
            # folders were not found -> assuming program err'd
            logging.error(f"Correct folders do not exist within {input_directory} -- assuming process error "
                          f"-- {datetime.now()}")
            print(f"Error: Correct folders not found within {input_directory}")
            return
        # check to see if directory is less than a gigabyte
        size_check = 1_073_741_824
        if os.stat(input_directory).st_size < size_check:
            logging.error(f"Process did not generate enough data - assuming process error -- {datetime.now()}")
        else:
            cwd = os.getcwd()
            date = datetime.now().date().strftime("%Y%m%d")
            try:
                # zip the entire directory
                shutil.make_archive(date, "zip", cwd, input_directory)
                logging.debug(f"Zipping successful -- located in {cwd}/{date} -- {datetime.now()}.zip")
                for folder in folder_check:
                    os.rmdir(os.path.join(input_directory, folder))
                logging.debug(f"All folders within {input_directory} have been deleted -- {datetime.now()}")
            except shutil.Error as err:
                logging.error(f"Zipping could not be completed -- Error:{err} -- {datetime.now()}")
    except subprocess.CalledProcessError as err:
        logging.error(f"Process call to '{' '.join(args)}' was unsuccessful "
                      f"-- {datetime.now()}")
        logging.error(f"{err} -- {datetime.now()}")


if __name__ == '__main__':
    command = ['python', 'test.py']
    directory = "/home/luke/Jangoflyte.ttv"
    main(command, directory)


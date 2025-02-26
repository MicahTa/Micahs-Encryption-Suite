import os
import random

##################################################################################################
################################### Remove Utility ###############################################

#TODO this utility does not properly remove folders when there are other folders inside of them
class remove():
    # Wrights 0's to the entire file (secure delete)
    @classmethod
    def zero_out_file(self, file_path: str):
        """
        Zero's out file
        :file_path -> file to be erased
        """
        try:
            file_size = os.path.getsize(file_path)
            with open(file_path, 'wb') as file:
                file.write(b'\x00' * file_size)
        except: self.error = True

    # Generate a random string (also for secure delete) Im not 100% shure this works lol
    @classmethod
    def generate_random_string(self, length: int) -> str:
        """
        Generates random string
        """
        characters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    # Cycle through files and directories to remove them
    @classmethod
    def go_through_r(self, target: str, secure: bool):
        '''
        DO NOT CALL UPON this is dependant on another function
        :Call on remove instead
        :target -> target file/folder
        :secure -> weather the folder should be zero'ed out
        '''
        # Target --> target directory   Secure --> 0 out file?
        # get list of all the files in the target directory
        self.error = False

        try:
            all = os.listdir(target)
        except OSError as error:
            self.error = True
            return self.error
        # Go through eatch file/folder in list
        for ff in all:
            # If current item is file
            if os.path.isfile(f'{target}/{ff}'):
                # Handle secure remove
                if secure:
                    # Zero out file
                    self.zero_out_file(f'{target}/{ff}')
                    tmp_name = self.generate_random_string(len(ff))
                    # Try to remove
                    try:
                        print (f'Removing {target}/{ff}')
                        os.rename(f'{target}/{ff}', f'{target}/{tmp_name}')
                        os.remove(f'{target}/{tmp_name}')
                    except OSError as error:
                        self.error = True
                        print (f'Error: {error}')
                # Handle regular deleation
                else:
                    # Try to remove
                    try:
                        print (f'Removing {target}/{ff}')
                        os.remove(f'{target}/{ff}')
                    except OSError as error:
                        self.error = True
                        print (f'Error: {error}')
            # If current item is directory
            else:
                # Opens and removes target folder (Calls on self)
                self.go_through_r(f'{target}/{ff}', secure)
                # Handle secure remove
                if secure:
                    tmp_name = self.generate_random_string(len(ff))
                    # try to remname and remove it
                    try:
                        print (f'Removing {target}/{ff}')
                        os.rename(f'{target}/{ff}', f'{target}/{tmp_name}')
                        os.rmdir(f'{target}/{tmp_name}')
                    except OSError as error:
                        self.error = True
                        print (f'Error: {error}')
                # Handle regular removing
                else:
                    # Try to remove folder
                    try:
                        print (f'Removing {target}/{ff}')
                        os.rmdir(f'{target}/{ff}')
                    except OSError as error:
                        self.error = True
                        print (f'Error: {error}')

    # Remove utility
    @classmethod
    def remove(self, target: str, secure: bool):
        """
        Removes folder/files
        :target -> target file/folder
        :secure -> if the file should be zero'ed out
        """
        self.error = False
        # If the target if file
        if os.path.isfile(target):
            # If recure remove and 0 out
            if secure:
                self().zero_out_file(target)
                tmp_name = self().generate_random_string(len(os.path.basename(target)))
                try:
                    print (f'Removing {target}')
                    os.rename(f'{target}', f'{os.path.dirname(target)}/{tmp_name}')
                    os.remove(f'{os.path.dirname(target)}/{tmp_name}')
                except OSError as error:
                    self.error = True
                    print (f'Error {error}')
            else:
                # Try to remove
                try:
                    print (f'Removing {target}')
                    os.remove(target)
                except OSError as error:
                    self.error = True
                    print (f'Error {error}')
        # If target is a directory
        elif os.path.isdir(target):
            # Start going through lists of items in target directory
            try:
                self().go_through_r(target, secure)
            except:
                self.error = True
                print (f'Error: {error}')
                return None
            # Remove target directory
            if secure:
                tmp_name = self().generate_random_string(len(os.path.basename(target)))
                try:
                    print (f'Removing {target}')
                    os.rename(target, f'{os.path.dirname(target)}/{tmp_name}')
                    os.rmdir(f'{os.path.dirname(target)}/{tmp_name}')
                except OSError as error:
                    self.error = True
                    print (f'Error: {error}')
            else:
                try:
                    os.rmdir(target)
                except OSError as error:
                    self.error = True
                    print (f'Error {error}')
        
        return self.error

##################################################################################################
###################################### Copy Utility ##############################################
##################################################################################################

class copy():
    # Copy file
    @classmethod
    def copy_c(self, what, where, ext=''):
        """
        DO NOT CALL UPON this is dependant on another function
        :Call go_through_c_start instead
        :what -> target
        :where -> destination directory
        :ext -> extention for new file
        """
        print (f'What {what}\nWhere {where}')
        print (f'Copying {what}')
        try:
            with open(what, 'rb') as input_file:
                file_content = input_file.read()
            
            with open(f'{where}/{os.path.basename(what)}{ext}', 'wb') as output_file:
                output_file.write(file_content)
        except: self.error = True

    # Cycle through copying
    @classmethod
    def go_through_c(self, target: str, destination: str):
        """
        DO NOT CALL UPON this is dependent on another function
        :Call upon go_through_c_start instead
        :target -> target file/folder
        :destination -> Destination directory
        """
        # target --> target directory, destination --> target directory
        # get list of things in target directory
        try: all = os.listdir(target)
        except: self.error = True
        else:
            # Cycle through list
            for ff in all:
                # If its a file then copy it
                if os.path.isfile(f'{target}/{ff}'):
                    self.copy_c(f'{target}/{ff}', f'{destination}')
                else:
                    # If its a directory try to make a directory and call apon myself
                    os.mkdir(f'{destination}/{ff}')
                    self.go_through_c(f'{target}/{ff}', f'{destination}/{ff}')

    # Start the procsess of copying
    @classmethod
    def go_through_c_start(self, target: str, destination: str):
        """
        Copyies file/folders
        :Target -> Target file/folder to be copied
        :Destination -> destination directory
        """
        self.error = False

        # Copy files if its directory
        if os.path.isfile(target):
            self().copy_c(target, destination, ' - copy')
        else:
            # If directory
            # Create new directory
            os.mkdir(f'{destination}/{os.path.basename(target)} - copy')
            # Start going through it
            self().go_through_c(target, f'{destination}/{os.path.basename(target)} - copy')

        return self.error
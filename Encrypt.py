import base64
import os
from Crypto.Cipher import AES

from globalVaribles import *

##################################################################################################
########################################### Get Size #############################################
##################################################################################################
# Go through target directory to get the total size of the directory
def get_size_re(target: str) -> int:
    """
    DO NOT CALL UPON
    :Call get_size_start
    """
    # Try to get directory contents
    try:
        all = os.listdir(target)
    except OSError as error:
        print(f"Error: {error}")
        return None
    size = 0

    # Go through each thing in directory
    for file in all:
        # If file
        if os.path.isfile(f'{target}/{file}'):
            # Add file to total
            size += os.path.getsize(f'{target}/{file}')
        # if directory
        elif os.path.isdir(f'{target}/{file}'):
            # Call upon myself
            size += get_size_re(f'{target}/{file}')

    # Return size so far
    return size

# Start the get size
def get_size_start(target: str) -> int:
    """
    Get the size of the file/folder
    :target -> Absolute path
    :Returns the size in byes (at least one)
    """
    # If file
    if os.path.isfile(target):
        # Return the file size
        return os.path.getsize(target) if os.path.getsize(target) != 1 else 1
    # If directory
    elif os.path.isdir(target):
        # Start going through the contents
        return get_size_re(target) if  get_size_re(target) != 1 else 1


##################################################################################################
########################################### Encrypt ##############################################
##################################################################################################

# Pad data
def pad_data(data) -> bytes:
    """
    Pads the data
    """
    block_size = 16
    return data + (block_size - len(data) % block_size) * bytes([block_size - len(data) % block_size])

# Encrypts data
def encrypt(data: bytes, key: bytes) -> bytes:
    """
    Encrypts data
    """
    padded_data = pad_data(data)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(padded_data)

# Encrypts the name
def encrypt_name(name: str, key: bytes) -> str:
    """
    Encrypts file name
    :name -> name of file (not absolute path)
    :key -> key to encrypt file
    """
    bin_text = name.encode('utf-8')
    enc_text = encrypt(bin_text, key)
    string = (base64.urlsafe_b64encode(enc_text).decode('utf-8'))
    return f'{string}.aes'

# Says whats currently being encrypted and how much more it left
def copy_e(what: str, where: str, total_size: int, id: str, key: bytes, size_done: int = 0) -> int:
        """
        DO NOT CALL UPON relyes on another function
        :Call go_through_e_start instead
        :what -> file being copied
        :where -> destitaion
        :total_size -> total size encrypting
        :id -> ID of the queue item
        :size_done -> how much has been finished
        """

        with open(what, 'rb') as input_file:
            file_content = input_file.read()
        # Fuck anyone trynig to encode large files and doesn't have a crazy amount of RAM or swap
        # Just sayin I did a 4GB file without a problem with 8GB of RAM and it just barley didnt crash ¯\_(ツ)_/¯
        #TODO make it encrypt and decrypt in chunks
        
        # Write new file
        with open(f'{where}/{encrypt_name(os.path.basename(what), key)}', 'wb') as output_file:
            output_file.write(encrypt(file_content, key))

        size_done += os.path.getsize(what)
        if size_done == 0:
            size_done += 1
        if total_size == 0:
            total_size += 1
        if id is not None:
            global queue
            for i in range (len(queue)):
                if queue[i]['id'] == id:
                    queue[i]['progress'] = round(100 * size_done / total_size, 5)
                    if queue[i]['status'] == 'Canceling':
                        queue[i]['status'] = 'Canceled'
                        return None # End the process
                    break
        print (f'encrypting {what}')
        print (f'{(100 * size_done / total_size):.5f} % Done', end='\r')

        # Return how much it just encrypted
        return os.path.getsize (what)

# This goes through eatch directory and file
def go_through_e(target: str, destination: str, total_size: int, id: str, key: bytes, size_done: int = 0) -> int:
    """
    DO NOT CALL UPON is relient on another function
    :Call go_through_e_start instead
    :target -> target directory
    :destination -> target directory
    :total_size -> size of entire encryption
    :size_done -> Size done so far
    """
    # try to get list of directories and files in target directory
    try:
        all = os.listdir(target)
    except OSError as error:
        print(f"Error: {error}")
        return size_done
    # Go through eatch thing in target directory
    for ff in all:
        # If its a file the just encrypt it
        if os.path.isfile(f'{target}/{ff}'):
            tmp = copy_e(f'{target}/{ff}', f'{destination}', total_size, id, key, size_done)
            if tmp is None: # This is for the canceling feture
                break
            size_done += tmp
        else:
            # If its a directory try to create a new directory and then go through it
            try:
                os.mkdir(f'{destination}/{encrypt_name(ff, key)}')
            except OSError as error:
                print(f"Error: {error}")
            size_done = go_through_e(f'{target}/{ff}', f'{destination}/{encrypt_name(ff, key)}', total_size, id, key, size_done)
    # This if for calculating how mich is done
    return size_done

# Start the encryption process
def go_through_e_start(target: str, destination: str, key: bytes, id: str = None):
    """
    Encrypts target file/folder to the destination 
    :id -> This is to edit the queue later
    """
    # If target is file then encrypt it
    if os.path.isfile(target):
        copy_e(target, destination, os.path.getsize(target), id, key)
    else:
        # If directory
        try:
            # Make new directory
            os.mkdir(f'{destination}/{encrypt_name(os.path.basename(target), key)}')
            # Start going through encryption
            go_through_e(target, f'{destination}/{encrypt_name(os.path.basename(target), key)}', get_size_start(target), id, key)
        except OSError as error:
            print(f"Error: {error}")

    if id is not None:
        global queue
        for i in range (len(queue)):
            if queue[i]['id'] == id:
                queue[i]['progress'] = 100
                queue[i]['status'] = 'Done'
                break
    print ('100 % Done')











##################################################################################################
########################################### decrypt ##############################################
##################################################################################################

# Upad data
def unpad_data(data) -> bytes:
    return data.rstrip(bytes([data[-1]]))

# Decrypt the data
def decrypt_data(data: bytes, key: bytes) -> bytes:
    """
    Decrypts any data
    """
    cipher = AES.new(key, AES.MODE_ECB)
    uncrypted_data = cipher.decrypt(data)
    return uncrypted_data.rstrip(bytes([uncrypted_data[-1]]))

# Decrypt the name
def decrypt_name (name: str, key: bytes) -> tuple:
    """
    Decrypts the name of a file
    :name -> name of file (Not absolute path)
    :key -> the key to unlock it
    : return (name, weather it was encrypted or not)
    """
    if len(name) > 4:

        if name[-4:] == '.aes':
            try:
                enc_text = base64.urlsafe_b64decode(name[:-4])
                dec_text = decrypt_data(enc_text, key)
                original_text = dec_text.decode('utf-8')
                return original_text, True
            except:
                return name, False
        else:
            return name, False
    else:
        return name, False

# copy the decrypted file
def copy_d(what: str, where: str, total_size: int, id: str, key: bytes, size_done: int = 0) -> int:
        """
        DO NOT CALL UPON this is dependant on another function
        :Call go_through_d_start instead
        :what -> target
        :where -> directory
        :total_size -> Total copy size
        :id -> ID of the queue item
        :size_done -> Amount copied
        """
        # Read the contents
        with open(what, 'rb') as input_file:
            file_content = input_file.read()
        
        # Wright the decrypted file
        name, e = decrypt_name(os.path.basename(what), key)
        with open(f'{where}/{name}', 'wb') as output_file:
            output_file.write(decrypt_data(file_content, key))

        size_done += os.path.getsize(what)
        if size_done == 0:
            size_done += 1
        if total_size == 0:
            total_size += 1
        if id is not None:
            global queue
            for i in range (len(queue)):
                if queue[i]['id'] == id:
                    queue[i]['progress'] = round(100 * size_done / total_size, 5)
                    if queue[i]['status'] == 'Canceling':
                        queue[i]['status'] = 'Canceled'
                        return None # End the process
                    break
        print (f'decrypting {what}')
        # Print the size done so far
        print (f'{(100 * size_done / total_size):.5f} % Done', end='\r')

        # Return how much asitional size done
        return os.path.getsize (what)

# Go through the directories
def go_through_d(target: str, destination: str, total_size: int, id: str, key: bytes, size_done: int = 0) -> int:
    """
    DO NOT CALL UPON this is dependant on another function
    :Call go_through_d_start instead
    :target -> target directory
    :destination -> desintaion directory
    :total_size -> Total size tobe copied
    :id -> ID of queue item
    :size_done -> size copied
    """
    # Try to get contents of directory
    try:
        all = os.listdir(target)
    except OSError as error:
        print(f"Error: {error}")
        return size_done
    # Go through contents
    for ff in all:
        # If file
        if os.path.isfile(f'{target}/{ff}'):
            # Decrypt the data
            tmp = copy_d(f'{target}/{ff}', f'{destination}', total_size, id, key, size_done)
            if tmp is None: # This is for the canceling feature
                break
            size_done += tmp
        else:
            # If directory
            try:
                # Create the new directory
                name, e = decrypt_name(ff, key)
                os.mkdir(f'{destination}/{name}')
                # Start going through the files
                size_done = go_through_d(f'{target}/{ff}', f'{destination}/{name}', total_size, id, key, size_done)
            except OSError as error:
                print(f"Error: {error}")
    # Return how much has been done
    return size_done

# Start decrypting
def go_through_d_start(target: str, destination: str, key: bytes, id: str = None):
    """
    Starts decrypting
    :target -> Absolute path
    :destination -> Absolute path of directory
    :id -> ID of queue item
    """
    # If file
    if os.path.isfile(target):
        # Decrypt and copy it
        copy_d(target, destination, os.path.getsize(target), id, key)
    # If file
    else:
        try:
            # Try to create new directory
            name, e = decrypt_name(os.path.basename(target), key)
            os.mkdir(f'{destination}/{name}')
            # Start going through the directories
            go_through_d(target, f'{destination}/{name}', get_size_start(target), id, key)
        except OSError as error:
            print(f"Error: {error}")

    if id is not None:
        global queue
        for i in range (len(queue)):
            if queue[i]['id'] == id:
                queue[i]['progress'] = 100
                queue[i]['status'] = 'Done'
                break
    print ('100 % Done')
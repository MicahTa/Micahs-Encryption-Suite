import os
import json
import base64
from Crypto.Protocol.KDF import PBKDF2
from hashlib import sha256
import hmac
import datetime

from modal import *
from globalVaribles import *
from Encrypt import *

class keyMethods:
    """
    Handles the key methods and what not
    """
    def __init__(self, api = None):
        """
        Starts this bitch up
        :api -> The pointer to the API class (This is barley used)
        """
        # Comunicates back to the API (barley used)
        self.api = api
        self.keyOptions = [] # On the password page this is all the options there for the key

    def loadWindow(self):
        global window
        window=shared_dict['my_global_var']
    
    def wrongPass(self):
        modal.code("WrongPass")

    def backup(self):
        try:
            with open('secured_keys.json', 'rb') as f:
                # Load the JSON data from the file
                data = f.read()

            now = datetime.datetime.now()
            # Format the date as "mm-dd-yyyy-hh-mm--ss"
            formatted_date = now.strftime("%m-%d-%Y-%H-%M-%S")

            with open(f'./KeysBackup/backup{formatted_date}.json', 'wb') as f:
                # Load the JSON data from the file
                f.write(data)

            with open('secured_keys.json', 'w') as f:
                f.write("{}")
        except:
            modal.ok("Error Creating Backup", "There was an error when creating your backup. If keys cannot be accesed they will be in the backup folder and naimed by the data and time.")
            return False
        else:
            return True

    def verifyPassword(self, name: str, password: str, salt: str = None) -> bool:
        """
        Returns true if password matches and false if it doesnt
        :name -> Name of key
        :password -> Password to verify
        :salt -> path to salt file
        """
        try:
            with open('secured_keys.json', 'r') as f:
                # Load the JSON data from the file
                data = json.load(f)
        except:
            modal.code("ReadingKeys")
            return None

        # Decrypt Key
        if data[name]["type"] == "passwordBased":
            key = self.PDkey(password, salt, True, False, name)
            # Validate that the key matches
            validation = base64.b64encode(encrypt(name.encode('utf-8'), key)).decode('utf-8') == data[name]["auth"]
        elif data[name]["type"] == "keyBased":
            # KDkey Validates the key by itself
            key = self.KDkey(name, password, salt, True)
            validation = (key is not None) # Weather the key is validated
        else:
            return False
        
        return validation

    def changePass(self, name: str, password: str, newPass: str, salt: str = None):
        """
        This will change the password for the string
        : This is only for computer derived keys, since password derived keys are created from the password it cannot be changed.
        :name -> Name of the key you want to change
        :password -> Current password of the key
        :newPass -> New password of the key
        :salt -> path to salt file
        """
        key = self.KDkey(name, password, salt, True)

        if key is None:
            self.wrongPass()
            return None

        # Recreates the key with the new password
        self.delete(name, password, salt)
        self.createKey(name, newPass, "KD", "AES256", salt, key)

        self.updateKeyNames()


    def delete(self, name: str, password: str, salt: str = None):
        """
        Deleates a key after verifying it's password
        :name -> name of key to remove
        :password -> password of key
        :salt -> path to salt file
        """
        # TODO ask are you sure
        # TODO if you deleate the key you currently have loaded unload it
        # Validate it matches
        validation = self.verifyPassword(name, password, salt)

        if not validation:
            self.wrongPass()
            return None

        try:
            with open('secured_keys.json', 'r') as f:
                # Load the JSON data from the file
                data = json.load(f)

            # Remove name
            del data[name]

            # Wright it out
            with open('secured_keys.json', 'w') as f:
                json.dump(data, f)
        except:
            modal.code("ReadingKeys")
            return None
        
        # Update everything
        self.updateKeyNames()
        
        
    def rename(self, name: str,  newName: str, password: str, salt: str = None):
        """
        Renames the key
        :name -> Name of key
        :Password -> Old password
        :newPassword -> New password
        :salt -> Salt file path
        """
        # Open the json file with the secured keys
        try:
            with open('secured_keys.json', 'r') as f:
                # Load the JSON data from the file
                data = json.load(f)
        except:
            modal.code("ReadingKeys")
            return None

        validation = self.verifyPassword(name, password, salt)

        # Auth
        if not validation: # Password is wrong
            # Show an error saying wrong password
            self.wrongPass()
            return None

        # Encrpyt new name
        auth = base64.b64encode(encrypt(base64.b64encode(newName.encode("utf-8")), key)).decode('utf-8')

        # Make changes
        data[newName] = data[name]
        data[newName]['auth'] = auth

        del data[name]

        # Wright it out
        try:
            with open('secured_keys.json', 'w') as f:
                json.dump(data, f)
        except:
            modal.code("ReadingKeys")
            return None
        
        # Update everything
        self.updateKeyNames()

    
    def createSharedKey(self, name: str, password: str, newPassword: str, exp: int = 1):
        """
        WARNING: This is kinda dumb if you want to share keys use the premium server version (at the time of wrighting this it doesnt exist)
        : This is stupid for multible reasons but mainly becuse you cannot revoke there acsses and its possible for then to give the share string to unwanted people, its also not very secure.
        :This shares (Key Based) keys (If you want to share Password Derived keys share the password, this is even more stupid)
        :name -> Name of (Key Based) key to be shared
        :password -> Password of the key
        :newPassword -> Password for the next user
        """
        # TODO create a shared key system
        sharedKeyString = 'AHHHHHHHHHH'
        modal.ok("Shared Key", sharedKeyString)


    def addSharedKey(self, string: str): # TODO This
        """
        Add shared key generated by this program
        :string -> Shared key string
        """
        print (string)
    
    def createKey(self, name, password, Keytype: str = "PD", method: str = "AES256", salt: str = None, rootKey: bytes = None):
        print (name, password, Keytype)
        """
        Creates a new key based on the parameters shown
        :name -> Name of the new key
        :password -> Password of the new key
        :type -> Options are either PD (Password Derived Key) and KD (Key Derived Key)
        :method -> Encryption method (Currently AES is the only encryption method and this will do nothing if changed)
        :salt -> File path to salt file, leave empty for no salt.
        :rootKey -> This will set the computer derived key to this varible instead of a random one
        """
        # TODO add salt functinality
        # TODO add all that "security" stuff (:

        # Create the auth string
        # base64.b64encode(encrypt(item.encode('utf-8'), tmp_key)).decode('utf-8')
        if salt is None or salt == "":
            salt = b'\x9cmNx\xa5\xd6\xdf\x98\x10Zr\xe0\xd4\xeb\x989'

        # Open the json file with the secured keys
        try:
            with open('secured_keys.json', 'r') as f:
                # Load the JSON data from the file
                data = json.load(f)
        except:
            self.backup() 
            modal.code("ReadingKeys")
            data = {}

        # Check if there is a duplicate key
        if name in data:
            # Send error and exit
            modal.code("InvalidKeyName")
            return None
        
        # Blacklisted names
        if name.lower() in ["", "password based", "passwordbased"] or type(name) != str:
            # Send error and exit
            modal.code("InvalidKeyName")
            return None

        # Create the auth string and secureKey (if applicable)
        PDKey = PBKDF2(password.encode(), salt, dkLen=32, count=1000000, prf=lambda p, s: hmac.new(p, s, sha256).digest())
        if Keytype == 'PD':
            # Password Derived key
            auth = base64.b64encode(encrypt(name.encode('utf-8'), PDKey)).decode('utf-8')
            secureKey = None
        else:
            # Key Based Key
            if rootKey is None:
                randomKey = os.urandom(16)
            else:
                randomKey = rootKey
            secureKey = base64.b64encode(encrypt(randomKey, PDKey)).decode('utf-8')
            auth = base64.b64encode(encrypt(base64.b64encode(name.encode("utf-8")), randomKey)).decode('utf-8')

        # Make addition
        add = {"type": 'passwordBased' if Keytype == 'PD' else 'keyBased', "secureKey": secureKey, "encryption_method": "AES256", "auth": auth}
        data[name] = add
        # Wright it out
        try:
            with open('secured_keys.json', 'w') as f:
                json.dump(data, f)
        except:
            modal.code("ReadingKeys")
            return None
        
        # Clear the password and tell user its done
        window.evaluate_js(f'ClearPasswordSettings();')
        modal.ok("New Key Created", f"The key \\\"{name}\\\" has been created and is now being set to the current key!")
        
        # Update all the key names
        self.updateKeyNames()
        # Update the current key to be the newly created one
        self.handelKeyIndex(password, len(self.keyOptions)-1)


    def handelKeyIndex(self, password: str, keyName: int = 0, salt: str = None):
        """
        This handels setting the key, it will run either PDkey() or KDkey accordingly
        :After the key is changed it will also refresh the file exployer
        :keyName -> index of the key acording to self.keyOptions. (0) is password derived key. This value is also always turned into the int version so strings are alowed too.
        :password -> password duh
        :salt -> Path to salt file. This can also be a emtpy string intead of None
        """
        # Key name comes in as a index number accoring to self.keyOptions
        keyName = int(keyName)
        if salt == '':
            salt = None
        
        # If key name is 0 its a password derived key
        if keyName == 0:
            self.PDkey(password, salt)
        else:
            # Open the js file
            try:
                with open('secured_keys.json', 'r') as f:
                    data = json.load(f)
            except:
                modal.code("ReadingKeys")
                return None

            # Make shure the index relates to something
            try:
                # Get name from index
                name = self.keyOptions[int(keyName)]
            except:
                # Show error if no cooralation and exit
                modal.code("InvalidKeyType")
                return None

            # Send to proper funtion to handel key
            if data[name]['type'] == "passwordBased":
                self.PDkey(password, salt, name=keyName)
            elif data[name]['type'] == "keyBased":
                self.KDkey(self.keyOptions[int(keyName)], password, salt)
            else:
                # Show error just in case
                modal.code("InvalidKeyType")

        if self.api is not None:
            self.api.refreshFileExp()

    def updateKeyNames(self):
        """ This will set the option menu on the password page to have all of the key names and the option for password based keys
        :This also updates the keys on the settings page """
        # Password page
        optionsArray = ['Password Based Key']
        # Settings page
        SettingsArray = []
        
        # Open the json file and read it
        try:
            with open('secured_keys.json', 'r') as f:
                data = json.load(f)
        except:
            modal.code("ReadingKeys")
            return None
        
        # Go through the data
        for i in data:
            # Add names to the password page
            optionsArray.append(i)

            # Get the type for the settings page
            keyType = ""
            if data[i]['type'] == 'passwordBased': keyType = 'PD'
            elif data[i]['type'] == 'keyBased': keyType = 'KD'
            else: # This should not happen unless someone has messed with the json file or the json file was made with a later version of the app
                # Show the error and quit
                modal.code('ReadingKeys')
                return None
            # Add the name and the type to the list
            SettingsArray.append({"name": i, "type": keyType})

        # self.keyOptions is used to get the name from the index
        self.keyOptions = optionsArray

        # Update the settings page
        window.evaluate_js(f'SettingsKey.populate({SettingsArray});')
        # Update the password page
        window.evaluate_js(f'updateSelectOptions({optionsArray})')


    def PDkey(self, password: str, salt: str = None, ret: bool = False, notify: bool = True, name: str = None):
        """
        Loads a password derived key
        :This is for key derived keys (The password is safely stored on the computer)
        :name -> The name of the new key
        :password -> The password of the key
        :salt -> salt file
        :ret -> returns the key intead of having the app use it (Returns the bytes)
        """
        if salt is None:
            salt = b'\x9cmNx\xa5\xd6\xdf\x98\x10Zr\xe0\xd4\xeb\x989'
        # TODO make the salt the file specified
        # TODO add saftey stuff
        
        # Return key if ret == True
        if ret:
            return PBKDF2(password.encode(), salt, dkLen=32, count=1000000, prf=lambda p, s: hmac.new(p, s, sha256).digest())
        else:
            # Otherwise go on to changing the key
            global key
            # See if the key coorasponds to something
            commented = False
            # Set the temparary key
            tmp_key = PBKDF2(password.encode(), salt, dkLen=32, count=1000000, prf=lambda p, s: hmac.new(p, s, sha256).digest())
            # If we are not checking a cooasponding key then change it
            if name is None:
                key = tmp_key
            # Open the keys file
            try:
                with open('secured_keys.json', 'r') as f:
                    data = json.load(f)
            except:
                modal.code("ReadingKeys")
                return None

            # Go through the data
            for item in (data):
                # If the key type is password based go on
                if data[item]["type"] == "passwordBased":
                    # See if key coorasponds with the name
                    if base64.b64encode(encrypt(item.encode('utf-8'), tmp_key)).decode('utf-8') == data[item]["auth"]:
                        # Update title and say we found it
                        window.title = f'Micah\'s Encryption Suite -- Key: {item}'
                        commented = True
                        # If we are not checking key name
                        if name is None:
                            # Notify who it belongs to
                            if notify: modal.ok(f"Password Assigned to \\\"{item}\\\"", f"The password you used is assigned to \\\"{item}\\\"")
                        # If we are checking key name
                        else:
                            # Update Key
                            key = tmp_key
                        break
                            

            # If no cooraspondace is found
            if not commented:
                # If we arn't checking key name
                if name is None:
                    # Update title and give a warning message
                    window.title = 'Micah\'s Encryption Suite -- Key: PSWD Based'
                    modal.ok("Password not Assigned", "The password you used is not assigned to anything. You can still use it, however, it is good to assign the password to a key in settings. This is to detect mistyped passwords.")
                else:
                    # Otherwise give a wrong password error
                    self.wrongPass()

    def KDkey(self, name: str, password: str, salt: str = None, ret: bool = False):
        """
        Loads a computer derived key
        :This is for key derived keys (The password is safely stored on the computer)
        :name -> The name of the new key
        :password -> The password of the key
        :salt -> salt file
        :ret -> returns the key intead of having the app use it (returns None or the bytes)
        """
        #secureKey = base64.b64encode(encrypt(randomKey, PDKey)).decode('utf-8')
        #auth = base64.b64encode(encrypt(base64.b64encode(name.encode("utf-8")), randomKey)).decode('utf-8')        

        global key
        # TODO add saftey stuff
        try:
            with open('secured_keys.json', 'r') as f:
                # Load the JSON data from the file
                data = json.load(f)
        except:
            modal.code("ReadingKeys")
            return None
        
        passwordKey = self.PDkey(password, salt, True)
        unValidatedKey = decrypt_data(base64.b64decode(data[name]["secureKey"].encode('utf-8')), passwordKey)
        try:
            auth = base64.b64encode(encrypt(base64.b64encode(name.encode("utf-8")), unValidatedKey)).decode('utf-8')
        except:
            auth = 'Wrong'

        if data[name]["auth"] == auth:
            if ret:
                return unValidatedKey
            else:
                key = unValidatedKey
                window.title = f'Micah\'s Encryption Suite -- Key: {name}'
        elif not ret:
            self.wrongPass()

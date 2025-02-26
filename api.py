import os
import threading
import time
import json
import webview

from Encrypt import *


from globalVaribles import *
from Encrypt import *
from RemoveANDCopy import *
from KeyMethods import keyMethods


def is_hidden(path):
    """Checks if a file or directory is hidden."""

    if os.name == 'nt':  # Windows
        return bool(os.stat(path).st_file_attributes & 0x02)
    else:  # Unix-like systems (Linux, macOS)
        return os.path.basename(path).startswith('.')

def generate_random_string(self, length: int) -> str:
    """
    Generates random string
    """
    characters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string






class Api:
    """
    An api to control the pywebview GUI
    """
    def __init__(self):
        """
        Sets some important varibles incliding the defult path
        """
        #window.events.closing += self.askToClose

        #self.dir=os.path.expanduser("~").replace('\\', '/') # TODO set defult path remove line below #BETA
        self.dir = 'C:/Users/micah/OneDrive/Desktop'
        self.prev_contents = [] # This is a list of all the files in current directory (for refreshing logic)
        self.prev_queue = [] # This is the previous queue (for refreshing logic)
        self.closing = False
        self.showHiddenFiles = False

        # Key class
        self.keyMeth = keyMethods(self)

    def log(self, value):
        """ Logs the data in the terminal DUH """
        print(value)
    
    def applySettings(self, firstTime = True):
        """ Applies Settings json file """
        # TODO litterly everthing but toggling show hidden files
        with open('settings.json', 'r') as f:
            # Load the JSON data from the file
            data = json.load(f)
        
        if firstTime: window.evaluate_js(f"ShowHiddenCheckbox.checked = {'true' if data['ShowHidden'] else 'false'};")
        window.evaluate_js(f"fileExp.ShowHidden={'true' if data['ShowHidden'] else 'false'};fileExp.refresh();")
    
    def toggleHiddenFileVisibility(self):
        """ Self explanitory """
        with open('settings.json', 'r') as f:
            # Load the JSON data from the file
            data = json.load(f)
        data['ShowHidden'] = not data['ShowHidden']
        with open('settings.json', 'w') as f:
            json.dump(data, f)
        self.applySettings(False)

    def newPage(self): #TODO Reopen the program Reentry of password manditory
        pass

    def load(self):
        """ Starts the js code that relies on the API; This will run soon as the API starts working """
        #TODO Sent weather or not its running on windows or linux to front end (Send ti searchbar.js)
        window.evaluate_js('make();')
        self.changeDir(self.dir)
        threading.Thread(target=lambda: self.overAllRefresher(True)).start()

    def overAllRefresher(self, recursive: bool = False):
        """
        This funtion will refresh nessisary parts of the screen every eight seconds such as the file exployer
        :This is also the thread that manages all of the other threads (:
        :This should be run on a thread
        :recursive -> weather it should run recursevly
        """
        #TODO put queue items that are done to the bottom
        if self.closing:
            pass
        else:
            global MAX_THREADS, THREADS
            if self.prev_contents != os.listdir(self.dir):
                self.refreshFileExp()
            # Refresh the queue and run the stuff waiting inside of it
            if queue != self.prev_queue:
                self.prev_queue = queue.copy()
                # Start the items waiting in the queue
                if len(THREADS) <= MAX_THREADS:
                    for item in range (len(queue)):
                        if (queue[item]['action'] == 'Encrypting') & (queue[item]['status'] == 'Pending'):
                            queue[item]['status'] = 'Running'
                            THREADS.append({"id": queue[item]['id'],"thread": threading.Thread(target=lambda: go_through_e_start(queue[item]['target'], queue[item]['destination'], key, queue[item]['id']))})
                            THREADS[-1]["thread"].start()
                        elif (queue[item]['action'] == 'Decrypting') & (queue[item]['status'] == 'Pending'):
                            queue[item]['status'] = 'Running'
                            THREADS.append({"id": queue[item]['id'],"thread": threading.Thread(target=lambda: go_through_d_start(queue[item]['target'], queue[item]['destination'], key, queue[item]['id']))})
                            THREADS[-1]["thread"].start()
            window.evaluate_js(f'queue.populate({queue})')
            if recursive:
                time.sleep(5)
                self.overAllRefresher(True)
    
    def cancel(self, id: str):
        '''
        Cancel a thread by ID
        :Litterly just chance status to Canceling
        '''
        global queue
        for i in range (len(queue)):
            if queue[i]['id'] == id:
                queue[i]['status'] = 'Canceling'






    def get_drives(self) -> list:
        """ Returns an array of drive locations """
        #drives = [] #TODO create a better way of getting list of drives
        #if os.name == 'nt':  # checking if the OS is Windows
            #drives = [f"{d}:/" for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f"{d}:/")]
        #return drives
        return ['/']

    def open(self, value: list):
        """ If dir open new dir, else open the file """
        # TODO if its a file then is a Virtual Workspace
        value = value[0]
        if not os.path.isabs(value):
            value = f'{self.dir}/{value}'
        if os.path.isdir(value):
            self.changeDir(value)
    
    def refreshFileExp(self):
        self.changeDir()

    def changeDir(self: str, value: str = None):
        ''' Changes the directory and refreshes the page; If you dont set value it refreshes the page '''
        value = f'{value}'
        if value is None or value == 'None': # ?
            value = self.dir

        # Try to get contents of directory
        try:
            contents = os.listdir(value)
            self.prev_contents = contents
            self.dir = value
        except: # Raise an error and back peddle
            window.evaluate_js(f'showModalOK("Permission Denied", "There was an error while trying to open \\\"{value}\\\" you probably don\'t have permission or the file doesn\'t exist", "Okay");')
            contents = os.listdir(self.dir)
            value = self.dir

        info = []
        for con in contents:
            name, enc = decrypt_name (con, key)
            tmp = f"{{'name': '{name}', 'real_name': '{con}', 'isDirectory': {'true' if os.path.isdir(f'{value}/{con}') else 'false'}, 'isEncrypted': {'true' if enc else 'false'}, 'isHidden': {'true' if is_hidden(f'{value}/{con}') else 'false'}}}"
            info.append(tmp)
        
        info.sort() 

        joined_string = ', '.join(info)
        final_string = joined_string.strip(',')
        window.evaluate_js(f'fileExp.files=[{final_string}];fileExp.refresh();')

        path_array = value.split('/')
        path_array = [item for item in path_array if item != '']
        window.evaluate_js(f'fileExp.searchBar.workingDirectory = {path_array};fileExp.searchBar.refreshButtons();')

    def deleate(self, targets: str, secure: bool):
        """ This deleates the file or folder """
        # TODO Put deleated items in recycling bin linux?
        for target in targets:
            error = remove.remove(f'{self.dir}/{target}', secure)
            if error: window.evaluate_js(f'showModalOK("Permission Denied", "There was an error while trying to remove \\\"{target}\\\" you probably don\'t have permission", "Okay");')
        self.refreshFileExp()

    def encrypt(self, targets: str, destination: str, overWrightPreExisiting: bool = False):
        """ This starts the encryption """
        #TODO add overWrightPreExisiting functinality
        global key, queue
        if key is None:
            self.keyMeth.noKey()
        else:
            for target in targets:
                id = generate_random_string(20)
                queue.append({'action': 'Encrypting', 'status': 'Pending', 'target': f'{target}', 'destination': f'{destination}', 'progress': 0, 'id': f'{id}'})

    def decrypt(self, targets: str, destination: str, overWrightPreExisiting: bool = False):
        #TODO add overWrightPreExisiting functinality
        """ This starts the decryption """
        global key, queue
        if key is None:
            self.keyMeth.noKey()
        else:
            for target in targets:
                id = generate_random_string(20)
                queue.append({'action': 'Decrypting', 'status': 'Pending', 'target': f'{target}', 'destination': f'{destination}', 'progress': 0, 'id': f'{id}'})
                #go_through_d_start(target, destination, key, id)
    
    def move(self, targets: str, destination: str):
        """
        Moves the target to the destination
        """
        #TODO see if file exists first
        for target in targets:
            os.rename(target, f'{destination}/{os.path.basename(target)}')
        self.refreshFileExp()

    def copy(self, targets: str, destination: str):
        #TODO add functinality so that it doesn't overwight something else
        """
        Copies the target file/folder to the destination directory
        """
        # TODO Fix the renameing of the file, - copy(2) && fix it when your coping something encrypted
        for target in targets:
            error = copy.go_through_c_start(target, destination)
            if error: window.evaluate_js(f'showModalOK("Permission Denied", "There was an error while trying to copy \\\"{target}\\\". We tried our best and copied all the files we could however 1 or more did not copy and you probably don\'t have permission", "Okay");')
        self.refreshFileExp()

    def rename(self, target: str, new_Name: str, encryptedNameOverWright: bool = False):
        """
        Renames and removes files
        :target & new_Name need to be absolute paths
        :encryptedNameOverWright if this is false it will reencrypt the name (This is for the move functinality)
        """
        #TODO see if file exists first
        n, e = decrypt_name(os.path.basename(target), key)
        try:
            if e or encryptedNameOverWright:
                os.rename(target, f'{os.path.dirname(new_Name)}/{encrypt_name(os.path.basename(new_Name), key)}')
            else:
                os.rename(target, new_Name)
            self.refreshFileExp()
        except Exception as e:
            window.evaluate_js(f'showModalOK("Permission Denied", "There was an error while trying to rename \\\"{target}\\\" you probably don\'t have permission or the file doesn\'t exist {e}", "Okay");')
    
    def newFile(self, location: str, encrpytion: bool):
        """
        Creates a new file
        :location absolute path of file (Including unecrypted name)
        :encrpytion Weather or not the file is encrypted
        """
        #TODO see if the file exists first
        try:
            if encrpytion:
                if key is None:
                    self.keyMeth.noKey()
                else:
                    with open(f'{os.path.dirname(location)}/{encrypt_name(os.path.basename(location), key)}', 'wb') as file:
                        file.write(encrypt(b'', key))
            else:
                with open(location, 'w') as file:
                    pass
            self.refreshFileExp()
        except:
            window.evaluate_js(f'showModalOK("Permission Denied", "There was an error while trying to make the file \\\"{location}\\\" you probably don\'t have permission or you used am illegal character \\/\":*?<>|", "Okay");')


    def newFolder(self, location: str, encrpytion: bool):
        """
        Creates a new folder
        :location absolute path of folder (Including unecrypted name)
        :encrpytion weather or not the folder is encrypted
        """
        try:
            if encrpytion:
                if key is None:
                    self.keyMeth.noKey()
                else:
                    os.makedirs(f'{os.path.dirname(location)}/{encrypt_name(os.path.basename(location), key)}', exist_ok=False)
            else:
                os.makedirs(location, exist_ok=False)
            self.refreshFileExp()
        except:
            window.evaluate_js(f'showModalOK("Permission Denied", "There was an error while trying to make the file \\\"{location}\\\" you probably don\'t have permission or you used an illegal character \\/\":*?<>|", "Okay");')






    def askToClose(self):
        """
        Funtion that runs when app is trying to close
        :Tests to see if the app should be closing
        :If not cancel close and ask user
        :BTW This was a fucking rediculous work around and it sucked ass
        """
        if not self.closing:
            self.fuckyou = True
            pending = 0
            running = 0
            for item in range (len(queue)):
                if queue[item]['status'] == 'Running':
                    running += 1
                elif queue[item]['status'] == 'Pending':
                    pending += 1
            threading.Thread(target = lambda: self.waitUntilAsk(running, pending)).start()
            self.fuckyou = False
            return False
        return True
    
    def waitUntilAsk(self, running, pending):
        """
        Ask if the user wants to close the app, wait until signal
        """
        while self.fuckyou:
            time.sleep(.1)
        time.sleep(.1)
        window.evaluate_js(f'showModalTF(kma.exit, \'Do you want to exit?\', \'Do you really want to exit? You have {running} item(s) running and {pending} item(s) pending.\', \'Close\', \'Cancel\')')

    def close(self):
        """
        Close the entire application gracefully
        """
        self.closing = True
        global queue
        for i in range (len(queue)):
            if queue[i]['status'] == 'Running':
                queue[i]['status'] = 'Canceling'
        time.sleep(.1)
        window.destroy()


class initiateApp:
    def __init__(self):
        global window
        API_Cont=Api()
        window = webview.create_window("Micah's Encryption Suite", 'GUI/main.html', js_api=API_Cont)
        set_global_var('my_global_var', window)
        window.events.closing += API_Cont.askToClose
        
        webview.start(API_Cont.load, debug=True)
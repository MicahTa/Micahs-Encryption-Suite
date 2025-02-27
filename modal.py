from globalVaribles import *
#TODO I should probobly make this more efficent by not maing it reget the window varible all the time

class modal:
    @classmethod
    def defineWin(self):
        if not 'window' in locals():
            global window
            window=shared_dict['my_global_var']
        
    @classmethod
    def code(self, code: str):
        """
        code -> The error code you want to display
        """
        self.defineWin()

        codes = {
            "NoKey": {
                "type": "ok",
                "title": "No key Selected",
                "text": "No key has been selected and unlocked. This must be done before any decrypting or encrypting can take place. Please select the shield icon on the left bar to do so.",
                "button": "Okay"
                    },
            "WrongPass": {
                "type": "ok",
                "title": "Wrong Password",
                "text": "You either entered the wrong password or you used the wrong/no salt file when it was required.",
                "button": "Okay"
                    },
            "ReadingKeys": {
                "type": "ok",
                "title": "Error Reading Keys",
                "text": "There has been an error while trying to read keys file. Please contact HR if applicable otherwise please go to settings and restore keys.",
                "button": "Okay"
            },
            "InvalidKeyName": {
                "type": "ok",
                "title": "Invalid name",
                "text": "You have entered an invalid name, due to it already existing or being blocked. Please try another name. (:",
                "button": "Okay"
            },
            "InvalidKeyType": {
                "type": "ok",
                "title": "Invalid Key Type",
                "text": "The key you used seemed to not have a valid type, try updating the software or restoring a backup of the Keys",
                "button": "Okay"
            }
                }

        if code in codes:
            if codes[code]["type"] == "ok":
                self.ok(codes[code]["title"], codes[code]["text"], codes[code]["button"])
            else: raise Exception("Invalid Modal Type")
        else: raise Exception("Invalid Modal Code")


    @classmethod
    def ok(self, title: str, text: str, button: str = "Okay"):
        """
        Title -> The title of the modal
        Text -> Text of the modal
        Button -> Text to be displayed on button
        """
        self.defineWin()

        window.evaluate_js(f'showModalOK("{title}", "{text}", "{button}");')
    
    @classmethod
    def tf(self, function, title: str, text: str, true: str = "Yes", false: str = "No"):
        """"
        funtion -> javaScript funtion the output will be directed towards
        Title -> Title of the modal
        Text -> Text of the modal
        true -> text on true button
        false -> text on false button
        """
        self.defineWin()

        window.evaluate_js(f'showModalTF({function}, \'{title}?\', \'{text}\', \'{true}\', \'{false}\')')
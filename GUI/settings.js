/////////////////////////// Key Code //////////////////////////////////////
// Toggle Visability of Password Box
const SettingsPasswordInputOne = document.getElementById('SettingsPasswordInputOne');
const SPIOTVI = document.getElementById('SPIOTVI');

SPIOTVI.addEventListener('click', function() {
if (SettingsPasswordInputOne.type === 'password') {
    SettingsPasswordInputOne.type = 'text';
    SPIOTVI.className = 'fa-regular fa-eye SettingsToggleVisibilityIcon';
} else {
    SettingsPasswordInputOne.type = 'password';
    SPIOTVI.className = 'fa-regular fa-eye-slash SettingsToggleVisibilityIcon';
}
});

// Toggle Visability of Second Password Box
const SettingsPasswordInputTwo = document.getElementById('SettingsPasswordInputTwo');
const SPITTVI = document.getElementById('SPITTVI');

SPITTVI.addEventListener('click', function() {
if (SettingsPasswordInputTwo.type === 'password') {
    SettingsPasswordInputTwo.type = 'text';
    SPITTVI.className = 'fa-regular fa-eye SettingsToggleVisibilityIcon';
} else {
    SettingsPasswordInputTwo.type = 'password';
    SPITTVI.className = 'fa-regular fa-eye-slash SettingsToggleVisibilityIcon';
}
});

// Clear settings after a key has been created
function ClearPasswordSettings() {
    document.getElementById('settingsNewKeyName').value = "";
    document.getElementById('SettingsKeyType').value = "";
    document.getElementById('EncryotionType').value = "";
    document.getElementById('SettingsPasswordInputOne').value = "";
    document.getElementById('SettingsPasswordInputTwo').value = "";
}






class SettingsKeyList {
    constructor() {
        this.settingsKeyMain = document.getElementById('SettingsKeys');
    }

    /*      Share Password     */
    ////////////////////////////////////////////////////////////////////////////////
    share = (name) => {
        this.sharingPassword = name;
        showModalTF(this.shareNewPass, '⚠️ WARNING ⚠️', 'Sharing keys is very unsecure, once this person has your key there is no way of disallowing them to use it, this means that they will access to all of your data. If you want to share password securely upgrade to the enterprize edition. It would also be way easier for a threat to gain access to your keys. If you choose to share the password the share string will only be valid for one day. (-;', 'Continue', 'Cancel');
    }
    shareNewPass = (aceptedWarning) =>  {
        if (aceptedWarning) {
            showModalPswd(this.shareCurrentPassword, 'New Password', 'This will be the password the new user will have and will be used to unlock the key when you share it', 'Continue', 'Cancel')
        }
    }
    shareCurrentPassword = (NewPass) =>  {
        this.newSharePass = NewPass
        showModalPswd(this.callShareAPI, 'Current Password', `Enter the current password for ${this.sharingPassword}`, 'Continue', 'Cancel')
    }

    callShareAPI = (password) => {
        pywebview.api.keyMeth.createSharedKey(this.sharingPassword, password, this.newSharePass);
    }
    ////////////////////////////////////////////////////////////////////////////////

    /*      Change password     */
    ////////////////////////////////////////////////////////////////////////////////
    changePSWD = (name) =>  {
        console.log(`Changing Password on key key ${name}`);
        this.changing = name;

        showModalPswd(this.CPGetNewPass, 'Password', `Enter the password for ${this.changing}`, 'Continue', 'Cancel')
        // Get old password, get new password twice
    }
    CPGetNewPass = (oldPass) => {
        this.oldPass = oldPass
        showModalPswd(this.CPConfirmPass, 'New Password', `Enter the new password for ${this.changing}`, 'Continue', 'Cancel')
    }
    CPConfirmPass = (firstPass) => {
        this.firstPass = firstPass
        showModalPswd(this.CPCallAPI, 'Retype New Password', `Enter the new password for ${this.changing}`, 'Continue', 'Cancel')
    }
    CPCallAPI = (secondPass) => {
        if (secondPass != this.firstPass) {
            showModalOK('Passwords do not match', 'The passwords you have entered do not match', 'Ok')
        } else {
            pywebview.api.keyMeth.changePass(this.changing, this.oldPass, secondPass)
        }
        this.oldPass = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        this.firstPass = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    }
    ////////////////////////////////////////////////////////////////////////////////

    /*      Delete     */
    ////////////////////////////////////////////////////////////////////////////////
    deleate = (name) => {
        this.deleting = name;
        showModalPswd(this.callDelAPI, 'Password', `Type the password to delete '${name}'`, 'Continue', 'Cancel');
    }
    callDelAPI = (pswd) => {
        pywebview.api.keyMeth.delete(this.deleting, pswd);
    }
    ////////////////////////////////////////////////////////////////////////////////

    /*      Rename     */
    ////////////////////////////////////////////////////////////////////////////////
    rename = (name) => {
        let textbox = document.getElementById(`Settings-Key-ID-${name}`);
        if (name != textbox.value) {
            this.renaming = name;
            showModalPswd(this.callRenameAPI, 'Password', `Type the password for '${name}' to rename it`, 'Continue', 'Cancel');
        }
    }
    callRenameAPI = (password) => {
        let textbox = document.getElementById(`Settings-Key-ID-${this.renaming}`);
        pywebview.api.keyMeth.rename(this.renaming, textbox.value, password);
    }
    ////////////////////////////////////////////////////////////////////////////////
    
    // ######################################## Cell Controll ######################################## //
    depopulate() {
        Array.from(this.settingsKeyMain.getElementsByClassName('settingTile')).forEach(segment => {
            segment.remove(); // Remove each directory button
        });
    }

    populate(array) {
        this.depopulate()
        for (let i = 0; i < array.length; i++) {
            const fileElement = document.createElement('div');
            fileElement.classList.add('settingTile');
            fileElement.innerHTML = `
            <input type="text" id="Settings-Key-ID-${array[i].name}" class="keyTextBox keyTitle" value="${array[i].name}">
            <input type="text" class="keyTextBox" value="${(array[i].type == 'PD' ? "Password Based Key" : "Computer Based Key")}" readonly>
            <i class="fa-solid fa-share keyIcons ${(array[i].type == 'PD' ? "keyBlankIcons" : "")}" title="Share" id="Settings-Key-Share-${array[i].name}"></i>
            <i class="fa-solid fa-pen keyIcons ${(array[i].type == 'PD' ? "keyBlankIcons" : "")}" title="Change Password" id="Settings-Key-ChangePassword-${array[i].name}"></i>
            <i class="fa-solid fa-trash keyIcons keyDeleateIcon" title="Deleate" id="Settings-Key-Deleate-${array[i].name}"></i>
            `;
            this.settingsKeyMain.appendChild(fileElement);

            // Add listener for sharing
            if (array[i].type != 'PD') {
                document.getElementById(`Settings-Key-Share-${array[i].name}`).addEventListener('click', function () {
                    SettingsKey.share(array[i].name);
                });
            }
            // Add listener for Changing Password
            if (array[i].type != 'PD') {
                document.getElementById(`Settings-Key-ChangePassword-${array[i].name}`).addEventListener('click', function () {
                    SettingsKey.changePSWD(array[i].name);
                });
            }
            // Add listener for deleating keys
            document.getElementById(`Settings-Key-Deleate-${array[i].name}`).addEventListener('click', function () {
                SettingsKey.deleate(array[i].name);
            });
            // Add event listener for when the text box is edited
            let textbox = document.getElementById(`Settings-Key-ID-${array[i].name}`);
            textbox.addEventListener('blur', function() {
                SettingsKey.rename(array[i].name);
            });

        };
    }
}
const SettingsKey = new SettingsKeyList();
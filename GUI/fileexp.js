class fileexp {
    // Mkes eveything
    constructor() {
        // Holds all the files in current dir
        this.files = [{name: "LOADING...", isDirectory: true, isEncrypted: false}]

        this.ShowHidden = false;
    
        // Icons and icon varibles
        this.fileExplorer = document.getElementById('fileExplorer');
        this.ToggeledIconsContainer = document.getElementById('ToggeledIconsContainer');
        this.selectedFiles = {name: [], real_name: []};
        this.ClipOcupied = [];
        this.selectingType = ''; // decrypt encrypt move or ''
        this.selectingWhat = [];

        this.renameIcon = document.getElementById('Rename');
        this.deleteIcon = document.getElementById('Delete');
        this.lockIcon = document.getElementById('Lock');
        this.unlockIcon = document.getElementById('Unlock');
        // this.openIcon = document.getElementById('Open');
        this.moveIcon = document.getElementById('Move');
        this.copyIcon = document.getElementById('Copy');
        this.pasteIcon = document.getElementById('Paste');
        this.selectIcon = document.getElementById('Select');
        this.saltIcon = document.getElementById('Salt');
        this.driveIcon = document.getElementById('Drive');


        this.addFolderIcon = document.getElementById('AddFolder');
        this.addFileIcon = document.getElementById('AddFile');
        this.addFolderIcon.addEventListener('click', this.addFolderIconClickHandler);
        this.addFileIcon.addEventListener('click', this.addFileIconClickHandler);
        this.driveIcon.addEventListener('click', this.driveIconClickHandler);


        this.addIconListeners();
        this.toggleIcons();
        // Open files when you hit enter and have them selected
        /* document.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                this.open_file(this.selectedFiles.name)
                this.deselect_all()
            }
        }); */
        // papulate the file exployer
        this.populateFileExplorer();
    }

    // changes the directory and then repopultes
    make(){
        // Python runs the refresh code
        this.searchBar = new searchbar();
    }

    findIsDirectory(value) {
        for (let i = 0; i < this.files.length; i++) {
            if (this.files[i].real_name === value) {
                return this.files[i].isDirectory;
            }
        }
        // If value not found, return null or handle as appropriate
        return undefined;
    }

    // Icon listiners for when you press them
    addIconListeners() {
        Array.from(this.ToggeledIconsContainer.getElementsByClassName('topbar-icon')).forEach(segment => {
            //topbar-icon-grey
            segment.classList.remove('topbar-icon-grey');
        });
        // Add a click event listeners
        this.renameIcon.addEventListener('click', this.renameIconClickHandler);
        this.deleteIcon.addEventListener('click', this.deleteIconClickHandler);
        this.lockIcon.addEventListener('click', this.lockIconClickHandler);
        this.unlockIcon.addEventListener('click', this.unlockIconClickHandler);
        // this.openIcon.addEventListener('click', this.openIconClickHandler);
        this.moveIcon.addEventListener('click', this.moveIconClickHandler);
        this.copyIcon.addEventListener('click', this.copyIconClickHandler);
        this.pasteIcon.addEventListener('click', this.pasteIconClickHandler);
        this.selectIcon.addEventListener('click', this.selectIconClickHandler);
        this.saltIcon.addEventListener('click', this.saltIconClickHandler);
        //this.driveIcon.addEventListener('click', this.driveIconClickHandler);
        //this.addFolderIcon.addEventListener('click', this.addFolderIconClickHandler);
        //this.addFileIcon.addEventListener('click', this.addFileIconClickHandler);
    }

    // Icon listener handlers
    renameIconClickHandler = () => {
        showModalTxt(this.renameAction, 'Rename', 'Please enter the new file name', 'Continue', 'Cancel');
    }
    renameAction = (newname) => {
        const location = this.searchBar.getPath()
        pywebview.api.rename(`${location}/${this.selectedFiles.real_name[0]}`, `${location}/${newname}`)
    }
    deleteIconClickHandler = () => {
        showModalTF(this.deleateVerifyOption, 'Are you sure?', `This operation will delete ${this.selectedFiles.name.length} item(s)`, 'Yes', 'No');
    }
    deleateVerifyOption = (Option) => {
        if (Option) {
            showModalTF(this.deleateAfterOption, 'Do you want to securely remove these items', 'Securely removing the files will first overwrite them with 0\'s to make them impossible to recover. Note that with some services like OneDrive previous versions are stored and cannot be removed by this app', "Yes", "No")
        }    
    }
    deleateAfterOption = (Option) => {
        pywebview.api.deleate(this.selectedFiles.real_name, Option);
    }
    lockIconClickHandler = () => {
        this.selectingType = 'encrypt';
        const location = this.searchBar.getPath()
        for (let i of this.selectedFiles.real_name) {
            this.selectingWhat.push(`${location}/${i}`);
        }
        this.toggleIcons();
    }
    unlockIconClickHandler = () => {
        this.selectingType = 'decrypt';
        const location = this.searchBar.getPath()
        for (let i of this.selectedFiles.real_name) {
            this.selectingWhat.push(`${location}/${i}`);
        }
        this.toggleIcons();
    }
    /* openIconClickHandler = () => {
        console.log(`Opening ${this.selectedFiles.real_name}`)
    } */
    moveIconClickHandler = () => {
        this.selectingType = 'move';
        const location = this.searchBar.getPath()
        for (let i of this.selectedFiles.real_name) {
            this.selectingWhat.push(`${location}/${i}`);
        }
        this.toggleIcons();
    }
    copyIconClickHandler = () => {
        this.ClipOcupied = []
        for (let i = 0; i < this.selectedFiles.real_name.length; i++) {
            this.ClipOcupied.push(`${this.searchBar.getPath()}/${this.selectedFiles.real_name[i]}`)
        }
        this.toggleIcons();
    }
    pasteIconClickHandler = () => {
        pywebview.api.copy(this.ClipOcupied, `${this.searchBar.getPath()}`);
    }
    selectIconClickHandler = () => {
        //decrypt encrypt move
        console.log(this.selectingWhat)
        if (this.selectingType == 'decrypt'){
            showModalTF(this.decrypt, 'Remove existing files', 'If files with the same name already exist do you want to overwrite them?', 'Yes', 'No')
        } else if (this.selectingType == 'encrypt') {
            showModalTF(this.encrypt, 'Remove existing files', 'If files with the same name already exist do you want to overwrite them?', 'Yes', 'No')
        } else if (this.selectingType == 'move') {
            pywebview.api.move(this.selectingWhat, `${this.searchBar.getPath()}`)
            this.selectingWhat = [];
        }
        this.selectingType = '';
        this.toggleIcons();
    }
    decrypt = (removeIfAlreadyExits) => {
        pywebview.api.decrypt(this.selectingWhat, `${this.searchBar.getPath()}`, removeIfAlreadyExits)
        this.selectingWhat = [];
    }
    encrypt = (removeIfAlreadyExits) => {
        pywebview.api.encrypt(this.selectingWhat, `${this.searchBar.getPath()}`, removeIfAlreadyExits)
        this.selectingWhat = [];
    }
    addFolderIconClickHandler = () => {
        showModalTxt(this.folderIconOption, 'Create Folder', 'Enter the name of the new folder', 'Continue', 'Cancel');
    }
    folderIconOption = (name) => {
        this.folderName = name;
        showModalTF(this.FolderCreateAfterName, 'Encrypted?', 'Do you want to encrypt the folder name?', 'Yes', 'No');
    }
    FolderCreateAfterName = (enc) => {
        pywebview.api.newFolder(`${this.searchBar.getPath()}/${this.folderName}`, enc)
    }
    addFileIconClickHandler = () => {
        showModalTxt(this.fileIconOption, 'Create File', 'Enter the name of the new file', 'Continue', 'Cancel');
    }
    fileIconOption = (name) => {
        this.fileName = name;
        showModalTF(this.FileCreateAfterName, 'Encrypted?', 'Do you want to encrypt the file name and its contents?', 'Yes', 'No');
    }
    FileCreateAfterName = (enc) => {
        pywebview.api.newFile(`${this.searchBar.getPath()}/${this.fileName}`, enc)
    }
    saltIconClickHandler = () => {
        salt_file = this.selectedFiles.real_name[0];
        if (salt_file === undefined) {
            salt_file = '';
        }
    }
    async driveIconClickHandler() {
        // Get drives
        let drives = await pywebview.api.get_drives();
        showModalOption(fileExp.driveAfterOption, "Select Drive", "", drives, "Cancel");
    }
    driveAfterOption = (option) => {
        pywebview.api.changeDir(option);
    }

    // Toggle icons
    // Runs every time selectedFiles is changes
    toggleIcons() {
        this.addIconListeners();
        // Select Button
        if (this.selectingType == '') {
            this.selectIcon.removeEventListener('click', this.selectIconClickHandler);
            this.selectIcon.classList.add('topbar-icon-grey');
        }
        // Clip board
        if (this.ClipOcupied.length == 0) {
            this.pasteIcon.removeEventListener('click', this.pasteIconClickHandler);
            this.pasteIcon.classList.add('topbar-icon-grey');
        }
        // Remane icon
        let count = this.selectedFiles.name.length;
        if (count != 1) {
            this.renameIcon.removeEventListener('click', this.renameIconClickHandler);
            this.renameIcon.classList.add('topbar-icon-grey');
        }
        // Salt icon
        if (count < 2) {
            let tmp = this.selectedFiles.real_name[0];
            if (tmp != undefined) {
                if (this.findIsDirectory(tmp)) {
                    this.saltIcon.removeEventListener('click', this.saltIconClickHandler);
                    this.saltIcon.classList.add('topbar-icon-grey');
                }
            }
        } else {
            this.saltIcon.removeEventListener('click', this.saltIconClickHandler);
            this.saltIcon.classList.add('topbar-icon-grey'); 
        }
        // Everyhting else
        if (count == 0) {
            this.deleteIcon.removeEventListener('click', this.deleteIconClickHandler);
            this.deleteIcon.classList.add('topbar-icon-grey');
            this.lockIcon.removeEventListener('click', this.lockIconClickHandler);
            this.lockIcon.classList.add('topbar-icon-grey');
            this.unlockIcon.removeEventListener('click', this.unlockIconClickHandler);
            this.unlockIcon.classList.add('topbar-icon-grey');
            // this.openIcon.removeEventListener('click', this.openIconClickHandler);
            // this.openIcon.classList.add('topbar-icon-grey');
            this.moveIcon.removeEventListener('click', this.moveIconClickHandler);
            this.moveIcon.classList.add('topbar-icon-grey');
            this.copyIcon.removeEventListener('click', this.copyIconClickHandler);
            this.copyIcon.classList.add('topbar-icon-grey');
        }

    }
    // If you click a file togle its selected ness
    toggleSelection(fileElement) {
        fileElement.classList.toggle('fileExplorer-selected');
        const index = (fileElement.getAttribute('data-index'));
        const index_FRN = (fileElement.getAttribute('data-RN-Index'));
        if (fileElement.classList.contains('fileExplorer-selected')) {
            this.selectedFiles.name.push(index);
            this.selectedFiles.real_name.push(index_FRN);
        } else {
            const indexToRemove = this.selectedFiles.real_name.indexOf(index_FRN);
            
            if (indexToRemove !== -1) {
                // Remove the element at the index from both arrays
                this.selectedFiles.real_name.splice(indexToRemove, 1);
                this.selectedFiles.name.splice(indexToRemove, 1);
            }
            //this.selectedFiles = this.selectedFiles.filter(idx => idx.real_name !== index_FRN);
        }
    }

    // Deselect all files
    deselect_all() {
        const fileElements = document.querySelectorAll('.file');
        fileElements.forEach(fileElement => {
            if (this.selectedFiles.name.includes(parseInt(fileElement.getAttribute('data-index')))) {
                fileElement.classList.remove('fileExplorer-selected');
            }
        });
        this.selectedFiles = {name: [], real_name: []};
    }

    // This will open a file in a new window
    async open_file(index_array) {
        pywebview.api.open(index_array);
    }

    refresh() {
        this.depopulateFileExplorer();
        this.populateFileExplorer();
    }

    // Removes everything file file explyer
    depopulateFileExplorer() {
        Array.from(this.fileExplorer.getElementsByClassName('fileExplorer-file')).forEach(segment => {
            segment.remove(); // Remove each directory button
        });
    }

    // Adds everything from the files varible to file exp
    populateFileExplorer() {
        this.deselect_all();
        this.toggleIcons();
        console.log(this.files);
        for (let i = 0; i < this.files.length; i++) {
            console.log(this.ShowHidden)
            if (this.files[i].isHidden && !this.ShowHidden){
                continue
            }
            const fileElement = document.createElement('div');
            fileElement.classList.add('fileExplorer-file');
            const iconClass = this.files[i].isDirectory ? 'fas fa-folder' : 'fas fa-file';
            const encrypClass = this.files[i].isEncrypted ? 'color: #b0199f;' : 'color: #000000;';
            fileElement.innerHTML = `
                <div class="fileExplorer-icon" style="${encrypClass}"><i class="${iconClass}"></i></div>
                <div class="fileExplorer-file-name">${this.files[i].name}</div>
            `;
            let nm_for_lstner = this.files[i].name
            let nm_for_lstner_RN = this.files[i].real_name
            fileElement.addEventListener('dblclick', () => {
                this.open_file([nm_for_lstner_RN])
                this.deselect_all()
            });
            fileElement.setAttribute('data-index', nm_for_lstner);
            fileElement.setAttribute('data-RN-Index', nm_for_lstner_RN);
            fileElement.addEventListener('click', (event) => {
                this.toggleSelection(fileElement);
                console.log(this.selectedFiles);
                this.toggleIcons();
                event.stopPropagation();
            });
            this.fileExplorer.appendChild(fileElement);
        };
    }
}

const fileExp = new fileexp();
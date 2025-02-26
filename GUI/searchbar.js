class searchbar {
    constructor() {
        this.workingDirectory = []; // Initial working directory
        this.searchBar = document.getElementById('searchBar');
        this.currentDirectoryInput = document.getElementById('currentDirectoryInput');
        this.prev = ''
        this.linux = false

        
        // Event listener to detect when space to right is pressed
        this.searchBar.addEventListener('click', (event) => {

            // Get the target element of the click event
            const target = event.target;

            // Check if the click target is not a directory button or the text input field
            if (!target.classList.contains('search-directory-button') && !target.classList.contains('search-text-input')) {
                // If the click is not on a directory button or the text input field, collapse the buttons into the text input
                this.collapseToTextInput();
            }
        });

        // Event listener to show directory buttons when exiting the input field
        this.currentDirectoryInput.addEventListener('blur', () => {

            // Split the value of the input field by '/'
            this.workingDirectory = this.currentDirectoryInput.value.replace(/\\/g, '/').split('/');
            this.expandToButton();

        });

        // Event listener to update buttons text when input field changes
        this.currentDirectoryInput.addEventListener('input', () => {
            // Split the value of the input field by '/'
            const segments = this.currentDirectoryInput.value.replace(/\\/g, '/').split('/');

            // Update the text content of each directory button
            Array.from(this.searchBar.getElementsByClassName('search-directory-button')).forEach((segment, index) => {
                segment.textContent = segments[index] || ''; // Set the text content to the corresponding segment, or empty string if segment is undefined
            });
        });

        this.expandToButton();

    }


    // Function to log directory
    async API() {
        let tmp = this.workingDirectory.join('/')
        if (tmp != this.prev) {
            this.prev = tmp
            pywebview.api.changeDir(tmp);
        }
    }


    // Function to get current directory path
    getPathFromText() {

        // Select all elements with the class 'directory-segment' within the this.searchBar
        const directorySegments = Array.from(this.searchBar.querySelectorAll('.search-directory-button'));

        // Map each selected element to its text content (directory name)
        const directoryNames = directorySegments.map(segment => segment.textContent);

        // Return the array of directory names representing the current directory path
        return directoryNames;
    }


    getPath () {
        let path = this.getPathFromText().join('/'); // Set the value of the text input to the current directory path
        if (this.linux) {
            path = path.slice(1);
            if (path === '') {
                path = '/'
            }
        }
        return path
    }

    // Collapse the buttons into the text input
    collapseToTextInput() {
        this.currentDirectoryInput.classList.remove('invisible'); // Make the text input visible

        this.currentDirectoryInput.focus(); // Focus on the text input
        let path = this.getPathFromText().join('/'); // Set the value of the text input to the current directory path
        if (this.linux) {
            path = path.slice(1);
            if (path === '') {
                path = '/'
            }
        }
        this.currentDirectoryInput.value = path
        this.removeButtons();
    }

    removeButtons() {
        Array.from(this.searchBar.getElementsByClassName('search-directory-button')).forEach(segment => {
            segment.remove(); // Remove each directory button
        });
    }

    refreshButtons() {
        this.removeButtons();
        this.expandToButton();
        
    }

    expandToButton() {
        let segments = this.workingDirectory;
        if (this.linux) { segments = ['/'].concat(segments); }
        console.log(segments)
        // Create a directory button for each segment
        segments.forEach((segment, index) => {
            const button = document.createElement('div');
            button.classList.add('search-directory-button');
            button.textContent = segment;
            // Add event listener to the button
            button.addEventListener('click', () => {
                this.workingDirectory = segments.slice(0, index+1);
                this.refreshButtons();
            });
            this.searchBar.insertBefore(button, this.currentDirectoryInput); // Insert the button before the input field

        });

        // Hide the input field
        this.currentDirectoryInput.classList.add('invisible');

        // Log the current directory (optional)
        this.API();
    }


}
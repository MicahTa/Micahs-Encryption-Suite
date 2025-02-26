// Modal script Password Input
const modalPswd = document.getElementById("myPswdModal");


const PswdModTitle = document.getElementById("PswdModalTitle");
const PswdModText = document.getElementById("PswdModalText");
const PswdModbuttonGo = document.getElementById("PswdModalButtonEnter");
const PswdModbuttonCancel = document.getElementById("PswdModalButtonCancel");
let PswdModGo = function() {
};
function HidePswdMod() {
    modalPswd.style.display = "none";
    document.getElementById('PswdModTextBox').value = '';
};
PswdModbuttonGo.addEventListener('click', PswdModGo);
PswdModbuttonGo.setAttribute('data-event-listener', PswdModGo);
PswdModbuttonCancel.addEventListener('click', HidePswdMod);
PswdModbuttonCancel.setAttribute('data-event-listener', HidePswdMod);

// Function to display the modal
function showModalPswd(secondaryFunction, Title, Text, BT, BF) {
    // Hide the input
    const ModalPswdInput = document.getElementById('PswdModTextBox');
    const ModalPswdShowHidePswd = document.getElementById('PswdModalVisibility');
    ModalPswdInput.type = 'password';
    ModalPswdShowHidePswd.className = 'fa-regular fa-eye-slash ToggleVisibilityIcon';

    PswdModTitle.innerText = Title;
    PswdModText.innerText = Text;
    PswdModbuttonGo.innerText = BT;
    PswdModbuttonCancel.innerText = BF;

    modalPswd.style.display = "block";


    // Check if an event listener has already been added
    PswdModbuttonGo.removeEventListener('click', PswdModGo);

    PswdModGo = function() {
        // Run the secondary function with the opposite boolean value
        modalPswd.style.display = "none";
        let PswdModEntry = document.getElementById("PswdModTextBox").value;
        document.getElementById('PswdModTextBox').value = '';
        secondaryFunction(PswdModEntry);
    };

    PswdModbuttonGo.addEventListener('click', PswdModGo);
    PswdModbuttonGo.setAttribute('data-event-listener', PswdModGo);
}

        /*      Toggle Password Visiablity      */
const ModalPswdInput = document.getElementById('PswdModTextBox');
const ModalPswdShowHidePswd = document.getElementById('PswdModalVisibility');

ModalPswdShowHidePswd.addEventListener('click', function() {
if (ModalPswdInput.type === 'password') {
    // <i class="fa-regular fa-eye ToggleVisibilityIcon"></i>
    ModalPswdInput.type = 'text';
    ModalPswdShowHidePswd.className = 'fa-regular fa-eye ToggleVisibilityIcon';
    //ModalPswdShowHidePswd.appendChild(document.createElement('span')).innerHTML = '&#x1f527;';
} else {
    // <i class="fa-regular fa-eye-slash ToggleVisibilityIcon" id="ModalPswdShowHidePswd"></i>
    ModalPswdInput.type = 'password';
    ModalPswdShowHidePswd.className = 'fa-regular fa-eye-slash ToggleVisibilityIcon';
    //ModalPswdShowHidePswd.appendChild(document.createElement('span')).innerHTML = '&#x1f606;';
}
});




// Modal script Options
const optionModal = document.getElementById("myOptionModal");


const OptionModTitle = document.getElementById("OptionModalTitle");
const OptionModText = document.getElementById("OptionModalText");
const optionContainer = document.getElementById('OptionModelOptions');
const OptionModbuttonCancel = document.getElementById("OptionModalButtonCancel");
let OptionModGo = function() {
};
function HideOptionMod() {
    optionModal.style.display = "none";
    document.getElementById('TxtModTextBox').value = '';
};
OptionModbuttonCancel.addEventListener('click', HideOptionMod);
OptionModbuttonCancel.setAttribute('data-event-listener', HideOptionMod);

function depopulateModOptionOptions() {
    Array.from(optionContainer.getElementsByClassName('optionModOption')).forEach(segment => {
        segment.remove(); // Remove each directory button
    });
}

// Function to display the modal
function showModalOption(secondaryFunction, Title, Text, options, BF) {
    depopulateModOptionOptions();
    OptionModTitle.innerText = Title;
    OptionModText.innerText = Text;
    OptionModbuttonCancel.innerText = BF;

    optionModal.style.display = "block";


    for (let i = 0; i < options.length; i++) {
        const optionElement = document.createElement('div');
        optionElement.classList.add('optionModOption');
        optionElement.innerHTML = `
            <div class="modalOption-icon"><i class="fa-solid fa-circle"></i></div>
            <div class="modOption-OptionName">${options[i]}</div>
        `;
        let nm_for_lstner = options[i]
        optionElement.addEventListener('dblclick', () => {
            optionModal.style.display = "none";
            secondaryFunction(nm_for_lstner);
        });
        optionContainer.appendChild(optionElement);
    };

}




// Modal script Text Input
const modalTxt = document.getElementById("myTxtModal");


const TxtModTitle = document.getElementById("TxtModalTitle");
const TxtModText = document.getElementById("TxtModalText");
const TxtModbuttonGo = document.getElementById("TxtModalButtonEnter");
const TxtModbuttonCancel = document.getElementById("TxtModalButtonCancel");
let txtModGo = function() {
};
function HideTxtMod() {
    modalTxt.style.display = "none";
    document.getElementById('TxtModTextBox').value = '';
};
TxtModbuttonGo.addEventListener('click', txtModGo);
TxtModbuttonGo.setAttribute('data-event-listener', txtModGo);
TxtModbuttonCancel.addEventListener('click', HideTxtMod);
TxtModbuttonCancel.setAttribute('data-event-listener', HideTxtMod);

// Function to display the modal
function showModalTxt(secondaryFunction, Title, Text, BT, BF) {
    TxtModTitle.innerText = Title;
    TxtModText.innerText = Text;
    TxtModbuttonGo.innerText = BT;
    TxtModbuttonCancel.innerText = BF;

    modalTxt.style.display = "block";


    // Check if an event listener has already been added
    TxtModbuttonGo.removeEventListener('click', txtModGo);

    txtModGo = function() {
        // Run the secondary function with the opposite boolean value
        modalTxt.style.display = "none";
        let TxtModEntry = document.getElementById("TxtModTextBox").value;
        document.getElementById('TxtModTextBox').value = '';
        secondaryFunction(TxtModEntry);
    };

    TxtModbuttonGo.addEventListener('click', txtModGo);
    TxtModbuttonGo.setAttribute('data-event-listener', txtModGo);
}




// Modal script OKAY
const OKmodal = document.getElementById("myOKModal");


const OKModTitle = document.getElementById("OKModalTitle");
const OKModText = document.getElementById("OKModalText");
const OKModButton = document.getElementById("ModalButtonOK");
function HideOkayMod() {
    OKmodal.style.display = "none";
};
OKModButton.addEventListener('click', HideOkayMod);

// Function to display the modal
function showModalOK(Title, Text, Button) {
    OKModTitle.innerText = Title;
    OKModText.innerText = Text;
    OKModButton.innerText = Button;

    OKmodal.style.display = "block";
}





// Modal script True/False
const modal = document.getElementById("myTFModal");


const ModTitle = document.getElementById("ModalTitle");
const ModText = document.getElementById("ModalText");
const buttonTrue = document.getElementById("ModalButtonTrue");
const buttonFalse = document.getElementById("ModalButtonFalse");
let clickHandlerButtonFalse = function() {
};
let clickHandlerButtonTrue = function() {
};
buttonTrue.addEventListener('click', clickHandlerButtonTrue);
buttonTrue.setAttribute('data-event-listener', clickHandlerButtonTrue);
buttonFalse.addEventListener('click', clickHandlerButtonFalse);
buttonFalse.setAttribute('data-event-listener', clickHandlerButtonFalse);

// Function to display the modal
function showModalTF(secondaryFunction, Title, Text, BT, BF) {
    ModTitle.innerText = Title;
    ModText.innerText = Text;
    buttonTrue.innerText = BT;
    buttonFalse.innerText = BF;

    modal.style.display = "block";


    // Check if an event listener has already been added
    buttonTrue.removeEventListener('click', clickHandlerButtonTrue);
    buttonFalse.removeEventListener('click', clickHandlerButtonFalse);

    clickHandlerButtonTrue = function() {
        // Run the secondary function with the opposite boolean value
        modal.style.display = "none";
        secondaryFunction(true);
    };
    clickHandlerButtonFalse = function() {
        // Run the secondary function with the opposite boolean value
        modal.style.display = "none";
        secondaryFunction(false);
    };

    buttonTrue.addEventListener('click', clickHandlerButtonTrue);
    buttonTrue.setAttribute('data-event-listener', clickHandlerButtonTrue);
    buttonFalse.addEventListener('click', clickHandlerButtonFalse);
    buttonFalse.setAttribute('data-event-listener', clickHandlerButtonFalse);

}
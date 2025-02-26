class queueC {
    constructor() {
        this.queueMain = document.getElementById('queueMain');
        this.canceling = ''
        //this.populate([{action: 'Encrypting', target: 'C:/File', destination: 'C:/folder', progress: 69.56, id: 'qeeVBWANTxKEtj0K4bZ6'}]);
    }

    cancel() {
        showModalTF(this.goAhead, 'Are you sure?', `This will cancel this operation and it will not finish`, 'Yes', 'No');
    }

    goAhead(val) {
        if (val) {
            console.log(`Canceling ${queue.canceling}`);
        }
    }

    depopulate() {
        Array.from(this.queueMain.getElementsByClassName('queueItem')).forEach(segment => {
            segment.remove(); // Remove each directory button
        });
    }

    populate(array) {
        this.depopulate()
        for (let i = 0; i < array.length; i++) {
            const fileElement = document.createElement('div');
            fileElement.classList.add('queueItem');
            fileElement.innerHTML = `
            <div class="queueTile">
                <input type="text" class="queueText" value="${array[i].action}" readonly>
                <input type="text" class="queueText" value="Target: ${array[i].target}" readonly>
                <input type="text" class="queueText" value="Destination: ${array[i].destination}" readonly>
                <i class="fa-solid fa-circle-xmark queueX" id="${array[i].id}"></i>
            </div>
            <div class="progress-container">
                <div class="progress-bar" id="progress-bar" style="width: ${array[i].progress}%;">${array[i].progress}%</div>
            </div>
            `;
            this.queueMain.appendChild(fileElement);
            document.getElementById(array[i].id).addEventListener('click', function () {
                queue.canceling=array[i].id
                queue.cancel();
            });
        };
    }
}

const queue = new queueC();
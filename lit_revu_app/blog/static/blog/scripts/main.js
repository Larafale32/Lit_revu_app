import * as functions from './functions.js';

function lancerScript() {
    functions.confirmDelete();
    functions.closeModal();
    
    const profileElement = document.querySelector("h1[data-username]");
    if (profileElement) {
        const username = profileElement.dataset.username;
        functions.followButtons(username);
    }

   
}

lancerScript();
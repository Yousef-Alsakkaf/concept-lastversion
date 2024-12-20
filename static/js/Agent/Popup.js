const popupModal = document.getElementById('create-user-popup');
const closeModalBtn = document.querySelector('.popup-close');
const createUserButton = document.querySelector('.create-user-button');

createUserButton.addEventListener('click', () => {
    popupModal.style.display = 'flex';
});

// closeModalBtn.addEventListener('click', () => {
//     popupModal.style.display = 'none';
// });

window.addEventListener('click', (event) => {
    if (event.target === popupModal) {
        popupModal.style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const createUserButton = document.querySelector('.create-user-button');
    const popupModal = document.getElementById('create-user-popup');
    const popupClose = document.querySelector('.popup-close');
    const createUserForm = document.getElementById('create-user-form');

    createUserButton.addEventListener('click', () => {
        popupModal.style.display = 'flex';
    });

    createUserForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const userName = document.getElementById('user-name').value;
        const userEmail = document.getElementById('user-email').value;
        const userRole = document.getElementById('user-role').value;

        console.log(`User Name: ${userName}, Email: ${userEmail}, Role: ${userRole}`);

        popupModal.style.display = 'none';
    });
});




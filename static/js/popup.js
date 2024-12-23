const closeButton = document.getElementById('closeButton');
const popup = document.getElementById('popup');
const setval = document.getElementById('loc');
const userLocation = localStorage.getItem('location');


// if setval is clicked, show popup
setval.addEventListener('click', function() {
    popup.style.display = 'flex';
});



//show location 
setval.innerHTML = userLocation;
if (localStorage.getItem('location')) {
    popup.style.display = 'none';
} else {
    popup.style.display = 'flex';
}

if (userLocation) {
    const url = new URL(window.location.href);
    if (url.searchParams.has('location') == false) {
        url.searchParams.set('location', userLocation);
        window.history.replaceState({}, '', url.toString());
        // reload
        window.location.reload();
    }
   
}

// Close popup when user selects location and clicks submit button, save location in local storage
document.getElementById('location-btn').addEventListener('click', function() {
    const location = document.querySelector('.location-select').value;
    const previousLocation = localStorage.getItem('location');
    if (location && location !== previousLocation) {
        localStorage.setItem('location', location);
        popup.style.display = 'none';
        window.location.reload();
    } else if (!location) {
        popup.style.display = 'flex';
    } else {
        popup.style.display = 'none';
    }
});


// Close popup when close button is clicked
closeButton.addEventListener('click', function() {
    popup.style.display = 'none';
});
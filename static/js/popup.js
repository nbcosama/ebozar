const closeButton = document.getElementById('closeButton');
const popup = document.getElementById('popup');
const setval = document.getElementById('loc');
const userLocation = localStorage.getItem('location');

// if setval is clicked, show popup
setval.addEventListener('click', function() {
    popup.style.display = 'flex';
});


// if loacal storage has location, add location at the end of the url
if (localStorage.getItem('location')) {
    // const currentUrl = new URL(window.location.href);
    // currentUrl.searchParams.set('location', localStorage.getItem('location'));
    // window.history.pushState({}, '', currentUrl);
}





// show location
if(userLocation === null){
    setval.innerHTML = 'Select Location';
} else {
    setval.innerHTML = userLocation;
}
if (localStorage.getItem('location')) {
    popup.style.display = 'none';
} else {
    popup.style.display = 'none';
}


document.getElementById('location-btn').addEventListener('click', function() {
    const location = document.querySelector('.location-select').value;
    const previousLocation = localStorage.getItem('location');
    if (location && location !== previousLocation) {
        localStorage.setItem('location', location);
        popup.style.display = 'none';
        // send a GET request with the value location to the URL "landingpage"
        const xhr = new XMLHttpRequest();
        xhr.open('GET', `/?location=${location}`, true);
        xhr.send();
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

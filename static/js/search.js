const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('elevated');
    } else {
        navbar.classList.remove('elevated');
    }
});



// Get the search field and search box elements
const searchField = document.getElementById('searchInput');
const searchBox = document.getElementById('search_box');
const search_suggestions = document.getElementById('search_suggestions');
const search_form = document.getElementById('searchForm');
// set value in the search field from the suggestion list li which under the "search_suggestions" ul
search_suggestions.addEventListener('click', function(event) {
    searchField.value = event.target.innerText;
    search_suggestions.style.display = 'none';
    searchField.focus();
    search_form.submit();
});
// Function to apply styles to the search box
function showSearchBox() {
    searchBox.style.position = 'absolute';
    searchBox.style.top = '7px';
    searchBox.style.left = '160px';
    searchBox.style.padding = '5px';
    searchBox.style.backgroundColor = 'white';
    searchBox.style.boxShadow = '0 2px 8px 1px rgba(64, 60, 67, .24)';
    searchBox.style.maxHeight = '50vh'; // Use camelCase for max-height
    searchBox.style.overflowY = 'auto';
    search_suggestions.style.display = 'block';
}
// Function to remove styles from the search box
function hideSearchBox() {
    searchBox.style.position = '';
    searchBox.style.top = '';
    searchBox.style.left = '';
    searchBox.style.padding = '';
    searchBox.style.height = '';
    searchBox.style.boxShadow = '';
    search_suggestions.style.display = 'none';
}
// Add click event listener to the search field
searchField.addEventListener('click', function(event) {
    event.stopPropagation(); // Prevent the event from bubbling up to the document
    showSearchBox();
});
// Add click event listener to the document
document.addEventListener('click', function() {
    hideSearchBox();
});








// Ai search suggestions API

let url = "/search_query?q=";
let searchInput = document.getElementById('searchInput');
let suggestionPlace = document.getElementById('search_suggestions');
let debounceTimeout;
const debounceDelay = 500; // Adjust delay time as needed (500ms in this example)
searchInput.addEventListener('input', function() {
    let searchQuery = searchInput.value;
    // Clear the previous debounce timeout if the user keeps typing
    clearTimeout(debounceTimeout);
    // Set a new timeout
    debounceTimeout = setTimeout(() => {
        if (searchQuery) {
            fetch(url + searchQuery)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    suggestionPlace.innerHTML = '';
                    data.forEach(element => {
                        let li = document.createElement('li');
                        li.style.padding = '5px';
                        li.textContent = element;
                        suggestionPlace.appendChild(li);
                    });
                });
        } else {
            suggestionPlace.innerHTML = '';
        }
    }, debounceDelay);
});


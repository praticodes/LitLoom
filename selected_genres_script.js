const urlParams = new URLSearchParams(window.location.search);
const selectedGenresList = document.getElementById('selectedGenresList');

// Loop through query parameters and add selected genres to the list
for (const [key, value] of urlParams) {
    if (key === 'genre') {
        const listItem = document.createElement('li');
        listItem.textContent = decodeURIComponent(value);
        selectedGenresList.appendChild(listItem);
    }
}

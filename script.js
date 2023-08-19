function showLoadingOverlay() {
    document.getElementById('loadingOverlay').style.display = 'block';
}

function hideLoadingOverlay() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function redirectToSelectedGenresPage(selectedGenres) {
    // Build the URL with selected genres as query parameters
    const genresQueryString = selectedGenres.map(genre => `genre=${encodeURIComponent(genre)}`).join('&');
    const url = `selected_genres_page.html?${genresQueryString}`;

    // Redirect the user to the new page
    window.location.href = url;
}

function submitForm() {
    showLoadingOverlay();

    const selectedGenres = [];
    const genreCheckboxes = document.querySelectorAll('input[name="genres"]:checked');

    genreCheckboxes.forEach(checkbox => {
        selectedGenres.push(checkbox.value);
    });

    // Simulate a delay to show the loading overlay
    setTimeout(() => {
        // Replace with your Python function call or asynchronous action
        // After the function completes, hide the loading overlay and redirect to the new page
        hideLoadingOverlay();
        redirectToSelectedGenresPage(selectedGenres);
    }, 2000); // Adjust the delay time as needed
}

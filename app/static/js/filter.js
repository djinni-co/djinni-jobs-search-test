function resetFilters() {
    // Get the form element
    var form = document.getElementById("filter-form");

    // Clear all input fields in the form
    form.reset();

    // Redirect to the original page without any query parameters
    window.location.href = window.location.pathname;
}
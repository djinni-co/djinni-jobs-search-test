document.addEventListener('DOMContentLoaded', function () {
    const toggleFiltersBtn = document.getElementById('toggleFiltersBtn');
    const filtersContainer = document.getElementById('filtersContainer');

    toggleFiltersBtn.addEventListener('click', function () {
        if (filtersContainer.style.display === 'none' || filtersContainer.style.display === '') {
            filtersContainer.style.display = 'block';
            toggleFiltersBtn.textContent = 'Hide Filters';
        } else {
            filtersContainer.style.display = 'none';
            toggleFiltersBtn.textContent = 'Show Filters';
        }
    });

    const rangeInput = document.getElementById('salaryRange');
    const rangeMin = document.getElementById('rangeMin');
    const rangeMax = document.getElementById('rangeMax');

    rangeInput.addEventListener('input', function () {
        rangeMin.textContent = rangeInput.value;
    });
});

function toggleExpand(id) {
    var element = document.getElementById(id).parentNode;
    if (element.classList.contains('open')) {
        element.classList.remove('open');
        element.querySelector('.read-more').textContent = 'Read More';
    } else {
        element.classList.add('open');
        element.querySelector('.read-more').textContent = 'Read Less';
    }
};

document.addEventListener("DOMContentLoaded", function () {
    const sortBy = "{{ sort_by|escapejs }}";
    const sortSelect = document.getElementById("sort");

    for (let i = 0; i < sortSelect.options.length; i++) {
        if (sortSelect.options[i].value === sortBy) {
            sortSelect.options[i].selected = true;
            break;
        }
    }
});

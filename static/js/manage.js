document.addEventListener("DOMContentLoaded", updateRating);

[...document.querySelectorAll('.fa-star')].forEach(addStarFunctionality)

function addStarFunctionality (el, i) {
    let stars = [...document.querySelectorAll('.fa-star')];
    addStarClickFunctionality(el, i);
    addStarMouseOverFunctionality(stars, el, i);
    addStarMouseOutFunctionality(stars, el, i)
}

function addStarClickFunctionality(el, i) {
    el.onclick = () => {
        let starRating = document.querySelector('#star-rating');
        starRating.setAttribute('data-rating', (i+1)*2);
        starRating.setAttribute('data-rated', 'true');
        document.querySelector('#rating').setAttribute('value', (i+1)*2)
        console.log((i+1)*2);
        updateRating()
    }
}

function addStarMouseOverFunctionality(stars, el, i) {
    el.onmouseover = () => {
        let rating = document.querySelector('#star-rating')
        .getAttribute('data-rating');
        stars.slice(0, i+1).forEach((el, i) => {
            if (i+1 > rating/2) {
                el.classList.remove('fa-regular'); 
                el.classList.add('fa-solid');     
            }
        });
    };
}

function addStarMouseOutFunctionality(stars, el, i) {
    el.onmouseout = () => {
        let rating = document.querySelector('#star-rating')
        .getAttribute('data-rating');
        stars.slice(0, i+1).forEach((el, i) => {
            if (i+1 > rating/2) {
            el.classList.add('fa-regular'); 
            el.classList.remove('fa-solid');     
            }
        })
    };
}

function updateRating() {
    let stars = [...document.querySelectorAll('.fa-star')];
    let starRating = document.querySelector('#star-rating');
    let rating = starRating.getAttribute('data-rating');
    if (starRating.getAttribute('data-rated') == 'true') {
        for (let star of stars) {
            star.classList.add('text-warning')
            star.classList.remove('pointer')
        }
    }
    for (let star of stars.slice(0, rating/2)) {
        star.classList.remove('fa-regular'); 
        star.classList.add('fa-solid'); 
    }
    for (let star of stars.slice(rating/2)) {
        star.classList.remove('fa-solid'); 
        star.classList.add('fa-regular'); 
    }
}
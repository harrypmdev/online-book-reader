/* A script to add functionality to the rating stars feature 
on the OnlineBookReader manage book page. */

/*
On DOMContentLoaded, update rating stars to reflect their value
as provided by the server.
*/
document.addEventListener("DOMContentLoaded", displayRating);

// Add functionality for each star on screen
[...document.querySelectorAll('.fa-star')].forEach(addStarFunctionality)

/**
 * Add functionality to a rating star. Applies hover and click functionality.
 * @param {Element} el The star to which functionality should be applied.
 * @param {Number} i The star's index in the list of stars, i.e, which star
 * it is out of the 5 on screen.
 */
function addStarFunctionality (el, i) {
    let stars = [...document.querySelectorAll('.fa-star')];
    addStarClickFunctionality(el, i);
    addStarMouseOverFunctionality(stars, i);
    addStarMouseOutFunctionality(stars, i)
}

/**
 * Add click functionality to a rating star.
 * @param {Element} el The star to which click functionality should be applied.
 * @param {Number} i The star's index in the list of stars, i.e, which star
 * it is out of the 5 on screen.
 */
function addStarClickFunctionality(el, i) {
    el.onclick = () => {
        let starRating = document.querySelector('#star-rating');
        starRating.setAttribute('data-rating', (i+1)*2);
        starRating.setAttribute('data-rated', 'true');
        document.querySelector('#rating').setAttribute('value', (i+1)*2)
        console.log((i+1)*2);
        displayRating()
    }
}

/**
 * Add mouse over functionality to a rating star.
 * @param {Element[]} stars the array of stars which comprise the rating
 * feature.
 * @param {Number} i The star's index in the list of stars, i.e, which star
 * it is out of the 5 on screen.
 */
function addStarMouseOverFunctionality(stars, i) {
    let el = stars[i];
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

/**
 * Add mouse out functionality to a rating star.
 * @param {Element[]} stars the array of stars which comprise the rating
 * feature.
 * @param {Number} i The star's index in the list of stars, i.e, which star
 * it is out of the 5 on screen.
 */
function addStarMouseOutFunctionality(stars, i) {
    let el = stars[i];
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

/**
 * Update the rating stars to display the star-rating element's
 * current data-rating attribute (0-10) to the user.
 */
function displayRating() {
    let stars = [...document.querySelectorAll('.fa-star')];
    let starRating = document.querySelector('#star-rating');
    let rating = starRating.getAttribute('data-rating');
    let ratingGiven = starRating.getAttribute('data-rated') == 'true';
    if (ratingGiven) {
        applyRatingGivenStyles(stars);
    }
    fillStarsAccordingToRating(stars, rating);
}

/**
 * Make stars yellow and make cursor pointer when hovering over stars.
 * @param {Element[]} stars the array of stars for which the styles
 * should be applied.
 */
function applyRatingGivenStyles(stars) {
    for (let star of stars) {
        star.classList.add('text-warning')
        star.classList.remove('pointer')
    }
}

/**
 * Make stars appear 'filled' according to the rating provided.
 * Stars fill from the left, with a rating corresponding to 2 points per
 * star. For example, a rating of 2 is 1 star. A rating of 10 is 5 stars.
 * @param {Element[]} stars the array of stars for which the icon should
 * be changed.
 * @param {Number} rating The rating according to which the stars should be
 * filled, from 0 to 10.
 */
function fillStarsAccordingToRating(stars, rating) {
    // Make all stars under rating appear filled in
    for (let star of stars.slice(0, rating/2)) {
        star.classList.remove('fa-regular'); 
        star.classList.add('fa-solid'); 
    }
    // Make all stars over rating appear unfilled
    for (let star of stars.slice(rating/2)) {
        star.classList.remove('fa-solid'); 
        star.classList.add('fa-regular'); 
    }
}
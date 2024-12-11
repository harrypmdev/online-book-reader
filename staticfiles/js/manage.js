addEventListener("DOMContentLoaded", updateRating);

let stars = [...document.querySelectorAll('.fa-star')];
stars.forEach((el, i) => {
	
    el.onclick = () => {
        document.querySelector('#star-rating')
        .setAttribute('data-rating', (i+1)*2);
        console.log((i+1)*2);
        updateRating()
    }

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
  
})

function updateRating() {
    let rating = document.querySelector('#star-rating')
    .getAttribute('data-rating');
    for (let star of stars.slice(0, rating/2)) {
        star.classList.remove('fa-regular'); 
        star.classList.add('fa-solid'); 
    }
    for (let star of stars.slice(rating/2)) {
        star.classList.remove('fa-solid'); 
        star.classList.add('fa-regular'); 
    }
}
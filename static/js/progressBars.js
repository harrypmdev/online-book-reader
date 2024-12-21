// Add progress bar animation to all dashboard books.
[...document.querySelectorAll('.book')].forEach(addProgressBarAnimation);

/**
 * Add hover animation to the progress bar for a book on the dashboard.
 * @param  {Element} el the element to which the hover animation 
 * should be applied.
 */
function addProgressBarAnimation(el) {
    let bar = el.querySelector(".progress-bar"); 
    let bookCard = el.querySelector(".book-card"); 

    bookCard.onmouseover = () => { 
        bar.classList.add('progress-bar-animated'); 
    }; 
  
    bookCard.onmouseout = () => { 
        bar.classList.remove('progress-bar-animated'); 
    };
}
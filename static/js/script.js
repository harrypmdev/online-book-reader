// Dashboard progress bar animation
[...document.querySelectorAll('.book')].forEach((el) => { 
    let bar = el.querySelector(".progress-bar"); 
    let bookCard = el.querySelector(".book-card"); 

    bookCard.onmouseover = () => { 
        bar.classList.add('progress-bar-animated'); 
    }; 
  
    bookCard.onmouseout = () => { 
        bar.classList.remove('progress-bar-animated'); 
    };
});
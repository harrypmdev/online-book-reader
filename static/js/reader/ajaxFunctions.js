export async function postProgressToServer(progress, length) {
    let bookText = document.getElementById('book-text')
    let url = bookText.getAttribute('data-ajax-update-url');
    let csrfToken = bookText.getAttribute('data-csrf-token');
    let bookID = bookText.getAttribute('data-book-id');
    const response = await fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrfToken,
        }, 
        body:JSON.stringify({
            'progress': progress,
            'book_id': bookID,
            'length': length,
            })
    });
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
    let data = await response.json()
    if (!data['completion'].includes('Progress updated.')) {
        throw new Error(`Error updating progress: ${data['completion']}`);
    }
}

export async function getBook(line_width="default", caching=true) {
    let bookText = document.getElementById('book-text')
    if (line_width == "default") {   
        line_width = parseInt(bookText.getAttribute('data-char-limit'));
    }
    let bookID = bookText.getAttribute('data-book-id');
    if (sessionStorage.getItem("id") == bookID && 
    sessionStorage.getItem("line-width") == line_width && caching) {
        return JSON.parse(sessionStorage.getItem('text_list'));
    }
    let url = bookText.getAttribute('data-ajax-url');
    let csrfToken = bookText.getAttribute('data-csrf-token');
    const response = await fetch(url, {
       method:'POST',
       headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrfToken,
       }, 
       body:JSON.stringify({
        'num': line_width,
        'book_id': bookID,
        })
    })
    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
    let data = await response.json()
    sessionStorage.setItem("id", bookID);
    sessionStorage.setItem("line-width", line_width);
    sessionStorage.setItem("text_list", JSON.stringify(data));
    return data

}
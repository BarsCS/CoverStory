let page = 1;
let emptyPage = false;
let blockRequests = false;

window.addEventListener('scroll', () => {

    let scrollPosition = window.innerHeight + window.scrollY;
    let threshold = document.documentElement.scrollHeight - 300;

    if(scrollPosition >= threshold && !emptyPage && !blockRequests) {
        blockRequests = true;

        page += 1;

        fetch('?books_only=1&page=' + page)
        .then(
            response => response.text()
        )
        .then(
            html => {
                if (html === '') {
                    emptyPage = true;
                } else {
                    div = document.querySelector('.books-list');
                    console.log(div);

                    div.insertAdjacentHTML('beforeend', html);

                    blockRequests = false;
                }
            }
        )
    }
})

const scrollEvent = new Event('scroll');
window.dispatchEvent(scrollEvent);
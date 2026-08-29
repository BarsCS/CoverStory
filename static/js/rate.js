import Cookies from 'https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/+esm';
const csrftoken = Cookies.get('csrftoken')

document.addEventListener('DOMContentLoaded', () => {
    
    let ratings = document.querySelector('.ratings');
    let stars = document.querySelectorAll('.ratings span');
    const URL = ratings.dataset.rateurl;

    const BookURL = ratings.dataset.bookurl;
    const LoginURL = ratings.dataset.loginurl;

    const RedirectUrl = `${LoginURL}?next=${BookURL}`;

    let isAuthenticated = ratings.dataset.user == 'true';

    const currentRate = Number(ratings.dataset.rate)

    highlightStars(currentRate);
    
    let options = {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin'
    }

    stars.forEach((span) => {
        span.addEventListener('click', (event) => {

            if (!isAuthenticated){
                window.location.replace(RedirectUrl);
                return;
            }

            let star = event.target;

            let bookId = ratings.dataset.bookid;
            let rate = star.dataset.rating;
            
            let formData = new FormData();
            formData.append('book_id', bookId);
            formData.append('rate', rate);
            options['body'] = formData;

            fetch(URL, options)
            .then((response) => response.json())
            .then((data) => {

                if (data['status'] === 'ok') {
                    ratings.dataset.rate = rate;
                } else {
                    return false;
                }
                
            })
            .catch(
                () => {
                    return false;
                }
            )
        })

        span.addEventListener('mouseenter', (event) => {

            const rate = event.currentTarget.getAttribute('data-rating');

            highlightStars(rate);
        })

        span.addEventListener('mouseleave', (event) => {

            const stars = document.querySelector('.ratings');

            highlightStars(stars.dataset.rate);
        })
    })

    // Function to highlight stars
    function highlightStars(rate) {
    
        stars.forEach((star) => {
    
            if (star.dataset.rating <= rate) {
                star.classList.add('selected');
            } else {
                star.classList.remove('selected');
            }
        })
    }
})


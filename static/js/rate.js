import Cookies from 'https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/+esm';
const csrftoken = Cookies.get('csrftoken')
const URL = 'http://localhost:8000/book/rate/'

let stars = document.querySelectorAll('.ratings span');
let stars_div = document.querySelector('.ratings');
let rate;

document.addEventListener('DOMContentLoaded', () => {
    
    let options = {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin'
    }
    
    let ratings = document.querySelector('.ratings');

    stars.forEach((span) => {
        span.addEventListener('click', (event) => {

            // console.log(stars);

            let star = event.target;

            let bookId = ratings.dataset.id;
            let rate = star.dataset.rating;
            
            let formData = new FormData();
            formData.append('id', bookId);
            formData.append('rate', rate);

            options['body'] = formData;

            fetch(URL, options)
            .then((response) => response.json())
            .then((data) => {
                // console.log("start");

                if (data['status'] === 'ok') {

                    // console.log('SUCCESS');

                    stars_div.dataset.rate = rate;
                } 
            })

        })

        span.addEventListener('mouseenter', (event) => {

            const rate = event.currentTarget.getAttribute('data-rating');

            highlightStars(rate);
        })

        span.addEventListener('mouseleave', (event) => {

            const stars = document.querySelector('.ratings');

            console.log(stars)

            highlightStars(stars.dataset.rate);
        })
    })
})


function highlightStars(rate) {

    stars.forEach((star) => {

        if (star.dataset.rating <= rate) {
            star.classList.add('selected');
        } else {
            star.classList.remove('selected');
        }
    })
}
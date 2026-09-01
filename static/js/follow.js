import Cookies from 'https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/+esm';
const csrftoken = Cookies.get('csrftoken')

let options = {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin'
    }

document.addEventListener('DOMContentLoaded', (event) => {

    let followButton = document.querySelector('a.follow');

    // let action = 'unfollow';
    const URL = followButton.dataset.url;
    
    followButton.addEventListener('click', (event) => {
        event.preventDefault();
        
        let action = followButton.dataset.action;
        let profileId = followButton.dataset.profileid;
        
        let formData = new FormData();

        formData.append('action', action);
        formData.append('profile_id', profileId);

        options['body'] = formData;

        fetch(URL, options)
        .then((response) => response.json())
        .then((data) => {
            if (data['status'] == 'ok'){
                let previousAction = action;

                followButton.dataset.action = previousAction === 'follow' ? 'unfollow' : 'follow';
                
                followButton.innerHTML = previousAction === 'follow' ? 'Unfollow' : 'Follow';
            }
        })
    })
})
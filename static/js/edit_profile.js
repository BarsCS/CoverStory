import Cookies from 'https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/+esm';
const csrftoken = Cookies.get('csrftoken');

let options = {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
    }


document.addEventListener("DOMContentLoaded", () => {

    let button = document.querySelector(".avatar-container span.edit")
    let fileInput = document.querySelector(".fileInput")

    button.addEventListener("click", (event) => {
       fileInput.click()
    })

    fileInput.addEventListener("change", (event) => {
        const avatar = event.target.files[0]
        console.log(avatar);
        
        if (avatar.name.split('.')[1] == "jpg" || avatar.name.split('.')[1] == "png" || avatar.name.split('.')[1] == "jpeg") {
            console.log("TRUE");
        } else {
            console.log("FALSE");
            return;
        }
        
        let formData = new FormData()
        formData.append("avatar", avatar)
        options.body = formData
        
        console.log(options);
        fetch('/account/edit/', options)
        .then((response) => {
            console.log(response)
            response.json()
        })
        .then((data) => {
            console.log(data)
        })
        .catch((reject) => {
            console.log("error")
        })
    })
})
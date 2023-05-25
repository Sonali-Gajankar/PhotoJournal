let menu = document.querySelector("#mobile-menu");
let menuLinks = document.querySelector('.navbar__menu');

menu.addEventListener('click', function() {
    menu.classList.toggle('is-active');
    menuLinks.classList.toggle('active');
})

let upload_elem = document.getElementById("img__upload_field");
let preview_elem = document.getElementById("img_upload_photos");

if(upload_elem && preview_elem){
    upload_elem.addEventListener("change", function(event) {
    preview_elem.src = URL.createObjectURL(event.target.files[0]);
})
}


let desc = document.querySelector(".description");
let test;
if(desc){
    desc.addEventListener("input", function(event){
        test=event;
        event.target.style.height = (event.target.scrollHeight)+"px";
    })
}

fetch("http://127.0.0.1:8000/get-photos/", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        result = response.json()
        status_code = response.status;
        if(status_code != 200) {
            console.log('Error in getting brand info!')
            return false;
        }

        return result
    })
    .then(result => {
        console.log(result);
        console.log(result[0].photo);
        let img = document.createElement('img');
        img.src = result[0].photo;
        document.body.append(img);
        // Do something with the result

    })
    .catch(error => {
        console.log(error)
    })
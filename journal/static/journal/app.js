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

const gallery_container = document.querySelector(".gallery__container");
let next;
if (gallery_container && window.location.pathname=="/user-home/") {
    loadScript("https://echoes.up.railway.app/fetch-photos/");
}

function loadScript(url){
    return fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        result = response.json();
        temp = result;
        status_code = response.status;
        if(status_code != 200) {
            console.log('Error in getting data!')
            return false;
        }
        return result;
    })
    .then(result => {
        next = result.next;
        loadContentOnScroll(result.results);
        return result;
    })
    .catch(error => {
        console.log(error)
    })
}

function loadContentOnScroll(result){
    result.forEach(function(elem){
        let card = document.createElement("figure");
        card.innerHTML = `
        <section class="content">
            <span>${elem.title}</span>
            <div class="icons">
                <div class="icons__menu">
                    <a href="${elem.id}/delete/"><i class="fa-solid fa-trash-can fa-lg" style="color: #0f1108;"></i></a>
                    <a href="update/${elem.id}/"><i class="fa-solid fa-pen-to-square fa-lg" style="color: #0f1108;"></i></a>
                </div>
                <div class="icons__toggle">
                    <span class="dot"></span>
                    <span class="dot"></span>
                    <span class="dot"></span>
                </div>
            </div>
        </section><hr>
        <figcaption class="content_description">${elem.description}</figcaption>
        <img src=${elem.photo} alt="">
        <div>${elem.date}</div>`;
        gallery_container.appendChild(card);
    })
}

var throttleTimer;
const throttle = (callback, time) => {
  if (throttleTimer) return;
  throttleTimer = true;
  setTimeout(() => {
    callback();
    throttleTimer = false;
  }, time);
};


const handleInfiniteScroll = () => {
    throttle(() => {
        const endOfPage = window.innerHeight + window.pageYOffset >= document.body.offsetHeight;
        if (endOfPage && next) {
            result = loadScript(next);
        }
    }, 1000);

};

if (gallery_container && window.location.pathname=="/user-home/") {
    window.addEventListener("scroll", handleInfiniteScroll);
}

document.addEventListener("click", function(event){
    let target = event.target.closest(".icons__toggle");
    if(target){
        let update_icons = target.previousElementSibling;
        target.classList.toggle('is-active');
        update_icons.classList.toggle('active');
    }

})
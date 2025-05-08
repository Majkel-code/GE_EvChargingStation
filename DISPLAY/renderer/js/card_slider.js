const chargingPage = document.querySelector(".charging-page");
const slidesCards = document.querySelector(".slides-cards");
const threshold = 100
let posX1 = 0
let posX2 = 0
let allowShift = true;
let posInitial
let posFinal
const slides = slidesCards.getElementsByClassName('slide')
const slidesLength = slides.length
const slideSize = 480
let index = 0
slidesCards.addEventListener('touchstart', dragStart);
slidesCards.addEventListener('touchend', dragEnd);
slidesCards.addEventListener('touchmove', dragAction);

slidesCards.onmousedown = dragStart;
function dragStart (e) {
    e = e || window.event;
    e.preventDefault();
    posInitial = slidesCards.offsetLeft;
    if (e.type == 'touchstart') {
        posX1 = e.touches[0].clientX;
    } else {
        posX1 = e.clientX;
        document.onmouseup = dragEnd;
        document.onmousemove = dragAction;
    }
}
function dragEnd (e) {
    posFinal = slidesCards.offsetLeft;
    if (posFinal - posInitial < -threshold) {
        shiftSlide(1, 'drag');
    } else if (posFinal - posInitial > threshold) {
        shiftSlide(-1, 'drag');
    } else {
        slidesCards.style.left = (posInitial) + "px";
    }

    document.onmouseup = null;
    document.onmousemove = null;
}
function shiftSlide(dir, action) {
    slidesCards.classList.add('shifting');
    if (allowShift) {
        if (!action) { posInitial = slidesCards.offsetLeft; }

        if (dir == 1) {
        slidesCards.style.left = (posInitial - slideSize) + "px";
        index++;      
        } else if (dir == -1) {
        slidesCards.style.left = (posInitial + slideSize) + "px";
        index--;      
        }
    };
}

function dragAction (e) {
    e = e || window.event;
    let cards_position = slidesCards.style.left
    let cards_position_num = cards_position.split("px")[0]
    if(cards_position_num < -480 || cards_position_num > 0){
        return
    }
    else{
        if (e.type == 'touchmove') {
            posX2 = posX1 - e.touches[0].clientX;
            posX1 = e.touches[0].clientX;
        } else {
            posX2 = posX1 - e.clientX;
            posX1 = e.clientX;
        }
        slidesCards.style.left = (slidesCards.offsetLeft - posX2) + "px";
    }
}
slidesCards.addEventListener('transitionend', checkIndex);
function checkIndex (){
    changeDots()
    slidesCards.classList.remove('shifting');

    if (index == -1) {
        slidesCards.style.left = -(slidesLength * slideSize) + "px";
        index = slidesLength - 1;
    }

    if (index == slidesLength) {
        slidesCards.style.left = -(1 * slideSize) + "px";
        index = 0;
    }
    allowShift = true;
}

function changeDots() {
    const dots = document.querySelectorAll(".dot");
    dots.forEach((dot, i) => {
        if (i == index) {
            dot.classList.add("active");
        } else {
            dot.classList.remove("active");
        }
    });
}

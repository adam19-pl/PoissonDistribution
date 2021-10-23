const hamburger = document.querySelector('.hamburger');
const menu = document.querySelector('.menu')

hamburger.addEventListener('click',function(){
    this.classList.toggle('is-active');
    if(this.classList.value.includes("is-active")){
    menu.classList.add("mobile-menu");
    }else{
    menu.classList.remove("mobile-menu");
    }
    console.log(menu.classList.value);
});
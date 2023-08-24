const menubarBtn = document.querySelector ('.navbar_tablet i')
menubarBtn.addEventListener('click', function(){
    document.querySelector('.navbar_tablet ul').classList.toggle('active')
})
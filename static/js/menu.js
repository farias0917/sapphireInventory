const imgPerfil = document.getElementById("imgPerfil")
const options = document.getElementById("options")
const bntMenu = document.getElementById("bntMenu")
const navMenuContainer = document.getElementById("navMenuContainer")

imgPerfil.addEventListener("click",function (e) {
    e.preventDefault
    options.style.display = "Block"
})

document.addEventListener("click", event=>{
    if (!options.contains(event.target) && event.target !== imgPerfil) {
        options.style.display = "none";
    }
})

bntMenu.addEventListener("click",function (e) {
    e.preventDefault

    if (navMenuContainer.className == "navMenuContainer navMenuContainerHidde") {
        navMenuContainer.classList.add("navMenuContainerShow") 
        navMenuContainer.classList.remove("navMenuContainerHidde") 
    }else{
        navMenuContainer.classList.add("navMenuContainerHidde") 
        navMenuContainer.classList.remove("navMenuContainerShow") 
    }
})


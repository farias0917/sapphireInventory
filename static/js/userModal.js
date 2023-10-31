const BtnModalPerfil = document.getElementById("BtnModalPerfil")
const modalPerfil = document.getElementById("modalPerfil")
const closeModal = document.getElementById("closeModal")


BtnModalPerfil.addEventListener("click", e=>{
    e.preventDefault()
    modalPerfil.style.display = "block"
})

closeModal.addEventListener("click", e=>{
    e.preventDefault()
    modalPerfil.style.display = "none"
})






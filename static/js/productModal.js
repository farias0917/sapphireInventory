const btnProductModal = document.getElementById("btnProductModal")
const productModal = document.getElementById("productModal")
const close = document.getElementById("close")
const btnUpdate = document.getElementById("btnUpdate")
const UpdateProductModal = document.getElementById("UpdateProductModal")


btnProductModal.addEventListener("click",e=>{
    e.preventDefault()

    productModal.style.display = "Flex"
})

close.addEventListener("click",e=>{
    e.preventDefault()
    productModal.style.display = "none"
})




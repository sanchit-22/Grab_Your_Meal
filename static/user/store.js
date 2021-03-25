//console.log("sdfdsf")
if (document.readyState == 'loading') {
    //console.log("sdfdsfd")
    document.addEventListener('DOMContentLoaded', ready)
} else {
    //console.log("sdfdsfd")
    ready()
}

function load() {
    var list = [];
    var keyArray = ["one","two"];
  for (var i = 0; i < keyArray.length; i++) {
        var item = localStorage.getItem(keyArray[i]);
       if (item.charAt(0) == "+") {
            item = parseFloat(item.substring(1));
      }
        list.push(item);
        //console.log(item)
  }
    return list;
}



function save(a,b) 
{
	var itemArray = [a,b];
	var keyArray = ["one","two"];
	for (var i = 0; i < keyArray.length; i++) {
      	if (typeof(itemArray[i]) === "number") {
          	itemArray[i] = "+"+itemArray[i];
        }
        if (typeof(itemArray[i]) !== undefined) {
          	localStorage.setItem(keyArray[i],itemArray[i]);
        }   
    }
}

function ready() {
    var removeCartItemButtons = document.getElementsByClassName('btn-danger')
    for (var i = 0; i < removeCartItemButtons.length; i++) {
        var button = removeCartItemButtons[i]
        button.addEventListener('click', removeCartItem)
    }

    var quantityInputs = document.getElementsByClassName('cart-quantity-input')
    for (var i = 0; i < quantityInputs.length; i++) {
        var input = quantityInputs[i]
        input.addEventListener('change', quantityChanged)
    }

    var addToCartButtons = document.getElementsByClassName('shop-item-button')
    for (var i = 0; i < addToCartButtons.length; i++) {
        var button = addToCartButtons[i]
        button.addEventListener('click', addToCartClicked)
    }

    document.getElementsByClassName('btn-purchase')[0].addEventListener('click', purchaseClicked)
}

function purchaseClicked() {
    var cartItems = document.getElementsByClassName('cart-items')[0]
    while (cartItems.hasChildNodes()) {
        cartItems.removeChild(cartItems.firstChild)
    }
    updateCartTotal()
}

function removeCartItem(event) {
    var buttonClicked = event.target
    buttonClicked.parentElement.parentElement.remove()
    updateCartTotal()
}

function quantityChanged(event) {
    var input = event.target
    if (isNaN(input.value) || input.value <= 0) {
        input.value = 1
    }
    updateCartTotal()
}

function addToCartClicked(event) {
    console.log("sdfsff")
    var button = event.target
    var shopItem = button.parentElement.parentElement
    var title = shopItem.getElementsByClassName('shop-item-title')[0].innerText
    var price = shopItem.getElementsByClassName('shop-item-price')[0].innerText
    var imageSrc = shopItem.getElementsByClassName('shop-item-image')[0].src
    addItemToCart(title, price, imageSrc)
    updateCartTotal()
}

function addItemToCart(title, price, imageSrc) {
    var cartRow = document.createElement('div')
    cartRow.classList.add('cart-row')
    var cartItems = document.getElementsByClassName('cart-items')[0]
    var cartItemNames = cartItems.getElementsByClassName('cart-item-title')
    for (var i = 0; i < cartItemNames.length; i++) {
        if (cartItemNames[i].innerText == title) {
            alert('This item is already added to the cart')
            return
        }
    }
    var cartRowContents = `
        <div class="cart-item cart-column">
            <img class="cart-item-image" src="${imageSrc}" width="100" height="100">
            <span class="cart-item-title">${title}</span>
        </div>
        <span class="cart-price cart-column">${price}</span>
        <div class="cart-quantity cart-column">
            <input class="cart-quantity-input" type="number" value="1">
            <button class="btn btn-danger" type="button">REMOVE</button>
        </div>`
    cartRow.innerHTML = cartRowContents
    cartItems.append(cartRow)
    cartRow.getElementsByClassName('btn-danger')[0].addEventListener('click', removeCartItem)
    cartRow.getElementsByClassName('cart-quantity-input')[0].addEventListener('change', quantityChanged)
}

function updateCartTotal() {
    var cartItemContainer = document.getElementsByClassName('cart-items')[0]
    var cartRows = cartItemContainer.getElementsByClassName('cart-row')
    var total = 0
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var priceElement = cartRow.getElementsByClassName('cart-price')[0]
        var quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0]
        var price = parseFloat(priceElement.innerText.replace('Rs', ''))
        var quantity = quantityElement.value
        total = total + (price * quantity)
      //  console.log(price+"\n",quantity+"\n",cartRow)
    }
    total = Math.round(total * 100) / 100
    //console.log(cartRows)
    document.getElementsByClassName('cart-total-price')[0].innerText = 'Rs' + total
    var myArray = [price,quantity];
    save.apply(this, myArray)
    myArray = load();
    console.log(myArray[0],myArray[1])
    var c=myArray[0]
    sessionStorage.setItem("test","sdfsdf")
    var result = sessionStorage.getItem('test');
    console.log(result)
}
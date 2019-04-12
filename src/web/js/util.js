var currentDB;

function setCurrentDB(json){
    currentDB = json;
    console.log(currentDB);
}

function makeDiv(className = "") {
    var div = document.createElement('div');
    div.setAttribute('class', className);
    return div;
}

function createItem(jsonItem) {
    var itemWrapper = makeDiv('item-wrapper');
    var itemWrapperLeft = makeDiv('item-wrapper-left');
    var itemImage = document.createElement('img');
    itemImage.setAttribute('class', 'item-image');
    if (jsonItem.Image === "")
        itemImage.setAttribute('src', "../images/No-Image-Available.png");
    else
        itemImage.setAttribute('src', jsonItem.Image);
    itemWrapperLeft.appendChild(itemImage);
    var itemWrapperRight = makeDiv('item-wrapper-right');
    var itemTitle = makeDiv('item-title');
    itemTitle.innerHTML = jsonItem.Name;
    itemWrapperRight.appendChild(itemTitle);
    var itemCategory = makeDiv('item-category');
    itemCategory.innerHTML = new String("Category: " + jsonItem.Category);
    itemWrapperRight.appendChild(itemCategory);
    var itemOwner = makeDiv('item-owner');
    itemOwner.innerHTML = new String("Owner: " + jsonItem["Permanent Owner"]);
    itemWrapperRight.appendChild(itemOwner);
    var itemAvailable = document.createElement('div');
    if (jsonItem.Available) {
        itemAvailable.innerHTML = "Available";
        itemAvailable.setAttribute('class', 'item-available');
    }
    else {
        itemAvailable.innerHTML = "Unavailable";
        itemAvailable.setAttribute('class', 'item-unavailable');
    }
    itemWrapperRight.appendChild(itemAvailable);
    var itemRequest = document.createElement('button');
    itemRequest.setAttribute('class', 'item-request');
    itemRequest.innerHTML = "Request";
    itemRequest.addEventListener("click", function (e) { 
        e.stopPropagation();
        alert("Item Requested"); 
    });
    itemWrapperRight.appendChild(itemRequest);

    itemWrapper.appendChild(itemWrapperLeft);
    itemWrapper.appendChild(itemWrapperRight);
    itemWrapper.onclick = () => displayItem(jsonItem);
    return itemWrapper;
}

function filterBySearch() {
    console.log('currentDB: ');
    console.log(currentDB);

    var prop = document.getElementById("search").value;
    if (prop == '') {
        return;
    }
    var container = document.getElementById('items-container');
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }
    if (currentDB.hasOwnProperty(prop)) {
        var item = createItem(currentDB[prop]);
        container.appendChild(item);
    }
    else 
    {
        noResults = makeDiv('no-results');
        noResults.innerHTML = 'No Search Results';
        container.appendChild(noResults);
    }
}

function createLightBox() {
    console.log('in createLightBox()');
    var lightBox = makeDiv('lightbox-wrapper-hidden');
    lightBox.setAttribute('id', 'lightbox-wrapper')
    lightBox.onclick = function() {
        while (lightBox.firstChild) {
            lightBox.removeChild(lightBox.firstChild);
            lightBox.className = ('lightbox-wrapper-hidden');
        }
    }
    return lightBox;
}

function displayItem(jsonItem) {
    console.log('in displayItem()');
    var lightboxItem = makeDiv('lightbox-item')
    var lightBox = document.getElementById('lightbox-wrapper');
    lightBox.className = 'lightbox-wrapper-visible';
    while (lightBox.firstChild) {
        lightBox.removeChild(lightBox.firstChild);
    }
    lightBox.appendChild(lightboxItem);


    var itemWrapperLeft = makeDiv('item-wrapper-left');
    var itemImage = document.createElement('img');
    itemImage.setAttribute('class', 'item-image');
    if (jsonItem.Image === "")
        itemImage.setAttribute('src', "../images/No-Image-Available.png");
    else
        itemImage.setAttribute('src', jsonItem.Image);
    itemWrapperLeft.appendChild(itemImage);
    var itemWrapperRight = makeDiv('item-wrapper-right');
    var itemTitle = makeDiv('item-title');
    itemTitle.innerHTML = jsonItem.Name;
    itemWrapperRight.appendChild(itemTitle);
    var itemCategory = makeDiv('item-category');
    itemCategory.innerHTML = new String("Category: " + jsonItem.Category);
    itemWrapperRight.appendChild(itemCategory);
    var itemOwner = makeDiv('item-owner');
    itemOwner.innerHTML = new String("Owner: " + jsonItem["Permanent Owner"]);
    itemWrapperRight.appendChild(itemOwner);
    var itemAvailable = document.createElement('div');
    if (jsonItem.Available) {
        itemAvailable.innerHTML = "Available";
        itemAvailable.setAttribute('class', 'item-available');
    }
    else {
        itemAvailable.innerHTML = "Unavailable";
        itemAvailable.setAttribute('class', 'item-unavailable');
    }
    itemWrapperRight.appendChild(itemAvailable);

    lightboxItem.appendChild(itemWrapperLeft);
    lightboxItem.appendChild(itemWrapperRight);
}

export { makeDiv, createItem, filterBySearch, setCurrentDB, createLightBox, displayItem };
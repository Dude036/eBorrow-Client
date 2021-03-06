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

function createItem(jsonItem, mine=false, hash) {
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
    if(mine)
    {
        var itemRequest = document.createElement('button');
        itemRequest.setAttribute('class', 'item-request');
        itemRequest.innerHTML = "Edit";
        itemRequest.addEventListener("click", function (e) {
            e.stopPropagation();
            alert("Would go to Edit Item Page, It is basically just a delete then add new one.");
        });
        itemWrapperRight.appendChild(itemRequest);
    } else {
        var itemRequest = document.createElement('button');
        itemRequest.setAttribute('class', 'item-request');
        itemRequest.innerHTML = "Request";
        itemRequest.addEventListener("click", function (e) {
            e.stopPropagation();
            //eel.item_request(hash, jsonItem["Permanent Owner"])();
            alert("Item Requested");
        });
        itemWrapperRight.appendChild(itemRequest);
    }
    
    itemWrapper.appendChild(itemWrapperLeft);
    itemWrapper.appendChild(itemWrapperRight);
    itemWrapper.onclick = () => displayItem(jsonItem);
    return itemWrapper;
}

function filterBySearch() {
    var keyword = document.getElementById("search").value.toUpperCase();
    if (keyword == '') {
        return;
    }
    var container = document.getElementById('items-container');
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }

    for(var obj in currentDB)
    {
        if(currentDB.hasOwnProperty(obj))
        {
            if(currentDB[obj].Name.toUpperCase() == keyword)
            {
                var item = createItem(currentDB[obj]);
                container.appendChild(item);
            }
        }
    }
    if(!container.hasChildNodes())
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

function createInput(type, id, className, place) {
    var input = document.createElement('input');
    input.setAttribute('type', type);
    input.setAttribute('id', id);
    input.setAttribute('class', className);
    input.setAttribute('placeholder', place);
    return input;
}

async function reloadProgram() {
    await eel.send_all()();
    await eel.send_message()();
    await eel.send_exchange()();
    await eel.send_pending_friends()();
    await eel.send_pending_exchanges()();
    location.reload();
}

function getDateString(currentDate) {
    var date = currentDate.getDate();
    var month = currentDate.getMonth();
    var year = currentDate.getFullYear();
    var monthDateYear = (month + 1) + "/" + date + "/" + year;
    return monthDateYear;
}

export { makeDiv, createItem, filterBySearch, setCurrentDB, createLightBox, displayItem, createInput, reloadProgram, getDateString };

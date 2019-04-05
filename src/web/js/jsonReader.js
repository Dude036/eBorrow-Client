function createItem(jsonItem)
{
    var itemWrapper = document.createElement('div');
    itemWrapper.setAttribute('class', 'item-wrapper');
    var itemWrapperLeft = document.createElement('div');
    itemWrapperLeft.setAttribute('class', 'item-wrapper-left');
    var itemImage = document.createElement('img');
    itemImage.setAttribute('class', 'item-image');
    if(jsonItem.Image === "")
        itemImage.setAttribute('src', "../images/No-Image-Available.png");
    else
        itemImage.setAttribute('src', jsonItem.Image);
    itemWrapperLeft.appendChild(itemImage);
    var itemWrapperRight = document.createElement('div');
    itemWrapperRight.setAttribute('class', 'item-wrapper-right');
    var itemTitle = document.createElement('div');
    itemTitle.setAttribute('class', 'item-title');
    itemTitle.innerHTML = jsonItem.Name;
    itemWrapperRight.appendChild(itemTitle);
    var itemCategory = document.createElement('div');
    itemCategory.setAttribute('class', 'item-category');
    itemCategory.innerHTML = new String("Category: " + jsonItem.Category);
    itemWrapperRight.appendChild(itemCategory);
    var itemOwner = document.createElement('div');
    itemOwner.setAttribute('class', 'item-owner');
    itemOwner.innerHTML = new String("Owner: " + jsonItem["Permanent Owner"]);
    itemWrapperRight.appendChild(itemOwner);
    var itemAvailable = document.createElement('div');
    if (jsonItem.Available){
        itemAvailable.innerHTML = "Available";
        itemAvailable.setAttribute('class', 'item-available');
    }
    else{
        itemAvailable.innerHTML = "Unavailable";
        itemAvailable.setAttribute('class', 'item-unavailable');
    }
    itemWrapperRight.appendChild(itemAvailable);
    var itemRequest = document.createElement('button');
    itemRequest.setAttribute('class', 'item-request');
    itemRequest.innerHTML = "Request";
    itemRequest.addEventListener("click", function () { alert("Item Requested"); });
    itemWrapperRight.appendChild(itemRequest);

    itemWrapper.appendChild(itemWrapperLeft);
    itemWrapper.appendChild(itemWrapperRight);
    itemWrapper.onclick = () => console.log(jsonItem);
    return itemWrapper;
}

function loadJSON(callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', '../database/mystuff.json', true);
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            callback(xobj.responseText);
        }
    }
    xobj.send(null);
}
loadJSON(function (response) {
    jsonresponse = JSON.parse(response);
    var itemsContainer = document.createElement('div');
    itemsContainer.setAttribute('class', 'items-container');
    for (var prop in jsonresponse) {
        if (jsonresponse.hasOwnProperty(prop)) {
            item = createItem(jsonresponse[prop]);
            itemsContainer.appendChild(item);
        }
    }
    document.querySelector('body').appendChild(itemsContainer);
});
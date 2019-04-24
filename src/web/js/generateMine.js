import * as util from './util.js';

function loadJSON(callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', '../db/mine.json', true);
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            callback(xobj.responseText);
        }
    }
    xobj.send(null);
}

var lightBox = util.createLightBox();
document.querySelector('body').appendChild(lightBox);

loadJSON(function (response) {
    var jsonresponse = JSON.parse(response);
    util.setCurrentDB(jsonresponse);
    var itemsContainer = util.makeDiv('items-container');
    itemsContainer.setAttribute('id', 'items-container');
    var addItemWrapper = util.makeDiv('item-add-wrapper');
    var addItem = document.createElement('button');
    addItem.setAttribute('class', 'item-add');
    addItem.innerHTML = "Add New Item";
    addItem.addEventListener("click", function (e) {
        e.stopPropagation();
        window.location = 'newItem.html';
    });
    addItemWrapper.appendChild(addItem);
    itemsContainer.appendChild(addItemWrapper);

    for (var prop in jsonresponse) {
        if (jsonresponse.hasOwnProperty(prop)) {
            var item = util.createItem(jsonresponse[prop], true, prop);
            itemsContainer.appendChild(item);
        }
    }
    document.getElementById('main-wrapper').appendChild(itemsContainer);
});
import * as util from './util.js';

function loadJSON(callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', '../db/theirs.json', true);
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

    for (var prop in jsonresponse) {
        if (jsonresponse.hasOwnProperty(prop)) {
            var item = util.createItem(jsonresponse[prop], false, prop);
            itemsContainer.appendChild(item);
        }
    }
    document.getElementById('main-wrapper').appendChild(itemsContainer);
});


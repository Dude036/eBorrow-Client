import * as util from './util.js';

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
    var jsonresponse = JSON.parse(response);
    util.setCurrentDB(jsonresponse);
    var itemsContainer = util.makeDiv('items-container');
    itemsContainer.setAttribute('id', 'items-container');

    for (var prop in jsonresponse) {
        if (jsonresponse.hasOwnProperty(prop)) {
            var item = util.createItem(jsonresponse[prop]);
            itemsContainer.appendChild(item);
        }
    }
    document.getElementById('main-wrapper').appendChild(itemsContainer);
});
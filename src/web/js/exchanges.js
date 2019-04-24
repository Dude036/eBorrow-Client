import * as util from './util.js';

function loadJSON(callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', '../db/messages.json', true);
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            callback(xobj.responseText);
        }
    }
    xobj.send(null);
}

loadJSON(async function (response) {
    var jsonresponse = JSON.parse(response);
    var exchangesContainer = util.makeDiv('exchanges-container');
    exchangesContainer.setAttribute('id', 'exchanges-container');
    var exchanges = jsonresponse['exchanges'];

    for (var i in exchanges) {
        var request = exchanges[i];
        var perm = request['Permanent Owner'];
        var curr = request['Current Owner'];
        var cat = request.Category;
        var name = request.Name;
        var stat = request.Status;
        var inn = request.Schedule.In;
        var inDate = new Date(inn[2], inn[1], inn[0]);
        var out = request.Schedule.Out;
        var outDate = new Date(out[2], out[1], out[0]);
        var inString = util.getDateString(inDate);
        var outString = util.getDateString(outDate);
        var wrapper = util.makeDiv('exchange-request');
        var to = util.makeDiv('exchange-request-to exchange-request-line');
        to.innerHTML = 'To: ' + perm;
        var from = util.makeDiv('exchange-request-from exchange-request-line');
        from.innerHTML = 'From: ' + curr;
        var title = util.makeDiv('exchange-request-name exchange-request-line');
        title.innerHTML = 'Item: ' + name;
        if(stat == 'Open') {
            var status = util.makeDiv('exchange-request-status open');
        } else {
            var status = util.makeDiv('exchange-request-status closed');
        }
        status.innerHTML = 'Status: ' + stat;
        var dates = util.makeDiv('exchange-request-dates exchange-request-line');
        dates.innerHTML = 'Dates of Borrow: ' + inString + '-' + outString;
        wrapper.appendChild(to);
        wrapper.appendChild(from);
        wrapper.appendChild(title);
        wrapper.appendChild(dates);
        wrapper.appendChild(status);
        exchangesContainer.appendChild(wrapper);
    }
    document.getElementById('main-wrapper').appendChild(exchangesContainer);
});
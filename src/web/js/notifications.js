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
    var notifContainer = util.makeDiv('notif-container');
    notifContainer.setAttribute('id', 'notif-container');
    var exchangesContainer = util.makeDiv('notif-exchanges-container');
    exchangesContainer.innerHTML = 'New Borrow Requests';
    var friendsContainer = util.makeDiv('notif-friends-container');
    friendsContainer.innerHTML = 'New Friend Requests';
    notifContainer.appendChild(exchangesContainer);
    notifContainer.appendChild(friendsContainer);
    var exchanges = jsonresponse['pending exchanges'];
    var friends = jsonresponse['pending friends'];
    var username = await eel.get_username()();

    for(var i in exchanges) {
        var request = exchanges[i];
        var perm = request['Permanent Owner'];
        if (perm != username) { continue; }
        var curr = request['Current Owner'];
        var key = request['Key'];
        var cat = request.Category;
        var name = request.Name;
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
        var dates = util.makeDiv('exchange-request-dates exchange-request-line');
        dates.innerHTML = 'Dates of Borrow: ' + inString + '-' + outString;
        var accept = document.createElement('button');
        accept.setAttribute('class', 'exchange-request-accept');
        accept.innerHTML = "Accept";
        accept.addEventListener("click", function (e) {
            eel.change_owner(key, curr, inn, out)(alert("Request Accepted: " + name));
        });
        var deny = document.createElement('button');
        deny.setAttribute('class', 'exchange-request-deny');
        deny.innerHTML = "Deny";
        deny.addEventListener("click", function (e) {
            alert("Request Denied: " + name);
        });
        wrapper.appendChild(to);
        wrapper.appendChild(from);
        wrapper.appendChild(title);
        wrapper.appendChild(dates);
        wrapper.appendChild(deny);
        wrapper.appendChild(accept);
        exchangesContainer.appendChild(wrapper);

    }

    for (var i in friends) {
        var request = friends[i];
        var target = request.Target;
        if (target != username) { continue; }
        var sender = request.Sender;
        var wrapper = util.makeDiv('friend-request');
       
        var to = util.makeDiv('friend-request-to friend-request-line');
        to.innerHTML = 'To: ' + target;
        var from = util.makeDiv('friend-request-from friend-request-line');
        from.innerHTML = 'From: ' + sender;
        var accept = document.createElement('button');
        accept.setAttribute('class', 'friend-request-accept');
        accept.innerHTML = "Accept";
        accept.addEventListener("click", function (e) {
            eel.add_friend(sender, 2)(alert("Request from " + sender + " Accepted"));
            ;
        });
        var deny = document.createElement('button');
        deny.setAttribute('class', 'friend-request-deny');
        deny.innerHTML = "Deny";
        deny.addEventListener("click", function (e) {
            alert("Request Denied");
        });
        wrapper.appendChild(to);
        wrapper.appendChild(from);
        wrapper.appendChild(deny);
        wrapper.appendChild(accept);
        friendsContainer.appendChild(wrapper);
    }
    document.getElementById('main-wrapper').appendChild(notifContainer);
});
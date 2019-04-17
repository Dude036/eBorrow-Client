import * as util from './util.js';

function createFriend(friend) {
    var friendWrapper = util.makeDiv('friend-wrapper');
    friendWrapper.innerHTML = friend;
    return friendWrapper;
}

function loadJSON(callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', '../db/friends.json', true);
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
    var container = util.makeDiv('friend-container');
    var addFriendWrapper = util.makeDiv('friend-add-wrapper');
    var addFriendForm = document.createElement('form');
    var userName = util.createInput('text', 'friend-name', 'friend-name', 'Friend\'s Username');
    var addFriend = document.createElement('button');
    addFriend.setAttribute('class', 'friend-add');
    addFriend.innerHTML = "Add New Friend";
    addFriend.addEventListener("click", function (e) {
        e.stopPropagation();
        var name = document.getElementById("friend-name").value;
        console.log(name)
        eel.friend_request(name)(alert("Friend Request Sent to: " + name));
    });
    addFriendForm.appendChild(userName);
    addFriendForm.appendChild(addFriend);
    
    addFriendWrapper.appendChild(addFriendForm);
    container.appendChild(addFriendWrapper);

    for (var friend in jsonresponse) {
        if (jsonresponse.hasOwnProperty(friend)) {
            var item = createFriend(friend);
            container.appendChild(item);
        }
    }
    document.getElementById('main-wrapper').appendChild(container);
});
import * as util from './util.js';

function createMenuItem(inner, href) {
    var wrap = util.makeDiv('sidemenu-itemwrapper');
    var item = document.createElement('a');
    item.setAttribute('class', 'sidemenu-item');
    item.setAttribute('href', href);
    item.innerHTML = inner;
    wrap.appendChild(item);
    return wrap;
}

var sideMenuWrapper = util.makeDiv('sidemenu-wrapper');
var mine = createMenuItem("My Items", "myStuff.html");
var theirs = createMenuItem("Friends' Items", "theirStuff.html");
var exhanges = createMenuItem("Exchanges", "");
var profile = createMenuItem("My Profile", "");
var friends = createMenuItem("My Friends", "");
sideMenuWrapper.appendChild(theirs);
sideMenuWrapper.appendChild(mine);
sideMenuWrapper.appendChild(exhanges);
sideMenuWrapper.appendChild(profile);
sideMenuWrapper.appendChild(friends);


document.getElementById('main-wrapper').appendChild(sideMenuWrapper);

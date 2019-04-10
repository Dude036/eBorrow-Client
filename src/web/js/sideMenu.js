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
var mine = createMenuItem("View My Stuff", "myStuff.html");
var theirs = createMenuItem("View Friends Stuff", "theirStuff.html");
sideMenuWrapper.appendChild(mine);
sideMenuWrapper.appendChild(theirs);
for (var i = 0; i < 6; i++) {
    var tmp = createMenuItem("Menu Item", "");
    sideMenuWrapper.appendChild(tmp);
}
document.getElementById('main-wrapper').appendChild(sideMenuWrapper);

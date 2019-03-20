function createMenuItem(inner, href) {
    var wrap = document.createElement('div');
    wrap.setAttribute('class', 'sidemenu-itemwrapper');
    var item = document.createElement('a');
    item.setAttribute('class', 'sidemenu-item');
    item.setAttribute('href', href);
    item.innerHTML = inner;
    wrap.appendChild(item);
    return wrap;
}

var sideMenuWrapper = document.createElement('div');
sideMenuWrapper.setAttribute('class', 'sidemenu-wrapper');
var mine = createMenuItem("View My Stuff", "hello.html");
var theirs = createMenuItem("View Friends Stuff", "theirStuff.html");
sideMenuWrapper.appendChild(mine);
sideMenuWrapper.appendChild(theirs);
for (i = 0; i < 6; i++) {
    var tmp = createMenuItem("Menu Item", "");
    sideMenuWrapper.appendChild(tmp);
}
document.querySelector('body').appendChild(sideMenuWrapper);

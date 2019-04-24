import * as util from './util.js';

function createIcon(anchorClass, anchorHREF, iconClass) {
    var anchor = document.createElement('a');
    anchor.setAttribute('class', anchorClass);
    anchor.setAttribute('href', anchorHREF);
    var icon = document.createElement('i');
    icon.setAttribute('class', iconClass);
    anchor.appendChild(icon);
    return anchor;
}

var headerwrapper = util.makeDiv('header-wrapper');
var title = util.makeDiv('header-title');
title.setAttribute('id', 'header-title');
title.innerHTML = "eBorrow";
headerwrapper.appendChild(title);

var searchwrapper = util.makeDiv('header-search-wrapper');
var left = util.makeDiv('header-search-wrapper-left');
var search = document.createElement('input');
search.setAttribute('class', 'header-search');
search.setAttribute('type', 'text');
search.setAttribute('placeholder', 'Search...');
search.setAttribute('id', 'search');

var right = util.makeDiv('header-search-wrapper-right');
var reload = createIcon("header-anchor", "#", "fas fa-redo-alt header-icon");
reload.addEventListener('click', util.reloadProgram)
var profile = createIcon("header-anchor", "myProfile.html", "far fa-user header-icon");
var messages = createIcon("header-anchor", "messages.html", "far fa-envelope header-icon");
var notifications = createIcon("header-anchor", "notifications.html", "far fa-bell header-icon");

right.appendChild(reload);
right.appendChild(profile);
right.appendChild(messages);
right.appendChild(notifications);

var searchIcon = document.createElement('i');
searchIcon.setAttribute('class', 'fas fa-search header-search-icon');
searchIcon.addEventListener("click", util.filterBySearch);
left.appendChild(search);
left.appendChild(searchIcon);
searchwrapper.appendChild(left);
searchwrapper.appendChild(right);

document.getElementById('main-wrapper').appendChild(headerwrapper);
document.getElementById('main-wrapper').appendChild(searchwrapper);

var logoAnchor = document.createElement('a');
logoAnchor.setAttribute('class', "header-logo-anchor");
logoAnchor.setAttribute('href', "myStuff.html");
var logo = document.createElement('img');
logo.setAttribute('class', 'header-logo');
logo.setAttribute('src', "../images/logo1.png");
logoAnchor.appendChild(logo);
document.getElementById('main-wrapper').appendChild(logoAnchor);

var blueHex = util.makeDiv('header-blue hex');
document.getElementById('header-title').appendChild(blueHex);

var greenHex = util.makeDiv('header-green hex');
document.getElementById('header-title').appendChild(greenHex);

var tealHex = util.makeDiv('header-teal hex');
document.getElementById('header-title').appendChild(tealHex);


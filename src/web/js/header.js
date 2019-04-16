import * as util from './util.js';

var headerwrapper = util.makeDiv('header-wrapper');
var title = util.makeDiv('header-title');
title.setAttribute('id', 'header-title');
title.innerHTML = "eBorrow";
headerwrapper.appendChild(title);

var searchwrapper = util.makeDiv('header-search-wrapper');
var search = document.createElement('input');
search.setAttribute('class', 'header-search');
search.setAttribute('type', 'text');
search.setAttribute('placeholder', 'Search...');
search.setAttribute('id', 'search');

var searchIcon = document.createElement('i');
searchIcon.setAttribute('class', 'fas fa-search header-search-icon');
searchIcon.addEventListener("click", util.filterBySearch);
searchwrapper.appendChild(search);
searchwrapper.appendChild(searchIcon);

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
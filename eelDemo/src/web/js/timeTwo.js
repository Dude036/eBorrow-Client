var timeButton = document.createElement('button');
timeButton.setAttribute('onclick','timeGetter()');
timeButton.innerHTML = 'get the time';
document.querySelector('body').appendChild(timeButton);

async function timeGetter(){
    let value = await eel.getTime()();
    var theTime = document.createElement('p');
    theTime.textContent = value;
    document.querySelector('body').appendChild(theTime);
};

var jsonButton = document.createElement('button');
jsonButton.setAttribute('onclick','jsonGetter()');
jsonButton.innerHTML = 'get the json';
document.querySelector('body').appendChild(jsonButton);

async function jsonGetter(){
    let value = await eel.getJson()();
    var theJson = document.createElement('p');
    theJson.textContent = value;
    document.querySelector('body').appendChild(theJson);
};
import * as util from './util.js';

var inputWrapper = util.makeDiv('new-wrapper');
inputWrapper.innerHTML = 'Input the Information'
var inputForm = document.createElement('form');
inputWrapper.appendChild(inputForm);
var name = util.createInput('text', 'new-name', 'new-name new-input', 'Name');
name.required = true;
var category = util.createInput('text', 'new-category', 'new-category new-input', 'Category');
category.required = true;
var subCategory = util.createInput('text', 'new-subcategory', 'new-subcategory new-input', 'Sub Category');
var groups = util.createInput('text', 'new-groups', 'new-groups new-input', 'Groups');
var types = util.createInput('text', 'new-types', 'new-types new-input', 'Types');
var img = util.createInput('url', 'new-img', 'new-img new-input', "Image URL");
var tag = util.createInput('text', 'new-tag', 'new-tag new-input', "Tags");
var submit = document.createElement('button');
submit.setAttribute('class', 'new-button');
submit.setAttribute('type', 'button');
submit.innerHTML = "Create New Item";
submit.addEventListener("click", async function (e) {
    e.stopPropagation();
    var name = document.getElementById("new-name").value;
    var category = document.getElementById("new-category").value;
    var subCategory = document.getElementById("new-subcategory").value;
    var groups = document.getElementById("new-groups").value;
    var types = document.getElementById("new-types").value;
    var img = document.getElementById("new-img").value;
    var tag = document.getElementById("new-tag").value;
    var key = await eel.add_item(name, category, subCategory, groups, types, img, tag)();
    console.log(key);
    window.location = 'myStuff.html';
});
inputForm.appendChild(name);
inputForm.appendChild(category);
inputForm.appendChild(subCategory);
inputForm.appendChild(groups);
inputForm.appendChild(types);
inputForm.appendChild(tag);
inputForm.appendChild(img);
inputForm.appendChild(submit);

document.getElementById('main-wrapper').appendChild(inputWrapper);

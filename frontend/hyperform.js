/*!
 * hyperform.js
 */
export const EVENT_ADD_FORM = 'formset.add';
export const EVENT_DEL_FORM = 'formset.del';

const parseHTML = function(str) {
  var tmp = document.implementation.createHTMLDocument();
  tmp.body.innerHTML = str.trim();
  return tmp.body.children[0];
};

const dispatchEvent = function(target, name) {
  if (window.CustomEvent) {
    var event = new CustomEvent(name);
  } else {
    var event = document.createEvent("CustomEvent");
    event.initCustomEvent(name, true, true);
  }
  target.dispatchEvent(event);
};

const addForm = function(button) {

};

const delForm = function(button) {

};

const getWrapper = function(button) {
};

const setupAdd = function(wrapper) {
  wrapper.addEventListener("click", function(e) {
    if (e.target && e.target.hasAttribute("data-formset-add")) {
      addForm(e.target);
    }
  });
};

const setupDel = function(wrapper) {
  wrapper.addEventListener("click", function(e) {
    if (e.target && e.target.hasAttribute("data-formset-del")) {
      delForm(e.target);
    }
  });
};

export const setupFormSets = function(wrapper) {
  wrapper = wrapper || document;
  setupAdd(wrapper);
  setupDel(wrapper);
};

function initSubForms($wrapper){
    $wrapper.find('[data-forms]').each(function(){
        initSubForm($(this));
    });
}
initSubForms($(document));

function initSubForm($w){
    var delmsg = $w.attr('data-delmsg');

    var $btnAdd = $w.next('[data-addbtn]');
    $btnAdd = $btnAdd.length ? $btnAdd : $w.next().find('[data-addbtn]');

    var tmplSel = $btnAdd.attr('data-addbtn');

    $btnAdd
        .off('click')  // deactivate any action set by a possible parent form
        .on('click', function(e){
            e.preventDefault();
            e.stopPropagation();
            addSubForm($w, tmplSel);
        });

    $w.on('click', '[data-delbtn]', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var $f = $(this).closest('[data-form]');
        if (!delmsg || $f.prop('data-new') || confirm(delmsg)){
            removeSubForm($w, $f);
        }
    });
}

function addSubForm($w, tmplSel){
    var maxforms = parseInt($w.attr('data-maxforms'), 10);
    if (!isNaN(maxforms)){
        var $subForms = $w.find('[data-form="' + $w.attr('data-forms') + '"]');
        if ($subForms.length >= maxforms){
            return;
        }
    }

    var html = $(tmplSel).html();
    var $pre = parseHTML(html);
    $pre.prop('data-new', true);
    $pre.hide().appendTo($w).slideDown('fast');
    updateSubFormsNames($w);

    $w.trigger(EVENT_ADD_FORM, $pre);

    // Recursive subforms
    initSubForm($pre.find('[data-forms]'));
    return $pre;
}

function insertDeleteFlag($f){
    var $inputs = $f.find('[name]');
    if (!$inputs.length) return;
    var name = $inputs.eq(0).attr('name');
    var nameRoot = name.slice(0, name.indexOf('-'));
    var $flag = $('<input name="' + nameRoot + '__deleted' + '" value="1"/>')
    $flag.insertAfter($inputs.eq(0));
    $inputs.remove();
}

function removeSubForm($w, $f){
    $f.find('[data-delbtn]').hide();
    $f.slideUp('fast', function(){

        if ($f.is('[data-new]')){
            $f.remove();
            updateSubFormsNames($w);
        } else {
            insertDeleteFlag($f);
            $f.css('display', 'none');
        }
        $w.trigger(EVENT_DEL_FORM, $f);
    });
}

function updateSubFormsNames($w){
    var name, newName, $fw, $subForms, depth, i, j;
    var aa = $w.toArray();
    var bb = $w.parents('[data-forms]').toArray();
    var $wrappers = $(bb.concat(aa));

    for (i=$wrappers.length; i>0; i--){
        depth = i - 1;
        $fw = $wrappers.eq(depth);
        $subForms = $fw.find('[data-form="' + $fw.attr('data-forms') + '"]');

        for (j=0; j<$subForms.length; j++){
            var num = j + 1;
            updateNames($subForms.eq(j), depth, num);
        }
    }
}

function updateNames($form, depth, num){
    var $fields = $form.find('[name]');
    var $field, oldName, newName, nameParts;

    $fields.each(function(){
        $field = $(this);
        oldName = $field.attr('name');
        nameParts = deconstructName(oldName);
        newName = getNewName(nameParts, depth, num);
        $field.attr('name', newName);
    });
}

function deconstructName(name){
    var nameParts = [];
    var parts = name.split('-');
    var maxIndex = parts.length - 1;
    var i = 0, subpart;

    for (i=0; subpart=parts[i]; i++) {
        if (i > 0){
            subpart = '-' + subpart;
        }
        if (i == maxIndex){
            nameParts.push(subpart);
            continue;
        }
        n = subpart.length - subpart.split('').reverse().join('').indexOf('.')
        nameParts.push(subpart.substring(0, n));
        nameParts.push(subpart.substring(n));
    }
    return nameParts;
}

function getNewName(nameParts, depth, num){
    nameParts[depth * 2 + 1] = num;
    return nameParts.join('');
}

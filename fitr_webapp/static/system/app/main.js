// cast form to json
function castJson(arr) {
    $json_object = {};

    for (var x = 0; x < arr.length; x++) {
        if (arr[x].type == "checkbox") {
            $json_object[arr[x].name] = arr[x].checked;
            continue;
        }
        if (arr[x].name == "") {
            continue;
        }
        $json_object[arr[x].name] = arr[x].value;
    }

    return $json_object;
}

(function ($) {
    $.fn.jsonString = function () {
        jsonData = castJson($(this).serializeArray());
        return JSON.stringify(jsonData);
    };
})(jQuery);


// uuid gen
function generateUUID() {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
        var r = (Math.random() * 16) | 0,
            v = c == "x" ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
}

// element redraw
jQuery.fn.redraw = function () {
    return this.hide(0, function () {
        $(this).show();
    });
};

// generate auto complete for forms
function generate_autocomp_hash(elements_arr) {
    elements_arr.forEach(element => {
        $(element).attr("autocomplete", generateUUID());
        $(element).redraw();
    });
}


// string to color
function stringToColor(i) {
    function hashCode(str) { // java String#hashCode
        var hash = 0;
        for (var i = 0; i < str.length; i++) {
            hash = str.charCodeAt(i) + ((hash << 5) - hash);
        }
        return hash;
    }

    var c = (hashCode(i) & 0x00FFFFFF)
        .toString(16)
        .toUpperCase();

    return "00000".substring(0, 6 - c.length) + c;
}
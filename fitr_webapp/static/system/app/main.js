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
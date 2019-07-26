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

(function($) {
  $.fn.jsonString = function() {
    jsonData = castJson($(this).serializeArray());
    return JSON.stringify(jsonData);
  };
})(jQuery);

// remove card if on small screen
function decide_form_card(form_card) {
  let window_width = $( window ).width();
  if (window_width <= 600) {
    let card = $(form_card).find(".card-panel");
    if (window[`card_classes${form_card}`] == undefined) {
      window[`card_classes${form_card}`] = card.attr("class");
    }
    card.removeAttr('class').addClass("p-4");
  } else {
    let card = $(form_card).find(".p-4");
    card.removeAttr('class').attr("class", window[`card_classes${form_card}`]);
  }
}

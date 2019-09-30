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
  function apply() {
    var window_width = $( window ).width();
    if (window_width <= 550) {
      var card = $(form_card).find(".card-panel");
      if (window[`card_classes${form_card}`] == undefined) {
        window[`card_classes${form_card}`] = card.attr("class");
      }
      card.removeAttr('class').addClass("p-3");
    } else {
      var card = $(form_card).find(".p-3");
      card.removeAttr('class').attr("class", window[`card_classes${form_card}`]);
    }
  };

  // on change
  window.addEventListener("resize", function() {
    setTimeout(function() {
      apply();
    }, 120);
  });

  // init
  setTimeout(function() {
    apply();
  }, 60);
}

// sidebar nav and dropdown
// $(document).ready(function(){
//   $('.sidenav').sidenav({
//     edge: 'right'
//   });
//   $(".dropdown-trigger").dropdown();
//   $('.collapsible').collapsible();
// });

// for chartjs
var stringToColour = function(str) {
  var hash = 0;
  for (var i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  var colour = '#';
  for (var i = 0; i < 3; i++) {
    var value = (hash >> (i * 8)) & 0xFF;
    colour += ('00' + value.toString(16)).substr(-2);
  }
  return colour;
}

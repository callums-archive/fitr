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

// Datepicker inline
var datepicker_inline = function(el, format = "YYYY-MM-DD") {
  this.init(el, format);
}

datepicker_inline.prototype = {
  init: function(el, format) {
    if ($(el).attr('id') != undefined) {
      this.name = $(el).attr('id');
    } else if ($(el).attr('name') != undefined) {
      this.name = $(el).attr('name');
    }

    this.input = document.createElement("input");
    this.input.setAttribute("name", this.name);
    this.input.setAttribute("type", "text");
    this.input.setAttribute("value", "");
    this.input.style.display = "none";
    this.input.style.disabled = true;
    this.input.classList = "form-control";
    this.input.value = $(el).data("DateTimePicker").date().format(format);

    $(el).append(this.input);

    var root = this;
    $(el).on('dp.change', function(e) {
      root.input.value = e.date.format(format);
    });
  }
};
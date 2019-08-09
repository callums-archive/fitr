/*!
 *Form Generator
 *By Callum Fleming (c)2019
 *This is LECENCED SOFTWARE
 */


// constructor
var formGen = function(formId, settings) {
  this.formId = formId;
  this.settings = settings;

  this.init();
}

// formGen.prototype = function () {
//
// };

formGen.prototype = {
  init() {
    console.log("gets here !!!!");
    console.log(this.formId);

    this.formEle = $(this.formId);


    this.generateForm();
    this.registerEvents();
    console.log(this.settings);

  },

  generateForm() {
    var root = this;
    this.settings.form.forEach(function(formField) {
      // assign random id (screw you auto correct!)
      if (!(formField.hasOwnProperty("noHash") && formField.noHash == true)) {
        formField.id = root.generateUUID();
      }

      switch (formField.type) {
        case "string":
          formField.html = root.createStringInput(formField, "text");
          root.formEle.append(formField.html);
          break;
        case "password":
          formField.html = root.createStringInput(formField, "password");
          root.formEle.append(formField.html);
          break;
        case "email":
          formField.html = root.createStringInput(formField, "text");
          root.formEle.append(formField.html);
          break;
        case "integer":
          formField.html = root.createIntegerInput(formField);
          root.formEle.append(formField.html);
          break;
        case "float":
          formField.html = root.createFloatInput(formField);
          root.formEle.append(formField.html);
          break;
        case "date":
          formField.html = root.createDateInput(formField);
          root.formEle.append(formField.html);
          $(`#${formField.id}_year`).formSelect();
          $(`#${formField.id}_month`).formSelect();
          $(`#${formField.id}_day`).formSelect();
          break;
        case "select":
          formField.html = root.createSelectInput(formField);
          root.formEle.append(formField.html);
          $(`#${formField.id}`).formSelect();
          break;
      }
      console.log(formField);
    });
  },

  generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0,
        v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  },



  createStringInput(formField, type) {
    name = formField.hasOwnProperty("noHash") ? formField.name : formField.id;
    console.log(formField)
    element = $(`
      <div class="row">
        <div class="input-field col s12">
          <input id="${name}" type="${type}">
          <label for="${name}">${formField.placeholder}</label>
        </div>
      </div>
    `);
    return element
  },

  createDateInput(formField) {
    name = formField.hasOwnProperty("noHash") ? formField.name : formField.id;
    if (formField.hasOwnProperty("min")) {
      minDate = new Date(formField.min);
    } else {
      minDate = new Date("1900-01-01");
    }

    if (formField.hasOwnProperty("max")) {
      maxDate = new Date(formField.max);
    } else {
      maxDate = new Date();
      maxDate.setFullYear(maxDate.getFullYear() + 10)
    }

    // generate years
    var years = "";
    for (var i = minDate.getFullYear(); i <= maxDate.getFullYear(); i++) {
      years += `<option value="${i}">${i}</option>`
    }

    // generate months
    var months = "";
    for (var i = 1; i != 13; i++) {
      month = new Date(`${i}-01-1970`).toLocaleString('default', {
        month: 'long'
      });
      months += `<option value="${i}">${month}</option>`
    }

    element = $(`
      <div class="row">
        <div class="input-field col s3">
          <select id="${formField.id}_year">
            <option value="" disabled selected>YYYY</option>
            ${years}
          </select>
          <label>${formField.placeholder}</label>
        </div>

        <div class="input-field col s6">
          <select id="${formField.id}_month">
            <option value="" disabled selected>MM</option>
            ${months}
          </select>
        </div>

        <div class="input-field col s3">
          <select id="${formField.id}_day">
            <option value="" disabled selected>DD</option>
          </select>
        </div>
      </div>
    `);
    return element
  },

  createIntegerInput(formField) {
    name = formField.hasOwnProperty("noHash") ? formField.name : formField.id;
    console.log(formField)
    element = $(`
      <div class="row">
        <div class="input-field col s12">
          <input id="${name}" type="text" pattern="[0-9]*" inputmode="numeric" step="1">
          <label for="${name}">${formField.placeholder}</label>
        </div>
      </div>
    `);
    return element
  },

  createFloatInput(formField) {
    name = formField.hasOwnProperty("noHash") ? formField.name : formField.id;
    console.log(formField)
    element = $(`
      <div class="row">
        <div class="input-field col s12">
          <input id="${name}" type="text" pattern="[0-9]*" inputmode="numeric" step="0.01">
          <label for="${name}">${formField.placeholder}</label>
        </div>
      </div>
    `);
    return element
  },

  createSelectInput(formField) {
    name = formField.hasOwnProperty("noHash") ? formField.name : formField.id;
    options = "";
    formField.options.forEach(function(option) {
      if (option.name == formField.value) {
        options += `
          <option value="${option.value}" selected>${option.name}</option>
        `;
      } else {
        options += `
          <option value="${option.value}">${option.name}</option>
        `;
      }
    });

    if (!formField.hasOwnProperty("value")) {
      options = `<option value="" disabled selected>Choose ${formField.placeholder}</option>`.concat(options);
    }

    element = $(`
      <div class="input-field col s12 select-input-width">
        <select id="${name}">
          ${options}
        </select>
        <label>${formField.placeholder}</label>
      </div>
    `);
    return element
  },

  registerEvents() {
    var root = this;
    var ignored = ["year", "month", "day"];

    this.formEle.on("change keyup keypress", function(e) {
      var ref = e.target.id.substring(0, (e.target.id.length - e.target.id.split("_").pop().length) - 1);
      if (!ignored.includes(e.target.id.split("_").pop())) {
        root.pullField(e.target.id).value = e.target.value
      }

      if (e.target.id.split("_").pop() == "month" || e.target.id.split("_").pop() == "year") {
        $(`#${ref}_day`).val("");
        root.pullField(ref).value = "";
        var year = $(`#${ref}_year`).val();

        if (year != null && e.target.value != null) {
          var days = ""
          for (var day=1; day <= new Date(year, e.target.value, 0).getDate();day++) {
            days+= `<option value="${day}">${day}</option>`;
          }
          $(`#${ref}_day`).append(days).formSelect();
        }
      }

      if (e.target.id.split("_").pop() == "day") {
        var year = $(`#${ref}_year`).val();
        var month =  $(`#${ref}_month`).val();
        root.pullField(ref).value = `${year}-${month}-${e.target.value}`;
        console.log(root.settings.form);
      }
    })
  },

  pullField(field) {
    // this should be a promise
    var res = undefined;
    this.settings.form.forEach(function(formField) {
      if (formField.name == field && ((formField.hasOwnProperty("noHash") && formField.noHash == true))) {
        res = formField
      } else if (formField.id == field) {
        res = formField
      }
    });
    return res;
  },
};

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

formGen.prototype = {
  init() {
    this.formEle = $(this.formId);
    this.generateForm();
    this.registerEvents();
    this.validationMethods.root = this;
  },

  generateForm() {
    var root = this;
    this.settings.form.forEach(function(formField) {

      // assign random id (screw you auto correct!)
      if (formField.hasOwnProperty("noHash") && formField.noHash == true) {
        formField.id = formField.name;
        formField.autocomplete = formField.name
      } else {
        formField.id = root.generateUUID();
        formField.autocomplete = root.generateUUID();
      }

      switch (formField.type) {
        case "string":
          formField.html = root.createStringInput(formField, "text");
          root.addToForm(formField);
          break;
        case "password":
          formField.html = root.createStringInput(formField, "password");
          root.addToForm(formField);
          break;
        case "confirm-password":
          formField.html = root.createStringInput(formField, "password");
          root.addToForm(formField);
          break;
        case "email":
          formField.html = root.createStringInput(formField, "text");
          root.addToForm(formField);
          break;
        case "integer":
          formField.html = root.createIntegerInput(formField);
          root.addToForm(formField);
          break;
        case "float":
          formField.html = root.createFloatInput(formField);
          root.addToForm(formField);
          break;
        case "date":
          formField.html = root.createDateInput(formField);
          root.addToForm(formField);
          if (formField.hasOwnProperty("value")) {
            set_date = new Date(formField.value);
            $(`#${formField.id}_year`).val(set_date.getFullYear());
            $(`#${formField.id}_month`).val(1 + set_date.getMonth());
            root.dateAddDays(formField.id);
            root.setDate(formField.id, (1 + set_date.getDate()));
            $(`#${formField.id}_day`).val(1 + set_date.getDate());
          }
          $(`#${formField.id}_year`).formSelect();
          $(`#${formField.id}_month`).formSelect();
          $(`#${formField.id}_day`).formSelect();
          break;
        case "select":
          formField.html = root.createSelectInput(formField);
          root.addToForm(formField);
          $(`#${formField.id}`).formSelect();
          break;
        default:
          console.error(`field type not defined ${formField.type}`);
      }
    });
  },

  addToForm(field) {
    if (field.hasOwnProperty("element")) {
      $(field.element).append(field.html);
    } else {
      if (!$("#formElements").length) {
        this.formEle.prepend($("<div id='formElements'></div>"));
      }
      console.log(field.html);
      $("#formElements").append(field.html);
    }
  },

  generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0,
        v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  },



  createStringInput(formField, type) {
    element = $(`
      <div class="row">
        <div class="input-field col s12">
          <input id="${formField.id}" autocomplete="${formField.autocomplete}" type="${type}" autocorrect="off" autocapitalize="off">
          <label for="${formField.id}">${formField.placeholder}</label>
        </div>
      </div>
    `);
    return element
  },

  createDateInput(formField) {
    if (formField.hasOwnProperty("min")) {
      minDate = new Date(formField.min);
    } else {
      minDate = new Date("1930-01-01");
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
    for (var i = 1; i < 13; i++) {
      month = new Date(`1970-${i}-02`).toLocaleString('default', {
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
          <label for="${formField.id}_year" style="overflow: auto; width: calc(100% * 4);">${formField.placeholder}</label>
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
    element = $(`
      <div class="row">
        <div class="input-field col s12">
          <input id="${formField.id}" autocomplete="${formField.autocomplete}" type="text" inputmode="numeric">
          <label for="${formField.id}">${formField.placeholder}</label>
        </div>
      </div>
    `);
    return element
  },

  createFloatInput(formField) {
    element = $(`
      <div class="row">
        <div class="input-field col s12">
          <input id="${formField.id}" autocomplete="${formField.autocomplete}" type="text" inputmode="numeric">
          <label for="${formField.id}">${formField.placeholder}</label>
        </div>
      </div>
    `);
    return element
  },

  createSelectInput(formField) {
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
      options = `<option value="null" disabled selected>Choose ${formField.placeholder}</option>`.concat(options);
    }

    element = $(`
      <div class="row">
        <div class="input-field col s12">
          <select id="${formField.id}" autocomplete="${formField.autocomplete}">
            ${options}
          </select>
          <label for="${formField.id}">${formField.placeholder}</label>
        </div>
      </div>
    `);
    return element
  },

  registerEvents() {
    var root = this;
    var ignored = ["year", "month", "day"];

    this.formEle.on("change keyup", function(e) {
      var ref = e.target.id.substring(0, (e.target.id.length - e.target.id.split("_").pop().length) - 1);
      if (!ignored.includes(e.target.id.split("_").pop())) {
        root.pullField(e.target.id).value = e.target.value
      }

      // add days to day select
      if (e.target.id.split("_").pop() == "month" || e.target.id.split("_").pop() == "year") {
        root.dateAddDays(ref, e.target.value);
      }

      // set day
      if (e.target.id.split("_").pop() == "day") {
        root.setDate(ref, e.target.value);
      }

      // validate form
      root.validateForm(ref);
    })

    this.formEle.on("submit", function(e) {
      e.preventDefault();
      e.stopPropagation();
      if (root.validateForm() != 0) {
        root.lockSubmit();
      }

      console.log(root.settings.form);
    })
  },

  lockSubmit() {
    this.formEle.find("button[type='submit']").attr("disabled", "");
  },

  dateAddDays(ref, month = undefined) {
    $(`#${ref}_day`).val("");
    $(`#${ref}_day`).children().remove().end().append('<option disabled selected value="">DD</option>');
    this.pullField(ref).value = "";
    var year = $(`#${ref}_year`).val();
    if (month == undefined) {
      month = $(`#${ref}_month`).val();
    }

    if (year != null && month != null) {
      var days = ""
      for (var day = 1; day <= new Date(year, month, 0).getDate(); day++) {
        days += `<option value="${day}">${day}</option>`;
      }
      $(`#${ref}_day`).append(days).formSelect();
    }
  },

  setDate(ref, day) {
    var year = $(`#${ref}_year`).val();
    var month = $(`#${ref}_month`).val();
    this.pullField(ref).value = `${year}-${month}-${day}`;
  },

  pullField(field, strict=true) {
    // this should be a promise
    var res = undefined;
    this.settings.form.forEach(function(formField) {
      passName  = strict ? ((formField.hasOwnProperty("noHash") && formField.noHash == true)) : true;
      if (formField.name == field && passName) {
        res = formField
      } else if (formField.id == field) {
        res = formField
      }
    });
    return res;
  },

  validateForm(field=null) {
    var root = this;
    var total_errors = 0;
    var fieldArray = [];

    if (field == null) {
      fieldArray = this.settings.form;
    } else {
      fieldArray.push(root.pullField(field));
      console.log(fieldArray)
    }

    fieldArray.forEach(function(field) {
      if($(`#${field.id}`).attr("id") === undefined && field.type != "date") {
        console.error(`(${field.name})#${field.id} has not been created!`);
      } else if(field.type == "date" && $(`#${field.id}_year`).attr("id") === undefined) {
        console.error(`(${field.name})#${field.id} has not been created!`);
      }

      // set value for validators and scoped global
      var res = true;
      var errors = 0;
      root.validationMethods.value = field.value;

      // general validation for types
      switch (field.type) {
        case 'float':
          res = root.validationMethods.isFloat();
          break;
        case 'integer':
          res = root.validationMethods.isInteger();
          break;
        case 'email':
          res = root.validationMethods.isEmail();
          break;
        case 'confirm-password':
          res = root.validationMethods.sameAs("password");
          break;
      }

      if (res != true && res[0] == 0) {
        errors++;
        root.attachError(field, res[1]);
      }

      if (field.hasOwnProperty("validators")) {
        field.validators.forEach(function(val_func) {
          if (typeof val_func === 'string') {
            // this is a default validator
            res = eval(`root.validationMethods.${val_func}`);
          } else {
            res = val_func.call(field.value);
          }

          if (res[0] == 0) {
            errors++;
            root.attachError(field, res[1]);
          }
        });
      }

      // clear errors if needed
      if (errors == 0) {
        root.validField(field);
      } else {
        total_errors+=errors;
      }
    })

    return total_errors;
  },

  attachError(field, error) {
    switch (field.type) {
      case 'string':
      case 'password':
      case 'integer':
      case 'float':
      case 'email':
      case 'confirm-password':
        $(`#${field.id}`).parent().find("span[class='helper-text']").remove();
        $(`label[for="${field.id}"]`).after(`<span class="helper-text" data-error="${error}"></span>`);
        $(`#${field.id}`).removeClass("valid").addClass("invalid");
        break;

      case 'select':
        $(`#${field.id}`).parentsUntil(".row").find("span[class='helper-text']").remove();
        $(`label[for="${field.id}"]`).after(`<span class="helper-text" data-error="${error}"></span>`);
        $(`#${field.id}`).parentsUntil(".row").removeClass("valid").addClass("invalid");
        break;

      case 'date':
        $(`#${field.id}_year`).parentsUntil(".row").find("span[class='helper-text']").remove();
        $(`label[for="${field.id}_year"]`).after(`<span class="helper-text" style="position: relative; overflow: auto; width: calc(100% * 4);" data-error="${error}"></span>`);
        $(`#${field.id}_year`).parentsUntil(".row").removeClass("valid").addClass("invalid");
        $(`#${field.id}_month`).parentsUntil(".row").removeClass("valid").addClass("invalid");
        $(`#${field.id}_day`).parentsUntil(".row").removeClass("valid").addClass("invalid");
        break;
    }
  },

  validField(field) {
    switch (field.type) {
      case 'string':
      case 'password':
      case 'integer':
      case 'float':
      case 'email':
      case 'confirm-password':
        $(`#${field.id}`).parent().find("span[class='helper-text']").remove();
        $(`#${field.id}`).removeClass("invalid").addClass("valid");
        break;

      case 'select':
        $(`#${field.id}`).parentsUntil(".row").find("span[class='helper-text']").remove();
        $(`#${field.id}`).parentsUntil(".row").removeClass("invalid").addClass("valid");
        break;

      case 'date':
        $(`#${field.id}_year`).parentsUntil(".row").find("span[class='helper-text']").remove();
        $(`#${field.id}_year`).parentsUntil(".row").removeClass("invalid").addClass("valid");
        $(`#${field.id}_month`).parentsUntil(".row").removeClass("invalid").addClass("valid");
        $(`#${field.id}_day`).parentsUntil(".row").removeClass("invalid").addClass("valid");
        break;
    }
  },

  validationMethods: {
    strMin(min) {
      notEmptyRes = this.notEmpty();
      if (notEmptyRes[0] == 0) {
        return notEmptyRes;
      }
      if (this.value.length < min) {
        return [0, `This field length is too short min: ${min}`];
      }
      return [1, ""];
    },
    strMax(max) {
      notEmptyRes = this.notEmpty();
      if (notEmptyRes[0] == 0) {
        return notEmptyRes;
      }
      if (this.fieldValue.length > max) {
        return [0, `This field length is too short min: ${max}`];
      }
      return [1, ""];
    },
    strMinMax(min, max) {
      notEmptyRes = this.notEmpty();
      if (notEmptyRes[0] == 0) {
        return notEmptyRes;
      }
      if (this.fieldValue.length > max || this.fieldValue.length < min) {
        return [0, `This field length is out of bounds min: ${min}, max: ${max}`];
      }
      return [1, ""];
    },
    notEmpty() {
      if (this.value == undefined || this.value == null || this.value.length == 0 || this.value == "") {
        return [0, `This field is required`];
      }
      return [1, ""];
    },
    isFloat() {
      if (this.value == null) {
        return [1, ""];
      }

      if (/^(\d+\.?\d*|\.\d+)$/.test(this.value) == false) {
        return [0, "Value is not a decimal, decimals only support (.)"];
      }
      return [1, ""];
    },
    isInteger() {
      if (this.value == null) {
        return [1, ""];
      }

      if (/^\d+$/.test(this.value) == false) {
        return [0, "Value is not a number."];
      }
      return [1, ""];
    },
    isEmail() {
      if (this.value == null) {
        return [1, ""];
      }
      if (/(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/i.test(this.value) == false) {
        return [0, "Email is invalid."];
      }
      return [1, ""];
    },
    sameAs(field) {
      notEmptyRes = this.notEmpty();
      if (notEmptyRes[0] == 0) {
        return notEmptyRes;
      }
      compairField = this.root.pullField(field, false);
      if (compairField.value != this.value) {
        return [0, `This field doesn't match the ${compairField.name} field.`];
      }
      return [1, ""];
    }
  }
};

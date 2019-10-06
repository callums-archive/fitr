/*!
 *Materialize Form Mapper
 *By Callum Fleming (c)2019 (@howzitcal)
 *Licence: GPl v2
 */

var formGen = function(formId, settings) {
  this.formId = formId;
  this.settings = settings;

  this.init();
};

formGen.prototype = {
  init() {
    this.formEle = $(this.formId);
    this.generateForm();
    this.registerEvents();
    this.validationMethods.self = this;
  },

  generateForm() {
    var self = this;
    this.settings.form.forEach(function(formField) {
      // assign random id (screw you auto correct!)
      if (formField.hasOwnProperty("noHash") && formField.noHash == true) {
        formField.id = formField.name;
        formField.autocomplete = formField.name;
      } else {
        formField.id = self.generateUUID();
        formField.autocomplete = self.generateUUID();
      }

      switch (formField.type) {
        case "string":
          formField.html = self.createStringInput(formField, "text");
          self.addToForm(formField);
          break;
        case "password":
          formField.html = self.createStringInput(formField, "password");
          self.addToForm(formField);
          break;
        case "confirm-password":
          formField.html = self.createStringInput(formField, "password");
          self.addToForm(formField);
          break;
        case "email":
          formField.html = self.createStringInput(formField, "text");
          self.addToForm(formField);
          break;
        case "integer":
          formField.html = self.createSpecialInput(formField, "integer");
          self.addToForm(formField);
          break;
        case "float":
          formField.html = self.createSpecialInput(formField, "float");
          self.addToForm(formField);
          break;
        case "date":
          formField.html = self.createDateInput(formField);
          self.addToForm(formField);
          if (formField.hasOwnProperty("value")) {
            set_date = new Date(formField.value);
            $(`#${formField.id}_year`).val(set_date.getFullYear());
            $(`#${formField.id}_month`).val(1 + set_date.getMonth());
            self.dateAddDays(formField.id);
            self.setDate(formField.id, 1 + set_date.getDate());
            $(`#${formField.id}_day`).val(1 + set_date.getDate());
          }
          break;
        case "select":
          formField.html = self.createSelectInput(formField);
          self.addToForm(formField);
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
      $("#formElements").append(field.html);
    }
  },

  generateUUID() {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {
      var r = (Math.random() * 16) | 0,
        v = c == "x" ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  },

  createSpecialInput(formField, type) {
    var extras = "";
    if (type == "integer" || type == "float") {
      extras += 'inputmode="numeric"';
    }
    label = formField.placeholder
      ? `<label for="${formField.id}">${formField.placeholder}</label>`
      : "";

    fg_adjust = "";
    if (
      formField.hasOwnProperty("formGroupAdj") &&
      formField.hasOwnProperty("element")
    ) {
      $(formField.element).addClass(formField.formGroupAdj);
    } else if (formField.hasOwnProperty("formGroupAdj")) {
      fg_adjust = formField.formGroupAdj;
    }

    element = $(`
      <div class="form-group ${fg_adjust}">
        ${label}
        <input id="${formField.id}" autocomplete="${formField.autocomplete}" class="form-control" autocorrect="off" autocapitalize="off" ${extras}>
      </div>
    `);
    return element;
  },

  createStringInput(formField, type) {
    label = formField.placeholder
      ? `<label for="${formField.id}">${formField.placeholder}</label>`
      : "";

    fg_adjust = "";
    if (
      formField.hasOwnProperty("formGroupAdj") &&
      formField.hasOwnProperty("element")
    ) {
      $(formField.element).addClass(formField.formGroupAdj);
    } else if (formField.hasOwnProperty("formGroupAdj")) {
      fg_adjust = formField.formGroupAdj;
    }

    element = $(`
      <div class="form-group ${fg_adjust}">
        ${label}
        <input id="${formField.id}" autocomplete="${formField.autocomplete}" class="form-control" type="${type}" autocorrect="off" autocapitalize="off">
      </div>
    `);
    return element;
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
      maxDate.setFullYear(maxDate.getFullYear() + 10);
    }

    // generate years
    var years = "";
    for (var i = minDate.getFullYear(); i <= maxDate.getFullYear(); i++) {
      years += `<option value="${i}">${i}</option>`;
    }

    // generate months
    var months = "";
    var months_arr = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec"
    ];

    for (var i = 1; i < 13; i++) {
      months += `<option value="${i}">${months_arr[i - 1]}</option>`;
    }

    element = $(`

      <label>${formField.placeholder}</label>
      <div class="row">
        <div class="col pr-1">
          <select id="${formField.id}_year" class="form-control pl-0" style="padding-right: 0px;" autocomplete="${formField.autocomplete}">
            <option value="" disabled selected>YYYY</option>
            ${years}
          </select>
        </div>

        <div class="col pl-1 pr-1">
          <select id="${formField.id}_month" class="form-control pl-0" style="padding-right: 0px;" autocomplete="${formField.autocomplete}">
            <option value="" disabled selected>MM</option>
            ${months}
          </select>
        </div>

        <div class="col pl-1">
          <select id="${formField.id}_day" class="form-control pl-0" style="padding-right: 0px;" autocomplete="${formField.autocomplete}">
            <option value="" disabled selected>DD</option>
          </select>
        </div>
      </div>

      <div class="input-group mb-3" id="${formField.id}_error" >
        <input type="text" style="display: contents" class="form-control is-invalid">
      </div>
    `);
    return element;
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
      options = `<option value="" disabled selected>Choose ${formField.placeholder}</option>`.concat(
        options
      );
    }

    label = formField.placeholder
      ? `<label for="${formField.id}">${formField.placeholder}</label>`
      : "";

    fg_adjust = "";
    if (
      formField.hasOwnProperty("formGroupAdj") &&
      formField.hasOwnProperty("element")
    ) {
      $(formField.element).addClass(formField.formGroupAdj);
    } else if (formField.hasOwnProperty("formGroupAdj")) {
      fg_adjust = formField.formGroupAdj;
    }

    element = $(`
      <div class="form-group ${fg_adjust}">
        ${label}
        <select id="${formField.id}" class="form-control" autocomplete="${formField.autocomplete}">
          ${options}
        </select>
      </div>
    `);
    return element;
  },

  registerEvents() {
    var self = this;
    var ignored = ["year", "month", "day"];

    this.formEle.on("change keyup", function(e) {
      // ref for date
      var ref = e.target.id.substring(
        0,
        e.target.id.length - e.target.id.split("_").pop().length - 1
      );

      if (!ignored.includes(e.target.id.split("_").pop())) {
        // set the valus and the "basic ref" for other fields (this is mainly for validation)
        self.pullField(e.target.id).value = e.target.value;
        ref = e.target.id;
      }

      // add days to day select
      if (
        e.target.id.split("_").pop() == "month" ||
        e.target.id.split("_").pop() == "year"
      ) {
        self.dateAddDays(ref, e.target.value);
      }

      // set day
      if (e.target.id.split("_").pop() == "day") {
        self.setDate(ref, e.target.value);
      }

      // validate form
      self.validateForm(ref);

      // try to unlock submit button
      if (self.submitStatus == false && self.validateForm(ref) == 0) {
        console.log(self.formEle.find(".invalid-feedback"));
        if (self.formEle.find(".invalid-feedback").length == 0) {
          self.unlockSubmit();
        }
      }
    });

    this.formEle.on("submit", function(e) {
      e.preventDefault();
      e.stopPropagation();
      self.lockSubmit();

      if (self.validateForm() != 0) {
        $("html, body").animate(
          {
            scrollTop: 0
          },
          "slow"
        );
      } else {
        // TODO XXX check this out (removed to lock submit)
        // console.log("unlocked")
        // self.unlockSubmit();
        // get the data ready
        formFields = {};
        self.settings.form.forEach(function(field) {
          formFields[field.name] = field.value;
        });
        formFields = JSON.stringify(formFields);

        //run validation via ajax
        $.ajax({
          accept: "application/json",
          contentType: "application/json",
          type: self.settings.remote.submit.method,
          url: self.settings.remote.submit.url,
          data: formFields
        })
          .done(function(data, status, jqXHR) {
            self.settings.onSuccess(data, status, jqXHR);
          })
          .fail(function(jqXHR, status) {
            self.settings.onFail(jqXHR, status);
          })
          .always(function() {
            self.unlockSubmit();
          });
      }
    });
  },

  lockSubmit() {
    this.submitStatus = false;
    this.formEle.find("button[type='submit']").attr("disabled", "");
  },

  unlockSubmit() {
    this.submitStatus = true;
    this.formEle.find("button[type='submit']").removeAttr("disabled");
  },

  dateAddDays(ref, month = undefined) {
    console.log("we get here");
    $(`#${ref}_day`).val("");
    $(`#${ref}_day`)
      .children()
      .remove()
      .end()
      .append('<option disabled selected value="">DD</option>');
    this.pullField(ref).value = "";
    var year = $(`#${ref}_year`).val();
    if (month == undefined) {
      month = $(`#${ref}_month`).val();
    }

    if (year != null && month != null) {
      var days = "";
      for (var day = 1; day <= new Date(year, month, 0).getDate(); day++) {
        days += `<option value="${day}">${day}</option>`;
      }
    }

    $(`#${ref}_day`).append(days);
  },

  setDate(ref, day) {
    var year = $(`#${ref}_year`).val();
    var month = $(`#${ref}_month`).val();

    var proposed_date = `${year}-${month}-${day}`;
    if (proposed_date.includes("null")) {
      this.pullField(ref).value = null;
    } else {
      this.pullField(ref).value = proposed_date;
    }
  },

  pullField(field, strict = true) {
    // this should be a promise
    var res = undefined;
    this.settings.form.forEach(function(formField) {
      passName = strict
        ? formField.hasOwnProperty("noHash") && formField.noHash == true
        : true;
      if (formField.name == field && passName) {
        res = formField;
      } else if (formField.id == field) {
        res = formField;
      }
    });
    return res;
  },

  validateForm(fieldValidate = null) {
    var self = this;
    var total_errors = 0;
    var fieldArray = [];

    if (fieldValidate == null) {
      fieldArray = this.settings.form;
    } else {
      fieldArray.push(self.pullField(fieldValidate));
    }

    fieldArray.forEach(function(field) {
      if ($(`#${field.id}`).attr("id") === undefined && field.type != "date") {
        console.error(`(${field.name})#${field.id} has not been created!`);
      } else if (
        field.type == "date" &&
        $(`#${field.id}_year`).attr("id") === undefined
      ) {
        console.error(`(${field.name})#${field.id} has not been created!`);
      }

      // set value for validators and scoped global
      var res = true;
      var errors = 0;

      self.validationMethods.value = field.value;
      self.validationMethods.id = field.id;
      self.validationMethods.name = field.name;

      // general validation for types
      switch (field.type) {
        case "float":
          res = self.validationMethods.isFloat();
          break;
        case "integer":
          res = self.validationMethods.isInteger();
          break;
        case "email":
          res = self.validationMethods.isEmail();
          break;
        case "confirm-password":
          res = self.validationMethods.sameAs("password");
          break;
        case "date":
          res = self.validationMethods.isDate();
      }

      if (res != true && res[0] == 0) {
        errors++;
        self.attachError(field, res[1]);
      }

      if (field.hasOwnProperty("validators")) {
        field.validators.forEach(function(val_func) {
          canContinue =
            (fieldValidate != null && errors == 0) ||
            (fieldValidate == null && errors == 0)
              ? true
              : false;
          if (canContinue) {
            if (typeof val_func === "string") {
              // this is a default validator
              res = eval(`self.validationMethods.${val_func}`);
            } else {
              res = val_func.call(field.value);
            }
          }

          if (res[0] == 0) {
            errors++;
            self.attachError(field, res[1]);
          }
        });
      }

      // clear errors if needed
      if (errors == 0) {
        self.validField(field);
      } else {
        total_errors += errors;
      }
    });

    return total_errors;
  },

  attachError(field, error) {
    switch (field.type) {
      case "string":
      case "password":
      case "integer":
      case "float":
      case "email":
      case "confirm-password":
      case "select":
        $(`#${field.id}`)
          .parent()
          .find('div[class="valid-feedback"]')
          .remove();
        $(`#${field.id}`)
          .parent()
          .find('div[class="invalid-feedback"]')
          .remove();
        $(`#${field.id}`)
          .parent()
          .append(`<div class="invalid-feedback">${error}</div>`);
        $(`#${field.id}`)
          .removeClass("is-valid")
          .addClass("is-invalid");
        break;

      case "date":
        $(`#${field.id}_error`)
          .find('div[class="valid-feedback"]')
          .remove();
        $(`#${field.id}_error`)
          .find('div[class="invalid-feedback"]')
          .remove();
        $(`#${field.id}_error`).append(
          `<div class="invalid-feedback">${error}</div>`
        );
        $(`#${field.id}_year`)
          .removeClass("is-valid")
          .addClass("is-invalid");
        $(`#${field.id}_month`)
          .removeClass("is-valid")
          .addClass("is-invalid");
        $(`#${field.id}_day`)
          .removeClass("is-valid")
          .addClass("is-invalid");
        break;
    }
  },

  validField(field) {
    switch (field.type) {
      case "string":
      case "password":
      case "integer":
      case "float":
      case "email":
      case "confirm-password":
      case "select":
        $(`#${field.id}`)
          .parent()
          .find('div[class="valid-feedback"]')
          .remove();
        $(`#${field.id}`)
          .parent()
          .find('div[class="invalid-feedback"]')
          .remove();
        $(`#${field.id}`)
          .removeClass("is-invalid")
          .addClass("is-valid");
        break;

      case "date":
        $(`#${field.id}_error`)
          .find('div[class="valid-feedback"]')
          .remove();
        $(`#${field.id}_error`)
          .find('div[class="invalid-feedback"]')
          .remove();
        $(`#${field.id}_year`)
          .removeClass("is-invalid")
          .addClass("is-valid");
        $(`#${field.id}_month`)
          .removeClass("is-invalid")
          .addClass("is-valid");
        $(`#${field.id}_day`)
          .removeClass("is-invalid")
          .addClass("is-valid");
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
        return [
          0,
          `This field length is out of bounds min: ${min}, max: ${max}`
        ];
      }
      return [1, ""];
    },
    notEmpty() {
      console.log(this.name, this.value);
      if (
        !this.value ||
        this.value == undefined ||
        this.value == null ||
        this.value.length == 0 ||
        this.value == ""
      ) {
        return [0, `This field is required`];
      }
      return [1, ""];
    },
    isDate() {
      // this is here to check to see if a date is valid
      // see if date is required
      var self = this;
      var required = false;
      var elem = null;

      this.self.settings.form.forEach(function(ele) {
        if (ele.name == self.name) {
          if (ele.validators.includes("notEmpty()")) {
            required = true;
            elem = ele;
          }
        }
      });

      // if the date is not required and the date is empty the pass
      if ((required == false) & (this.notEmpty()[0] == 0)) {
        return [1, ""];
      }

      // if the date is required and it's empty
      else if ((required == true) & (this.notEmpty()[0] == 0)) {
        return [0, "Date is required"];
      }

      // res scoped
      var res = [1, ""];

      if ((self.notEmpty()[0] == 1) & (self.value.split("-").length == 3)) {
        dateArr = self.value.split("-");
      } else {
        return [0, "Date is required"];
      }

      dateArr.forEach(function(val) {
        if (!parseInt(val) >= 1) {
          res = [0, "Date is required"];
        }
      });
      return res;
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
    isUsername() {
      if (this.value == null) {
        return [1, ""];
      }

      if (/^[A-Za-z0-9_]{3,16}$/.test(this.value) == false) {
        return [
          0,
          "Username supports upto 16 letters and numbers and underscores, minimum 3."
        ];
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
      if (
        /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/i.test(
          this.value
        ) == false
      ) {
        return [0, "Email is invalid."];
      }
      return [1, ""];
    },
    sameAs(field) {
      notEmptyRes = this.notEmpty();
      if (notEmptyRes[0] == 0) {
        return notEmptyRes;
      }
      compairField = this.self.pullField(field, false);
      if (compairField.value != this.value) {
        return [0, `This field doesn't match the ${compairField.name} field.`];
      }
      return [1, ""];
    },
    remote() {
      var request_method = this.self.settings.remote.validate.method;
      var validate_url = this.self.settings.remote.validate.url;

      var formData = {};
      formData[this.name] = this.value;

      var currentField = this.self.pullField(this.id, false);

      var local_self = this;

      $.ajax({
        accept: "application/json",
        contentType: "application/json",
        type: request_method,
        url: validate_url,
        data: JSON.stringify(formData)
      })
        .done(function(data, status, jqXHR) {
          if (data["valid"] == false) {
            local_self.self.attachError(currentField, data["message"]);
            local_self.self.lockSubmit();
          } else if (data["valid"] == true) {
            local_self.self.validField(currentField);
          }
        })
        .fail(function(data, status, jqXHR) {
          local_self.self.attachError(currentField, "Server Error. Try again.");
          local_self.self.lockSubmit();
        });

      // innocent till prouven guilty
      return [1, ""];
    }
  }
};

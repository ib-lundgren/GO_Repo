// Library for interacting with the Game Object Repository
// Find out more at http://go-repo.appspot.com

function capitalise(string)
{
    return string.charAt(0).toUpperCase() + string.slice(1);
}

var go = {
    forms : {}
}

go.create_form = function(form, target, object_id, updated) {
    go.forms[target] = form;
    creators = {
        object : go.create_object,
        file : go.create_file,
        textfield : go.create_textfield,
        textarea : go.create_textarea,
        list : go.create_list,
        choice : go.create_choice
    }
    for (var key in form) {
        go.forms[target][key]["element"] = null;
        go.forms[target][key]["valid"] = true;
        if (!updated) {
            go.forms[target][key]["value"] = null;
        }
        (creators[(form[key].type)])(form[key], target);
    }
    var t = target;
    if (object_id) {
        $.getJSON("/api/" + target + "/" + object_id + "/", {}, function(data, textStatus, xhr) {
            for (var key in go.forms[t]) {
                go.forms[t][key].value = data[key];
            }
            go.create_form(go.forms[t], t, null, true);
        });
    }
}

go.check_and_append = function(target) {
    var ok = true;
    var t = target;
    for (var field in go.forms[target]) {
        ok &= go.forms[target][field].element != null; 
    }

    if (ok) {
        $("#" + target).empty();
        var f = $("<form>");
        f.attr("enctype", "multipart/form-data");

        var error = $("<p>");
        error.attr("id", "error");
        error.attr("name", "error");
        error.addClass("alert-message alert-block warning");
        error.hide();
        f.append(error);

        for (var field in go.forms[target]) {
            f.append(go.forms[target][field].element);
        }   

        actions = $("<div>");
        actions.addClass("actions");
        input = $("<div>");
        input.addClass("input");

        save = $("<button>");
        save.addClass("btn");
        save.addClass("primary");
        save.attr("name", "environment-submit");
        save.attr("id", "environment-submit");
        save.html("Create");
        save.click(function(event) {
            event.preventDefault();
            return go.submit_form(t);
        });
        input.append(save);

        cancel = $("<button>");
        cancel.addClass("btn");
        cancel.addClass("danger");
        cancel.attr("name", "environment-cancel");
        cancel.attr("id", "environment-cancel");
        cancel.html("Cancel");
        input.append(cancel);

        actions.append(input);
        f.append(actions);

        $("#" + target).append(f);
    }
    
}

go.update_form = function(target, key, field, value) {
    go.forms[target][key][field] = value;
    go.check_and_append(target);
}

go.validate_form = function(target) {
    var success = true;
    for (var key in go.forms[target]) {
        var field = go.forms[target][key];
        go.validate_field(field);
        success &= field.valid;
    }
    return success;
}

go.submit_form = function(target) {
    if (!go.validate_form(target)) {
        // TODO: Display error message
    }
    else if (go.has_files(target)) {
        console.log("got ya");
        var iframe = $("<iframe>");
        iframe.attr("id", "our_secret_iframe");
        iframe.attr("name", "our_secret_iframe");
        iframe.attr("src", "#");
        iframe.attr("width", "0");
        iframe.attr("height", "0");
        iframe.css("display: none; visibility:hidden;");

        var data = {}
        for (var key in go.forms[target]) {
            var field = go.forms[target][key];
            // Lists have to be handled separately after the object
            // has been created. 
            if (field.type != "list")
                data[field.id] = field.value;
        }
        var url = "/api/" + target + "/";
        // Check if we are updating an object
        if (data.obj_id) 
            url += data.obj_id + "/";

        console.log(data);
        console.log(url);
        var form = $("#" + target + " form");
        form.attr("method", "POST");
        form.attr("action", url);
        form.attr("target", "our_secret_iframe");
        form.after(iframe);
        console.log(form);
        form.submit();
        return true;
    }
    else {
        var data = {}
        for (var key in go.forms[target]) {
            var field = go.forms[target][key];
            // Lists have to be handled separately after the object
            // has been created. 
            if (field.type != "list")
                data[field.id] = field.value;
        }
        var url = "/api/" + target + "/";
        // Check if we are updating an object
        if (data.obj_id) 
            url += data.obj_id + "/";
        console.log(data);
        $.ajax({
            type : "POST",
            url : url,
            dataType : "json",
            data : data,
            statusCode : {
                201 : go.object_created,
                200 : go.object_updated,
                400 : go.invalid_form,
                403 : go.unauthorized,
                404 : go.object_not_found,
                500 : go.internal_error
            }
        });
        return false;
    }
}

go.has_files = function(target) {
    var has_files = false;
    for (var key in go.forms[target]) {
        has_files |= go.forms[target][key].type == "file";
    }
    return has_files;
}

go.validate_field = function(field) {
    getters = {
        object : go.val_object,
        file : go.val_file,
        textfield : go.val_textfield,
        textarea : go.val_textarea,
        list : go.val_list,
        choice : go.val_choice
    };
    var val = (getters[field.type])(field);
    for (var i = 0; i < field.validators.length; i++) {
        field.valid = (field.validators[i])(val);        
    }
    if (!field.valid) {
        $("#" + field.id + "Error").addClass("error");
        field.value = null;
    } 
    else {
        $("#" + field.id + "Error").removeClass("error");
        field.value = val;
    }
}

go.val_object = function(field) {
    return $("#" + field.id).val();
}

go.val_file = function(field) {
    return $("#" + field.id).val();
}

go.val_textfield = function(field) {
    return $("#" + field.id).val();
}

go.val_textarea = function(field) {
    return $("#" + field.id).val();
}

go.val_list = function(field) {
    var values = [];
     $("input[name='" + field.id + "']:checked").each(function() {
        values.push($(this).val());
     });
    return values;
}

go.val_choice = function(field) {
    return $("input[name='" + field.id + "']:checked").val();
}

go.not_empty = function(val) {
    return val && val.length > 0;
}

go.is_float = function(val) {
    var float_pattern = /^\d+\.?\d*$/;
    return float_pattern.test(val);
}

go.object_created = function(data, textStatus, xhr) {
    $(".page-title").html("Thank you for creating a new object");
    var info = $("<pre>");
    info.html(JSON.stringify(data, null, '\t'));
    $("#"+data.category).html(info);
}

go.object_updated = function(data, textStatus, xhr) {
    $(".page-title").html("Thank you for updating an object");
    var info = $("<pre>");
    info.html(JSON.stringify(data, null, '\t'));
    $("#"+data.category).html(info);
}

go.invalid_form = function(xhr) {
    var data = $.parseJSON(xhr.responseText);
    var error = "<strong>Error</strong>: Received invalid form data when trying to update object."; 
    for (field in data.message) {
        error += "<br/><strong>" + capitalise(field) + "</strong>: " + data.message[field]; 
    }
    $("#error").html(error);
    $("#error").show();
    console.log(data);
}

go.unauthorized = function(xhr) {
    var data = $.parseJSON(xhr.responseText);
    $("#error").html("<strong>Error</strong>: " + data.message);
    $("#error").show();
}

go.object_not_found = function(xhr) {
    var data = $.parseJSON(xhr.responseText);
    $("#error").html("<strong>Error</strong>: " + data.message);
    $("#error").show();
}

go.internal_error = function(xhr) {
    var data = $.parseJSON(xhr.responseText);
    $("#error").html("<strong>Internal Server Error</strong>: Please note exactly " +
                     "what you did and contact the website administrator.");
    $("#error").show();
    console.log(xhr.responseText);
}

go.create_object = function(field, target) {
    text = $("<input>");
    text.attr("type", "hidden");
    text.attr("id", field.id);
    text.attr("name", field.id);
    text.attr("value", field.key);
    go.update_form(target, field.id, "element", text); 
}

go.create_list = function(field, target) {
    var f = field;
    var t = target;
    $.ajax({ type : "GET",
            url : "/api/" + f.category + "/",
            data : {},
            dataType : "json",
            statusCode : {
                "200" : function(data, textStatus, xhr) {
                    table = $("<table>");
                    table.addClass("condensed-table");

                    for (var i = 0; i < data.length; i++) {
                        var o = data[i];
                        var tr = $("<tr>");
                        var key = o.key;

                        delete o.rating;
                        delete o.votes;
                        delete o.extra;
                        delete o.key;
                        delete o.downloads;
                        delete o.created;
                        delete o.category;

                        if (i == 0) {
                            var trh = $("<tr>");
                            trh.append($("<th>"));
                            for (prop in o) { 
                                if (o[prop]) {        
                                    var th = $("<th>");
                                    th.html(capitalise(prop.replace("_", " ")));
                                    trh.append(th); 
                                }
                            }
                            theader = $("<thead>");
                            theader.append(trh);
                            table.append(theader);
                        } 
                        var td = $("<td>");
                        var btn = $("<input>");
                        btn.attr("type", "checkbox");
                        btn.attr("name", f.id);
                        btn.attr("id", f.id);
                        btn.attr("value", key);
                        if (f.value && f.value.indexOf(key)) 
                            btn.attr("checked", "true");
                        btn.click(function() {
                            p = this.parentNode.parentNode;
                            if (p.style.background=="rgb(51, 155, 185)") {
                                p.style.background = "#FFFFFF";
                                p.style.color = "#404040";
                            }
                            else {
                                p.style.background = "#339BB9";
                                p.style.color = "#FFFFFF";
                            }
                            go.validate_field(f);
                        });
                        td.append(btn);
                        tr.append(td);
                       
                        for (var field in o) {
                            if (o[prop]) {
                                var td = $("<td>");
                                td.html(o[field].toString());
                                tr.append(td);
                            }
                        }
                        table.append(tr);
                    }
                    table.tablesorter({ sortList: [[1,0]] });
                    clear = $("<div>");
                    clear.addClass("clearfix");
                    clear.attr("id", f.id + "Error");

                    lbl = $("<label>");
                    lbl.attr("for", f.id);
                    lbl.html(f.label);
                    clear.append(lbl);

                    input = $("<div>");
                    input.addClass("input");
                    input.append(table);
                    clear.append(input);

                    go.update_form(t, f.id, "element", clear); 
                },
                "404" : function(data, textStatus, xhr) {
                    alert("Attempting to access invalid category");
                    console.log(data);
                    console.log(textStatus);
                    console.log(xhr);
                }
            }
   });
}

go.create_file = function(field, target) {
    clear = $("<div>");
    clear.addClass("clearfix");
    clear.attr("id", field.id + "Error");

    lbl = $("<label>");
    lbl.attr("for", field.id);
    lbl.html(field.label);
    clear.append(lbl);

    input = $("<div>");
    input.addClass("input");
    
    text = $("<input>");
    text.attr("type", "file");
    text.attr("id", field.id);
    text.attr("name", field.id);
    text.attr("size", field.length);
    text.addClass(field.size);
    var f = field;
    text.keyup(function(event) {
        go.validate_field(f);
    });
    input.append(text);

    helper = $("<span>");
    helper.addClass("help-block");
    helper.html(field.help)
    input.append(helper);

    clear.append(input);
    go.update_form(target, field.id, "element", clear); 
}
go.create_textfield = function(field, target) {
    clear = $("<div>");
    clear.addClass("clearfix");
    clear.attr("id", field.id + "Error");

    lbl = $("<label>");
    lbl.attr("for", field.id);
    lbl.html(field.label);
    clear.append(lbl);

    input = $("<div>");
    input.addClass("input");
    
    text = $("<input>");
    text.attr("type", "text");
    text.attr("id", field.id);
    text.attr("name", field.id);
    text.attr("size", field.length);
    if (field.value)
        text.attr("value", field.value)
    text.addClass(field.size);
    var f = field;
    text.keyup(function(event) {
        go.validate_field(f);
    });
    input.append(text);

    helper = $("<span>");
    helper.addClass("help-block");
    helper.html(field.help)
    input.append(helper);

    clear.append(input);
    go.update_form(target, field.id, "element", clear); 
}

go.create_textarea = function(field, target) {
    clear = $("<div>");
    clear.addClass("clearfix");
    clear.attr("id", field.id + "Error");

    lbl = $("<label>");
    lbl.attr("for", field.id);
    lbl.html(field.label);
    clear.append(lbl);

    input = $("<div>");
    input.addClass("input");
    
    text = $("<textarea>");
    text.attr("id", field.id);
    text.attr("name", field.id);
    text.attr("rows", field.rows);
    if (field.value)
        text.attr("value", field.value)
    text.addClass(field.size);
    var f = field;
    text.keyup(function(event) {
        go.validate_field(f);
    });
    input.append(text);

    helper = $("<span>");
    helper.addClass("help-block");
    helper.html(field.help)
    input.append(helper);

    clear.append(input);
    go.update_form(target, field.id, "element", clear); 
}

go.create_choice = function(field, target) {
    clear = $("<div>");
    clear.addClass("clearfix");
    clear.attr("id", field.id + "Error");

    lbl = $("<label>");
    lbl.attr("for", field.id);
    lbl.html(field.label);
    clear.append(lbl);

    input = $("<div>");
    input.addClass("input");
   
    var list = $("<ul>");
    list.addClass("inputs-list");
    var f = field;
    for (var i = 0; i < field.choices.length; i++) {
        c = field.choices[i];
        var li = $("<li>");
        var lbl = $("<label>");
        choice = $("<input>");
        choice.attr("type", "radio");
        choice.attr("id", field.id);
        choice.attr("name", field.id);
        choice.attr("value", c.value);
        if (field.value && field.value.indexOf(c.value) >= 0)
            choice.attr("checked", "");
        choice.click(function(event) {
            go.validate_field(f);
        });
        var span = $("<span>");
        span.html(c.title);
        lbl.append(choice);
        lbl.append(span);
        li.append(lbl);
        list.append(li);
    }
    input.append(list);

    helper = $("<span>");
    helper.addClass("help-block");
    helper.html(field.help)
    input.append(helper);

    clear.append(input);
    go.update_form(target, field.id, "element", clear); 
}


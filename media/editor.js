$(document).ready(function() {
    var url = "http://go-repo.appspot.com/api/";
    
    function fetch_json(category, handler) {
        var callback = url + category + "?callback=?";
        
        $.getJSON(callback, { }, function(data) {
            handler(data);
        });
    }


    var displayEnvironments = function(data) {
        var json = JSON.stringify(data, null, "\t");
        var output = $("<div>");
        $.each(data, function(index, value) {
            output.append($("<h3>").html(value.title));
            output.append($("<p>").html("Created: " + value.created));
            output.append($("<p>").html(value.description));
            output.append($("<pre>").html(json));
        });
        $('#browse-content').html(output);
    }

    var displayCharacters = function(data) {
        $('#browse-content').html(JSON.stringify(data, null, "\t"));
    }

    var displayEquipment = function(data) {
        $('#browse-content').html(JSON.stringify(data, null, "\t"));
    }

    var displayMissions = function(data) {
        $('#browse-content').html(JSON.stringify(data, null, "\t"));
    }

    $("#browse-environment").click(function() {
        fetch_json("Environment", displayEnvironments);
    });

    $("#browse-character").click(function() {
        fetch_json("Character", displayCharacters);
    });

    $("#browse-equipment").click(function() {
        fetch_json("Equipment", displayEquipment);
    });

    $("#browse-mission").click(function() {
        fetch_json("Mission", displayMissions);
    });
});

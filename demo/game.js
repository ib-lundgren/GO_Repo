$(document).ready(function() {
    // Start Crafty
    //Crafty.init(800, 600);
    //Crafty.canvas.init();

    $.getJSON("http://localhost:8080/api/Graphics?callback=?", { }, function(data) {
        var items = [];
        $.each(data, function(key, val) {
            items.push('<li id="' + key + '">' + '<p>' + val.title + ': ' + val.description + '</p><img width="350" src="http://localhost:8080/' + val.path + '"/></li>');
        });

        $('<ul/>', {
            'class': 'image-list',
            html: items.join('')
        }).appendTo('body');
    });
});
serverURL = "http://go-repo.appspot.com"

var objects = new Array();
var loadingText;
var fireText;

maxObjects = 3;
$(document).ready(function() {
    Crafty.init(800, 600);
    Crafty.canvas();

    spawnUltros();
    spawnBox();
    spawnFire();

    Crafty.scene("loading");
});

Crafty.scene("loading", function () {
    Crafty.background("#000");

    loadingText = Crafty.e("2D, DOM, Text").attr({ w: 100, h: 20, x: 150, y: 120 })
            .text("Loading 0/" + maxObjects)
            .css({ "text-align": "center" });
});

 Crafty.scene("main", function () {
        Crafty.background("#222");
        Crafty.e("2D, DOM, Text")
              .attr({ w: 400, h: 20, x: 150, y: 120 })
              .text("Done loading all objects!")
              .css({ "text-align": "center" });
        
        // Create player
        speed = 4;
        player = Crafty.e("2D, DOM, Ultros, LeftControls")
                .attr({ x: 16, y: 16, z: 1 })       
                .leftControls(3)
                .Ultros();
                
        fireText = Crafty.e("2D, DOM, Flamable, Text")
              .attr({ w: 300, h: 40, x: 350, y: 300 })
              .text("Is ok!")
              .css({ "text-align": "center" });
              
        fireText.text("Hello");

        for (var j = 0; j < 10; j++) {
            grassType = Crafty.randRange(1, 4);
            Crafty.e("2D, DOM, Box")
            .attr({x: j * 64, y: 536})
            .Box();
        }
    });
    
function addToObjectList(obj) {
    objects.push(obj);
    console.log("Loaded Object Graphic: " + obj.image);
    loadingText.text("Loading... " + objects.length + "/" + maxObjects);
    if (objects.length == maxObjects) {
       Crafty.scene("main");
    }
}

ultrosID = 17002
function spawnUltros() {
    loadVisualGameObject(ultrosID, function(obj) {
        Crafty.sprite(256, obj.image, {
            ultrosImage: [0,0]
        });
            
        Crafty.c('Ultros', {
                Ultros: function() {
                    this._direction = 0;
                    this._shotRecently = false;
                    this.requires("Controls, ultrosImage, Gravity, Animate")
                    .animate("walk_left", 0, 0, 1)
                    .animate("walk_right", 0, 1,1)
                    .gravity("Solid")
                    .bind('Moved', function(from) {
                        if(this.hit('Solid')){
                            this.attr({x: from.x, y:from.y});
                        }
                    })
                    .bind('Shoot', function() {
                        console.log("pew");
                        Crafty.e("2D, DOM, Fire")
                          .attr({ w: 64, h:64, x: this._x+120-10*this._direction, y:this._y+110})
                          .Fire(this._direction);
                    })
                    .bind("enterframe", function(e) {
                        if(this.isDown("LEFT_ARROW") || this.isDown("A")) {
                            if(!this.isPlaying("walk_left"))
                                this.stop().animate("walk_left", 5);
                                this._direction = 0;
                        } else if(this.isDown("RIGHT_ARROW") || this.isDown("D")) {
                            if(!this.isPlaying("walk_right"))
                                this.stop().animate("walk_right", 5);
                                this._direction = 1;
                        }
                        
                        if(this.isDown("SPACE") && this._shotRecently == false) {
                            this.trigger('Shoot');
                            this._shotRecently = true;
                            this.delay(function() {
                                this._shotRecently = false;
                            }, 64);
                        }
                    }).bind("keyup", function(e) {
                        this.stop();
                    })                    
                    return this;
                }
        });
    });
}

boxID = 21001
function spawnBox() {
    loadVisualGameObject(boxID, function(obj) {
        Crafty.sprite(64, obj.image, {
            boxImage: [0,0]
        });
            
        Crafty.c('Box', {
                Box: function() {
                    this.requires("Solid, boxImage, Collision")
                    .collision();
                    return this;
                }
        });
    });
}

fireID = 23001
function spawnFire() {
    loadVisualGameObject(fireID, function(obj) {
        Crafty.sprite(60, obj.image, {
            fireImage: [0,0]
        });
            
        Crafty.c('Fire', {
                Fire: function(direction) {
                    this._life = 64;
                    this.requires("fireImage, Animate, Collision").origin("center")
                    .attr({w:0, h:0})
                    .collision()
                    .bind("enterframe", function(e) {
                        this._life -= 1;
                        this.attr({ w: 64-this._life, h: 64-this._life, x: this._x + 10*direction - 5});
                        if (this._life == 0)
                            this.destroy();

                        if(this.hit('Flamable')){
                             fireText.attr({ w: 300, h: 40, x: 350, y: 300 })
                                          .text("FIREFIREFIRE!")
                                          .css({ "text-align": "center", "color":"#F00" });
                            console.log("helo");
                            
                            this.delay( function() {
                                fireText.text("Is ok!").css({"color":"#FFF"});
                             }, 1000);
                        } 
                    });
                    return this;
                }
                
        });
    });
}

function loadVisualGameObject(vid, componentCallback) {
  $.getJSON(serverURL + "/api/VisualGameObject/" + vid + "?callback=?", function(data) {
        $('<li/>', {'html': "Loaded: " + data.title}).appendTo('#object-list');

        console.log("Loaded Object : " + data.title);
        data.image = serverURL + "/api/images/" + data.graphic + ".png"
        componentCallback(data);
        addToObjectList(data);
        //});
     });
}


// -------------------------------------
Crafty.c("LeftControls", {
        init: function() {
            this.requires('Twoway');
        },
       leftControls: function(speed) {
            this.twoway(5,10);
            return this;
        }   });
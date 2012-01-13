f = {
    title : {
        type : "textfield",
        id : "title",
        label : "Title",
        help : "What would you like to call this object?",
        size : "xlarge",
        length : 20,
        validators : [go.not_empty]
    },
    description : {
        type : "textarea",
        id : "description",
        label : "Description",
        help : "Describe the object and how you intend it to be used.",
        size : "xlarge",
        rows : 3,
        validators : [go.not_empty]
    },
    width : {
        type : "textfield",
        id : "width",
        label : "Width",
        help : "Used mainly for layouting or basic collision detection.",
        size : "large",
        length : 20,
        validators : [go.not_empty, go.is_float]
    },
    height : {
        type : "textfield",
        id : "height",
        label : "Height",
        help : "Used mainly for layouting or basic collision detection.",
        size : "large",
        length : 20,
        validators : [go.not_empty, go.is_float]
    },
    weight : {
        type : "textfield",
        id : "weight",
        label : "Weight",
        help : "Can be used by the physics engine to calculate fall speed.",
        size : "large",
        length : 20,
        validators : [go.not_empty, go.is_float]
    },
    item_type : {
        type : "textfield",
        id : "item_type",
        label : "Item type",
        help : "What type of weapon? Bow? Gun? Sword?",
        size : "xlarge",
        length : 20,
        validators : []
    },
    item_class : {
        type : "textfield",
        id : "item_class",
        label : "Item class",
        help : "What class of weapon? Epic? Quest? Normal?",
        size : "xlarge",
        length : 20,
        validators : []
    },
    damage : {
        type : "textfield",
        id : "damage",
        label : "Damage",
        help : "Average weapon damage.",
        size : "large",
        length : 20,
        validators : []
    },
    armor : {
        type : "textfield",
        id : "armor",
        label : "Armor",
        help : "Armor value.",
        size : "large",
        length : 20,
        validators : []
    },
    item_value : {
        type : "textfield",
        id : "item_value",
        label : "Item value",
        help : "How much is this item worth?.",
        size : "large",
        length : 20,
        validators : []
    },
    enhancements : {
        type : "list",
        id : "enhancements",
        label : "Item enhancements and modifiers",
        help : "",
        category : "Modifier",
        validators : []
    },
    extra : {
        type : "textarea",
        id : "extra",
        label : "Extra information",
        help : "Describe other properties of this object. If this will be parsed, consider using json.",
        size : "xlarge",
        rows : 3,
        validators : []
    }
};

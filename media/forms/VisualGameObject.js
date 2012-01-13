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

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
    objective : {
        type : "textfield",
        id : "objective",
        label : "Objective",
        help : "",
        size : "large",
        length : 20,
        validators : []
    },
    targets : {
        type : "list",
        id : "targets",
        label : "Targets",
        help : "Whom to kill / talk to?.",
        category : "Character",
        validators : []
    },
    items : {
        type : "list",
        id : "items",
        label : "Items",
        help : "What to pick up?",
        category : "Equipment",
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

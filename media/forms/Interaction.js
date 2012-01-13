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
    trigger : {
        type : "choice",
        id : "trigger",
        label : "Trigger",
        help : "On what action will the modifier be activated/triggered?",
        choices : [ { title : "Enter", value : "enter" },
                    { title : "Leave", value : "leave" },
                    { title : "Activate", value : "activate"} ],
        validators : [go.not_empty]
    },
    action : {
        type : "textarea",
        id : "action",
        label : "Action",
        help : "An action can be anything but is usually a javascript function.",
        size : "xlarge",
        rows : 3,
        validators : [go.not_empty]
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

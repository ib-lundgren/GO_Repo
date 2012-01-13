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
    graphic : {
        type : "list",
        id : "graphic",
        label : "Graphic",
        help : "What this object looks like.",
        category : "Graphic",
        validators : []
    },
    skills : {
        type : "list",
        id : "skills",
        label : "Skills",
        help : "",
        category : "Skill",
        validators : []
    },
    attributes : {
        type : "list",
        id : "attributes",
        label : "Attributes",
        help : "",
        category : "Attribute",
        validators : []
    },
    equipment : {
        type : "list",
        id : "equipment",
        label : "Equipment",
        help : "",
        category : "Equipment",
        validators : []
    },
    missions : {
        type : "list",
        id : "missions",
        label : "Missions",
        help : "",
        category : "Mission",
        validators : []
    },
    teams : {
        type : "list",
        id : "teams",
        label : "Teams",
        help : "",
        category : "Team",
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

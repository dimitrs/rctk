Onion.widget.Control = function(jwin, parent, controlid) {
    this.cssclass = "control";
    this.jwin = jwin;
    this.controlid = controlid;
    this.parent = parent;
}

/* 
 * a control has been updated (changed) on the serverside,
 * this change needs to be reflected locally.
 * "sync" may be more consistent, controls on the serverside
 * implement a sync() method for changes from the clientside
 */
Onion.widget.Control.prototype.update = function(data) {
    if('state' in data) {
        if(data.state == 0) { // ENABLED
            this.control.removeAttr("disabled");
        }
        else if(data.state == 1) { // DISABLE
            this.control.attr("disabled", "disabled");
        }
    }
    if ('visible' in data) {
        if (data.visible) {
            this.control.show();
        } else {
            this.control.hide();
        }
    }
}

Onion.widget.Control.prototype.set_properties = function(data) {
    if(data === undefined) {
        return;
    }
    // handle base properties
    if('width' in data && data.width) {
        this.control.css("width", data.width + "px");
    }
    if('height' in data && data.height) {
        this.control.css("height", data.height + "px");
    }
    if('foreground' in data && data.foreground) {
        this.control.css("color", data.foreground);
    }
    if('background' in data && data.background) {
        this.control.css("background-color", data.background);
    }
}

Onion.widget.Control.prototype.create = function(data) {
    var controlid = "ctrl"+this.controlid;
    this.jwin.factory.append('<div id="' + controlid + '"></div>');
    this.control = $("#"+controlid);
    this.control.addClass(this.cssclass);
    this.set_properties(data);

}

Onion.widget.Control.prototype.destroy = function() {
    this.control.remove();
}

/*
 * A container is a control that can contain controls, i.e. a window,
 * a layout manager. Its control may be different from its container
 * (i.e. a window, which has outer divs as decoration)
 */
Onion.widget.Container = function(jwin, parent, controlid) {
    Onion.widget.Control.apply(this, arguments);
    // default layout manager
    this.layout = new Onion.layout.Power(this.jwin, this);
}

Onion.widget.Container.prototype = new Onion.widget.Control();

Onion.widget.Container.prototype.create = function(data) {
    Onion.widget.Control.prototype.create.apply(this, arguments);
    this.container = this.control;
}

Onion.widget.Container.prototype.append = function(control, data) {
    this.layout.append(control, data);
}

Onion.widget.Container.prototype.remove = function(control, data) {
    this.layout.remove(control, data);
}

Onion.widget.Container.prototype.setLayout = function(type, config) {
    // unimplemented options:
    // hgap, vgap, resize (default true)
    var layout_class = Onion.layout.map(type);
    if (layout_class) {
        this.layout = new layout_class(this.jwin, this, config);
        this.layout.create();
    }
}

Onion.widget.Container.prototype.relayout = function() {
    this.layout.layout();
    this.layout.layout_fase2();
    this.layout_updated();
}

Onion.widget.Container.prototype.layout_updated = function() {}


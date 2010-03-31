Onion.widget.RadioButton = function(jwin, parent, controlid) {
    Onion.widget.Control.apply(this, arguments);
}

Onion.widget.RadioButton.prototype = new Onion.widget.Control();

Onion.widget.RadioButton.prototype.create = function(data) {
    var controlid = "ctrl" + this.controlid;
    this.jwin.factory.append('<input type="radio" id="' + controlid + '"></input>')
    this.control = $("#" + controlid);
    this.control.attr('name', data.name);
    this.control.attr('value', data.value);
    this.control.attr('defaultChecked', data.defaultChecked);
    this.handle_click = false;
    
    var self=this;
    this.control.change( function() { self.changed(); self.jwin.flush() });
    this.set_properties(data);
}

Onion.widget.RadioButton.prototype.changed = function() {
    this.jwin.add_task("sync", "sync", this.controlid, {'checked':this.control.attr('checked') });

    if(this.handle_click) {
        this.jwin.add_task("event", "click", this.controlid);
    }
}

Onion.widget.RadioButton.prototype.update = function(data) {
    if(data.group) {
        this.control.attr('name', data.name);
    }
    if(data.value) {
        this.control.attr('value', data.value);
    }
    if(data.checked !== undefined) {
        this.control.attr('checked', data.checked);
    }
}

// register
Onion.widget.register("radiobutton", Onion.widget.RadioButton);

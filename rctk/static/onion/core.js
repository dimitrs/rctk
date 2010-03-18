
Onion.core.JWinClient = function() {
    this.loopinterval = 1000;

    var root = new Onion.widget.Root(this);
    root.create();

    this.controls = {0:root};
    // references to the actual div's
    this.root = $("#root");
    this.factory = $("#factory");
    this.toplevels = $("#toplevels");
    
}

Onion.core.JWinClient.prototype.sync = function(data) {
    $.ajax({
        type: "POST",
        url: "sync",
        data: data,
        success: function() {},
        dataTye: "json",
        async: false});
}

Onion.core.JWinClient.prototype.do_work = function(data) {
    Onion.util.log("do_work ", data);

    var control_map = {
        "panel": Onion.widget.Panel,
        "button": Onion.widget.Button,
        "text": Onion.widget.Text,
        "statictext": Onion.widget.StaticText,
        "window": Onion.widget.Frame,
        "checkbox": Onion.widget.CheckBox,
        "radiobutton": Onion.widget.RadioButton,
        "dropdown": Onion.widget.Dropdown,
        "list": Onion.widget.List,
        "date": Onion.widget.DateText,
        "password": Onion.widget.Password
    }
    var control_class = control_map[data.control];
    var parent = this.controls[data.parentid];
    var id = data.id;
                       
    switch(data.action) {
    case "append":
        var container = this.controls[data.id];
        var child = this.controls[data.child];

        container.append(child, data);
        break;
    case "show":
        // show all - hack!
        for(var i = 0; i < this.controls.length; i++) {
            this.controls[i].css("display", "inline");
        }
        break;
    case "create":
        if(control_class) {
           c = new control_class(this, parent, id);
           c.create(data);
           this.controls[id] = c;
        }
        break;
    case "update":
        // update a control. Rename to sync?
        var control = this.controls[id];
        control.update(data.update);
        break;
    case "handler":
        var control = this.controls[id];
        control["handle_"+data.type] = true;
        break;
    case "layout":
        var container = this.controls[id];
        container.setLayout(data.type, data.config);
        break;
    case "relayout":
        var container = this.controls[id];
        container.relayout();
        break;
    case "timer":
        Onion.util.log("Handling timer " + id + ", " + data.milliseconds);
        var callback = Onion.util.hitch(this, "handle_tasks");
        setTimeout(
          function() { 
             $.post("event", {"type":"timer", "id":id}, callback, "json")
           }, data.milliseconds);
        break;
    }

}

Onion.core.JWinClient.prototype.handle_tasks = function (data, status) {
    if(data) {
      for(var i=0; i < data.length; i++) {
        this.do_work(data[i]);
      }
    }
}

Onion.core.JWinClient.prototype.get_work = function() {
    $.post('pop', { 'key':'value' }, Onion.util.hitch(this, "handle_tasks"), "json");
}

Onion.core.JWinClient.prototype.start_work = function () {
    var self = this;
    var h = function(data, status)
        {
            data = data || "{}";
            if(data) {
            }
            //setInterval(Onion.util.hitch(self, 'get_work'), self.loopinterval);
            self.get_work();
        };
    $.post('start', {}, h, "json");
}

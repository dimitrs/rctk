from rctk.task import Task

class Event(object):
    def __init__(self, control, **kw):
        self.control = control
        self.args = kw

    @classmethod
    def invoke(cls, id, control, **kw):
        """ default is to map to a method equal to the eventid """
        handler = getattr(control, id, None)
        if handler:
            handler(cls(control, **kw))

class ClickEvent(Event):
    pass

class DoubleClickEvent(Event):
    pass

class ChangeEvent(Event):
    pass

class SubmitEvent(Event):
    pass

class KeypressEvent(Event):
    pass

class CloseEvent(Event):
    pass

class Clickable(object):
    _click_handler = None

    def _set_click(self, val):
        self._click_handler = val
        self.tk.queue(Task("Handler installed on %s %d" % (self.name, self.id),
          {'control':self.name, "id":self.id, "action":"handler", "type":"click"}))

    def _get_click(self):
        return self._click_handler

    click = property(_get_click, _set_click)    

class DoubleClickable(object):
    _doubleclick_handler = None

    def _set_doubleclick(self, val):
        self._doubleclick_handler = val
        self.tk.queue(Task("Handler installed on %s %d" % (self.name, self.id),
          {'control':self.name, "id":self.id, "action":"handler", "type":"doubleclick"}))

    def _get_doubleclick(self):
        return self._doubleclick_handler

    doubleclick = property(_get_doubleclick, _set_doubleclick)    

class Changable(object):
    _change_handler = None


    def _set_change(self, val):
        self._change_handler = val
        self.tk.queue(Task("Handler installed on %s %d" % (self.name, self.id),
          {'control':self.name, "id":self.id, "action":"handler", "type":"change"}))

    def _get_change(self):
        return self._change_handler

    change = property(_get_change, _set_change)

class Submittable(object):
    """ handler to catch explicit submit actions on controls. I.e.
        pressing enter on a Text input. This to avoid having to
        catch all keypresses """
    _submit_handler = None

    def _set_submit(self, val):
        self._submit_handler = val
        self.tk.queue(Task("Handler installed on %s %d" % (self.name, self.id),
          {'control':self.name, "id":self.id, "action":"handler", "type":"submit"}))

    def _get_submit(self):
        return self._submit_handler

    submit = property(_get_submit, _set_submit)

class Keypressable(object):
    _keypress_handler = None

    def _set_keypress(self, val):
        self._keypress_handler = val
        self.tk.queue(Task("KeypressHandler installed on %s %d" % (self.name, self.id),
          {'control':self.name, "id":self.id, "action":"handler", "type":"keypress"}))

    def _get_keypress(self):
        return self._keypress_handler

    keypress = property(_get_keypress, _set_keypress)

class Closable(object):
    _close_handler = None

    def _set_close(self, val):
        self._close_handler = val
        self.tk.queue(Task("CloseHandler installed on %s %d" % (self.name, self.id),
          {'control':self.name, "id":self.id, "action":"handler", "type":"close"}))

    def _get_close(self):
        return self._close_handler

    close = property(_get_close, _set_close)


class Dispatcher(object):
    events = {}

    def register(self, id, eventclass):
        self.events[id] = eventclass

    def __call__(self, id, control, **kw):
        """ 
            invoke an event. This may raise a keyerror for unregistered events 
        """
        self.events[id].invoke(id, control, **kw)

dispatcher = Dispatcher()

dispatcher.register('click', ClickEvent)
dispatcher.register('doubleclick', ClickEvent)
dispatcher.register('change', ChangeEvent)
dispatcher.register('submit', SubmitEvent)
dispatcher.register('keypress', KeypressEvent)
dispatcher.register('close', CloseEvent)

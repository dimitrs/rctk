from control import Control, remote_attribute

from rctk.task import Task
from rctk.event import Clickable

class Dropdown(Control, Clickable):
    """
        Display a dropdown containing values. The caller must supply
        items as tuples (key, label), label will be used for presentation,
        key can be used to identify the selection made. Keys can be any
        type of object.

        The dropdown widget will uniquely enumerate the options itself, it
        will not use the provided keys. 

        A Dropdown is clickable, the handler will receive the item selected
        in the eventobject as "key".

        TODO:
        - support multi-selection
        - support index for insertion
        - support removal of items
        - make the entire user-defined keystuff optional, provide a way to map
          the selection to the label (or just use label as key?)
    """
    name = "dropdown"

    selection = remote_attribute('selection', None)

    def __init__(self, tk, items=()):
        super(Dropdown, self).__init__(tk)
        self.indexer = 0

        self.items = []
        for (k, v) in items:
            self.items.append((self.indexer, (k, v)))
            self.indexer += 1

        if self.items:
            self._selection = 0
        else:
            self._selection = None

        self.create()

    def create(self):
        self.tk.queue(Task("Dropdown created id %d items '%s'" % (self.id, `self.items`),
         {'control':self.name, "id":self.id, "action":"create", "items":self._items()}))

    def add(self, key, value):
        """ this adds a new entry to the bottom. Removing items or selecting
            an insertion position is not yet possible """
        ## the first entry is the initial default. Check if this is the first entry
        if not self.items:
            self._selection = 0

        self.items.append((self.indexer, (key, value)))

        self.tk.queue(Task("Dropdown update id %d items '%s'" % 
          (self.id, `self.items`),
         {'control':self.name, "id":self.id, "action":"update", 
          "update":{"item":(self.indexer, value)}}))
        self.indexer += 1

    def sync(self, **data):
        if 'selection' in data:
            self._selection = int(data['selection'])

    def _items(self):
        return [(idx, label) for (idx, (k, label)) in self.items]

    def _get_value(self):
        for (idx, (key, value)) in self.items:
            if idx == self._selection:
                return key
        return None

    def _set_value(self, v):
        for (idx, (key, value)) in self.items:
            if v == key:
                self.selection = idx
                return
        raise KeyError, `search`

    value = property(_get_value, _set_value)

    def clear(self):
        self._items = []
        self._selection = None
        ## no strict need to reset indexer
        self.tk.queue(Task("Dropdown cleared id %d" % self.id,
         {'control':self.name, "id":self.id, "action":"update", 
          "update":{"clear":True}}))


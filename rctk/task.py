import copy

class Task(object):
    """ an item in the queue """
    def __init__(self, msg, task):
        self.msg = msg
        ##
        ## We need to deepcopy the taskdata to prevent it from changing
        ## after creating the task. I.e. if it contains a reference to
        ## some list.
        ## Consider for example the Dropdown control that passes self.items,
        ## which may get updated through a subsequent add()
        self._task = copy.deepcopy(task)

    def __eq__(self, other):
        return self.msg == other.msg and self._task == other._task

    def __str__(self):
        return "Task: %s" % self.msg

    def __repr__(self):
        return "<Task: %s>" % self.msg

    def task(self):
        return self._task

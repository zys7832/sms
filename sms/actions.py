#-*- encoding:utf8 -*-

class Action(object):
    def __init__(self,model):
        self.model = model
    pass

class AddAction(Action):
    pass

class EditAction(Action):
    pass

class DeleteAction(Action):
    pass

class ImportAction(Action):
    pass


class ExportAction(Action):
    pass

class PrintAction(Action):
    pass
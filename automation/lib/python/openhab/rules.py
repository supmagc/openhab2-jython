from java.util import UUID
from org.eclipse.smarthome.automation import Rule as SmarthomeRule

from openhab.log import logging, log_traceback, LOG_PREFIX

from openhab.jsr223 import scope, get_automation_manager
scope.scriptExtension.importPreset("RuleSimple")

def set_uid_prefix(rule, prefix=None):
    if prefix is None:
        prefix = type(rule).__name__
    uid_field = type(SmarthomeRule).getClass(SmarthomeRule).getDeclaredField(SmarthomeRule, "uid")
    uid_field.setAccessible(True)
    uid_field.set(rule, "{}-{}".format(prefix, str(UUID.randomUUID())))
    
def rule(clazz):
    def init(self, *args, **kwargs):
        scope.SimpleRule.__init__(self)
        set_uid_prefix(self)
        self.log = logging.getLogger(LOG_PREFIX + "." + clazz.__module__ + "." + clazz.__name__)
        self.events = scope.events
        clazz.__init__(self, *args, **kwargs)
        if self.description is None and clazz.__doc__:
            self.description = clazz.__doc__
        if hasattr(self, "getEventTriggers"):
            self.triggers = log_traceback(self.getEventTriggers)()
        elif hasattr(self, "getEventTrigger"):
            # For OH1 compatibility
            self.triggers = log_traceback(self.getEventTrigger)()
        addRule(self)
    subclass = type(clazz.__name__, (clazz, scope.SimpleRule), dict(__init__=init))
    subclass.execute = log_traceback(clazz.execute)
    return subclass

def addRule(rule):
    get_automation_manager().addRule(rule)

@rule
class BaseRule:

    def __init__(self):
        self.log = None
        self.events = None

    def sendCommand(self, item, *args):
        if (isinstance(item, str)):
            item = scope.itemRegistry.get(item)
        
        self.events.sendCommand(item, *args)

    def postUpdate(self, item, *args):
        if (isinstance(item, str)):
            item = scope.itemRegistry.get(item)
        
        self.events.postUpdate(item, *args)

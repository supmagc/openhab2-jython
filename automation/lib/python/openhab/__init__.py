from openhab.jsr223.scope import items, events, itemRegistry, things as thingRegistry, rules as ruleRegistry
from org.eclipse.smarthome.core.library.types import OnOffType, IncreaseDecreaseType, OpenClosedType, StopMoveType, RewindFastforwardType, NextPreviousType, PlayPauseType, UpDownType

#
# Add an attribute-resolver to the items map
#

def _item_getattr(self, name):
    return self[name]

type(items).__getattr__ = _item_getattr.__get__(items, type(items))

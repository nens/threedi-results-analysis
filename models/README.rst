Models: wrappers around QT tables
=================================

Mostly wrappers around QT's table/row/column stuff. Reinout thinks it all
looks pretty tricky. It isn' clear whether all functionality is really used or
not. It tries to make everything "more pythonic".

Also some signals are added so that changes can be reacted upon.

A starting point is :py:class:`.base.BaseModel`.

In :py:mod:`.base_fields`, wrappers for individual fields try to transparently
convert booleans/checkboxes and color fields between QT values and python
datatypes.

#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Base Module
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2014/09/23
:Status: This is a "work in progress"
:Revision: 0.1.0
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""


class Base:
    """Crafty base operations.  :ref:`base`

    :param w: The width of crafty window
    :param h: The height of crafty window
    :param stage: An element to which this window will be attached
    :returns: An instance of Crafty
    """
    def __init__(self, crafty):
        """Crafty game engine constructor.

        :param crafty: An element to which this window will be attached
        :returns: An instance of Crafty
        """
        self.__crafty = crafty
        #crafty.attr(self=self)

    def attr(self, **kwarg):
        """Set attributes.  :mod:`crafty.entity`

        :param: kwargs: keyword parameters with name and values of arguments to be changed
        :returns: Self, this same entity
        """
        #print(kwarg)
        self.__elt.attr(dict(**kwarg))
        return self

    def background(self, color):
        """Change background color. :class:`crafty.base.Base`

        :param color: A string with components ex:'2D, DOM, Color'
        :returns: This instance of Crafty
        """
        self.__crafty.background(color)
        return self

    @property
    def x(self):
        """The x position on the stage. :class:`crafty.base.Base`

        """
        return self.__crafty.x

    @property
    def y(self):
        """The y position on the stage. :class:`crafty.base.Base`

        """
        return self.__crafty.y

    @property
    def mousePos(self):
        """Mouse Position. :class:`crafty.base.Base`

        """
        return self.__crafty.mousePos

    @property
    def keys(self):
        """Keycodes. :class:`crafty.base.Base`

        exemple keys.RA keys.LA keys.UA keys. DA

        """
        return self.__crafty.keys

    def isDown(self, keyName):
        """Determine if a certain key is currently down. :class:`crafty.base.Base`

        **Example**

        .. code-block:: python

            entity.requires('Keyboard').bind('KeyDown', haldle_keydown)

        Determine if a certain key is currently down.
        :param keyName: Name or Code of the key to check. See Crafty.keys.
        :returns: If the key is Down.
        """
        return self.__crafty.isDown(keyName)

    def crafty(self):
        """Crafty js core. :class:`crafty.base.Base`

        :returns: A javascript crafty instance
        """
        return self.__crafty

    def text(self, texty):
        """Crafty Text. :class:`crafty.base.Base`

        String of text that will be inserted into the DOM or Canvas element.

        This method will update the text inside the entity.

        If you need to reference attributes on the entity itself you can pass a function instead of a string.
        Example

        Crafty.e("2D, DOM, Text").attr({ x: 100, y: 100 }).text("Look at me!!");

        Crafty.e("2D, DOM, Text").attr({ x: 100, y: 100 })
            .text(function () { return "My position is " + this._x });

        Crafty.e("2D, Canvas, Text").attr({ x: 100, y: 100 }).text("Look at me!!");

        Crafty.e("2D, Canvas, Text").attr({ x: 100, y: 100 })
            .text(function () { return "My position is " + this._x });

        :param text: Name of the event to bind to
        :returns: Load a crafty scene
        """
        print('Crafty Text. Text')
        self.__crafty.requires('Text')
        self.__crafty.text(texty)
        return self

    def bind(self, eventName, callback):
        """Crafty Bind. :class:`crafty.base.Base`

        Binds to a global event. Method will be executed when Crafty.trigger is used with the event name.

        :param eventName: Name of the event to bind to
        :param callback: Method to execute upon event triggered
        :returns: callback function which can be used for unbind
        """
        return self.__crafty.bind(eventName, callback)

    def onebind(self, eventName, callback):
        """Crafty OneBind. :class:`crafty.core.BCrafty`

        Binds to a global event. Method will be executed once when Crafty.trigger is used with the event name.

        :param eventName: Name of the event to bind to
        :param callback: Method to execute upon event triggered
        :returns: callback function which can be used for unbind
        """
        return self.__crafty.one(eventName, callback)

    def unbind(self, eventName, callback):
        """Crafty unbind. :class:`crafty.core.BCrafty`

        Binds to a global event. Method will be executed once when Crafty.trigger is used with the event name.

        :param eventName: Name of the event to unbind to
        :param callback: Method to unbind
        :returns: True or false depending on if a callback was unbound
        """
        return self.__crafty.unbind(eventName, callback)

    def destroy(self):
        """Destroy the Entity. :class:`crafty.core.BCrafty`
        Will remove all event listeners and delete all properties as well as removing from the stage

        :returns: The object destroyied
        """
        return self.__crafty.destroy()

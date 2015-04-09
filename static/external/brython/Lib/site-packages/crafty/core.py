#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Core Module
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2014/09/17
:Status: This is a "work in progress"
:Revision: 0.1.0
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""
from .graphics import Sprite
from .base import Base
try:
    from browser import document, window
    from javascript import JSObject, JSConstructor
    from .jscrafty import JSCrafty
    from __random import randint
except ImportError as ie:
    try:
        from unittest.mock import MagicMock
    except ImportError as iem:
        from mock import MagicMock
    window = JSObject = JSConstructor = JSCrafty = randint = MagicMock()

    class document:
        body = "Document Body"

#from .utils import create_script_tag
'''
crafty = JSObject(Crafty)

version = "1.0"
print(crafty.getVersion())
#create_script_tag("https://rawgithub.com/craftyjs/Crafty/release/dist/crafty-min.js")
'''


class BCrafty(Base):
    """Crafty game engine main class.  :ref:`crafty`

    :param w: The width of crafty window
    :param h: The height of crafty window
    :param stage: An element to which this window will be attached
    :returns: An instance of Crafty
    """
    def __init__(self, w=600, h=480, stage=document.body):
        """Crafty game engine constructor.

        :param w, h: The width and height of crafty window
        :param stage: An element to which this window will be attached
        :returns: An instance of Crafty
        """
        self.__crafty = JSObject(JSCrafty)
        self.__crafty.init(w, h, stage)
        Base.__init__(self, self.__crafty)

    def e(self, comp='2D, DOM, Color'):
        """Entity. :class:`crafty.core.BCrafty`

        :param comp: A string with components ex:'2D, DOM, Color'
        :returns: An Entity instance
        """
        from .entity import Entity
        return Entity(self.__crafty, comp)

    @property
    def crafty(self):
        """Crafty js core. :class:`crafty.core.BCrafty`

        :returns: A javascript crafty instance
        """
        return self.__crafty

    def canvas(self):
        """create a drawing canvas. :class:`crafty.core.BCrafty`

        :returns: A javascript crafty instance
        """
        return JSObject(JSCrafty.canvas)  # self.__crafty

    def scene(self, scene, init=None, uninit=lambda: None):
        """Crafty Scene. :class:`crafty.core.BCrafty`

        :returns: A crafty scene
        """
        if not init:
            return self.__crafty.enterScene(scene, 0)
        return self.__crafty.scene(scene, init, uninit)

    def load(self, name, init):
        """Crafty Load. :class:`crafty.core.BCrafty`

        :returns: Load a crafty scene
        """
        return self.__crafty.load(name, init)

    def randRange(self, mini, maxi):
        """Random Range. :class:`crafty.core.BCrafty`

        :returns: a number ranging from mini to maxi
        """
        return randint(mini, maxi)

    def sprites(self, tile, url, **mapper):
        """Collection of sprites. :class:`crafty.core.BCrafty`

        :param tile: Tile size of the sprite map, defaults to 1
        :param url: URL of the sprite image
        :param map: Object where the key is what becomes a new component
         and the value points to a position on the sprite map
        :param paddingX: Horizontal space in between tiles. Defaults to 0.
        :param paddingY: Vertical space in between tiles. Defaults to paddingX.
        :param paddingAroundBorder: If padding should be applied around the border of the sprite sheet.
         If enabled the first tile starts at (paddingX,paddingY) instead of (0,0). Defaults to false.        """
        return self.__crafty.sprite(tile, url, dict(**mapper))

    def sprite(self, x, y, w, h):
        """Create a Sprite. :class:`crafty.core.BCrafty`

        :param x: position x of sprite
        :param y: position y of sprite
        :param w: width w of sprite
        :param h: height h of sprite
        :returns: An instance of Sprite
        """
        return Sprite(self.__crafty).sprite(x, y, w, h)

    def c(self, name, *comp, **items):
        """Creates a component naming the ID and passing an object. :class:`crafty.core.BCrafty`

        A couple of methods are treated specially.
        They are invoked in partiular contexts, and (in those contexts) cannot be overridden by other components.
        init will be called when the component is added to an entity
        remove will be called just before a component is removed, or before an entity is destroyed.
        It is passed a single boolean parameter that is true if the entity is being destroyed.

        :param name: Name of the component
        :param comp: Object with the component's properties and methods that will be inherited by entities.
        :param items: If component is not provided each keyword argument will be attached as a member of component.
        """
        comp = {str(k): getattr(comp[0], k) for k in dir(comp[0]) if '__' not in k} if comp else dict(**items)
        return self.__crafty.c(name, comp)

#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Entity Module
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
from .graphics import Draggable
from .graphics import Sprite
from .base import Base


class Entity(Sprite, Draggable, Base):
    """Creates an entity.  :ref:`entity`

    Any arguments will be applied in the same way .addComponent()
    is applied as a quick way to add components.

    Any component added will augment the functionality of the created entity by
    assigning the properties and methods from the component to the entity.

    :param: stage: Element to which entity will be attached to
    :param: cmp: Componente name
    :returns: An instance of Entity
    """
    def __init__(self, stage, cmp):
        self.__elt = stage.e(cmp)
        self.__stage = stage
        #super(self, Sprite, self.__elt)
        Sprite.__init__(self, self.__elt)
        Base.__init__(self, self.__elt)

    def attach(self, entity):
        """Attach an entity to this one.  :mod:`crafty.entity`

        :param: entity: The entity to be attached
        :returns: Self, this same entity
        """
        self.__elt.attach(entity.entity)
        return self

    def color(self, col):
        """Creates an entity.  :mod:`crafty.entity`

        :param: col: new color of the entity
        :returns: Self, this same entity
        """
        self.__elt.color(col)
        return self

    def fourway(self, speed):
        """Creates an four way entity control.  :mod:`crafty.entity`

        :param: speed: the speed of movement
        :returns: Self, this same entity
        """
        self.__elt.requires('Fourway')
        self.__elt.fourway(speed)
        return self

    def multiway(self, speed, **directions):
        """Creates an four way entity control.  :mod:`crafty.entity`

        :param: speed: the speed of movement
        :param: directions: named directions and degree (UP_ARROW: -90, DOWN_ARROW: 90, RIGHT_ARROW: 0, LEFT_ARROW: 180)
        :returns: Self, this same entity
        """
        self.__elt.requires('Multiway')
        self.__elt.multiway(speed, dict(**directions))
        return self

    def gravity(self, entity):
        """Creates gravity to entity.  :mod:`crafty.entity`

        :param: entity: entity to gravitate to
        :returns: Self, this same entity
        """
        self.__elt.requires('Gravity')
        self.__elt.gravity(entity)
        return self

    @property
    def rotation(self):
        """Rotate entity.  :mod:`crafty.entity`

        :returns: Ammount of rotation
        """
        self.__elt.requires('2D')
        return self.__elt.rotation

    @rotation.setter
    def rotation(self, value):
        """Rotate entity.  :mod:`crafty.entity`

        :param: value: Ammount of rotation
        """
        self.__elt.requires('2D')
        self.__elt.rotation = value

    def origin(self, value):
        """Set rotation origin for entity.  :mod:`crafty.entity`

        :param: value: lef, top, right, bottom, center, middle
        :returns: Self, this same entity
        """
        self.__elt.requires('2D')
        self.__elt.origin(value)
        return self

    def _reel(self, reelId, duration, fromX, fromY, frameCount):
        """Create animation reel.

        :param: reelId: String name for this reel
        :param: duration: Duration time in miliseconds for this reel
        :param: fromX: reelId, Duration duration, Number fromX, Number fromY, Number frameCount
        :param: fromY: reelId, Duration duration, Number fromX, Number fromY, Number frameCount
        :param: frameCount: reelId, Duration duration, Number fromX, Number fromY, Number frameCount
        :returns: Self, this same entity
        """
        self.__elt.requires('SpriteAnimation')
        self.__elt.reel(reelId,  duration, fromX, fromY, frameCount)
        return self

    @property
    def visible(self):
        return None

    @visible.setter
    def visible(self, set_visibility):
        """Change Entity Visibility.

        :param set_visibility: String reel identification
        """
        self.__elt.visible = set_visibility

    @property
    def entity(self):
        """Entity property.

        """
        return self.__elt

    @entity.setter
    def entity(self, _):
        """Entity property is read only.

        :param _: Ignored
        """
        pass

    def hit(self, component):
        """Takes an argument for a component to test collision for.  :mod:`crafty.entity`

        If a collision is found, an array of every object in collision along with the amount of overlap is passed.

        If no collision, will return false. The return collision data will be an Array of Objects
        with the type of collision used, the object collided and if the type used was
        SAT (a polygon was used as the hitbox) then an amount of overlap.

        .. code:: python

            [{
               obj: [entity],
               type: "MBR" or "SAT",
               overlap: [number]
            }]

        MBR is your standard axis aligned rectangle intersection (.intersect in the 2D component).
        SAT is collision between any convex polygon.

        :param: component: Check collision with entities that has this component
        :returns: False if no collision. If a collision is detected, returns an Array of objects that are colliding.
        """
        self.__elt.requires('Collision')
        return self.__elt.hit(component)

    def collision(self, *points):
        """Constructor takes a polygon or array of points to use as the hit area.  :mod:`crafty.entity`

        The hit area (polygon) must be a convex shape and not concave for the collision detection to work.

        Points are relative to the object's position and its unrotated state.

        If no parameter is passed, the x, y, w, h properties of the entity will be used,
        and the hitbox will be resized when the entity is.

        If a hitbox is set that is outside of the bounds of the entity itself,
        there will be a small performance penalty as it is tracked separately.

        **Example**
        ..code:: python

            Crafty().e("2D, Collision").collision([50,0], [100,100], [0,100])

        **Events**

        NewHitbox [Data: Crafty.polygon]
            when a new hitbox is assigned

        :param: *points: Array with an x and y position to generate a polygon
        :returns: Self, this same entity
        """
        self.__elt.requires('Collision')
        self.__elt.collision(list(*points))
        return self

    def onHit(self, component, hit, nohit=lambda ev=0: None):
        """Creates an EnterFrame event calling .hit() each frame.  :mod:`crafty.entity`

        When a collision is detected the callback will be invoked.

        :param: hit: Callback method to execute upon collision with component.
            Will be passed the results of the collision check in the same format documented for hit().
        :param: nohit: Callback method executed once as soon as collision stops.
        :returns: Self, this same entity
        """
        self.__elt.requires('Collision')
        self.__elt.onHit(component, hit, nohit)
        return self

    def init(self):
        """Create a rectangle polygon based on the x, y, w, h dimensions.  :mod:`crafty.entity`

        By default, the collision hitbox will match the dimensions (x, y, w, h) and rotation of the object.

        :returns: Self, this same entity
        """
        self.__elt.requires('Collision')
        self.__elt.init()
        return self

    def image(self, url, repeat=""):
        """Create a rectangle polygon based on the x, y, w, h dimensions.  :mod:`crafty.entity`

        Draw specified image. Repeat follows CSS syntax ("no-repeat", "repeat", "repeat-x", "repeat-y");

        Note: Default repeat is no-repeat which is different to standard DOM (which is repeat)

        If the width and height are 0 and repeat is set to no-repeat the width and height will automatically assume that of the image. This is an easy way to create an image without needing sprites.
        **Example**

        Will default to no-repeat. Entity width and height will be set to the images width and height

        ..code:: python

            ent = Crafty().e("2D, DOM, Image").image("myimage.png")

        Create a repeating background.

        ..code:: python

            bg = Crafty().e("2D, DOM, Image")
                         .attr(w= Crafty.viewport.width, h= Crafty.viewport.height)
                         .image("bg.png", "repeat");

        **Events**

        Invalidate
            when the image is loaded

        :param: url: URL of the image.
        :param: repeat: If the image should be repeated to fill the entity.
        :returns: Self, this same entity
        """
        self.__elt.requires('Image')
        self.__elt.image(url, repeat)
        return self

    def tint(self, color, strength):
        """Similar to Color by adding an overlay of semi-transparent color.  :mod:`crafty.entity`

        Modify the color and level opacity to give a tint on the entity.

        **Example**

        ..code:: python

            Crafty().e("2D, Canvas, Tint").tint("#969696", 0.3)

        **Events**

        Invalidate
            when the tint is applied

        :param: color: The color in hexadecimal.
        :param: strength: Level of opacity.
        :returns: Self, this same entity
        """
        self.__elt.requires('Tint')
        self.__elt.tint(color, strength)
        return self


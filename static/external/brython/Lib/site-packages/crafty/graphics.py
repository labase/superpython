#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Graphic handling classes
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


class Canvas:
    """Canvas.  :ref:`canvas`

    When this component is added to an entity it will be drawn to the global canvas element.
    The canvas element (and hence all Canvas entities) is always rendered below any DOM entities.

    Crafty.canvas.init() will be automatically called if it is not called already to initialize the canvas element.
    """
    def __init__(self, stage, cmp):
        self.__stage = stage
        self.__elt = stage.e(cmp)

    def draw(self, ctx, x,  y,  w,  h):
        """ draw([[Context ctx, ]Number x, Number y, Number w, Number h]).

        """
        #print(kwarg)
        self.__elt.draw(ctx, x,  y,  w,  h)
        return self  # .__elt  # .attr(dict(**kwarg)).fourway(4)


class Sprite:
    """Sprite.  :ref:`sprite`

    Component for using tiles in a sprite map.
    """
    def __init__(self, ent):  # , x, y, w, h):
        self.__ent = ent

    def sprite(self, x, y, w, h):
        self.__ent.requires('Sprite')
        self.__ent.sprite(x, y, w, h)
        return self

    @property
    def coord(self):
        """The coordinate of the slide within the sprite in the format of [x, y, w, h].

        """
        return self.__ent.__coord

    def crop(self,  x, y, w, h):
        """Crop the sprite.

        If the entity needs to be smaller than the tile size, use this method to crop it.

        The values should be in pixels rather than tiles.

        :param x: Offset x position
        :param y: Offset y position
        :param w: New width
        :param h: New height
        :returns: Self, this same entity
        """
        self.__ent.requires('Sprite')
        self.__ent.crop(reelId,  x, y, w, h)
        return self

    def reel(self, reelId, duration, fromX, fromY, frameCount):
        """Create animation reel.

        :param: String reelId, Duration duration, Number fromX, Number fromY, Number frameCount
        :returns: Self, this same entity
        """
        self.__ent.requires('SpriteAnimation')
        self.__ent.reel(reelId,  duration, fromX, fromY, frameCount)
        return self

    def animate(self, reelId=None, loopCount=1):
        """Animate Entity.

        :param reelId: String reel identification
        :param loopCount:  Integer number of loops, default 1, indefinite if -1
        :returns: Self, this same entity
        """
        self.__ent.requires('SpriteAnimation')
        if reelId:
            self.__ent.animate(reelId,  loopCount)
        else:
            self.__ent.animate(loopCount)
        return self

    def isPlaying(self, reelId=''):
        """Return is the reel is playing.

        :param reelId: The reelId of the reel we wish to examine, if missing default to current reel
        :returns: The current animation state
        """
        self.__ent.requires('SpriteAnimation')
        if reelId:
            return self.__ent.isPlaying(reelId)
        else:
            return self.__ent.isPlaying()

    def resumeAnimation(self):
        """This will resume animation of the current reel from its current state.

         If a reel is already playing, or there is no current reel, there will be no effect.
        """
        self.__ent.resumeAnimation()

    def pauseAnimation(self):
        """Pauses the currently playing animation, or does nothing if no animation is playing.

        """
        self.__ent.pauseAnimation()

    def resetAnimation(self):
        """Resets the current animation to its initial state.

        Resets the number of loops to the last specified value, which defaults to 1.

        Neither pauses nor resumes the current animation.
        """
        self.__ent.resetAnimation()

    def loops(self, loopCount=None):
        """Set or return the number of loops.

        Sets the number of times the animation will loop for.
        If called while an animation is in progress, the current state will be considered the first loop.

        :param loopCount: The number of times to play the animation, if missig retun loops left.
        :returns: The number of loops left. Returns 0 if no reel is active.
        """
        if loopCount is None:
            return self.__ent.loops(loopCount)
        else:
            return self.__ent.loops()

    def reelPosition(self, position=None):
        """Sets the position of the current reel by frame number.

        :param position: The frame to jump to. This is zero-indexed.
            A negative values counts back from the last frame.
            Sets the position of the current reel by percent progress if number is float.
            Jumps to the specified position if string.
            The only currently accepted value is "end", which will jump to the end of the reel.

        :returns: The current frame number
        """
        if position is None:
            return self.__ent.reelPosition(position)
        else:
            return self.__ent.reelPosition()

    def tween(self, duration, **properties):
        """This method will animate numeric properties over the specified duration.

        These include x, y, w, h, alpha and rotation in degrees.

        :param properties: Object of numeric properties and what they should animate to
        :param duration: Duration to animate the properties over, in milliseconds.
        :returns: The current frame number
        """
        self.__ent.requires('Tween')
        self.__ent.tween(dict(**properties), duration)


class Draggable:
    """Enable drag and drop of the entity.  :ref:`draggable`

    """
    def __init__(self, ent):
        self.__ent = ent

    def dragDirection(self, degrees=None, x=None, y=None):
        """Specify the dragging direction.

        if no parameters are given, remove dragging.

        :param degrees: A number, the degree (clockwise) of the move direction with respect to the x axis.
        :param x: the vector (valx, valy) denotes the move direction.
        :param y: the vector (valx, valy) denotes the move direction.
        """
        if not degrees is None:
            self.__ent.dragDirection(degrees)
        elif not x is None:
            self.__ent.dragDirection(dict(x=x, y=y))
        else:
            self.__ent.dragDirection()

    def startDrag(self):
        """Make the entity follow the mouse positions.

        """
        self.__ent.startDrag()

    def stopDrag(self):
        """Stop the entity from dragging. Essentially reproducing the drop.

        """
        self.__ent.stopDrag()

    def enableDrag(self):
        """Rebind the mouse events. Use if .disableDrag has been called.

        """
        self.__ent.enableDrag()

    def disableDrag(self):
        """Stops entity from being draggable. Reenable with .enableDrag().

        """
        self.__ent.disableDrag()
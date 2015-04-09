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


class Extra:
    """Crafty base operations.  :ref:`base`

    """
    def __init__(self, crafty):
        """Extra Crafty functions.

        :param crafty: An element to which this window will be attached
        :returns: An instance of Crafty Extra
        """
        self.__crafty = crafty

    def uniqueBind(self, eventName,  callback):
        """Works like Crafty.bind, but prevents a callback from being bound multiple times.

        :param eventname: Name of the event to bind to
        :param callback: Method to execute upon event triggered
        :returns: callback function which can be used for unbind
        """
        return self.__crafty.uniqueBind(eventName,  callback)
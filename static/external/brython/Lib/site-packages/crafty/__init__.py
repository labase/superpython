#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Brython Crafty - INIT
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2014/09/17
:Status: This is a "work in progress"
:Revision: 0.2.3
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

.. _mod_crafty

"""
__version__ = "0.2.3"
#from .utils import create_script_tag
from browser import document
import urllib.request


def create_script_tag(src):
    _fp, _, _ = urllib.request.urlopen(src)
    _data = _fp.read()

    _tag = document.createElement('script')
    _tag.type = "text/javascript"
    _tag.text = _data
    #_tag.src=src
    document.get(tag='head')[0].appendChild(_tag)
    
create_script_tag('/js/crafty-min.js')

from .core import BCrafty


class Crafty(BCrafty):
    """Crafty game engine main class.  :ref:`crafty`

    """
    pass
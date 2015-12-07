#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa SuperPython
# Copyright 2013-2015 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
#
# SuperPython é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>

import lib.bottle as bottle
from lib.bottle import request
import os
import types
from ..models import code_store as cs
import collections
Item = collections.namedtuple('Item', 'name picture x y ox oy')
Par = collections.namedtuple('Par', 'x y')
PROJECTS = "jardim spy super surdo mgeo cups hero".split()

IPOS = [Par(96, -1), Par(249, -22), Par(393, -23), Par(555, -4),
        Par(45, 104), Par(205, 110), Par(432, 107), Par(600, 108),
        Par(78, 218), Par(214, 251), Par(320, 180), Par(431, 252), Par(564, 218),
        Par(127, 329), Par(212, 401), Par(320, 330), Par(432, 398), Par(528, 327),
        Par(79, 434), Par(207, 542), Par(430, 542), Par(564, 429),
        Par(43, 548), Par(320, 470), Par(600, 528),
        Par(96, 644), Par(249, 664), Par(393, 664), Par(555, 644)]
BPOS = [Par(-(dx*160), -(dy*120)) for dy in range(6) for dx in range(5)]

STEPX = 921 / 6
STEPY = 521 / 5
DX, DY = (300, 300)
# BRYTHON = "/external/brython/brython.js"
# BRYTHON = "https://dl.dropboxusercontent.com/u/1751704/lib/Brython3.2.3/brython.js"
BRYTHON = "https://dl.dropboxusercontent.com/u/1751704/lib/brython/brython.js"
# BRYTHON = "http://www.brython.info/src/brython.js"
# import sys
# project_server = '/'.join(os.getcwd().split('/')[:-1])
project_server = os.getcwd()
# make sure the default templates directory is known to Bottle
templates_dir = os.path.join(project_server, 'src/server/views/')
# print(templates_dir)
print("ctlinit ", project_server, templates_dir)
if templates_dir not in bottle.TEMPLATE_PATH:
    bottle.TEMPLATE_PATH.insert(0, templates_dir)

project = ""


def get_project(func, **kw):
    def decorator():
        _project = request.query.proj
        print("get_project", _project)
        if not _project or _project not in PROJECTS:
            _project = request.urlparts.hostname.split('.')
            if _project and (_project[0] in PROJECTS):
                _project = _project[0]
            elif request.get_cookie('_spy_project_') in PROJECTS:
                _project = request.get_cookie('_spy_project_')
            else:
                _project = "superpython"

        my_globals = {}
        my_globals.update(globals())
        my_globals['project'] = _project
        call_fn = types.FunctionType(func.func_code, my_globals)
        return call_fn()
    return decorator


def project_visual_data(project):
    """ Return User Selection at application root URL"""
    def gxy(project_name):
        index = person_sprite.index(project_name)
        return Par(-STEPX * (index % 6), -STEPY * (index//6))
    print("""project_visual_data""", project)
    persons, person_sprite = cs.DB.getlogged(project)
    pic_size = len(persons)
    sorted_persons = sorted(persons.keys())
    tops = [Item(name, persons[name], x, y, 0, 0) for name, (x, y) in zip(sorted_persons[:pic_size], IPOS)]
    items = [Item(name, persons[name], x, y, gxy(name).x, gxy(name).y)
             for name, (x, y) in zip(sorted_persons[:pic_size], IPOS)]
    print("home: persons, tops, items", persons, tops)
    print("home: items", items)
    return tops, items

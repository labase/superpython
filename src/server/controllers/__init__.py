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
from lib.bottle import Bottle, view, request, response, redirect
import os
import types
from ..models import code_store as cs
import collections
Item = collections.namedtuple('Item', 'name picture x y ox oy')
Par = collections.namedtuple('Par', 'x y')
PROJECTS = "jardim spy super surdo mgeo".split()
PICTURE = "https://dl.dropboxusercontent.com/u/1751704/igames/img/igeo/calcedonia1.png"
PROJECTS = "jardim spy super surdo mgeo".split()
IPOS = [Par(100, -5), Par(260, -19), Par(400, -19), Par(550, 0),
        Par(60, 108), Par(220, 108), Par(440, 108), Par(600, 108),
        Par(90, 219), Par(210, 249), Par(440, 249), Par(570, 219),
        Par(90, 319), Par(210, 349), Par(440, 349), Par(570, 319),
        Par(90, 419), Par(210, 449), Par(440, 449), Par(570, 419)]
BPOS = [Par(-(dx*160), -(dy*120)) for dy in range(6) for dx in range(5)]
NAMES = "granito _ _ _ _ arenito" \
        " calcita_laranja agua_marinha amazonita _ quartzo_rosa turmalina" \
        " citrino pirita silex ametista cristal quartzo-verde" \
        " _ _ fluorita _ _ onix" \
        " feldspato _ jaspe agata sodalita alabastro".split()
ONAME = "granito arenito" \
        " calcita_laranja agua_marinha amazonita quartzo_rosa turmalina" \
        " citrino pirita silex ametista cristal quartzo-verde" \
        " fluorita onix" \
        " feldspato jaspe agata sodalita alabastro".split()
STEPX = 921 / 6
STEPY = 521 / 5
# import sys
# project_server = '/'.join(os.getcwd().split('/')[:-1])
project_server = os.getcwd()
# make sure the default templates directory is known to Bottle
templates_dir = os.path.join(project_server, 'src/server/views/')
# print(templates_dir)
if templates_dir not in bottle.TEMPLATE_PATH:
    bottle.TEMPLATE_PATH.insert(0, templates_dir)

project = ""


def get_project(func):
    def decorator():
        _project = request.urlparts.hostname.split('.')
        if _project and (_project[0] in PROJECTS):
            _project = _project[0]
        elif request.get_cookie('_spy_project_'):
            _project = request.get_cookie('_spy_project_')
        else:
            _project = "superpython"

        my_globals = {}
        my_globals.update(globals())
        my_globals['project'] = _project
        call_fn = types.FunctionType(func.func_code, my_globals)
        return call_fn()
    return decorator

@get_project
def project_visual_data():
    """ Return User Selection at application root URL"""
    def gxy(project_name):
        index = NAMES.index(project_name)
        return Par(-STEPX * (index % 6), -STEPY * (index//6))
    persons = cs.DB.getlogged(project)
    sorted_persons = ONAME  # sorted(persons.keys())
    tops = [Item(name, persons[name], x, y, 0, 0) for name, (x, y) in zip(sorted_persons[:20], IPOS)]
    items = [Item(name, persons[name], x, y, gxy(name).x, gxy(name).y)
             for name, (x, y) in zip(sorted_persons[:20], IPOS)]
    print("home: persons, tops, items", persons, tops)
    print("home: items", items)
    return tops, items

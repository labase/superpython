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

"""Controller handles routes starting with /RESOURCE_NAME.

Change this file's name and contents as appropriate to the
resources your app exposes to clients.

"""
__author__ = 'carlo'
from lib.bottle import Bottle, view, request, response, redirect
# from ..models.code_store import DB
from ..models import code_store as cs
import collections

Item = collections.namedtuple('Item', 'name picture x y ox oy')
Par = collections.namedtuple('Par', 'x y')
# PICTURE = "http://www.floresjardim.com/imagens/bd/rosaazul.jpg"
PICTURE = "https://dl.dropboxusercontent.com/u/1751704/igames/img/igeo/calcedonia1.png"
PROJECTS = "jardim spy super geo".split()
IPOS = [Par(100, -5), Par(260, -19), Par(400, -19), Par(550, 0),
        Par(60, 108), Par(220, 108), Par(440, 108), Par(600, 108),
        Par(90, 219), Par(210, 249), Par(440, 249), Par(570, 219)]
BPOS = [Par(-(dx*160), -(dy*120)) for dy in range(6) for dx in range(5)]
NAMES = "granito _ _ _ _ arenito" \
        " calcita_laranja agua_marinha amazonita _ quartzo_rosa turmalina" \
        " citrino pirita silex ametista cristal quartzo-verde" \
        " _ _ fluorita _ _ onix" \
        " feldspato _ jaspe agata sodalita alabastro".split()
# NAMES = NAMES+NAMES
ONAME = "granito arenito" \
        " calcita_laranja agua_marinha amazonita quartzo_rosa turmalina" \
        " citrino pirita silex ametista cristal quartzo-verde" \
        " fluorita onix" \
        " feldspato jaspe agata sodalita alabastro".split()
STEPX = 921 / 6
STEPY = 521 / 5

bottle = Bottle()  # create another WSGI application for this controller and resource.
# debug(True) #  uncomment for verbose error logging. Do not use in production


@bottle.get('/')
@view('index')
def home():
    """ Return User Selection at application root URL"""
    def gxy(name):
        index = NAMES.index(name)
        return Par(-STEPX * (index % 6), -STEPY * (index//6))
    project = request.urlparts.hostname.split('.')
    project = project if project and (project[0] in PROJECTS) else "superpython"
    persons = cs.DB.getlogged(project)
    sorted_persons = ONAME  # sorted(persons.keys())
    tops = [Item(name, persons[name], x, y, 0, 0) for name, (x, y) in zip(sorted_persons[:12], IPOS)]
    items = [Item(name, persons[name], x, y, gxy(name).x, gxy(name).y)
             for name, (x, y) in zip(sorted_persons[:12], IPOS)]
    print("home: persons, tops, items", persons, tops)
    print("home: items", items)
    return dict(user="fake: %s" % project, result=items, selector=tops)  # IPOS[:2])


@bottle.post('/editor')
@view('projeto')
def edit():
    """ Return Project editor"""
    project = request.urlparts.hostname.split('.')
    project = project if project and (project[0] in PROJECTS) else "superpython"
    person = request.forms.get('module')
    if cs.DB.islogged(project, person):
        redirect("/main")
    # DB._populate_person(project, "", ["projeto%d" % d for d in range(30)])
    cursession, lastsession = cs.DB.login(project, person)
    lastcodename, lastcodetext = cs.DB.lastcode(lastsession)
    response.set_cookie('_spy_project_', project, cursession.name)
    cs.DB.logout(project, person)  # XXXXXXXXXXXXXX REMOVE
    return dict(projeto=person, codename=lastcodename, codetext=lastcodetext)


@bottle.post('/save')
def save():
    """ Save given file into datastore"""
    project = request.urlparts.hostname.split('.')
    project = project if project and (project[0] in PROJECTS) else "superpython"
    cookie = request.get_cookie('_spy_project_')
    codej = request.json
    codedict = {str(k): str(v) for k, v in codej.items()}
    print("code", codej["name"], project, cookie, codej, codedict)
    cs.DB.save(**codedict)
    return "file saved"


@bottle.post('/logout')
def logout():
    """ Logout from session"""
    project = request.urlparts.hostname.split('.')
    project = project if project and (project[0] in PROJECTS) else "superpython"
    # cookie = request.get_cookie('_spy_project_')
    person = request.forms.get('person')
    cs.DB.logout(project, person)
    return "logout"

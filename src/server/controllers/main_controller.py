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
from . import project, get_project, project_visual_data

bottle = Bottle()  # create another WSGI application for this controller and resource.
# debug(True) #  uncomment for verbose error logging. Do not use in production


@bottle.get('/')
@view('index')
@get_project
def home():
    """ Return User Selection at application root URL"""
    # prj = request.query.proj
    print("home project", project)
    tops, items = project_visual_data()
    return dict(user=project, result=items, selector=tops)  # IPOS[:2])


@bottle.post('/editor')
@view('projeto')
@get_project
def edit():
    """ Return Project editor"""
    person = request.forms.get('module')
    # if cs.DB.islogged(project, person):
    #     redirect("/main")
    cursession, lastsession = cs.DB.login(project, person)
    lastcodename, lastcodetext = cs.DB.lastcode(lastsession)
    print(""" Return Project editor""", lastcodetext)
    response.set_cookie('_spy_project_', project)  # , secret=cursession.name)
    # cs.DB.logout(project, person)  # XXXXXXXXXXXXXX REMOVE
    return dict(projeto=person, codename=lastcodename, codetext=lastcodetext)


@bottle.post('/save')
@get_project
def save():
    """ Save given file into datastore"""
    codej = request.json
    codedict = {str(k): unicode(v) for k, v in codej.items()}
    print("code", codej["name"], project, codej, codedict)
    cs.DB.save(**codedict)
    return "file saved"


@bottle.post('/logout')
@get_project
def logout():
    """ Logout from session"""
    person = request.forms.get('person')
    cs.DB.logout(project, person)
    return "logout"

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
from lib.bottle import Bottle, view, request, response, redirect, HTTPError
import lib.bottle as bt
# from ..models.code_store import DB
from ..models import code_store as cs
from . import project, get_project, project_visual_data, BRYTHON

bottle = Bottle()  # create another WSGI application for this controller and resource.
# debug(True) #  uncomment for verbose error logging. Do not use in production


@bottle.get('/')
@view('index')
@get_project
def home():
    """ Return User Selection at application root URL"""
    module = request.query.module
    module = "NOT FOUND: %s" % module.upper() if module else None
    print("home project", project)
    tops, items = project_visual_data()
    return dict(project=project, result=items, selector=tops, brython=BRYTHON, fault=module)


@bottle.post('/editor')
@view('projeto')
def edit():
    """ Return Project editor"""
    module = request.forms.get('module')
    code = request.forms.get('code')
    project = request.forms.get('project')
    # if cs.DB.islogged(project, person):
    #     redirect("/main")
    print ("Return Project editor", project, module)
    if not cs.DB.ismember(project, module):
        bt.redirect("/main?proj=%s&module=%s" % (project, ".".join([module, code])))

    cursession, lastsession = cs.DB.login(project, module)
    lastcodename, lastcodetext = cs.DB.lastcode(lastsession)
    lastcodename = '/'.join([module, code]) if code else lastcodename
    # print(""" Return Project editor""", lastcodetext)
    # response.set_cookie('_spy_project_', project)  # , secret=cursession.name)
    # cs.DB.logout(project, person)  # XXXXXXXXXXXXXX REMOVE
    return dict(projeto=module, codename=lastcodename, brython=BRYTHON)


@bottle.get('/load')
@get_project
def load():
    """ Return Project Module"""
    module = request.query.module
    code = cs.DB.load(module)
    print(""" Return Project Module""", module)
    return code


@bottle.post('/save')
@get_project
def save():
    """ Save given file into datastore"""
    codej = request.json
    codedict = {str(k): unicode(v) for k, v in codej.items()}
    print("code", codej["name"], project, codej, codedict)
    cs.DB.save(**codedict)
    return codej["name"]


@bottle.post('/logout')
@get_project
def logout():
    """ Logout from session"""
    person = request.forms.get('person')
    cs.DB.logout(project, person)
    return "logout"

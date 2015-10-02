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

"""
############################################################
SuperPython - Controlador Principal
############################################################

Controlador principal da funcionalidade do servidor web.

"""
__author__ = 'carlo'
from bottle import Bottle, view, request
from ..models import code_store as cs
from . import project, get_project, BRYTHON

bottle = Bottle()  # create another WSGI application for this controller and resource.
# debug(True) #  uncomment for verbose error logging. Do not use in production



@bottle.post('/editor')
@view('projeto')
@get_project
def edit():
    """ Return Project editor.
    """
    person = request.forms.get('module')
    cursession, lastsession = cs.DB.login(project, person)
    lastcodename, lastcodetext = cs.DB.lastcode(lastsession)
    print(""" Return Project editor""", lastcodetext)
    return dict(projeto=person, codename=lastcodename, brython=BRYTHON)


@bottle.get('/load')
@get_project
def load():
    """ Return Project Module.
    """
    module = request.query.module
    code = cs.DB.load(module)
    print(""" Return Project Module""", module)
    return code


@bottle.post('/save')
@get_project
def save():
    """ Save given file into datastore.
    """
    codej = request.json
    codedict = {str(k): unicode(v) for k, v in codej.items()}
    print("code", codej["name"], project, codej, codedict)
    cs.DB.save(**codedict)
    return codej["name"]


@bottle.post('/logout')
@get_project
def logout():
    """ Logout from session.
    """
    person = request.forms.get('person')
    cs.DB.logout(project, person)
    return "logout"

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

"""Controller handles routes for in project imports.

"""
__author__ = 'carlo'
from bottle import Bottle, HTTPError, request, view, TEMPLATE_PATH
from ..models import code_store as cs
from . import BRYTHON
import os
import bottle
appbottle = Bottle()  # create another WSGI application for this controller and resource.
# debug(True) #  uncomment for verbose error logging. Do not use in production
project_server = os.getcwd()
# make sure the default templates directory is known to Bottle
templates_dir = os.path.join(project_server, 'src/server/views/')
# print(templates_dir)
print("ctlinit ", project_server, templates_dir)
if templates_dir not in bottle.TEMPLATE_PATH:
    bottle.TEMPLATE_PATH.insert(0, templates_dir)


@appbottle.post('/<proj>/<pak>/___init___.py')
@view('projeto')
def edit(proj, pak):
    """ Return Project editor"""
    module = request.forms.get('module')
    code = request.forms.get('code')
    project = request.forms.get('project')
    print ("Return Project editor", project, module)
    if not cs.DB.ismember(project, module):
        bt.redirect("/main?proj=%s&module=%s" % (project, ".".join([module, code])))

    cursession, lastsession = cs.DB.login(project, module)
    lastcodename, lastcodetext = cs.DB.lastcode(lastsession)
    lastcodename = '/'.join([module, code]) if code else lastcodename
    print(""" Return Project editor""", lastcodename, TEMPLATE_PATH)
    return dict(projeto=module, codename=lastcodename, brython=BRYTHON)



@appbottle.get('/<proj>/<pak>/<mod>/<pypath:path>')
def handle(proj, pak, mod, pypath):
    project = proj
    module = '/'.join([mod, pypath])
    code = cs.DB.load(name=module)
    if code:
        return code
    if "__init__" in pypath:
        print('/<pypath:path__init__, module, project, cs.DB.ismember>', module, project, cs.DB.ismember(project, mod))
        if cs.DB.ismember(project, mod):
            return "#"

    raise HTTPError(404, "No such module.")

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
from bottle import Bottle, HTTPError, request
from ..models import code_store as cs

bottle = Bottle()  # create another WSGI application for this controller and resource.
# debug(True) #  uncomment for verbose error logging. Do not use in production


@bottle.get('/<pypath:path>')
def handle(pypath):
    project = request.get_cookie('_spy_project_')
    code = cs.DB.load(name=pypath)
    print('/<pypath:path>', pypath, project, code)
    if code:
        return code
    if "__init__" in pypath:
        module = pypath.split("/")
        print('/<pypath:path__init__, pypath, module, project>', pypath, module, project)
        module = module[0] if len(module) >= 2 else None
        print('/<pypath:path__init__, module, project, cs.DB.ismember>', module, project, cs.DB.ismember(project, module))
        if cs.DB.ismember(project, module):
            return "#"

    raise HTTPError(404, "No such module.")

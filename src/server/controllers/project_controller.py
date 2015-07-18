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

"""Controller handles routes starting with /project.

"""
__author__ = 'carlo'
from lib.bottle import Bottle, HTTPError, view, request, response
from ..models import code_store as cs

bottle = Bottle()  # create another WSGI application for this controller and resource.
# debug(True) #  uncomment for verbose error logging. Do not use in production


@bottle.get('/<pypath:path>')
def handle(pypath):
    # project = request.get_cookie('_spy_project_')
    print('/<pypath:path>', pypath)
    code = cs.DB.load(name=pypath)
    if code:
        return code
    '''
    if "project" in pypath:
        if "__init__" in pypath:
            return "\n"
        if "project/carlo" in pypath:
            return "main = 142857"
            '''

    raise HTTPError(404, "No such board.")

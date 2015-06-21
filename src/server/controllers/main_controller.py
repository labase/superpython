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
from lib.bottle import Bottle, view, request, response
import collections

Item = collections.namedtuple('Item', 'name picture')
PICTURE = "http://www.floresjardim.com/imagens/bd/rosaazul.jpg"
PROJECTS = "jardim spy super geo".split()

bottle = Bottle()  # create another WSGI application for this controller and resource.
# debug(True) #  uncomment for verbose error logging. Do not use in production


@bottle.get('/')
@view('index')
def home():
    """ Return Hello World at application root URL"""
    project = request.urlparts.geturl().split('/')[2].split('.')[0]
    if project in PROJECTS:
            response.set_cookie('_spy_project_', project)

    #  items = [[Item(name='projeto %d' % (a*4+b), picture=PICTURE) for a in range(4)] for b in range(4)]
    items = [Item(name='projeto %d' % (a*4+b), picture=PICTURE) for a in range(4) for b in range(4)]
    return dict(user="fake: %s" % project, result=items)

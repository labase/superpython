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


"""Main.py is the top level script.

Loads the Bottle framework and mounts controllers.  Also adds a custom error
handler.
"""
from lib import bottle
from lib.bottle import Bottle, redirect
# name and list your controllers here so their routes become accessible.
from server.controllers import main_controller, project_controller, code_controller
# Enable debugging, which gives us tracebacks
bottle.DEBUG = True

# Run the Bottle wsgi application. We don't need to call run() since our
# application is embedded within an App Engine WSGI application server.
appbottle = Bottle()

# Mount a new instance of bottle for each controller and URL prefix.
# bottle.mount("/pontos", main_controller.bottle)
appbottle.mount("/external", project_controller.bottle)

# Mount a new instance of bottle for each controller and URL prefix.
appbottle.mount("/main", main_controller.bottle)
appbottle.mount("/code", code_controller.bottle)
# bottle.mount("/pontos", pontos_controller.bottle)


@bottle.get('/')
def home():
    """ Return Hello World at application root URL"""
    redirect('/main')


@bottle.error(404)
def error_404(_):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'

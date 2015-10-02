#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Carinhas
# Copyright 2013-2014 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
#
# Carinhas é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser  útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
#  a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, escreva para a Fundação do Software
# Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
############################################################
SuperPython - Teste de Funcionalidade Web
############################################################

Verifica a funcionalidade do servidor web.

"""
__author__ = 'carlo'
import unittest
import sys

import bottle
import os
# import sys
# project_server = '/'.join(os.getcwd().split('/')[:-1])
project_server = os.getcwd()
# make sure the default templates directory is known to Bottle
templates_dir = os.path.join(project_server, '../src/server/views/')
# print(templates_dir)
if templates_dir not in bottle.TEMPLATE_PATH:
    bottle.TEMPLATE_PATH.insert(0, templates_dir)
if sys.version_info[0] == 2:
    from mock import MagicMock, patch
else:
    from unittest.mock import MagicMock, patch, ANY
from webtest import TestApp
from server.controllers import appbottle
from server.models import code_store as cs

class SpyWebTest(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock(name="db")
        modules = {
            'src.server.models.code_store': self.db,
            'src.server.models.code_store.DB': self.db
        }
        self.module_patcher = patch.dict('sys.modules', modules)
        self.module_patcher.start()
        cs.DB = MagicMock(name="sdb")
        pass

    def test_default_page(self):
        app = TestApp(appbottle)
        cs.DB.getlogged = MagicMock(name="dbl")
        cs.DB.getlogged.side_effect = lambda *a, **args: (dict(jaspe=False), ["jaspe"])
        response = app.get('/')
        self.assertEqual('200 OK', response.status)
        self.assertTrue('<title>SuperPython</title>' in response.text, response.text[:1000])

    def test_editor(self):
        app = TestApp(appbottle)
        session = MagicMock(name="dblc")
        session.name = '2222'
        cs.DB.login = MagicMock(name="dbl")
        cs.DB.login.side_effect = lambda *a, **args: (session, 1)
        cs.DB.islogged = MagicMock(name="dblg")
        cs.DB.islogged.side_effect = lambda *a, **args: False
        cs.DB.lastcode = MagicMock(name="dblc")
        cs.DB.lastcode.side_effect = lambda *a, **args: 'lastcodename lastcodetext'.split()
        response = app.post('/main/editor', dict(module="projeto2222"))
        self.assertEqual('200 OK', response.status)
        self.assertTrue('projeto2222-lastcodename' in response, str(response))

    def test_save(self):
        app = TestApp(appbottle)
        session = MagicMock(name="dblc")
        session.name = '2222'
        cs.DB.login = MagicMock(name="dbl")
        cs.DB.login.side_effect = lambda *a, **args: (session, 1)
        cs.DB.save = MagicMock(name="dblc")
        cs.DB.save.side_effect = lambda *a, **args: 'lastcodename lastcodetext'.split()
        response = app.post_json('/main/save', dict(person="projeto0", name="main", text="# main"))
        cs.DB.save.assert_called_once_with(text=u'# main', name=u'main', person=u'projeto0')
        self.assertEqual('200 OK', response.status)
        self.assertTrue('main' in response.text, response.text)

    def test_import(self):
        app = TestApp(appbottle)
        session = MagicMock(name="dblc")
        session.name = '2222'
        cs.DB.load = MagicMock(name="dbl")
        cs.DB.load.side_effect = lambda *a, **args: "#main"
        response = app.get('/main/superpython/core.py')
        cs.DB.load.assert_called_once_with(name='core.py')
        self.assertEqual('200 OK', response.status)
        self.assertTrue('#main' in response)

    def test_logout(self):
        app = TestApp(appbottle)
        session = MagicMock(name="dblc")
        session.name = '2222'
        cs.DB.logout = MagicMock(name="dbl")
        # cs.DB.load.side_effect = lambda *a, **args: "#main"
        response = app.post('/main/logout', dict(person="projeto2222"))
        cs.DB.logout.assert_called_once_with('superpython', 'projeto2222')
        self.assertEqual('200 OK', response.status)
        self.assertTrue('logout' in response)

if __name__ == '__main__':
    unittest.main()

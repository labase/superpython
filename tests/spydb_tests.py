#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Superpython
# Copyright 2013-2014 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
#
# Superpython é um software livre; você pode redistribuí-lo e/ou
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
SuperPython - Teste de Base de dados
############################################################

Verifica a funcionalidade do serviço de armazenamento.

"""
__author__ = 'carlo'
import unittest
import sys

if sys.version_info[0] == 2:
    from mock import MagicMock, patch, ANY
else:
    from unittest.mock import MagicMock, patch, ANY

import server.models.database as dbs

class SpyDBTest(unittest.TestCase):

    def setUp(self):
        self.ndb = dbs.NDB  # = MagicMock(name="db")
        from server.models.code_store import DB
        self.db = DB
        pass

    def test_default_page(self):
        self.db.login("a", "b")
        pass
    """

    def test_editor(self):
        modules = {
            'lib.minimock.Mock': self.ndb
        }
        self.module_patcher = patch.dict('sys.modules', modules)
        self.module_patcher.start()
        app = TestApp(appbottle)
        session = MagicMock(name="dblc")
        session.name = '2222'
        cs.DB.login = MagicMock(name="dbl")
        cs.DB.login.side_effect = lambda *a, **args: (session, 1)
        cs.DB.lastcode = MagicMock(name="dblc")
        cs.DB.lastcode.side_effect = lambda *a, **args: 'lastcodename lastcodetext'.split()
        response = app.post('/main/editor', dict(module="2222"))
        self.assertEqual('200 OK', response.status)
        self.assertTrue('projeto2222-lastcodename' in response)

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
        self.assertTrue('file saved' in response)
    """

if __name__ == '__main__':
    unittest.main()

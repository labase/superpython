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
SuperPython - Teste
############################################################

Verifica a funcionalidade do cliente web.

"""
import unittest
from client.superpython.core import SuperPython
from client.superpython import main
import sys
if sys.version_info[0] == 2:
    from mock import MagicMock, patch, ANY
else:
    from unittest.mock import MagicMock, patch, ANY


class SuperPythonTest(unittest.TestCase):

    def setUp(self):
        self.gui = MagicMock()
        self.app = SuperPython(self.gui, self.gui, self.gui)

    def test_main(self):
        """garante que intância de SuperPython é criada."""
        sp = main(self.gui, self.gui, self.gui)
        assert sp is not None


if __name__ == '__main__':
    unittest.main()
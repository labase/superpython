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
SuperPython - Pacote Principal
############################################################

Define a classe SuperPython.

"""
import traceback
GUI = None


class SuperPython:
    """Classe que define o ambiente de desenvolvimento

    :param browser: Referência ao módulo navegador do Brython
    """

    def __init__(self, browser, canvas, edit):
        """Constroi os objetos iniciais. """
        global GUI
        self.canvas, self.edit = canvas, edit
        self.gui = GUI = browser
        self.svg = browser.svg
        self.html = browser.html
        self.ajax = browser.ajax
        self.svgcanvas = self.cursor = self.icon = self.menu = self.back = self.div = None
        self.load = self.save = lambda ev: None
        self.dim = (800, 600)
        self._tabcount = 0
        # self._editors = []
        self._editors = None
        self._pyconsole = self.html.DIV()
        self._editordiv = self.html.DIV(id="%s", Class="editclass", style={"width": "100%%", "height": "100%%"})

    def main(self):
        self.add_editor()

    def add_editor(self, filename=None):
        if filename is None:
            filename = "Untitled-%s" % self._tabcount
            self._tabcount += 1
        # add ace editor to filename pre tag
        _editor = self.edit.edit(filename)
        self._editordiv <= _editor
        _session = _editor.getSession()
        _session.setMode("ace/mode/python")
        # _editor.setTheme("ace/theme/crimson_editor")
        # _session.setMode("ace/mode/python")
        # _session.setUseWrapMode(true)
        # _session.setTabSize(4)
        _editor.setOptions({
            'enableLiveAutocompletion': True,
            'enableSnippets': True,
            'highlightActiveLine': False,
            'highlightSelectedWord': True
        })
        _editor.focus()

        self._editors[filename] = _editor
        # set resize
        # document[filename].bind('resize', lambda x: self._editors[filename].resize(True))

    """# region Description
    import sys
    import json
    import urllib.request
    import time

    #this import causes loading to slow down.  See email
    # to Pierre on Dec 4th, 2014 for details..
    #import urllib.parse

    import editor
    editors=editor.Editor('editortabs')

    sys.path.append('libs/FileSystem')
    import FileObject

    _jquery=JSObject(window.jQuery)
    display_message=JSObject(window.display_message)

    sharelist={}
    # endregion
    """

    def run(self):
        # find selected Tab (and get its contents)
        self._pyconsole.value = ''
        src = self._editors.getCurrentText()
        # t0 = time.perf_counter()
        try:
            exec(src, globals())
            state = 1
        except Exception as _:
            traceback.print_exc()
            state = 0

        # print('<completed in %6.2f ms>' % ((time.perf_counter()-t0)*1000.0))
        return state

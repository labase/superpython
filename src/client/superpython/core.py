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
import traceback, sys
GUI = None


class SuperPython:
    """Classe que define o ambiente de desenvolvimento

    :param browser: Referência ao módulo navegador do Brython
    """

    def __init__(self, browser, edit, project):
        """Constroi os objetos iniciais. """
        global GUI
        self.edit, self.project = edit, project
        self.gui = GUI = browser
        self.canvas = browser.doc["edit"]
        self.container = browser.doc["main"]

        def _canvasresize(_=0):
            _height = self.gui.doc.documentElement.clientHeight
            self.canvas.style.height = '%spx' % int(_height * 0.90)
            self.gui.doc["console"].style.top = _height * 0.90
            _width = self.gui.doc.documentElement.clientWidth
            _swidth = min(_width, 1000)
            self.canvas.style.width = '%spx' % int(_swidth)
            self.container.style.width = '%spx' % int(_swidth)

        self.svg = browser.svg
        self.html = browser.html
        # self.ajax = browser.ajax
        self.svgcanvas = self.cursor = self.icon = self.menu = self.back = self.div = None
        self.load = self.save = lambda ev: None
        self.dim = (800, 600)
        self._tabcount = 0
        self._editors = {}
        self._pyconsole = browser.doc["pyconsole"]
        self._editordiv = self.html.DIV()

        self.canvas.html = '<div id="%s" class="editclass" style="width: 100%%; height: 100%%">ola</div>' % project
        self.gui.window.addEventListener('resize', _canvasresize, True)
        #self.gui.doc["run"].addEventListener('click', lambda x=0: self.write(x)) #self.run, True)
        self.gui.doc["run"].onclick = self.run
        _canvasresize()

    def main(self):
        # self.canvas <= self._editordiv
        print(self.canvas, self._editordiv)
        self.add_editor()
        return
        sys.stdout.write = self.write
        sys.stderr.write = self.write

    def write(self, data):
        self._pyconsole.value += '%s' % data

    def add_editor(self, filename=None):
        if filename is None:
            filename = "Untitled-%s" % self._tabcount
            self._tabcount += 1
        # add ace editor to filename pre tag
        _editor = self.edit.edit(self.project)
        _session = _editor.getSession()
        _session.setMode("ace/mode/python")
        #return
        #_editor.setTheme("ace/theme/cobalt")
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

        self._editors[self.project] = _editor
        # set resize
        self.gui.doc[self.project].bind('resize', lambda x: self._editors[self.project].resize(True))

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

    def run(self, _=0):
        # find selected Tab (and get its contents)
        print(self._pyconsole.value, self.project, self._editors)
        self._pyconsole.value = ''
        src = self._editors[self.project].getValue()  # .getCurrentText()
        print(src)
        # t0 = time.perf_counter()
        try:
            exec(src, globals())
            state = 1
        except Exception as _:
            traceback.print_exc()
            state = 0

        # print('<completed in %6.2f ms>' % ((time.perf_counter()-t0)*1000.0))
        return state

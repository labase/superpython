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
SuperPython - Pacote Cliente
############################################################

Adiciona um editor Ace, dois botões e dois consoles do programa.

"""
import traceback
import sys
import json
import collections
Dims = collections.namedtuple('Dims', 'x y w h')
GUI = None


class Ace:

    def __init__(self, browser, edit, project, code):
        """Constroi os objetos iniciais. """

        def _ace_editor_resize(_=0):
            _height = self.gui.doc.documentElement.clientHeight
            self._ace_editor.style.height = '%spx' % int(_height* 0.98)  # * 0.90)
            self._ace_editor.style.marginBottom = '2px'
            _width = self.gui.doc.documentElement.clientWidth
            _swidth = _width-100  # min(_width + 100, 1000)
            self._ace_editor.style.width = '%spx' % int(_swidth)
            self._container.style.width = '%spx' % int(_swidth)
        self.gui = browser
        self._ace_editor = browser.doc["edit"]
        self._container = browser.doc["main"]
        self._editors = {}
        self.edit, self.project = edit, project
        self.unescape = browser.unescape

        self.gui.window.addEventListener('resize', _ace_editor_resize, True)
        _ace_editor_resize()
        self.add_editor(self.unescape(code))

    def get_content(self):
        return self._editors[self.project].getValue()

    def add_editor(self, code=None):
        # add ace editor to filename pre tag
        _editor = self.edit.edit(self.project)
        _session = _editor.getSession()
        _session.setMode("ace/mode/python")
        _editor.setValue(code)

        _editor.setTheme("ace/theme/cobalt")
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
        # return
        self._editors[self.project] = _editor
        # set resize
        self._ace_editor.bind('resize', lambda x: self._editors[self.project].resize(True))


class Console:
    """Classe que define o console de resposta da execução

    :param browser: Referência ao módulo navegador do Brython
    :param ace: Referência ao módulo editor Ace
    """

    def __init__(self, browser, ace):
        """Constroi os objetos iniciais. """
        self.jq_canvas = self.jq_console = None
        self.jq_canvas_data = self.jq_console_data = None
        self._pyconsole = browser.doc["pyconsole"]
        self._pycanvas = browser.doc["pydiv"]
        self._run_or_code = self.run
        self.ace = ace
        self.jq = browser.jq
        browser.doc["run"].onclick = self.run
        self._owrite = sys.stdout.write
        self._ewrite = sys.stderr.write
        sys.stdout.write = self.write
        sys.stderr.write = self.write
        self._pycanvas.html = '<img id="emmenu"' \
                              ' src="https://dl.dropboxusercontent.com/u/1751704/img/site_em_construcao_.jpg"' \
                              ' alt="menu" title="menu" width="400px"/>'

    def write(self, data):
        self._pyconsole.value += '%s' % data

    def display_canvas(self, run_or_code, display="block"):
        def console_resize(*_):
            self.jq_console_data = Dims(
                int(self.jq_console.offset().left), int(self.jq_console.offset().top),
                self.jq_console.outerWidth(), self.jq_console.outerHeight())
            self.jq_canvas_data = Dims(
                int(self.jq_canvas.offset().left), int(self.jq_canvas.offset().top),
                self.jq_canvas.outerWidth(), self.jq_canvas.outerHeight())
        self._run_or_code = run_or_code
        self._pyconsole.style.display = display
        if self.jq_canvas_data:
            cs = self.jq_canvas_data
            self.jq_canvas = self.jq['pydiv'].dialog(
                dict(position=[cs.x, cs.y],
                     width=cs.w, height=cs.h), show=dict(effect="fade", duration=800),
                resizeStop=console_resize, dragStop=console_resize)
        else:
            self.jq_canvas = self.jq['pydiv'].dialog(
                dict(position=dict(my="right top", at="left bottom", of="#control"),
                     width="60%", height=400), show=dict(effect="fade", duration=800),
                resizeStop=console_resize, dragStop=console_resize)
        if self.jq_console_data:
            cs = self.jq_console_data
            self.jq_console = self.jq['console'].dialog(
                dict(position=[cs.x, cs.y], title="console",
                     width=cs.w, height=cs.h), show=dict(effect="fade", duration=800),
                resizeStop=console_resize, dragStop=console_resize)
        else:
            self.jq_console = self.jq['console'].dialog(
                dict(position=dict(my="right bottom", at="right bottom", of="#edit"), title="console",
                     width="60%", height=200), show=dict(effect="fade", duration=800),
                resizeStop=console_resize, dragStop=console_resize)

    def run(self, _=0):
        self._pyconsole.value = ''
        src = self.ace.get_content()  # .getCurrentText()
        self.display_canvas(self._code, "block")
        # print("self._run", src)
        try:
            self.display_canvas(self._code, "block")
            exec(src, globals())
            state = 1
        except Exception as _:
            self._run_or_code = self.run
            self._pycanvas.style.display = "none"
            traceback.print_exc()
            state = 0
        return state

    def _code(self, _=0):
        self._run_or_code = self.run
        self._pycanvas.style.display = "none"

    def runcode(self, _=0):
        # print("self._run_or_code")
        self._run_or_code()


class SuperPython:
    """Classe que define o ambiente de desenvolvimento

    :param browser: Referência ao módulo navegador do Brython
    """

    def __init__(self, browser, edit, project):
        """Constroi os objetos iniciais. """
        self.edit, self.project = edit, project
        self.gui = browser
        browser.window.addEventListener("beforeunload", self.logout_on_exit)
        self.ajax = browser.ajax
        self.ace = self.name = self._console = None
        browser.doc["menu"].onclick = self.save

    def logout_on_exit(self, ev):
        ev.returnValue = "SAIR?"
        try:
            data = {"person": self.project}

            req = self.ajax.ajax()
            req.open('POST', "logout")  # , async=False)
            req.set_header('content-type', 'application/x-www-form-urlencoded')
            req.send(data)
            print("logout", data)
        except Exception as _:
            print("logout request error")
        return "SAIR?"

    def main(self, name="", code=""):
        self.name = name
        self.ace = Ace(self.gui, self.edit, self.project, code)
        self._console = Console(self.gui, self.ace)

    def save(self, _=0):
        src = self.ace.get_content()  # .getCurrentText()
        # t0 = time.perf_counter()
        try:
            jsrc = json.dumps({"person": self.project, "name": self.name, "text": src})

            req = self.ajax.ajax()
            req.open('POST', "save")  # , async=False)
            req.set_header('content-type', 'application/json')  # x-www-form-urlencoded')
            req.send(jsrc)

            state = 1
            # print("save", jsrc)
        except Exception as _:
            state = 0

        # print('<completed in %6.2f ms>' % ((time.perf_counter()-t0)*1000.0))
        return state

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
    """ Inclui uma janela com um editor Acejs.

    :param browser: Brythom module browser
    :param edit: Referência ao módulo editor Ace
    :param project: Projeto que o usuário está desenvolvendo
    :param code: Texto do código a ser adicionado no editor
    """

    def __init__(self, browser, edit, project, code):
        """Constroi os objetos iniciais. """

        def _ace_editor_resize(_=0):
            _height = self.gui.doc.documentElement.clientHeight
            self._ace_editor.style.height = '%spx' % int(_height*0.98)  # * 0.90)
            self._ace_editor.style.marginBottom = '2px'
            # _width = self.gui.doc.documentElement.clientWidth
            self._container.style.width = '98\%'  # %spx' % int(_swidth)
            self._container.style.maxWidth = '1000px'  # %spx' % int(_swidth)
            self._ace_editor.style.width = '98\%'  # %spx' % int(_swidth)
            self._ace_editor.style.maxWidth = '1000px'  # %spx' % int(_swidth)
        self.gui = browser
        self._ace_editor = browser.doc["edit"]
        self._container = browser.doc["main"]
        self._editors = {}
        self.edit, self.project = edit, project
        # self.unescape = browser.unescape

        self.gui.window.addEventListener('resize', _ace_editor_resize, True)
        _ace_editor_resize()
        self._code = code
        self.add_editor(self._code[:])

    def annotate(self, row=1, message="indefinido"):
        self._editors[self.project].session.clearAnnotations()
        if not row:
            return None
        return self._editors[self.project].session.setAnnotations(
            [dict(row=row, column=0, text=message, type="error")])

    def get_content(self):
        return self._editors[self.project].getValue()

    def set_content(self, code):
        return self._editors[self.project].setValue(code)

    def test_dirty(self, _, code_saved=False):
        """ Confere e testa o estado de edição para detectar modificações.

        :returns Se o código foi modificado desde a última vez que foi salvo.
        """
        src = self.get_content()
        dirty = src != self._code
        if code_saved:
            self._code = src[:]
        return dirty and src

    def add_editor(self, code=None):
        # add ace editor to filename pre tag
        _editor = self.edit.edit(self.project)
        _session = _editor.getSession()
        _session.setMode("ace/mode/python")
        _editor.setValue(code)
        # _session.on('change', self.test_dirty)

        _editor.setTheme("ace/theme/cobalt")
        # _session.setMode("ace/mode/python")
        # _session.setUseWrapMode(true)
        # _session.setTabSize(4)
        _editor.setOptions({
            'enableLiveAutocompletion': True,
            'enableSnippets': True,
            'highlightActiveLine': False,
            'displayIndentGuides': True,
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
        self.jq_canvas = self.jq_console = self.jq_msg = None
        self.jq_canvas_data = self.jq_console_data = None
        self._pyconsole = browser.doc["pyconsole"]
        self._pycanvas = browser.doc["pydiv"]
        self._pymessage = browser.doc["pymessage"]
        self.ace = ace
        self.jq = browser.jq
        # browser.doc["run"].onclick = self.run
        self._owrite = sys.stdout.write
        self._ewrite = sys.stderr.write
        sys.stdout.write = self.write
        sys.stderr.write = self.write
        self._pycanvas.html = '<img id="emmenu"' \
                              ' src="https://dl.dropboxusercontent.com/u/1751704/img/site_em_construcao_.jpg"' \
                              ' alt="menu" title="menu" width="400px"/>'

    def write(self, data):
        self._pyconsole.value += '%s' % data

    def display_saved(self, message="SAVED"):
        self.jq_msg = self.jq['message'].dialog(
            dict(position=dict(my="left bottom", at="left bottom", of="#edit"),
                 width=250, height=40, dialogClass="no-titlebar"), show=dict(effect="fade", duration=800),
            hide=dict(effect="fade", duration=1800), buttons=[])
        self._pymessage.style.display = "block"
        self._pymessage.value = message
        self.jq['message'].dialog("close")

    def display_canvas(self, display="block"):
        def console_resize(*_):
            self.jq_console_data = Dims(
                int(self.jq_console.offset().left), int(self.jq_console.offset().top),
                self.jq_console.outerWidth(), self.jq_console.outerHeight())
            self.jq_canvas_data = Dims(
                int(self.jq_canvas.offset().left), int(self.jq_canvas.offset().top),
                self.jq_canvas.outerWidth(), self.jq_canvas.outerHeight())
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

    def beforerun(self):
        self._pyconsole.value = ''
        src = self.ace.get_content()  # .getCurrentText()
        self.display_canvas("block")
        self.ace.annotate(0)
        return src

    def onexec_error(self):
        # self._pycanvas.style.display = "none"
        self.jq_canvas.dialog("close")
        traceback.print_exc()
        self.ace.annotate(0)
        error = self._pyconsole.value
        lines = error.split(' line ')
        if len(lines) > 1:
            try:
                line = int(lines[-1].split("\n")[0])
                error = error.split("\n")[-2]
                print(error)
                self.ace.annotate(line, error)
            except Exception as _:
                pass

    """
    def _code(self, _=0):
        self._run_or_code = self.run
        self._pycanvas.style.display = "none"

    def runcode(self, _=0):
        # print("self._run_or_code")
        self._run_or_code()
    """
AUTOSAVE = 600000


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
        self._timer = self.gui.timer.set_timeout(lambda _=0: self.save(autosaved=True), AUTOSAVE)
        self.beforerun = self.onexec_error = None

    def _update_timer(self):
        self.gui.timer.clear_timeout(self._timer)
        self._timer = self.gui.timer.set_timeout(lambda _=0: self.save(autosaved=True), AUTOSAVE)

    def logout_on_exit(self, ev):
        ev.returnValue = "SAIR?"
        try:
            self.save()
            data = {"person": self.project}

            req = self.ajax.ajax()
            req.open('POST', "logout")  # , async=False)
            req.set_header('content-type', 'application/x-www-form-urlencoded')
            req.send(data)
            print("logout", data)
        except Exception as _:
            print("logout request error")
        return "SAIR?"

    def main(self, name="", code="# main"):
        self.name = name
        self.ace = Ace(self.gui, self.edit, self.project, code)
        self.load(msg="New Empty Module")
        self._console = Console(self.gui, self.ace)
        self.beforerun = self._console.beforerun
        self.onexec_error = self._console.onexec_error
        return self

    def save(self, _=0, autosaved=False):
        def on_complete(request):
            if request.text and (request.status == 200 or request.status == 0):
                msg = "AUTOSAVED: " if autosaved else "SAVED: "
                msg += request.text
                self._console.display_saved(msg)
                self.ace.test_dirty(None, code_saved=True)
            else:
                error = str(request.text) if len(request.text) > 2 else "WEB FAILURE"
                self._console.display_saved("NOT SAVED: " + error)

        src = self.ace.test_dirty(None)
        self._update_timer()
        if src is False:
            if not autosaved:
                self._console.display_saved("ALREADY SAVED")
            return 1
        try:
            jsrc = json.dumps({"person": self.project, "name": self.name, "text": src})

            req = self.ajax.ajax()
            req.bind('complete', on_complete)
            req.set_timeout('20000', lambda: self._console.display_saved("NOT SAVED: TIMEOUT"))
            req.open('POST', "save", async=False)
            req.set_header('content-type', 'application/json')  # x-www-form-urlencoded')
            req.send(jsrc)

            state = 1
        except Exception as _:
            state = 0
        return state

    def load(self, _=0, msg=None):
        def on_complete(request):
            if request.text and (request.status == 200 or request.status == 0):
                code = request.text
                self.ace.test_dirty(None, code_saved=True)
                self.ace.set_content(code)
            else:
                error = str(request.text) if len(request.text) > 2 else "WEB FAILURE"
                error = msg or "NOT LOADED: " + error
                self._console.display_saved(error)

        try:
            filename = self.name
            req = self.ajax.ajax()
            req.bind('complete', on_complete)
            req.set_timeout('20000', lambda: self._console.display_saved("NOT LOADED: TIMEOUT"))
            req.open('GET', "load?module="+filename, async=False)
            req.set_header('content-type', 'application/x-www-form-urlencoded')
            req.send()

            state = 1
        except Exception as _:
            state = 0
        return state

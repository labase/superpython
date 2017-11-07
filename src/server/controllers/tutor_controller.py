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

"""Controller handles routes starting with /code.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""
from lib.bottle import Bottle, request, response, HTTPError
from ..models import code_store as cs
from . import BRYTHON, PROJECTS, DX, DY
__author__ = 'carlo'
DEFAULT_CODE = """# default
try:
    import _spy.%s.main as main
    main.main()
except:
    from browser import document, html
    document["pydiv"].html = ""
    document["pydiv"] <= html.IMG(src="/images/site_em_construcao_.jpg")
"""

bottle = Bottle()  # create another WSGI application for this controller and resource.
# debug(True) #  uncomment for verbose error logging. Do not use in production


def decorator():
    _project = request.query.proj
    if not _project or _project not in PROJECTS:
        _project = request.urlparts.hostname.split('.')
        if _project and (_project[0] in PROJECTS):
            _project = _project[0]
        elif request.get_cookie('_spy_project_') in PROJECTS:
            _project = request.get_cookie('_spy_project_')
        else:
            _project = "superpython"
    print("get_project", _project)
    return _project


@bottle.get('/_<module>')
def game(module):
    """ Return Project editor"""
    project = decorator()
    path = "%s/main.py" % module
    if "spy" in module:
        return handle(module)
    print("game(module)", path)
    if len(module) >= 3:
        if cs.DB.ismember(project, module):
            code = cs.DB.load(name=path)
            print('handle/<pypath:path>', path, code and code[:80])
            if code:
                return CODE_DEFAULT.format(**dict(projeto=module, codename="main.py", path=path, code=code,
                                                  scp0=BRYTHON[0], scp1=BRYTHON[1], dx=DX, dy=DY))
    else:
        return CODE_DEFAULT.format(**dict(projeto=module, codename="main.py", path=path, code=DEFAULT_CODE,
                                          scp0=BRYTHON[0], scp1=BRYTHON[1], dx=DX, dy=DY))


@bottle.get('<pypath:path>')
def handle(pypath):
    pypath = pypath.split('_spy/')[1] if "_spy" in pypath else pypath
    pypath = pypath if pypath[0] != '/' else pypath[1:]
    print('handle /<pypath:path>', pypath)
    # project = request.get_cookie('_spy_project_')
    code = cs.DB.load(name=pypath)
    # print('/<pypath:path>', pypath, code and code[:200])
    if code:
        if pypath.endswith(".css"):
            # print("pypath.endswith", pypath)
            response.headers['Content-Type'] = 'text/css'
        return code
    if "__init__" in pypath:
        module = pypath.split("/")
        # module.remove("__init__.py")
        # print('/<pypath:path__init__, pypath, module, project>', pypath, module)
        if len(module) >= 3:
            project, module, path = module[0], module[1], '/'.join(module[1:])
            # print('/<pypath:module, cs.DB.ismember>', module, project, cs.DB.ismember(project, module))
            if cs.DB.ismember(project, module):
                code = cs.DB.load(name=path)
                # print('handle/<pypath:path>', path, code and code[:80])
                if code:
                    return code
                else:
                    return DEFAULT_CODE % module

        return "#"

    raise HTTPError(404, "No such module.")

CODE_DEFAULT = u"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <title>Superpython : {projeto}-{codename}</title>
        <link rel="stylesheet" href="/style.css" type="text/css" />
        <meta http-equiv="content-type" content="application/xml;charset=utf-8" />
        <link rel="shortcut icon" href="/images/favicon.ico" type="image/x-icon" />
        <script src="/js/ace/ace.js" type="text/javascript" charset="utf-8"></script>
        <script src="/js/ace/ext-language_tools.js" type="text/javascript" charset="utf-8"></script>
        <script src="/js/ace/ext-error_marker.js" type="text/javascript" charset="utf-8"></script>
        <script type="text/javascript" src="{scp0}"></script>
        <script type="text/javascript" src="{scp1}"></script>


        <script type="text/python">
            from javascript import JSObject
            from browser import window, document, html, ajax, svg, timer
            from jqueryui import jq
            import __core__


            class Browser:
                svg = svg
                html = html
                doc = document
                window = window
                ajax = ajax
                jq = jq
                timer = timer

            superpython = __core__.main(Browser, JSObject(window.ace), "vega", "{projeto}").main("{codename}")
            def run(self, _=0):
                try:
                    src = superpython.beforerun()
                    exec(src, globals())
                except Exception as _:
                    superpython.onexec_error()
            document["run"].onclick = run

        </script>
        <script type="text/python">
            {code}
        </script>
    </head>
    <body onLoad="brython(1)" background="/images/pipe_back.jpg">
        <div id="main"  style="position: relative; width: 100%; height: 400px; margin: 0px auto;">
            <div id="pydiv"  title="" style="width: {dx}px;
                    height: {dy}px;
                    position: absolute;
                    top:0;
                    bottom: 0;
                    left: 0;
                    right: 40%;

                    margin: auto;">
                <span style="color:white">LOADING..</span>
                <img src="/images/rotgears.gif" style="position: fixed; top: 50%; left: 20%;
                 transform: translate(-50%, -50%);" alt="gears"></img>
            </div>
            <div id="message">
                <textarea id="pymessage" style="width:100%;height:100%;resize: none;display: none;" readonly></textarea>
            </div>
            <div id="console">
                <textarea id="pyconsole" style="width:100%;height:100%;resize: none;display: none;" readonly></textarea>
            </div>
            <div id="control" style="position: absolute; width: 90px; height: 40px; right: 20px; top: -8px;">
                <img id="menu" src="/images/menu.png" alt="menu" title="menu" width="30px"/>
                <img id="run" src="/images/run.png" alt="run" title="run" width="30px"/>
            </div>
           <div id="tutor"  title="" style="width: {dx}px;
                    height: {dy}px;
                    position: absolute;
                    top:0;
                    bottom: 0;
                    left: 40%;
                    right: 0;

                    margin: auto;">
               <div id="tutorial"  style="position: relative; width: 100%; height: 100%; top: 0;">
                    <img id="e0" src="/images/site_em_construcao_.jpg"
                     alt="Em construção" title="Em construção" width="100%"/>
               </div>
                <div id="edit"  style="position: relative; width: 100%; height: 100%; top: 0;">
                    <div id="vega" class="editclass" style="width: 100%; height: 100%;"></div>
                </div>
           </div>
        </div>
   </body>
</html>

"""
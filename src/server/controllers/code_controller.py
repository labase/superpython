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
        <script type="text/javascript" src="{scp0}"></script>
        <script type="text/javascript" src="{scp1}"></script>

        <script type="text/python">
            {code}
        </script>
    </head>
    <body onLoad="brython({{debug:1, cache:'browser', static_stdlib_import:true}})" background="/images/pipe_back.jpg">
           <div id="pydiv"  title="" style="width: {dx}px;
    height: {dy}px;
    position: absolute;
    top:0;
    bottom: 0;
    left: 0;
    right: 0;

    margin: auto;">
                <span style="color:white">LOADING..</span>
           </div>
    </body>
</html>
"""
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
__author__ = 'carlo'
from lib.bottle import Bottle, view, request, response, HTTPError
from ..models import code_store as cs
from . import BRYTHON, PROJECTS, DX, DY
DEFAULT_CODE = """# default
try:
    import superpython.%s.main as main
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
    print("get_project", _project)
    if not _project or _project not in PROJECTS:
        _project = request.urlparts.hostname.split('.')
        if _project and (_project[0] in PROJECTS):
            _project = _project[0]
        elif request.get_cookie('_spy_project_') in PROJECTS:
            _project = request.get_cookie('_spy_project_')
        else:
            _project = "superpython"
    return _project

@bottle.get('/_<module>')
@view('game')
def game(module):
    """ Return Project editor"""
    project = decorator()
    path = "superpython.%s.%s" % (project, module)
    print("game(module)", path)
    return dict(projeto=module, codename="main.py", path=path, brython=BRYTHON, dx=DX, dy=DY)



@bottle.get('/superpython/<pypath:path>')
def handle(pypath):
    # project = request.get_cookie('_spy_project_')
    code = cs.DB.load(name=pypath)
    print('/<pypath:path>', pypath, code and code[:200])
    if code:
        return code
    if "__init__" in pypath:
        module = pypath.split("/")
        # module.remove("__init__.py")
        print('/<pypath:path__init__, pypath, module, project>', pypath, module)
        if len(module) >= 3:
            project, module, path = module[0], module[1], '/'.join(module[1:])
            print('/<pypath:path__init__, module, project, cs.DB.ismember>', module, project, cs.DB.ismember(project, module))
            if cs.DB.ismember(project, module):
                code = cs.DB.load(name=path)
                print('handle/<pypath:path>', path, code and code[:80])
                if code:
                    return code
                else:
                    return DEFAULT_CODE % module

        return "#"

    raise HTTPError(404, "No such module.")


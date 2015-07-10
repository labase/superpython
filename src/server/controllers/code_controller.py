#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Enplicaw
# Copyright 2013-2015 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
#
# Enplicaw é um software livre; você pode redistribuí-lo e/ou
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
from lib.bottle import Bottle, view, request, response
from ..models.code_store import DB
import collections
LIKERT = "nunca pouquíssimo pouco mediano muito muitíssimo sempre".split()
Item = collections.namedtuple('Item', 'label value')
Likert = collections.namedtuple('Likert', 'label name value')
TITLE = "Habilidades de Alunos - %s"
PICTURE = "https://dl.dropboxusercontent.com/u/1751704/igames/img/superp%C3%BDthon.jpg"
PROJECTS = "JardimBotanico SuperPlataforma SuperPython MuseuGeo".split()
QNAME = "q%02d"
bottle = Bottle()  # create another WSGI application for this controller and resource.
# debug(True) #  uncomment for verbose error logging. Do not use in production
def methodroute(route):
    def decorator(f):
        f.route = route
        return f
    return decorator
'''
class App(object):
    @methodroute('/index/')
    def index(self):
        pass
'''


@bottle.get('/')
@view('index')
def home():
    """ Open the survey with surveyor identification.
    """
    ident = [dict(label="Nome", name="name"), dict(label="Escola", name="school")]
    project = request.urlparts.geturl().split('/')[2].split('.')[0]
    if project in PROJECTS:
            response.set_cookie('_enplicaw_project_', "%s %s %s" % (project, "__", "__"))
    else:
        project = "SuperPython"
        response.set_cookie('_enplicaw_project_', "%s %s %s" % (project, "__", "__"))
    return dict(title=TITLE % project, image=PICTURE, identification=ident, submit="Enviar")


@bottle.post('/identify')
@view('survey')
def identify():
    """ Collects the identification from surveyor an opens the survey form.
    """
    project = "SuperPython"
    user = request.forms.get('name')
    school = request.forms.get('text')
    DB.instance(project, user, school, QUESTION)
    response.set_cookie('_enplicaw_project_', "%s %s %s" % (project, user, school))

    survey = [Likert(label=question, name=qname, value=LIKERT) for qname, question in QUESTION]
    return dict(title=TITLE % project, columns=len(LIKERT), survey=survey, submit="Enviar")


def _points():
    """ Post the surveied data to the data base.
    """
    project = "SuperPython"
    data = {a: b for a, b in request.POST.items()}
    cookie = request.get_cookie('_enplicaw_project_')
    _, author, _ = cookie.split()
    surveydata = {q: LIKERT.index(value)+1 for q, value in data.items() if q in QITEM}
    [DATA[q].update({data[q]:DATA[q][data[q]]+1}) for q in data.keys() if q in QITEM]
    PLOT[data["name"]] = [LIKERT.index(data[key])+1 if key in data.keys() else 0
                          for key in QITEM]+["ns".index(data["super"])]+[cookie]
    DB.post(name=data["name"], classifier=data["super"],
                 data=surveydata, session=DB.instance(project=project, author=author))
    print(PLOT)
    return data


@bottle.post('/survey')
@view('survey')
def survey():
    """ Collects the survey data from the form and provides a new form.
    """
    project = "SuperPython"
    _points()
    survey = [Likert(label=question, name=qname, value=LIKERT) for qname, question in QUESTION]
    return dict(title=TITLE % project, columns=len(LIKERT), survey=survey, submit="Enviar")


@bottle.post('/endsurvey')
@view('resultado')
def endsurvey():
    """ Collects the survey data from the form and provides a sumary of collected data.
    """
    project = "SuperPython"
    data = _points()
    line = [Item(label=q, value=[DATA[q][i] for i in LIKERT]) for q in QITEM]
    return dict(title=TITLE % project, data='', columns=LIKERT, result=line, submit="Enviar")

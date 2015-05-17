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

"""Controller handles routes starting with /project.

"""
__author__ = 'carlo'
from lib.bottle import Bottle, view, request
LAST = None
PROJECTS = "jardim spy super geo".split()
#FAKE = [{k: 10*i+j for j, k in enumerate(HEAD)} for i in range(4)]

bottle = Bottle()  # create another WSGI application for this controller and resource.
# debug(True) #  uncomment for verbose error logging. Do not use in production


@bottle.get('/')
@view('projeto')
def score(author):
    project = request.get_cookie('_spy_project_')
    response.set_cookie('_spy_project_', project+author)

    try:
        record_id = LAST
        if record_id is None:
            raise Exception()
        '''
        print('resultado', record_id)
        record = database.DRECORD[record_id]
        record = record[PEC]
        print('record resultado:', record)
        return dict(user=record_id, result=record)
        '''
    except Exception:
        # return dict(user="FAKE", result=FAKE)
        fake = dict(user="FAKE", result=FAKE)
        # print('score', fake)
        return fake
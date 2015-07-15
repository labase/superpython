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


"""Google HDB storage.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""
__author__ = 'carlo'
# Imports the NDB data modeling API
import os
import sys
from uuid import uuid1

if "AUTH_DOMAIN" in os.environ.keys():
    from google.appengine.ext import ndb
else:
    from lib.minimock import Mock
    sys.modules['google.appengine.ext'] = Mock('google.appengine.ext')
    ndb = Mock('google.appengine.ext')

# import googledatastore as ndb

DEFAULT_PROJECTS = "DEFAULT_PROJECTS"
DEFAULT_PROJECT_NAMES = "JardimBotanico SuperPlataforma SuperPython MuseuGeo"


class Program(ndb.Expando):
    """A main model for representing all projects."""
    name = ndb.StringProperty(indexed=True)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def nget(cls, query):
        return query.fetch()[0] if query.fetch() else None

    @classmethod
    def instance(cls, name=DEFAULT_PROJECTS, names=DEFAULT_PROJECT_NAMES):
        def get_project():
            prj = cls.query(cls.name == name).fetch()
            print("prj", prj)
            cls._projects = prj[0] if prj else cls._start(name=name, names=names)

        return cls._projects or get_project()

    @classmethod
    def _start(cls, name=DEFAULT_PROJECTS, names=DEFAULT_PROJECT_NAMES):
        _prj = Projects.create(name=name, names=names)
        [Project.create(project=_prj.key, name=aname, kind=DEFAULT_PROJECTS) for aname in names.split()]
        return _prj


class Project(ndb.Expando):
    """Sub model for representing an project."""
    program = ndb.KeyProperty(kind=Program)
    name = ndb.StringProperty(indexed=True)
    persons = ndb.TextProperty(indexed=False)
    populated = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def nget(cls, name):
        query = cls.query(cls.name == name).fetch()
        return query and query[0]


class Person(ndb.Expando):
    """Sub model for representing an author."""
    project = ndb.KeyProperty(kind=Project)
    name = ndb.StringProperty(indexed=True)
    lastsession = ndb.KeyProperty(indexed=False)

    def updatesession(self, session):
        self.lastsession = session
        self.put()

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def nget(cls, name):
        query = cls.query(cls.name == name).fetch()
        return query and query[0]

    @classmethod
    def obtain(cls, name):
        return Person.nget(name=name) or Person.create(name=name)


class Code(ndb.Model):
    """A sub model for representing an individual Question entry."""
    person = ndb.KeyProperty(kind=Person)
    name = ndb.StringProperty(indexed=True)
    text = ndb.TextProperty(indexed=False)

    def set_text(self, value):
        self.text = value
        self.put()

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def nget(cls, name):
        query = cls.query(cls.name == name).fetch()
        return query and query[0]

    @classmethod
    def obtain(cls, person, name, text):
        personk = Person.nget(person)
        return Code.nget(name=name) or Code.create(person=personk.key, name=name, text=text)


class Error(ndb.Model):
    """A main model for representing an individual Question entry."""
    code = ndb.KeyProperty(kind=Code)
    message = ndb.TextProperty(indexed=False)
    value = ndb.IntegerProperty(indexed=False)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance


class Session(ndb.Expando):
    """A main model for representing a user interactive session."""
    _session = None
    project = ndb.KeyProperty(kind=Project)
    person = ndb.KeyProperty(kind=Person)
    code = ndb.KeyProperty(kind=Code)
    name = ndb.StringProperty(indexed=True)
    modified_date = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def nget(cls, name):
        query = cls.query(cls.name == name).fetch()
        return query and query[0]

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def save(cls, project, person, name, code):
        person = Person.nget(person)
        project = Project.nget(project)
        code = Code.obtain(person, name)
        code.set_text(code)
        code.put()
        return instance

    @classmethod
    def login(cls, project, person):
        print("project, person", project, person)
        sessionname = uuid1().hex
        person = Person.nget(person)
        project = Project.nget(project)
        lastsession = person.lastsession

        cursession = cls.create(project=project.key, person=person.key, name=sessionname)
        person.updatesession(cursession.key)
        #  cls._populate_persons(project, cursession, persons)
        return cursession, lastsession

    @classmethod
    def lastcode(cls, lastsession):
        # lastcode = Session.nget(lastsession).code
        lastcode = lastsession.get().code
        code = (lastcode.name, lastcode.text) if lastcode else ("main.py", "# main")
        return code

    @classmethod
    def _populate_codes(cls, session, persons):
        prj = session.project.get()  # Project.kget(key=session.project)
        if prj.populated:
            return prj.questions
        oquestions = [
            Code.create(name=key, text=value) for key, value in persons
            ]
        print(oquestions)
        prj.populated = True
        prj.questions = oquestions
        prj.put()
        return oquestions

    @classmethod
    def init_db_(cls):

        if "AUTH_DOMAIN" not in os.environ.keys():
            return

        prj = Project.nget(name="superpython")
        if prj == []:
            prj = Project.create(name="superpython")
        persons = ["projeto%d" % d for d in range(20)]
        ses = Session.create(name=uuid1().hex, project=prj.key)
        Session._populate_persons(prj, ses, persons)

    @classmethod
    def _populate_persons(cls, project, session, persons):
        prj = session.project.get()  # Project.kget(key=session.project)
        if prj.populated:
            return prj.persons
        new_persons = [
            Person.create(project=project.key, name=key, lastsession=session.key) for key in persons
            ]
        print(new_persons)
        prj.populated = True
        #  prj.persons = new_persons
        prj.put()
        return new_persons

Session.init_db_()
DB = Session

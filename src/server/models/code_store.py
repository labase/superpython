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
from uuid import uuid1
import database as dbs

DEFAULT_PROJECTS = "DEFAULT_PROJECTS"
DEFAULT_PROJECT_NAMES = "JardimBotanico SuperPlataforma SuperPython MuseuGeo"
OLDNA = "granito basalto pomes calcario marmore arenito" \
        " calcita_laranja agua_marinha amazonita hematita quartzo_rosa turmalina" \
        " citrino pirita silex ametista cristal quartzo-verde" \
        " seixo dolomita fluorita aragonita calcita onix" \
        " feldspato _ jaspe agata sodalita alabastro".split()
NAMES = "granito arenito" \
        " calcita_laranja agua_marinha amazonita quartzo_rosa turmalina" \
        " citrino pirita silex ametista cristal quartzo-verde" \
        " fluorita onix" \
        " feldspato jaspe agata sodalita alabastro".split()
SNAMES = "aries touro gemeos cancer leao virgem libra escorpiao ofiuco sargitario capricornio aquario peixes".split()
CNAMES = "chiclete framboesa red_velvet laranja baunilha limao goji morango capuccino marshmallow chocomenta blue_sky" \
         " cereja pao_de_mel milho_verde erva_doce mirtilo uva nozes banana pistache tutifruti vinho cassis".split()
HNAMES = "sonic mulher_maravilha chapolin mestre_kame coringa darth_vader batman arrow petra lanterna_verde yoda tarzan homem_aranha" \
         " verinha stelar florzinha lindinha docinho flash".split()
FNAMES = "abacate abacaxi acerola ameixa amora bananas caju caqui carambola cerejas damasco framboesas goiaba graviola" \
         " jaboticaba jaca kiwi laranjas manga maracuja melancia mirtilos morangos pera pitanga" \
         " sapoti tangerina tomate umbu uvas".split()
ENAMES = ['sirius', 'canopus', 'arcturus', 'vega', 'capella', 'rigel', 'procyon', 'achernar', 'hadar', 'altair',
          'acrux', 'spica', 'antares', 'pollux', 'deneb', 'mimosa', 'regulus', 'adhara', 'castor', 'gacrux', 'shaula',
          'alnilam', 'alnair', 'regor', 'alioth', 'kaus', 'mirfak', 'dubhe', 'wezen', 'alkaid', 'sargas',
          'avior', 'atria', 'alhena', 'peacock', 'polaris', 'mirzam', 'alphard', 'algieba', 'hamal']
KNAMES = ['adware', 'anonymous', 'autorun', 'backdoor', 'boot', 'botnet', 'hijacker', 'attack', 'overflow', 'chain',
          'cookie', 'darknet', 'leakage', 'loss', 'theft', 'denial', 'driveby', 'exploit', 'fake', 'hacker', 'hoax',
          'honeypot', 'worm', 'keylogging', 'malware', 'parasitic', 'patches', 'phishing', 'unwanted', 'ransomware',
          'rootkit', 'engineer', 'spam', 'spoofing', 'spyware', 'injection', 'suspicious', 'trojan', 'virus', 'zombie']




class Program(dbs.NDB.Expando):
    """A main model for representing all projects."""
    name = dbs.NDB.StringProperty(indexed=True)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance

    @classmethod
    def nget(cls, query):
        return query.fetch()[0] if query.fetch() else None


class Project(dbs.NDB.Expando):
    """Sub model for representing an project."""
    program = dbs.NDB.KeyProperty(kind=Program)
    name = dbs.NDB.StringProperty(indexed=True)
    persons = dbs.NDB.TextProperty(indexed=False)
    sprites = dbs.NDB.JsonProperty(indexed=False)
    populated = dbs.NDB.BooleanProperty(default=False)
    sessions = dbs.NDB.JsonProperty(default={})

    @classmethod
    def ismember(cls, project, person):
        prj = Project.nget(project)
        return prj and (person in prj.persons)

    def updatesession(self, person):
        # self.sessions = set(self.sessions).add(person)
        self.sessions[person] = True
        self.put()

    def removesession(self, person):
        # self.sessions = set(self.sessions).remove(person)
        self.sessions[person] = False
        print("removesession", person, self.sessions)
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

    def islogged(self, person):
        return person in self.sessions and self.sessions[person]


class Person(dbs.NDB.Expando):
    """Sub model for representing an author."""
    project = dbs.NDB.KeyProperty(kind=Project)
    name = dbs.NDB.StringProperty(indexed=True)
    lastsession = dbs.NDB.KeyProperty(indexed=False)
    lastcode = dbs.NDB.KeyProperty(indexed=False)

    def updatesession(self, session):
        self.lastsession = session
        self.put()

    def updatecode(self, code):
        self.lastcode = code
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


class Code(dbs.NDB.Model):
    """A sub model for representing an individual Question entry."""
    person = dbs.NDB.KeyProperty(kind=Person)
    name = dbs.NDB.StringProperty(indexed=True)
    text = dbs.NDB.TextProperty(indexed=False)

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
        print("codeobtain", dict(person=person, name=name, text=text))
        person = Person.nget(person)
        print(dict(person=person.key, name=name, text=text))
        code = Code.nget(name=name)
        if code:
            code.set_text(text)
            code.put()
        else:
            code = Code.create(person=person.key, name=name, text=text)
        person.updatecode(code.key)
        return code


class Error(dbs.NDB.Model):
    """A main model for representing an individual Question entry."""
    code = dbs.NDB.KeyProperty(kind=Code)
    message = dbs.NDB.TextProperty(indexed=False)
    value = dbs.NDB.IntegerProperty(indexed=False)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.put()
        return instance


class Session(dbs.NDB.Expando):
    """A main model for representing a user interactive session."""
    _session = None
    project = dbs.NDB.KeyProperty(kind=Project)
    person = dbs.NDB.KeyProperty(kind=Person)
    code = dbs.NDB.KeyProperty(kind=Code)
    name = dbs.NDB.StringProperty(indexed=True)
    modified_date = dbs.NDB.DateTimeProperty(auto_now=True)

    @classmethod
    def nget(cls, name):
        query = cls.query(cls.name == name).fetch()
        return query and query[0]

    @classmethod
    def create(cls, name, person=None, project=None):
        session = Session.nget(name)
        print("create(cls, **kwargs)", session, person, project, name)
        if session:
            session.project = project
            session.person = person
            session.put()
            return session
        instance = cls(person=person, project=project, name=name)
        instance.put()
        return instance

    @classmethod
    def load(cls, name):
        code = Code.nget(name=name)
        return code and code.text

    @classmethod
    def save(cls, **kwargs):
        code = Code.obtain(**kwargs)
        return code

    @classmethod
    def getlogged(cls, project):
        return Project.nget(project).sessions, Project.nget(project).sprites

    @classmethod
    def ismember(cls, project, person):
        if not project:
            return Person.nget(person)
        return Project.ismember(project, person)

    @classmethod
    def islogged(cls, project, person):
        project = Project.nget(project)
        return project.islogged(person)

    @classmethod
    def logout(cls, project, person):
        project = Project.nget(project)
        project.removesession(person)

    @classmethod
    def login(cls, project, person, session=None):
        print("project, person", project, person)
        sessionname = session if Session.nget(session) else str(uuid1())
        project = Project.nget(project)
        project.updatesession(person)
        person = Person.nget(person)
        print("project, person", project, person)
        cursession = cls.create(project=project.key, person=person.key, name=sessionname)
        lastsession = person.lastsession or cursession
        person.updatesession(cursession.key)
        return cursession, lastsession

    @classmethod
    def lastcode(cls, lastsession):
        session = lastsession.get()
        person = session.person.get()
        lastcode = person.lastcode
        if lastcode:
            code = lastcode.get()
            name = code.name if code else "nono"
            text = code.text if code else "# empty"
        else:
            name = "nono"
            text = "# empty"

        print("lastcode", person.name, person.lastsession, name, text)
        code = (name, text) if lastcode else ("%s/main.py" % session.person.get().name, "# main")
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

        Session.create(name=uuid1().hex)
        Session._populate_persons("superpython", NAMES, OLDNA)
        Session._populate_persons("surdo", SNAMES, SNAMES)
        Session._populate_persons("cups", CNAMES, CNAMES)
        Session._populate_persons("hero", HNAMES, HNAMES)
        Session._populate_persons("jardim", FNAMES, FNAMES)
        Session._populate_persons("star", ENAMES, ENAMES)
        Session._populate_persons("hacker", KNAMES, KNAMES)

    @classmethod
    def _populate_persons(cls, projectname, persons, sprites):
        prj = Project.nget(name=projectname)
        if not prj:
            prj = Project.create(name=projectname, sprites=sprites)
        if not prj.persons:
            print("_populate_persons if not prj.persons", ' '.join(persons), projectname)
            prj.persons = ' '.join(persons)
            prj.put()
        if prj.populated:
            return prj.persons
        new_persons = [
            Person.create(project=prj.key, name=key, lastsession=None) for key in persons
            ]
        print(new_persons)
        prj.sessions = {person: False for person in persons}
        prj.populated = True
        prj.put()
        return new_persons

Session.init_db_()
DB = Session

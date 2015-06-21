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

"""Controller handles routes starting with /RESOURCE_NAME.

Change this file's name and contents as appropriate to the
resources your app exposes to clients.

"""
__author__ = 'carlo'
import urllib
import json
from time import sleep
# USERS = "alpha bravo charlie echo golf hotel india" \
#        " kilo lima mike november oscar papa quebec sierra uniform zulu".split()
USERS = "aries touro gemeos cancer leao virgem libra escorpiao sagitario capricornio aquario peixes".split()

class Util:
    def __init__(self, user, passwd="nceufrj"):
        self._token = 0
        self._baseURL = "http://pyschool.net/"
        self.user = user
        self.passwd = passwd

    def login(self):
        sleep(0.5)
        if True:
            # send userid/password
            _userid = self.user
            _password = self.passwd
            _url = "http://pyschool.net/Auth?userid=%s&password=%s" % (_userid, _password)

            _fp = urllib.urlopen(_url)
            _data = _fp.read()

            _json = json.loads(_data)
            if _json['status'] == 'Okay':
                # import remote_storage_fs

                # fs = remote_storage_fs.GoogleDataStorage("/pyschool")
                self._token = _json['token']
                _cookie = 'token=%s|login_type=authenticate' % _json['token']
                return self
            print(self.user, _json)
            return self

    def _remote_call(self, data):
        # console.log("remote call", data)
        data['token'] = self._token  # add in token to call
        _json = json.dumps({'data': data})

        try:
            _fp = urllib.urlopen(self._baseURL + "FS", _json)
            return json.loads(_fp.read())  # returns a string (in json format)
        except:
            return {'status': 'Error',
                    'message': 'Network connectivity issues'}

    def _read_file(self, filename):
        """ retrieves file from storage, returns fileobj if successful,
            return None if unsuccessful
        """

        _json = self._remote_call({'command': 'read_file', 'filename': filename})

        try:
            # _f = FileObject.FileObject()
            # _f=FileSystemBase.FileObject()
            # _f = json.load(_json['fileobj'])#["contents"]
            _f = _json['fileobj']  # ["contents"]
            _f = json.loads(_f)[u'contents']
            return {'status': 'Okay', 'fileobj': _f}
        except Exception as e:
            return {'status': 'Error', 'message': str(e), 'json': _json, 'file':  filename}

    def read_main_file(self, filename):
        """ retrieves file from storage, returns fileobj if successful,
            return None if unsuccessful
        """
        try:
            cnt = self._read_file("/pyschool/%s" % filename)
            return cnt['fileobj']
        except Exception as e:
            return {'status': 'Error', 'message': str(e), 'json': cnt}



ps = Util('carlo', 'labase')
print(ps.login()._token)
#USERS =["alpha"]
files = [Util(fl).login().read_main_file("%s/%s.py" % (fl, "gripe")) for fl in USERS]
# print(ps._read_file("/pyschool/adv.py")['fileobj'])
for f in files:
    print(f)

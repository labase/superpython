<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>Superpython : {{ projeto }}</title>
    <link rel="stylesheet" href="style.css" type="text/css" />


  <script src="js/ace/ace.js" type="text/javascript" charset="utf-8"></script>
  <script src="js/ace/ext-language_tools.js" type="text/javascript" charset="utf-8"></script>
  <script src="js/ace/mode-python3.js" type="text/javascript" charset="utf-8"></script>
  <script src="js/ace/snippets/python.js" type="text/javascript" charset="utf-8"></script>

  <script type="text/javascript" src="external/brython/brython.js"></script>
  <script type="text/javascript" src="external/brython/py_VFS.js"></script>

  <script type="text/javascript" src="libs/custom_VFS.js"></script>

<script type="text/python">
from javascript import JSObject, console
from browser import window, document, alert
import sys
import json
import urllib.request
import time
import traceback

#this import causes loading to slow down.  See email
# to Pierre on Dec 4th, 2014 for details..
#import urllib.parse

import editor
editors=editor.Editor('editortabs')

sys.path.append('libs/FileSystem')
import FileObject

_jquery=JSObject(window.jQuery)
display_message=JSObject(window.display_message)

sharelist={}

def run():
    #find selected Tab (and get its contents)
    document['pyconsole'].value=''
    src=editors.getCurrentText()
    t0 = time.perf_counter()
    try:
        exec(src,globals())
        state = 1
    except Exception as exc:
        traceback.print_exc()
        state = 0

    print('<completed in %6.2f ms>' % ((time.perf_counter()-t0)*1000.0))
    return state

def create_tab(content=""):
    editors.add_editor()
</script>
</head>
<body>
</body>
</html>

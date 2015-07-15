<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <title>Superpython : {{ projeto }}-{{ codename }}</title>
        <link rel="stylesheet" href="/style.css" type="text/css" />
        <meta http-equiv="content-type" content="application/xml;charset=utf-8" />
        <link rel="shortcut icon" href="/images/favicon.ico" type="image/x-icon" />

        <script src="/js/ace/ace.js" type="text/javascript" charset="utf-8"></script>
        <script src="/js/ace/ext-language_tools.js" type="text/javascript" charset="utf-8"></script>
        <script src="/js/ace/mode-python3.js" type="text/javascript" charset="utf-8"></script>
        <script src="/js/ace/snippets/python.js" type="text/javascript" charset="utf-8"></script>

        <script type="text/javascript" src="/external/brython/brython.js"></script>
        <script type="text/javascript" src="/external/brython/py_VFS.js"></script>

        <script type="text/javascript" src="/libs/custom_VFS.js"></script>

        <script type="text/python">
            from javascript import JSObject
            from browser import window, document, svg, html, ajax
            class Browser:
                svg = svg
                html = html
                doc = document #  ["main"]
                window = window
                ajax = ajax
            from superpython import main
            main(Browser, JSObject(window.ace), "{{ projeto }}").main("{{ codename }}", "{{ codetext }}")
        </script>
    </head>
    <body onLoad="brython({debug:1, cache:'browser', static_stdlib_import:true})" background="/images/pipe_back.jpg">
        <div id="main"  style="position: relative; width: 100%; height: 100%; margin: 0px auto;">
            <div id="game"  style="position: absolute; width: 100%; height: 100%;"></div>
            <div id="edit"  style="position: absolute; width: 100%; height: 100%;"></div>
            <div id="control" style="position: absolute; width: 90px; height: 40px; right: -30px; top: -8px;">
                <img id="menu" src="/images/menu.png" alt="menu" title="menu" width="30px"/>
                <img id="run" src="/images/run.png" alt="run" title="run" width="30px"/>
            </div>
            <div id="console"  style="position: absolute; width: 100%; height: 40px; right: -10px; bottom: -8px;">
                <textarea id="pyconsole" style="background:white;width:98%;height:98%" readonly>
                </textarea>
            </div>
        </div>
    </body>
</html>

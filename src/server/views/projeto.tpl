<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <title>Superpython : {{ projeto }}-{{ codename }}</title>
        <link rel="stylesheet" href="/style.css" type="text/css" />
        <meta http-equiv="content-type" content="application/xml;charset=utf-8" />
        <link rel="shortcut icon" href="/images/favicon.ico" type="image/x-icon" />
        <!--<script src="http://cdnjs.cloudflare.com/ajax/libs/ace/1.2.0/ace.js" type="text/javascript" charset="utf-8"></script>-->
        <script src="/js/ace/ace.js" type="text/javascript" charset="utf-8"></script>
        <script src="/js/ace/ext-language_tools.js" type="text/javascript" charset="utf-8"></script>
        <script src="/js/ace/ext-error_marker.js" type="text/javascript" charset="utf-8"></script>
        <style type="">
            .ui-dialog{font-size: 30%;}
            .ui-dialog-title {font-size:10px !important; margin: -0.02em 0.1em !important;}
            .ui-dialog-titlebar {padding: 0.18em 1em !important;}
            .ui-dialog-content {padding: 0.3em 0.99em  0.99em 0.2em !important;font-size:12px !important; }
            .no-titlebar  .ui-dialog-titlebar {display: none;}
        </style>
        <script type="text/javascript" src="{{ brython }}"></script>

        <script type="text/python">
            from javascript import JSObject
            from browser import window, document, html, ajax, svg, timer
            from html.parser import HTMLParser
            from jqueryui import jq
            from superpython import main


            class Browser:
                svg = svg
                html = html
                doc = document
                window = window
                ajax = ajax
                jq = jq
                timer = timer
                unescape = HTMLParser().unescape

            main(Browser, JSObject(window.ace), "{{ projeto }}").main("{{ codename }}", "{{ codetext }}")

        </script>
    </head>
    <body onLoad="brython({debug:1, cache:'browser', static_stdlib_import:true})" background="/images/pipe_back.jpg">
        <div id="main"  style="position: relative; width: 100%; height: 400px; margin: 0px auto;">
            <div id="game"  style="position: absolute; width: 100%; height: 100%;"></div>
            <div id="edit"  style="position: absolute; width: 100%; height: 100%;">
                <div id="{{ projeto }}" class="editclass" style="width: 100%; height: 100%;"></div>
            </div>
            <div id="nopydiv"  style="position: absolute; width: 100%; height: 100%; right: -10px; bottom: -8px; display: none; z-index:100;">
                <img id="emmenu" src="/images/site_em_construcao_.jpg" alt="menu" title="menu" width="600px"/>

            </div>
            <div id="pydiv"  title="">
                <span style="color:white">LOADING..</span>
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
        </div>
    </body>
</html>

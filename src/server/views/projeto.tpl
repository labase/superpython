<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <title>Superpython : {{ projeto }}</title>
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
            from browser import window, document
            import browser
            from superpython import main
            main(browser, document["main"], JSObject(window.ace)).main()
        </script>
    </head>
    <body>
        <div id="main"></div>
    </body>
</html>

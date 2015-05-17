<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><!--

############################################################
Super Python - User Programming Interface
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2015/04/06
:Status: This is a "work in progress"
:Revision: 0.1.0
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2015, `GPL <http://is.gd/3Udt>`__.
-->
<html>
<head>
    <meta charset="iso-8859-1">
    <title>SuperPython</title>
    <meta http-equiv="content-type" content="application/xml;charset=utf-8" />
    <link rel="shortcut icon" href="/images/favicon.ico" type="image/x-icon" />
    <link rel="stylesheet" href="style.css" type="text/css" />
    <script type="text/javascript" src="external/brython/brython.js"></script>
    <script type="text/javascript" src="external/brython/py_VFS.js"></script>
    <script type="text/javascript" src="libs/custom_VFS.js"></script>
    <script type="text/python" src="libs/importhooks/localstorage.py"></script>
    <script type="text/python" src="libs/importhooks/custom_VFS.py"></script>
    <script type="text/python">
    from browser import window
    from browser import doc, svg
    from superpython import main
    main(doc,svg)
    </script>

</head>
<body onLoad="brython({debug:1, cache:'browser', static_stdlib_import:true,
                       custom_import_funcs:[import_hooks]})">
     <H1>USER: {{ user }}</H1>
     <div id="banner"></div>
    <table id="box-table-a" >
        <tbody>
            % for line in result:
            <tr>
                % for proj in line:
                <td><span>{{ proj }}</span></td>
                % end
            </tr>
            % end
        </tbody>

    </table>
<</body>
</html>

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
    <meta charset="iso-8859-1" />
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
    </script>
        <style>
            body, html {
                margin: 0;
                height: 100%;
                width: 100%;
            }
            #banner {
                margin: 0 auto;
                padding: 10px;
                position:relative;
                width:800px;
            }

            #menu {
                background-color: green;
                background-position: center;
                background-repeat: no-repeat;
                max-height: 80%;
                max-width: 90%;
                height: 100%;
                width: 100%;
                display: table;
                text-align: center;
            }
            #item {
                height: 120px;
                width: 130px;
                margin: 5px;
                display: inline-block;
            }
            .stretch {
                width: 100%;
                display: inline-block;
                font-size: 0;
                line-height: 0
            }


        </style>

</head>
<body onLoad="brython({debug:1, cache:'browser', static_stdlib_import:true,
                       custom_import_funcs:[import_hooks]})" background="/images/pipe_back.jpg">
    <H1>USER: {{ user }}</H1>
    <div id="banner">
        <div id="menu" style="position:absolute; left:0px; top:0px;">
            % for proj in result:
                <div id="item" style="position:absolute; left:{{ proj.x }}px; top:{{ proj.y+15 }}px;"> <!--id="{{ 'item' + "".join(proj.name.split()) }}">-->
                    <span>{{ proj.name }}</span><br/>
                    <img src="{{ proj.picture }}" width="80px" title="{{ proj.name }}"/>
                </div>
            %end

        </div>
        <div id="mask" style="position:absolute; left:0px; top:0px;">
            <img src="/images/selector.png"/>
        </div>
        <div id="selector" style="position:absolute; left:0px; top:0px;">
            <form id="select" method="post" action="main/editor">
                % for item, sel in enumerate(selector):
                    <div id="{{ 'topper%d'%item }}"
                         style="position:absolute; left:{{ sel.x+30 }}px; top:{{ sel.y+25 }}px;" onclick="submitform('{{ sel.name }}')">
                         <img src="images/crank.png" width="100px"
                              title="{{ sel.name }}" style="opacity:{{ [0,1][sel.picture] }}"/>
                    </div>
                %end
            <svg width="800" height="800">
            </svg>
                <input id="module" name="module" type="hidden"/>
                <script type="text/javascript">
                function submitform(item)
                {
                  document.getElementById('module').value = item
                  document.forms["select"].submit();
                }
                </script>
            </form>
        </div>
    </div>

</body>
</html>

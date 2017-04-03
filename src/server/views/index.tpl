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
    <title>SuperPython</title>
    <meta http-equiv="content-type" content="application/xml;charset=utf-8"/>
    <link rel="shortcut icon" href="/images/favicon.ico" type="image/x-icon"/>
    <link rel="stylesheet" href="style.css" type="text/css"/>
    % for scp in brython:
    <script type="text/javascript" src="{{ scp  }}"></script>
    % end
    <!--
    <script type="text/javascript" src="external/brython/py_VFS.js"></script>
    <script type="text/javascript" src="libs/custom_VFS.js"></script>
    <script type="text/python" src="libs/importhooks/localstorage.py"></script>
    <script type="text/python" src="libs/importhooks/custom_VFS.py"></script>
    -->
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
                height: 90px;
                width: 90px;
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

    <script type="text/python">
        from browser import alert, document, window
        class Edi:
            def __init__(self):
                self.last = (0,0)
                self.on = False
                self.z = document["selector"]
                self.cap = None
            def _on_mouse_down(self, ev):
                self.on = not self.on
                self.cap = ev.target.parent.id
                a, b, c, d = ev.clientX, ev.clientY, self.z.left, self.z.top
                self.last = (a, b)
                print(ev.target.parent.id, a, b, c, d, a-c, b-d )
                if ev.target.parent.id == "topper0":
                    print(["Par(%d, %d)" % (document["topper%d" % t].left-c-30, document["topper%d" % t].top-d-25) for t in range(20)])
            def _on_mouse_over(self, ev):
                if self.on:
                    cap = document[self.cap]
                    j, k = self.last
                    l, m = self.z.left, self.z.top
                    a, b, c, d = ev.clientX, ev.clientY, cap.left, cap.top
                    x, y = a-j+c-l, b-k+d-m
                    cap.left = x
                    cap.style.top = y
                    print(x, y, a, b, c, d, j, k, cap.left, cap.top)
                    self.last = (a, b)

                print(ev.target.id, ev.clientX, ev.clientY)
        def _request_login_if_available(user, blocked):
            #alert("%s, %s" % (user, blocked))
            #return
            if blocked:
                user_name = input("Este grupo esta em uso, digite o nome deste grupo para assumir o controle:")
                if user_name != user:
                    alert("Nome incorreto, login falhou.")
                    return
            document["module"].value = user
            document["code"].value = ""
            document["project"].value = "{{ project }}"
            old_action = document.get(selector='form')[0].action
            document.get(selector='form')[0].action = old_action % user
            document.get(selector='form')[0].submit()
            document.get(selector='form')[0].action = old_action
        window._request_login_if_available = _request_login_if_available
        def _request_login_with_code():
            #alert("%s, %s" % (user, blocked))
            #return
            dados = input("Digite modulo/arquivo.py").split("/")
            dados = dados if len(dados) > 1 else dados + ['']
            document["module"].value, document["code"].value = dados
            document["project"].value = "{{ project }}"
            old_action = document.get(selector='form')[0].action
            document.get(selector='form')[0].action = old_action % dados[0]
            document.get(selector='form')[0].submit()
            document.get(selector='form')[0].action = old_action
            # document.forms["select"].action = document.forms["select"].action % dados[0]
            # document.forms["select"].submit()
        window._request_login_with_code = _request_login_with_code
        def _dismiss_error_code():
            document["error"].style.display = "none"
            return False
        window._dismiss_error_code = _dismiss_error_code
        e =Edi()
        '''
        for i in range(20):
            document["topper%d" % i].onclick = e._on_mouse_down
            document["topper%d" % i].onmousemove = e._on_mouse_over
        '''

    </script>
</head>
<body onLoad="brython({debug:1, cache:'browser', static_stdlib_import:true})" background="/images/pipe_back.jpg">
<div id="banner">
]    <div id="mask" style="position:absolute; left:0px; top:0px; background-image: url(images/Bumpplat.jpg); height: 1000px; width: 890px">
        <div id="selector" style="position:float; left:0px; top:0px; padding: 60px">
            <form id="select" method="post" action="/superpython/{{ project }}/%s/___init___.py">
                % for item, (sel, proj) in enumerate(zip(selector, result)):
                <div id="{{ 'topper%d'%item }}"
                     style="background-image: url(images/stripped_paper.png); background-size: 100% 100%; margin: 20px 7px; width: 110px;
                     height: 90px; float: left; text-align:center;"
                     onclick="_request_login_if_available('{{ sel.name }}', {{ [0, 1][sel.picture] }})">
                     <div id="itemimg" style="position:relative; margin-top: 3px; margin-left: 30px; width: 50px; height: 50px;
                                background-image: url(images/{{ project }}.jpg); background-position: {{ proj.ox-45 }}px {{ proj.oy -25 }}px;">

                    </div>
                    <img src="images/spk.png" width="56px" height="60px" alt="{{ sel.name }}"
                         style="text-align:center; position:relative; margin-left: -1px; left: 0px; top: -60px"/>
                     <img src="images/hazard-tread-yellow-black.png" width="100px" alt="{{ sel.name }}"
                         title="{{ sel.name }}" style="opacity:{{ [0,1][sel.picture] }}; position:relative; margin-top: -54px; left: 0px"/>

                    <span style="text-align:center; position:relative; margin-top: 40px; left: 0px; top: -50px">{{ sel.name }}</span>
                </div>
                %end
                <input id="module" name="module" type="hidden"/>
                <input id="code" name="code" type="hidden"/>
                <input id="project" name="project" type="hidden"/>
                <script type="text/javascript">
                function submitform(item)
                {
                  document.getElementById('module').value = item
                  document.forms["select"].submit();
                }

                </script>
            </form>
            <div id="secret"
                 style="position:absolute; left:820px; top:824px; width=50px; min-height=50px"
                 onclick="_request_login_with_code()">O
            </div>
            <div id="error"
                 style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); display: {{ ['none','block'][fault!=None] }};"
                 onclick="_dismiss_error_code()">
                <img src="/images/error.png"></img>
                <img src="/images/rotgears.gif"
                     style="position: fixed; top: 70%; left: 50%; transform: translate(-50%, -50%);"></img>
                <div id="errmsg"
                     style="position: fixed; top: 43%; left: 45%; transform: translate(-43%, -45%);"
                     onclick="_dismiss_error_code()">
                    <span style="color:white">{{ fault }}</span>
                </div>
            </div>
        </div>
        ---
    </div>

</div>

</body>
</html>
        <!--style="position:absolute; left:{{ sel.x+30 }}px; top:{{ sel.y+25 }}px;" onclick="_request_login_if_available('{{ sel.name }}', {{ [0, 1][sel.picture] }})">-->

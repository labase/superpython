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
        <script src="/js/ace/ext-error_marker.js" type="text/javascript" charset="utf-8"></script>
        % for scp in brython:
        <script type="text/javascript" src="{{ scp  }}"></script>
        % end

        <script type="text/python">
            # from {{ "%s.main" % path }} import main
            # main()
            {{ code }}
        </script>
    </head>
    <body onLoad="brython({debug:1, cache:'browser', static_stdlib_import:true})" background="/images/pipe_back.jpg">
           <div id="pydiv"  title="" style="width: {{ dx }}px;
    height: {{ dy }}px;
    position: absolute;
    top:0;
    bottom: 0;
    left: 0;
    right: 0;

    margin: auto;">
                <span style="color:white">LOADING..</span>
           </div>
           <div id="edit"  style="position: absolute; width: 100%; height: 100%;">
                <div id="{{ modulo }}" class="editclass" style="width: 100%; height: 100%;"></div>
           </div>
   </body>
</html>

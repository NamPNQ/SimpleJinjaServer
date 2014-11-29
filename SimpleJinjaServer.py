__author__ = 'nampnq'


import os
import urllib
import posixpath
import sys
import importlib
import mimetypes

from flask import Flask
from flask import render_template_string, abort, escape, render_template, redirect, make_response, send_file

app = Flask(__name__, template_folder=os.getcwd(), static_folder=None)


def translate_path(path):
    """Translate a /-separated PATH to the local filename syntax.

    Components that mean special things to the local file system
    (e.g. drive or directory names) are ignored.  (XXX They should
    probably be diagnosed.)

    """
    # abandon query parameters
    path = path.split('?', 1)[0]
    path = path.split('#', 1)[0]
    path = posixpath.normpath(urllib.unquote(path))
    words = path.split('/')
    words = filter(None, words)
    path = os.getcwd()
    for word in words:
        drive, word = os.path.splitdrive(word)
        head, word = os.path.split(word)
        if word in (os.curdir, os.pardir):
            continue
        path = os.path.join(path, word)
    return path


def guess_type(path):
    """Guess the type of a file.

    Argument is a PATH (a filename).

    Return value is a string of the form type/subtype,
    usable for a MIME Content-type header.

    The default implementation looks the file's extension
    up in the table self.extensions_map, using application/octet-stream
    as a default; however it would be permissible (if
    slow) to look inside the data to make a better guess.

    """

    base, ext = posixpath.splitext(path)
    if ext in extensions_map:
        return extensions_map[ext]
    ext = ext.lower()
    if ext in extensions_map:
        return extensions_map[ext]
    else:
        return extensions_map['']

if not mimetypes.inited:
        mimetypes.init()  # try to read system mime.types
extensions_map = mimetypes.types_map.copy()
extensions_map.update({
    '': 'application/octet-stream',  # Default
    '.py': 'text/plain',
    '.c': 'text/plain',
    '.h': 'text/plain',
})


@app.route('/', defaults={'path': '/'})
@app.route('/<path:path>')
def index(path):
    path_orginal = path
    path = translate_path(path_orginal)
    if os.path.isdir(path):
        if not path_orginal.endswith('/'):
            return redirect(path_orginal+'/')
        else:
            try:
                lists = os.listdir(path)
            except os.error:
                abort(404, "No permission to list directory")
                return None
            lists.sort(key=lambda a: a.lower())
            lists_path = {}
            for name in lists:
                fullname = os.path.join(path, name)
                displayname = linkname = name
                # Append / for directories or @ for symbolic links
                if os.path.isdir(fullname):
                    displayname = name + "/"
                    linkname = name + "/"
                if os.path.islink(fullname):
                    displayname = name + "@"
                    # Note: a link to a directory displays with @ and links with /
                lists_path.update({urllib.quote(linkname): escape(displayname)})
            displaypath = escape(urllib.unquote(path_orginal))
            template = '''
            <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html>
            <title>Directory listing for {{displaypath}}</title>
            <body>
            <h2>Directory listing for {{displaypath}}</h2>
            <hr>
            <ul>
            {% for name in lists %}
                <li><a href="{{ name }}">{{lists[name]}}</a>
            {% endfor %}
            </ul>
            <hr>
            </body>
            </html>
            '''

            return render_template_string(template, displaypath=displaypath, lists=lists_path)
    ctype = guess_type(path)
    if ctype.startswith('text/'):
        return make_response(render_template(path_orginal),200,{'Content-Type': ctype})
    return send_file(path, mimetype=ctype)


def test(port=5000, debug=False, helper=None):
    if helper:
        mod = importlib.import_module(helper)
        if hasattr(mod, 'add_helpers'):
            print '[INFO] Log helper successfully.'
            mod.add_helpers(app)

    app.jinja_env.cache = {}
    app.run(port=port, debug=debug, use_reloader=False)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        test(int(sys.argv[1]))
    elif len(sys.argv) == 3:
        test(int(sys.argv[1]), sys.argv[2].lower() == "true")
    elif len(sys.argv) == 4:
        test(int(sys.argv[1]), sys.argv[2].lower() == "true", sys.argv[3])
    else:
        test()

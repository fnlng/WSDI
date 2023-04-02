import json
from flask import Flask, Blueprint


from .registry import registry



root_folder = r'C:\Users\fnlng\Desktop\pyp'
linux_folder = r'/run/media/fnlng/Windows/Users/fnlng/Desktop/pyp'
# root_folder = linux_folder


def init_app():
    app = Flask("WSI", 
                static_folder='static', static_url_path=None,
            )
    app.jinja_env.variable_start_string = '{['
    app.jinja_env.variable_end_string = ']}'
    app.jinja_env.line_statement_prefix = '//%'
    app.jinja_env.line_comment_prefix = '//#'
    app.config['imgtype'] = {'png', 'jpg', 'jpeg', 'jfif', 'gif', 'webp', 'bmp'}
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

    # Blueprint: `name` ex: app.py - app, `import_name` usually __name__
    bp = Blueprint('app', __name__)
    app.register_blueprint(bp)
    
    return app

def create_app(debug=False):
    
    app = registry(init_app(), root_folder=root_folder)
    
    return app


if __name__ == '__main__':
    debug = True
    
    app = create_app(debug)
    
    app.run(host='0.0.0.0', port=8000, debug=debug)


    # from waitress import serve
    # serve(app, listen='*:8000')

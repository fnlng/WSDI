import asyncio
import os
from flask import (
    send_from_directory, url_for, redirect, render_template, request, g
)
from markupsafe import escape
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import urllib
from urllib.parse import quote, unquote


def registry(app: "Flask", **context) -> "Flask":
    
    root_folder = context.get('root_folder')
    if not root_folder:
        root_folder = os.getcwd()

    @app.route('/<string:filename>', defaults={'folder': ''})
    @app.route("/<path:folder>/<string:filename>")
    def call(folder, filename):
        folder = os.path.join(root_folder, folder)
        paths = ['/'] + folder.split('/') + [filename]
        print('get the file', folder + '/' + filename)
        # raise Exception

        return send_from_directory(folder, filename)

    @app.route('/', defaults={"folder": ''})
    @app.route("/<path:folder>/")
    def file_list_html(folder):
        localFolder = os.path.join(root_folder, folder)
        paths = folder.split('/')
        print('get the folder', folder if folder else '/')
        
        # file_queue = asyncio.Queue(10)
        # dir_queue = asyncio.Queue(50)
        file_list = []
        dir_list = []
        for filename in os.listdir(localFolder):
            link = filename
            if os.path.isdir(os.path.join(localFolder, filename)):
                link += '/'
                dirDict = {
                    'name': link,
                    'link': quote(link),
                    'type': 'dir'
                }
                dir_list.append(dirDict)
                # dir_queue.put(dirDict)
            else:
                fileDict = {
                    'name': link,
                    'link': quote(link),
                    'type': '' if '.' not in filename else filename.rsplit('.', 1)[1].lower()
                }
                file_list.append(fileDict)
                # file_queue.put(fileDict)
        
        # file_list = [file_queue.get() for _ in range(file_queue.maxsize)]
        # dir_list = [dir_queue.get() for _ in range(dir_queue.maxsize)]
        return render_template('index.html', dirlist=dir_list, filelist=file_list, paths=paths)


    @app.route('/putfile', defaults={'folder': ''}, methods=['GET', 'POST'])
    @app.route('/<path:folder>/putfile', methods=['GET', 'POST'])
    def upload(folder):
        localFolder = os.path.join(root_folder, folder)
        if request.method == 'POST':
            for f in request.files.values():
                if f.filename == '':
                    continue
                dest = os.path.join(localFolder, secure_filename(f.filename))
                f.save(dest)
                ic(f'file saved in: {dest}')
                
            return redirect(url_for('file_list_html', folder=folder))
        return render_template('upload.html')
    
    return app

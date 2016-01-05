#!flask/bin/python
# Author: Johan Beekhuizen, Deltares
# This work is based on the Flask Upload Tool by Ngo Duy Khanh (https://github.com/ngoduykhanh/flask-file-uploader)
# which is based on the jQuery-File-Upload (https://github.com/blueimp/jQuery-File-Upload/)

import os
import simplejson
from flask import Flask, request, render_template, session, redirect, url_for, flash, send_from_directory
#from flask.ext.bootstrap import Bootstrap      # gives warning in pycharm?? can't be found
from flask_bootstrap import Bootstrap
#from werkzeug import secure_filename           # gives warning in pycharm?? can't be found
from werkzeug.utils import secure_filename
from lib.upload_file import uploadfile
import pysvn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfhlklasfjka'

my_dir = os.path.dirname(__file__)
app.config['UPLOAD_FOLDER'] = app.config['UPLOAD_FOLDER'] = os.path.join(my_dir, 'static/repos')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1024 * 1024

# not used at the moment; all files are ok
#ALLOWED_EXTENSIONS = set(['7z', 'pdf', 'txt', 'gif', 'png', 'jpg', 'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx'])
IGNORED_FILES = set(['.gitignore'])

bootstrap = Bootstrap(app)

# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filename):
    """
    If file exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i = i + 1

    return filename


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        #print (vars(objectvalue))

        if file:
            filename = secure_filename(file.filename)
            filename = gen_file_name(filename)
            mimetype = file.content_type

            #if not allowed_file(file.filename):
            #    result = uploadfile(name=filename, type=mimetype, size=0, not_allowed_msg="Filetype not allowed")
            #else:

            # save file to disk
            uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(uploaded_file_path)

            # get file size after saving
            size = os.path.getsize(uploaded_file_path)

            # return json for js call back
            result = uploadfile(name=filename, type=mimetype, size=size)


            # commit file
            fileOK = True

            #TODO: Check if file is OK for committing to repository
            if fileOK:
                client = pysvn.Client()
                client.add(uploaded_file_path)
                commitMessage = 'Added ' + uploaded_file_path + ' to the repository'
                client.checkin(app.config['UPLOAD_FOLDER'], commitMessage)

                #TODO: add message when file added succesfully. Redirect_url does not work; gives " SyntaxError: Unexpected token <"
                #flash("File uploaded succesfully; added to the repository")
                #return redirect(url_for('index'))

            else:
                # file is not OK, delete the file
                os.remove(uploaded_file_path)

                #flash("File not OK: deleted from the upload server")
                #return redirect(url_for('index'))


            return simplejson.dumps({"files": [result.get_file()]})


    if request.method == 'GET':
        # get all file in ./data directory
        files = [ f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],f)) and f not in IGNORED_FILES ]
        
        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], f))
            file_saved = uploadfile(name=f, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    return redirect(url_for('index'))


@app.route("/delete/<string:filename>", methods=['DELETE'])
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(file_path):
        try:
            client = pysvn.Client()
            client.remove(file_path) #  the file will be removed from the working copy
            commitMessage = 'Removed ' + file_path + ' from the repository'

            #committing the change removes the file from the repository
            client.checkin(app.config['UPLOAD_FOLDER'], commitMessage)

            #os.remove(file_path)   # for non-SVN versions

            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})


@app.route("/data/<string:filename>", methods=['GET'])
def get_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename=filename)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

#!flask/bin/python
# Author: Johan Beekhuizen, Deltares
# This work is based on the Flask Upload Tool by Ngo Duy Khanh (https://github.com/ngoduykhanh/flask-file-uploader)
# which in turn is based on the jQuery-File-Upload (https://github.com/blueimp/jQuery-File-Upload/)

import os
import simplejson
from flask import Flask, request, render_template, session, redirect, url_for, flash, send_from_directory
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from lib.upload_file import uploadfile
#import pysvn
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfhlklasfjka'

my_dir = os.path.dirname(__file__)
app.config['UPLOAD_FOLDER'] = os.path.join(my_dir, 'static/repos')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1024 * 1024
app.config['USE_REPOSITORY'] = False


# not used at the moment; all files are ok
#ALLOWED_EXTENSIONS = set(['7z', 'pdf', 'txt', 'gif', 'png', 'jpg', 'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx'])
IGNORED_FILES = set(['.gitignore'])

bootstrap = Bootstrap(app)

# set up logging
logFile = os.path.join(my_dir, 'datauploadtool.log')
file_handler = RotatingFileHandler(logFile, 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.info('Data Upload Tool startup')


# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def gen_file_name(dataset, filename):
    """
    If file exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], dataset, filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i = i + 1

    return filename


@app.route("/createdataset", methods=['POST'])
def createdataset():

    fullpath = os.path.join(app.config['UPLOAD_FOLDER'], request.form['datasetname'])

    if os.path.exists(fullpath):
        #return simplejson.dumps({"Warning: ": "Dataset name already in use"})
        app.logger.info('Dataset will be stored in existing folder: ' + fullpath)
        #return render_template('main.html', datasetfolder=request.form['datasetname'])
        return redirect(url_for('main', dataset=request.form['datasetname']))

    else:   # create the dataset folder
        os.makedirs(fullpath)

        app.logger.info('Dataset will be stored in: ' + fullpath)
        #return render_template('main.html', datasetfolder=request.form['datasetname'])
        return redirect(url_for('main', dataset=request.form['datasetname']))


@app.route("/main/<dataset>")
def main(dataset):
    return render_template('main.html', datasetfolder=dataset)


@app.route("/main/upload", methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        file = request.files['file']

        # get the folder
        dataset = request.form['dataset']

        if file:
            filename = secure_filename(file.filename)
            filename = gen_file_name(dataset, filename)
            mimetype = file.content_type

            #if not allowed_file(file.filename):
            #    result = uploadfile(name=filename, type=mimetype, size=0, not_allowed_msg="Filetype not allowed")
            #else:

            # save file to disk
            try:
                uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], dataset, filename)
                file.save(uploaded_file_path)
                # get file size after saving
                size = os.path.getsize(uploaded_file_path)
            except:
                errorMessage = 'Error saving file: ' + filename + ' to working copy'
                app.logger.error(errorMessage)
                return simplejson.dumps({"Error: ": errorMessage})

            app.logger.info('File: ' + filename + ' saved succesfully in working copy')


            # # Store file in repository
            # if app.config['USE_REPOSITORY']:
            #
            #     # commit file
            #     fileOK = True
            #     #TODO: Check if file is OK for committing to repository
            #
            #     if fileOK:
            #
            #         try:
            #             client = pysvn.Client()
            #             client.add(uploaded_file_path)
            #             commitMessage = 'Added ' + uploaded_file_path + ' to the repository'
            #             client.checkin(app.config['UPLOAD_FOLDER'], commitMessage)
            #
            #             #TODO: add message when file added succesfully. Redirect_url does not work; gives " SyntaxError: Unexpected token <"
            #             #flash("File uploaded succesfully; added to the repository")
            #             #return redirect(url_for('index'))
            #
            #         except:
            #             errorMessage = 'Error committing file: ' + filename + ' to repository'
            #             app.logger.error(errorMessage)
            #             return simplejson.dumps({"Error: ": errorMessage})
            #
            #         app.logger.info('File: ' + filename + ' committed to repository')
            #
            #     else:
            #         # file is not OK, delete the file
            #         os.remove(uploaded_file_path)
            #         errorMessage = 'File: ' + filename + ' is not suitable for committing to repository'
            #         app.logger.error(errorMessage)
            #         return simplejson.dumps({"Error: ": errorMessage})
            #
            #         #flash("File not OK: deleted from the upload server")
            #         #return redirect(url_for('index'))


            # return json for js call back
            result = uploadfile(name=filename, dataset=dataset, type=mimetype, size=size)
            return simplejson.dumps({"files": [result.get_file()]})


    if request.method == 'GET':
        # get all file in ./data directory
        dataset = request.args['dataset']
        datasetUrl = os.path.join(app.config['UPLOAD_FOLDER'], dataset)

        files = [ f for f in os.listdir(datasetUrl) if os.path.isfile(os.path.join(datasetUrl, f)) and f not in IGNORED_FILES ]

        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(datasetUrl, f))
            file_saved = uploadfile(name=f, dataset=dataset, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    return redirect(url_for('index'))


@app.route("/main/delete/<path:path>", methods=['DELETE'])
def delete(path):

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], path)

    if os.path.exists(file_path):
        try:

            # if app.config['USE_REPOSITORY']:
            #     client = pysvn.Client()
            #     client.remove(file_path) #  the file will be removed from the working copy
            #     commitMessage = 'Removed ' + file_path + ' from the repository'
            #
            #     #committing the change removes the file from the repository
            #     client.checkin(app.config['UPLOAD_FOLDER'], commitMessage)
            # else:
            #     os.remove(file_path)   # for non-SVN versions

            os.remove(file_path)

        except:
            app.logger.error("Failed to delete: " + path)
            return simplejson.dumps({path: 'False'})

        app.logger.info("Deleted file: " + path + " succesfully")
        return simplejson.dumps({path: 'True'})


@app.route("/main/data/<path:path>", methods=['GET'])
def get_file(path):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename=path)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()

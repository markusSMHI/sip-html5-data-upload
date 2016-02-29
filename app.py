#!flask/bin/python
# Author: Johan Beekhuizen, Deltares
# This work is based on the Flask Upload Tool by Ngo Duy Khanh (https://github.com/ngoduykhanh/flask-file-uploader)
# which in turn is based on the jQuery-File-Upload (https://github.com/blueimp/jQuery-File-Upload/)

import os
import simplejson
from flask import Flask, jsonify, request, render_template, session, redirect, url_for, flash, send_from_directory
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from lib.upload_file import uploadfile
#import pysvn   # used for version control
import logging
from logging.handlers import RotatingFileHandler
import json
import zipfile
import jsonurl
import time
import functions
import threddsclient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfhlklasfjka'
my_dir = os.path.dirname(__file__)

app.config['DEVELOP'] = True

if app.config['DEVELOP']:
    app.config['BASE_UPLOAD_FOLDER'] = os.path.join(my_dir, 'static/repos')  # FOR DEVELOPMENT
else:
    app.config['BASE_UPLOAD_FOLDER'] = os.path.join('/data')  # FOR SERVER

if app.config['DEVELOP']:
    app.config['THREDDS_SERVER'] = "http://dl-ng003.xtr.deltares.nl/thredds/catalog/thredds/thredds" #os.path.join(my_dir, 'static/repos')
else:
    app.config['THREDDS_SERVER'] = "http://dl-ng003.xtr.deltares.nl/thredds/catalog/thredds/thredds"

app.config['MAX_CONTENT_LENGTH'] = 99 * 1000 * 1024 * 1024
app.config['USE_REPOSITORY'] = False

# not used at the moment; all files are ok
ALLOWED_THREDDS_EXTENSIONS = set(['nc'])
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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_THREDDS_EXTENSIONS

def gen_file_name(fullpath, filename):
    """
    If file exist already, rename it and return a new name
    """
    i = 1
    while os.path.exists(os.path.join(fullpath, filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i = i + 1

    return filename


@app.route("/zip", methods=['POST'])
def zip():

    jsonString = request.data
    jsonDict = json.loads(jsonString)

    selectedFiles = jsonDict['files']
    zipFilename = jsonDict['zipfilename']

    #CHECK IF THERE IS A DATASET KEY
    # for key in filesDict.keys():
    #     filename, fileExtension = os.path.splitext(filesDict[key])
    #     if fileExtension == '.zip':
    #         flash("No .zip files allowed to zip. Please select only non-zip files.")
    #         return simplejson.dumps({"Error": "No zip files allowed"})


    if len(selectedFiles) > 0:

        servertype = ""
        datasetname = ""

        for key in selectedFiles.keys():
            servertype = selectedFiles[key].split('/')[0]
            datasetname = selectedFiles[key].split('/')[1]
            break
        datasetUrl = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetname)


        # Open a zip file
        zipPath = os.path.join(datasetUrl, "{}.zip".format(zipFilename))
        zf = zipfile.ZipFile(zipPath, 'w')

        # write all selected files to the zip file
        for key in selectedFiles.keys():
            #datasets.append(selectedFiles[key])
            filename = os.path.join(app.config['BASE_UPLOAD_FOLDER'], selectedFiles[key])
            arcName = selectedFiles[key]
            zf.write(filename, arcName)

        zf.close()

        # delete all the zipped files
        for key in selectedFiles.keys():
            filename = os.path.join(app.config['BASE_UPLOAD_FOLDER'], selectedFiles[key])
            os.remove(filename)

        return simplejson.dumps({"files": selectedFiles})

    else:
        flash("No files selected. Please select the files to zip using the checkboxes on the right.")
        return simplejson.dumps({"Error": "No file selected"})


    #region oldcode
    # return json for js call back
    #time.sleep(1)

    # files = [ f for f in os.listdir(datasetUrl) if os.path.isfile(os.path.join(datasetUrl, f)) and f not in IGNORED_FILES ]
    #
    # file_display = []
    #
    # for f in files:
    #     size = os.path.getsize(os.path.join(datasetUrl, f))
    #     file_saved = uploadfile(name=f, servertype=servertype, dataset=datasetname, size=size)
    #     file_display.append(file_saved.get_file())

    #return simplejson.dumps({"files": file_display})
    #return redirect(url_for('selectServer'))
    #endregion


@app.route("/submitfiles", methods=['GET', 'POST'])
def submitFiles():

    datasetname = request.form['datasetname']
    servertype = request.form['servertype']

    #region oldcode
    # datasetUrl = os.path.join(app.config['BASE_UPLOAD_FOLDER'], dataset)

    # files = [ f for f in os.listdir(datasetUrl) if os.path.isfile(os.path.join(datasetUrl, f)) and f not in IGNORED_FILES ]
    #
    # result = {}
    # fileList = []
    #
    # for f in files:
    #     fileInfo = {}
    #     fileInfo['url'] = os.path.join(request.url_root, 'data', dataset, f)
    #     fileInfo['name'] = f
    #     fileInfo['size_KB'] = os.path.getsize(os.path.join(datasetUrl, f)) / 1000.00
    #     fileList.append(fileInfo)
    #
    # result['files'] = fileList
    # result['dataset'] = os.path.join(request.url_root, 'data', dataset)

    #return simplejson.dumps(result)
    #endregion

    if request.form['submitButton'] == 'previous':
        return redirect('/?datasetname=' + datasetname)

    if request.form['submitButton'] == 'next':

        link = ""

        datasetUrl = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetname)
        files = [ f for f in os.listdir(datasetUrl) if os.path.isfile(os.path.join(datasetUrl, f)) and f not in IGNORED_FILES ]

        result = {}
        result['name'] = datasetname

        if len(files) > 0:
            if len(files) == 1:
                result['function'] = 'download'
                filename, fileExtension = os.path.splitext(f)

                if servertype == 'regular':
                    if fileExtension == ".zip":
                        result['format'] = 'application/zip'

                    result['link'] = os.path.join(request.url_root, 'data', servertype, datasetname, f)

                if servertype == 'thredds':
                    downloadUrl = os.path.join(app.config['THREDDS_SERVER'], datasetname, 'catalog.xml')

                    # use '/'.join instead of os.path.join because the threddsclient apparently can't handle the result of the os.path.join..
                    result['link'] = threddsclient.download_urls('/'.join((app.config['THREDDS_SERVER'], datasetname, 'catalog.xml')))[0]
                    result['serviceurl'] = threddsclient.download_urls('/'.join((app.config['THREDDS_SERVER'], datasetname, 'catalog.xml')))[0]
                    result['servicetype'] = 'OPeNDAP'

            if len(files) > 1:
                result['function'] = 'information'

                if servertype == 'regular':
                    result['link'] = os.path.join(request.url_root, 'data', servertype, datasetname)

                if servertype == 'thredds':
                    result['link'] = os.path.join(app.config['THREDDS_SERVER'], datasetname, 'catalog.html')

            queryString = jsonurl.query_string(result)
            url = "http://switchon.cismet.de/open-data-registration-snapshot/#?" + queryString
            return redirect(url)
        else:
            flash("Please upload at least one file")
            return redirect(url_for('uploadData'))


# accessed from the 'selectServer' page
@app.route("/uploaddata", methods=['GET', 'POST'])
def uploadData():

    #region OLD CODE
    # r =  request
    #
    # if request.method == 'POST':
    #     datasetname = request.form['datasetname']
    #     servertype = request.form['server'] # default value; can be 'regular', 'thredds' or 'geoserver'
    #
    #     # create the dataset folder in the folder of the servertype; if name already taken, increment foldername
    #     fullpath = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetname)
    #
    #     n = 1
    #     orig_datasetname = datasetname
    #     while os.path.exists(fullpath):
    #         datasetname = orig_datasetname + str(n)
    #         fullpath = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetname)
    #         n += 1
    #
    #     os.makedirs(fullpath)
    #     app.logger.info('Dataset will be stored in: ' + fullpath)
    #
    #     # set cookies (used for page refresh)
    #     session['DATASETNAME'] = datasetname
    #     session['SERVERTYPE'] = servertype
    #
    #     return render_template('upload.html', servertype=servertype, datasetname=datasetname)
    #
    # if request.method == 'GET':
    #endregion

    servertype = session['SERVERTYPE']
    datasetname = session['DATASETNAME']

    return render_template('upload.html', servertype=servertype, datasetname=datasetname)


# accessed from the 'selectServer' page
@app.route("/createfolder", methods=['GET', 'POST'])
def createFolder():

    datasetname = request.form['datasetname']
    servertype = request.form['server'] # default value; can be 'regular', 'thredds' or 'geoserver'

    # create the dataset folder in the folder of the servertype; if name already taken, increment foldername
    fullpath = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetname)

    n = 1
    orig_datasetname = datasetname
    while os.path.exists(fullpath):
        datasetname = orig_datasetname + str(n)
        fullpath = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetname)
        n += 1

    os.makedirs(fullpath)
    app.logger.info('Dataset will be stored in: ' + fullpath)

    # set cookies (used for page refresh)
    session['DATASETNAME'] = datasetname
    session['SERVERTYPE'] = servertype

    return redirect(url_for('uploadData'))


@app.route("/upload", methods=['GET', 'POST'])
def upload():

    r = request

    if request.method == 'POST':
        file = request.files['file']

        datasetname = request.form['datasetname']   # get the name of the dataset (and folder)
        servertype = request.form['servertype']

        fullpath = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetname)

        if file:
            filename = secure_filename(file.filename)
            filename = gen_file_name(fullpath, filename)
            mimetype = file.content_type

            if servertype == 'thredds' and not allowed_file(file.filename):
                result = uploadfile(name=filename, servertype=servertype, dataset=datasetname, type=mimetype, size=0, not_allowed_msg="Filetype not allowed")
                #flash("File type not allowed. Please upload a netcdf (.nc) file.")
            else:
                # save file to disk
                try:
                    uploaded_file_path = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetname, filename)
                    file.save(uploaded_file_path)
                    size = os.path.getsize(uploaded_file_path)                # get file size after saving
                except:
                    errorMessage = 'Error saving file: ' + filename + ' to working copy'
                    app.logger.error(errorMessage)
                    return simplejson.dumps({"Error: ": errorMessage})

                app.logger.info('File: ' + filename + ' saved succesfully in working copy')

                #region Reposcode
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
                #             client.checkin(app.config['BASE_UPLOAD_FOLDER'], commitMessage)
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
                #endregion

                # return json for js call back
                time.sleep(0.2)

                result = uploadfile(name=filename, servertype=servertype, dataset=datasetname, type=mimetype, size=size)

            return simplejson.dumps({"files": [result.get_file()]})


    if request.method == 'GET':
        # get all file in ./data directory
        datasetname = request.args['dataset']
        servertype = request.args['servertype']
        datasetUrl = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetname)

        files = [ f for f in os.listdir(datasetUrl) if os.path.isfile(os.path.join(datasetUrl, f)) and f not in IGNORED_FILES ]

        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(datasetUrl, f))
            file_saved = uploadfile(name=f, servertype=servertype, dataset=datasetname, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})


@app.route('/', methods=['GET'])
def selectServer():

    if request.args.get('datasetname') == None:
        return "Please send a GET request with a parameter datasetname"
    else:
        datasetname = request.args.get('datasetname')
        return render_template('selectserver.html', datasetfolder=datasetname)


@app.route("/data/<servertype>/<datasetname>/")
def downloadDataset(servertype, datasetname):

    result = {}
    result['datasetname'] = datasetname
    result['servertype'] = servertype

    if servertype == 'regular':
        datasetDir = os.path.join(os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetname))

        fileInfoList = []
        files = [ f for f in os.listdir(datasetDir) if os.path.isfile(os.path.join(datasetDir, f)) and f not in IGNORED_FILES ]
        for f in files:
            fileInfo = {}
            fileInfo['size'] = os.path.getsize(os.path.join(datasetDir, f))
            fileInfo['sizeText'] = functions.formatFileSize(fileInfo['size'])
            fileInfo['url'] = os.path.join(request.base_url, f)
            fileInfo['name'] = f

            fileInfoList.append(fileInfo)

        result['files'] = fileInfoList

        return render_template('download.html', result=result)

    if servertype == 'thredds':
        url = os.path.join(app.config['THREDDS_SERVER'], datasetname, 'catalog.html')
        return redirect(url)


@app.route("/data/<path:path>", methods=['GET'])
def downloadFile(path):
    return send_from_directory(os.path.join(app.config['BASE_UPLOAD_FOLDER']), filename=path)


@app.route("/downloadall", methods=['POST'])
def downloadAll():

    datasetname = request.form['datasetname']
    servertype = request.form['servertype']
    #zipFilename = "{}.zip".format(request.form['zipfilename'])
    zipFilename = "allFilesZipped.zip"

    # Test if zip file already exists; if yes, do not zip the file
    fullpath = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetname, zipFilename)
    # n = 1
    # orig_zipFilename = zipFilename
    # while os.path.exists(os.path.join(fullpath, zipFilename)):
    #     zipFilename = orig_zipFilename + str(n)
    #     fullpath = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetname)
    #     n += 1

    if os.path.exists(fullpath) == False:
        datasetDir = os.path.join(os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetname))

        files = [ f for f in os.listdir(datasetDir) if os.path.isfile(os.path.join(datasetDir, f)) and f not in IGNORED_FILES ]

        # Open a zip file
        zipPath = os.path.join(datasetDir, zipFilename)
        zf = zipfile.ZipFile(zipPath, 'w')

        for f in files:
            #datasets.append(selectedFiles[key])
            filename = os.path.join(datasetDir, f)
            arcName = f
            zf.write(filename, arcName)

        zf.close()

    return redirect(os.path.join("/data", servertype, datasetname, zipFilename))

    #return send_from_directory(datasetDir, filename=zipFilename)


if __name__ == '__main__':
    if app.config['DEVELOP']:
        app.run(debug=True)                 # DEVELOPMENT
    else:
        app.run(host='0.0.0.0')            # SERVER


#region Old routes

# @app.route("/uploaddata/<path:path>", methods=['GET'])
# def uploadFile(path):
#     return send_from_directory(os.path.join(app.config['BASE_UPLOAD_FOLDER']), filename=path)
# @app.route("/data/download", methods=['GET'])
# def download():
#
#     r = request
#
#     if request.method == 'GET':
#         # get all file in ./data directory
#         dataset = request.args['dataset']
#         datasetUrl = os.path.join(app.config['BASE_UPLOAD_FOLDER'], dataset)
#
#         files = [ f for f in os.listdir(datasetUrl) if os.path.isfile(os.path.join(datasetUrl, f)) and f not in IGNORED_FILES ]
#
#         file_display = []
#
#         for f in files:
#             size = os.path.getsize(os.path.join(datasetUrl, f))
#             file_saved = uploadfile(name=f, dataset=dataset, size=size)
#             file_display.append(file_saved.get_file())
#
#         return simplejson.dumps({"files": file_display})
#
#     return redirect(url_for('download'))

# @app.route('/')
# def index():
#     return render_template('index.html', fileupload=False)

# @app.route("/createdataset", methods=['GET', 'POST'])
# def createdataset():
#
#     if request.method == 'POST':
#
#         if request.form['submitButton'] == 'previous':
#             url = "http://switchon.cismet.de/open-data-registration-snapshot"
#             return redirect(url)
#
#         if request.form['submitButton'] == 'next':
#             fullpath = os.path.join(app.config['BASE_UPLOAD_FOLDER'], request.form['datasetname'])
#
#             if os.path.exists(fullpath):
#                 app.logger.info('Dataset name already in use')
#                 flash("Dataset name already exists. Please try another name.")
#                 return render_template('index.html', fileupload=False)
#
#             else:   # create the dataset folder
#                 os.makedirs(fullpath)
#                 app.logger.info('Dataset will be stored in: ' + fullpath)
#                 return redirect('data/' + request.form['datasetname'])
#     else:
#         return render_template('index.html', fileupload=False)

# @app.route("/zip", methods=['GET', 'POST'])
# def zip():
#
#     #filesDict = request.args.to_dict(flat=False)   # for using ajax request
#     filesDict = request.form.to_dict(flat=False)
#     datasets = []
#
#     datasetname = ""
#
#     r = request
#
#     for key in filesDict.keys():
#         datasetname = filesDict[key][0].split('/')[0]
#         break
#
#     zipFileName = os.path.join(session['UPLOAD_FOLDER'], datasetname, "testzip.zip")
#     zf = zipfile.ZipFile(zipFileName, 'w')
#
#     for key in filesDict.keys():
#         datasets.append(filesDict[key][0])
#         filename = os.path.join(session['UPLOAD_FOLDER'], filesDict[key][0])
#         arcName = filesDict[key][0]
#         zf.write(filename, arcName)
#
#     zf.close()
#
#     return redirect('data/upload/' + datasetname)

# @app.route("/delete/<path:path>", methods=['DELETE'])
# def delete(path):
#
#     file_path = os.path.join(session['UPLOAD_FOLDER'], path)
#
#     if os.path.exists(file_path):
#         try:#
#             # if app.config['USE_REPOSITORY']:
#             #     client = pysvn.Client()
#             #     client.remove(file_path) #  the file will be removed from the working copy
#             #     commitMessage = 'Removed ' + file_path + ' from the repository'
#             #
#             #     #committing the change removes the file from the repository
#             #     client.checkin(app.config['BASE_UPLOAD_FOLDER'], commitMessage)
#             # else:
#             #     os.remove(file_path)   # for non-SVN versions
#

# @app.route("/uploaddata/<servertype>/<datasetname>")
# def uploadDataset(servertype, datasetname):
#
#     datasetUrl = os.path.join(os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetname))
#
#     result = {}
#     result['datasetname'] = datasetname
#
#     fileInfoList = []
#     files = [ f for f in os.listdir(datasetUrl) if os.path.isfile(os.path.join(datasetUrl, f)) and f not in IGNORED_FILES ]
#     for f in files:
#         fileInfo = {}
#         fileInfo['size'] = os.path.getsize(os.path.join(datasetUrl, f))
#         fileInfo['sizeText'] = functions.formatFileSize(fileInfo['size'])
#         fileInfo['url'] = "{}/{}/{}".format(servertype, datasetname, f)
#         fileInfo['name'] = f
#
#         fileInfoList.append(fileInfo)
#
#     result['files'] = fileInfoList
#
#     return render_template('index.html', servertype=servertype, result=result, datasetfolder=datasetname, serverSelected=True)

# @app.route("/uploaddata/<datasetname>", methods=['GET', 'POST'])
# def selectServer(datasetname):
#     return render_template('index.html', servertype='regular', datasetfolder=datasetname, serverSelected=False)


#@app.route('/selectserver/<datasetname>', methods=['GET', 'POST'])
# def selectServer(datasetname):
#     if request.method == 'GET':
#         return render_template('selectserver.html', datasetfolder=datasetname)
#
#             os.remove(file_path)
#
#         except:
#             app.logger.error("Failed to delete: " + path)
#             return simplejson.dumps({path: 'False'})
#
#         app.logger.info("Deleted file: " + path + " succesfully")
#         return simplejson.dumps({path: 'True'})
#endregion


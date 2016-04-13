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
import requests
from requests.auth import HTTPBasicAuth
from settings import settings
import urllib
import re
from unicodedata import normalize

# used for 'slugify': creating a valid url
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

app = Flask(__name__)
my_dir = os.path.dirname(__file__)
app.config.update(settings)

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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_THREDDS_EXTENSIONS']

def slugify(text, delim=u'_'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))

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

def checkConnection(url, errorMessage):
    try:
        requests.get(url, timeout=1) # try for max 1 second
    except:
        flash(errorMessage)
        app.logger.error(errorMessage)
        return False

    return True

@app.route("/zip", methods=['POST'])
def zip():

    jsonString = request.data
    jsonDict = json.loads(jsonString)

    selectedFiles = jsonDict['files']
    zipFilename = jsonDict['zipfilename']

    if len(selectedFiles) > 0:

        servertype = ""
        datasetFoldername = ""

        for key in selectedFiles.keys():
            servertype = selectedFiles[key].split('/')[0]
            datasetFoldername = selectedFiles[key].split('/')[1]
            break
        #datasetUrl = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetFoldername)
        datasetUrl = '/'.join([app.config['BASE_UPLOAD_FOLDER'], servertype, datasetFoldername])

        # Open a zip file
        zipPath = os.path.join(datasetUrl, "{}.zip".format(zipFilename))
        zf = zipfile.ZipFile(zipPath, 'w')

        # write all selected files to the zip file
        for key in selectedFiles.keys():
            #datasets.append(selectedFiles[key])
            #filename = os.path.join(app.config['BASE_UPLOAD_FOLDER'], selectedFiles[key])
            filename = '/'.join([app.config['BASE_UPLOAD_FOLDER'], selectedFiles[key]])
            arcName = selectedFiles[key]
            zf.write(filename, arcName)

        zf.close()

        # delete all the zipped files
        for key in selectedFiles.keys():
            #filename = os.path.join(app.config['BASE_UPLOAD_FOLDER'], selectedFiles[key])
            filename = '/'.join([app.config['BASE_UPLOAD_FOLDER'], selectedFiles[key]])
            os.remove(filename)

        return simplejson.dumps({"files": selectedFiles})

    else:
        flash("No files selected. Please select the files to zip using the checkboxes on the right.")
        return simplejson.dumps({"Error": "No file selected"})

@app.route("/submitfiles", methods=['GET', 'POST'])
def submitFiles():

    r = request

    # datasetname = request.form['datasetname']
    # datasetname = request.form['datasetname']
    datasetname = session['DATASETNAME']
    datasetFoldername = session['DATASETFOLDERNAME']

    servertype = request.form['servertype']

    if request.form['submitButton'] == 'previous':
        return redirect('/?datasetname=' + datasetFoldername)

    if request.form['submitButton'] == 'next':

        datasetUrl = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetFoldername)
        files = [ f for f in os.listdir(datasetUrl) if os.path.isfile(os.path.join(datasetUrl, f)) and f not in app.config['IGNORED_FILES']]

        # result = {}
        # result['name'] = datasetname

        result = []

        if len(files) > 0:

            if servertype == "regular":

                representation = {}

                if len(files) == 1:
                    filename, fileExtension = os.path.splitext(f)
                    representation['name'] = datasetname
                    representation['description'] = "Regular file download"
                    representation['contentlocation'] = '/'.join([request.headers.environ['HTTP_ORIGIN'], 'data', servertype, datasetFoldername, f])

                    if fileExtension == ".zip":
                        representation['contenttype'] = "application/zip"
                    else:
                        representation['contenttype'] = "application/octet-stream"

                    representation['type'] = "original data"
                    representation['function'] = "download"
                    representation['protocol'] = "WWW:DOWNLOAD-1.0-http--download"

                if len(files) > 1:
                    filename, fileExtension = os.path.splitext(f)
                    representation['name'] = datasetname
                    representation['description'] = "Regular file download"
                    #representation['contentlocation'] = os.path.join(request.url_root, 'data', servertype, datasetFoldername)
                    representation['contentlocation'] = '/'.join([request.headers.environ['HTTP_ORIGIN'], 'data', servertype, datasetFoldername])
                    representation['contenttype'] = "application/octet-stream"

                    if fileExtension == ".zip":
                        representation['format'] = "application/zip"
                    else:
                        representation['format'] = "application/octet-stream"

                    representation['function'] = "information"
                    representation['protocol'] = "WWW:LINK-1.0-http--link"

                result = []
                result.append(representation)



            if servertype == 'thredds':

                # check if thredds server is online
                if (checkConnection(app.config['THREDDS_SERVER'],
                    "Failed to connect to the THREDDS server at " + app.config['THREDDS_SERVER'] + \
                    ". Please contact the system administrator or upload files to the regular server.")) == False:
                    return redirect(url_for('uploadData'))

                 # use '/'.join instead of os.path.join because the threddsclient apparently can't handle the result of the os.path.join..
                threddsCatalog = '/'.join((app.config['THREDDS_SERVER'], datasetFoldername, 'catalog.xml'))
                # threddsCatalog = "http://opendap.deltares.nl/thredds/catalog/opendap/test/DienstZeeland/catalog.xml"
                opendapUrls = threddsclient.opendap_urls(threddsCatalog)

                result = []

                # first store dataset root folder of netcdf
                representation = {}
                representation['name'] = datasetname
                representation['description'] = "Netcdf root directory THREDDS server"
                representation['contentlocation'] = '/'.join((app.config['THREDDS_SERVER'], datasetname, 'catalog.html'))
                representation['contenttype'] = "application/octet-stream"
                representation['type'] = "original data"
                representation['function'] = "information"
                representation['protocol'] = 'WWW:LINK-1.0-http--link'
                result.append(representation)

                for opendapUrl in opendapUrls:

                    filename = opendapUrl.split('/')[-1]
                    representation = {}

                    representation['name'] = filename
                    representation['description'] = "Netcdf file OPeNDAP service"
                    representation['contentlocation'] = opendapUrl
                    representation['contenttype'] = "application/x-netcdf"
                    representation['type'] = "original data"
                    representation['function'] = "service"
                    representation['protocol'] = 'OPeNDAP:OPeNDAP'
                    result.append(representation)

                    representation['name'] = filename
                    representation['description'] = "HTML interface OPeNDAP service"
                    representation['contentlocation'] = opendapUrl + ".html"
                    representation['contenttype'] = "application/x-netcdf"
                    representation['type'] = "original data"
                    representation['function'] = "download"
                    representation['protocol'] = 'OPeNDAP:OPeNDAP'
                    result.append(representation)


            # publish data on geoserver
            if servertype == "geoserver":

                # check if geoserver is online
                if (checkConnection(app.config['GEOSERVER'],
                    "Failed to connect to the geoserver at " + app.config['GEOSERVER'] + \
                    ". Please contact the system administrator or upload files to the regular server.")) == False:
                    return redirect(url_for('uploadData'))

                # create workspace
                r = requests.post(url= app.config['GEOSERVER'] + "/rest/workspaces",
                                 headers={'Content-type':  'text/xml'},
                                 data="<workspace><name>" + datasetFoldername + "</name></workspace>",
                                 auth=HTTPBasicAuth(app.config['GEOSERVER_ADMIN'], app.config['GEOSERVER_PASS']))

                if r.status_code > 299:    # status code of 201 is success; all else is failure
                    app.logger.error("Error in creating geoserver workspace for " + datasetname + "; Status code: " + str(r.status_code))
                    flash("Error in creating workspace on geoserver. Please contact the system administrator or upload the files to the regular server.")
                    return redirect(url_for('uploadData'))

                # Publish shapefile on the geoserver; the datastore is automatically created and has the same name as the dataset + ds
                #TODO: Change to uploaded shapefile location
                r = requests.put(url=app.config['GEOSERVER'] + "/rest/workspaces/" + datasetname + "/datastores/" + datasetname + "_ds/external.shp",
                                 headers={'Content-type': 'text/plain'},
                                 data=settings['GEOSERVER_DATA_DIR'] + "/shapefiles/states.shp",  # CHANGE FOR REAL VERSION
                                 auth=HTTPBasicAuth(app.config['GEOSERVER_ADMIN'], app.config['GEOSERVER_PASS']))

                if r.status_code > 299:
                    app.logger.error("Error in publishing shapefile " + datasetname + " on geoserver; Status code: " + str(r.status_code))
                    flash("Error in publishing shapefile on geoserver. Please contact the system administrator or upload the files to the regular server.")
                    return redirect(url_for('uploadData'))

                result = []

                representation = {}
                representation['name'] = datasetname
                representation['description'] = "WMS service"
                representation['contentlocation'] = app.config['GEOSERVER'] + "/" + datasetFoldername + "/" + "wms?service=WMS&version=1.1.0&request=GetCapabilities"
                representation['contenttype'] = "application/xml"
                representation['type'] = "original data"
                representation['function'] = "service"
                representation['protocol'] = 'OGC:WMS-1.1.1-http-get-capabilities'
                result.append(representation)

                representation = {}
                representation['name'] = datasetname
                representation['description'] = "WFS service"
                representation['contentlocation'] = app.config['GEOSERVER'] + "/" + datasetFoldername + "/" + "ows?service=WFS&version=1.0.0&request=GetCapabilities"
                representation['contenttype'] = "application/xml"
                representation['type'] = "original data"
                representation['function'] = "service"
                representation['protocol'] = "OGC:WFS-1.0.0-http-get-capabilities"
                result.append(representation)

            resultString = json.dumps(result)
            text = urllib.quote_plus(resultString.encode('utf-8'))
            url = "http://switchon.cismet.de/open-data-registration-snapshot/#?representations=" + text
            return redirect(url)

        else:
            flash("Please upload at least one file")
            return redirect(url_for('uploadData'))


# accessed from the 'selectServer' page
@app.route("/uploaddata", methods=['GET', 'POST'])
def uploadData():
    servertype = session['SERVERTYPE']
    datasetname = session['DATASETNAME']
    datasetFoldername = session['DATASETFOLDERNAME']

    return render_template('upload.html', servertype=servertype, datasetname=datasetname, datasetFoldername=datasetFoldername)


# accessed from the 'selectServer' page
@app.route("/createfolder", methods=['GET', 'POST'])
def createFolder():

    datasetname = request.form['datasetname']
    servertype = request.form['server'] # default value; can be 'regular', 'thredds' or 'geoserver'

    datasetFoldername = datasetname     # the dataset folder name must be unique and be allowed as an URL

    # create a valid datasetFoldername for use in an URL
    datasetFoldername = slugify(unicode(datasetFoldername))

    # create the dataset folder in the folder of the servertype; if name already taken, increment foldername
    fullpath = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetFoldername)

    n = 1
    origDatasetFoldername = datasetFoldername
    while os.path.exists(fullpath):
        datasetFoldername = origDatasetFoldername + str(n)
        fullpath = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetFoldername)
        n += 1

    os.makedirs(fullpath)
    app.logger.info('Dataset will be stored in: ' + fullpath)

    # if origDatasetFoldername != datasetFoldername:
    #     message = "Dataset folder name already exists. Dataset will be stored in the folder " + datasetFoldername
    #     flash(message)

    # set cookies (used for page refresh)
    session['DATASETNAME'] = datasetname
    session['DATASETFOLDERNAME'] = datasetFoldername
    session['SERVERTYPE'] = servertype

    return redirect(url_for('uploadData'))


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    '''
    The upload function is called as an AJAX request from within the Upload.html page in order to avoid refreshing the whole page
    when uploading new data.
    '''

    if request.method == 'POST':
        file = request.files['file']

        #datasetname = request.form['datasetname']    # use session stored parameters
        #servertype = request.form['servertype']
        datasetFoldername = session['DATASETFOLDERNAME']   # get the name of the dataset (and folder)
        servertype = session['SERVERTYPE']

        fullpath = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetFoldername)

        if file:
            filename = secure_filename(file.filename)
            filename = gen_file_name(fullpath, filename)
            mimetype = file.content_type

            if servertype == 'thredds' and not allowed_file(file.filename):
                result = uploadfile(name=filename, servertype=servertype, datasetFoldername=datasetFoldername, type=mimetype, size=0, not_allowed_msg="Filetype not allowed")
            else:
                # save file to disk
                try:
                    uploaded_file_path = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetFoldername, filename)
                    file.save(uploaded_file_path)
                    size = os.path.getsize(uploaded_file_path)                # get file size after saving
                except:
                    errorMessage = 'Error saving file: ' + filename + ' to working copy'
                    app.logger.error(errorMessage)
                    return simplejson.dumps({"Error: ": errorMessage})

                app.logger.info('File: ' + filename + ' saved succesfully in working copy')
                time.sleep(0.2)
                result = uploadfile(name=filename, servertype=servertype, datasetFoldername=datasetFoldername, type=mimetype, size=size)

            return simplejson.dumps({"files": [result.get_file()]})


    if request.method == 'GET':
        # get all file in ./data directory
        #datasetFoldername = request.args['datasetFoldername']  # use session stored parameters
        #servertype = request.args['servertype']
        datasetFoldername = session['DATASETFOLDERNAME']
        servertype = session['SERVERTYPE']

        datasetUrl = os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetFoldername)

        files = [ f for f in os.listdir(datasetUrl) if os.path.isfile(os.path.join(datasetUrl, f)) and f not in app.config['IGNORED_FILES']]

        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(datasetUrl, f))
            file_saved = uploadfile(name=f, servertype=servertype, datasetFoldername=datasetFoldername, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})


@app.route('/', methods=['GET'])
def selectServer():

    if request.args.get('datasetname') == None:
        return "Please send a GET request with a parameter datasetname"
    else:
        datasetname = request.args.get('datasetname')
        return render_template('selectserver.html', datasetname=datasetname)


@app.route("/data/<servertype>/<datasetFoldername>/")
def downloadDataset(servertype, datasetFoldername):

    result = {}
    result['datasetFoldername'] = datasetFoldername
    result['servertype'] = servertype

    if servertype == 'regular' or servertype == 'geoserver':
        datasetDir = os.path.join(os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetFoldername))

        fileInfoList = []
        files = [ f for f in os.listdir(datasetDir) if os.path.isfile(os.path.join(datasetDir, f)) and f not in app.config['IGNORED_FILES']]
        for f in files:
            fileInfo = {}
            fileInfo['size'] = os.path.getsize(os.path.join(datasetDir, f))
            fileInfo['sizeText'] = functions.formatFileSize(fileInfo['size'])
            fileInfo['url'] = os.path.join(request.base_url, f)
            fileInfo['name'] = f

            fileInfoList.append(fileInfo)

        result['files'] = fileInfoList

        return render_template('download.html', result=result)

    elif servertype == 'thredds':
        url = os.path.join(app.config['THREDDS_SERVER'], datasetFoldername, 'catalog.html')
        return redirect(url)
    else:
        return "Error: unknown server type"


@app.route("/data/<path:path>", methods=['GET'])
def downloadFile(path):
    return send_from_directory(os.path.join(app.config['BASE_UPLOAD_FOLDER']), filename=path)

@app.route("/downloadallzip/<path:path>", methods=['GET'])
def downloadallzip(path):
    return send_from_directory(os.path.join(app.config['BASE_UPLOAD_FOLDER']), filename=path)


@app.route("/downloadall", methods=['POST'])
def downloadAll():

    servertype = request.form['servertype']
    datasetFoldername = request.form['datasetFoldername']
    zipFilename = "{}{}.zip".format(servertype, datasetFoldername)

    zipFilepath = os.path.join(app.config['BASE_UPLOAD_FOLDER'], app.config['ZIP_DOWNLOAD_ALL_FOLDER'], zipFilename)

    # Test if zip file already exists; if yes, remove this .zip file
    if os.path.exists(zipFilepath):
        os.remove(zipFilepath)

    datasetDir = os.path.join(os.path.join(app.config['BASE_UPLOAD_FOLDER'], servertype, datasetFoldername))

    files = [ f for f in os.listdir(datasetDir) if os.path.isfile(os.path.join(datasetDir, f)) and f not in app.config['IGNORED_FILES']]

    # Open a zip file
    zf = zipfile.ZipFile(zipFilepath, 'w')

    for f in files:
        #datasets.append(selectedFiles[key])
        filename = os.path.join(datasetDir, f)
        arcName = f
        zf.write(filename, arcName)

    zf.close()

    #downloadPath = os.path.join("/downloadallzip", app.config['ZIP_DOWNLOAD_ALL_FOLDER'], zipFilename)
    downloadPath = '/'.join(["downloadallzip", app.config['ZIP_DOWNLOAD_ALL_FOLDER'], zipFilename])
    return redirect(downloadPath)


if __name__ == '__main__':
    if app.config['DEVELOP']:
        app.run(debug=True)                 # DEVELOPMENT
    else:
        app.run(host='0.0.0.0')             # SERVER
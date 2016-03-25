__author__ = 'beekhuiz'


# OLD GEOSERVER SUBMIT

# result['link'] = os.path.join(request.url_root, 'data', servertype, datasetname)
# #result['serviceurl'] = os.path.join(app.config['GEOSERVER'], datasetname, "ows?service=WFS&version=1.0.0&request=GetCapabilities")
# result['serviceurl'] = app.config['GEOSERVER'] + "/" + datasetname + "/" + "wms?service=WMS&version=1.1.0&request=GetCapabilities"
# result['servicetype'] = 'WMS'


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
#         files = [ f for f in os.listdir(datasetUrl) if os.path.isfile(os.path.join(datasetUrl, f)) and f not in app.config['IGNORED_FILES']]
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


# UPLOAD REPOS CODE:

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

# UPLOAD DATA

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


             #region OldGetparameters
        #     # publish data on geoserver
        #     if servertype == "geoserver":
        #
        #         # check if geoserver is online
        #         if (checkConnection(app.config['GEOSERVER'],
        #             "Failed to connect to the geoserver at " + app.config['GEOSERVER'] + \
        #             ". Please contact the system administrator or upload files to the regular server.")) == False:
        #             return redirect(url_for('uploadData'))
        #
        #         result['function'] = 'information'
        #
        #         # create workspace
        #         r = requests.post(url= app.config['GEOSERVER'] + "/rest/workspaces",
        #                          headers={'Content-type':  'text/xml'},
        #                          data="<workspace><name>" + datasetname + "</name></workspace>",
        #                          auth=HTTPBasicAuth(app.config['GEOSERVER_ADMIN'], app.config['GEOSERVER_PASS']))
        #
        #         if r.status_code > 299:    # status code of 201 is success; all else is failure
        #             app.logger.error("Error in creating geoserver workspace for " + datasetname + "; Status code: " + str(r.status_code))
        #             flash("Error in creating workspace on geoserver. Please contact the system administrator or upload the files to the regular server.")
        #             return redirect(url_for('uploadData'))
        #
        #         # Publish shapefile on the geoserver; the datastore is automatically created and has the same name as the dataset + ds
        #         #TODO: Change to uploaded shapefile location
        # #         r = requests.put(url=app.config['GEOSERVER'] + "/rest/workspaces/" + datasetname + "/datastores/" + datasetname + "_ds/external.shp",
        # #                          headers={'Content-type': 'text/plain'},
        # #                          data=settings['GEOSERVER_DATA_DIR'] + "/shapefiles/states.shp",  # CHANGE FOR REAL VERSION
        # #                          auth=HTTPBasicAuth(app.config['GEOSERVER_ADMIN'], app.config['GEOSERVER_PASS']))
        # #
        # #         if r.status_code > 299:
        # #             app.logger.error("Error in publishing shapefile " + datasetname + " on geoserver; Status code: " + str(r.status_code))
        # #             flash("Error in publishing shapefile on geoserver. Please contact the system administrator or upload the files to the regular server.")
        # #             return redirect(url_for('uploadData'))
        # #
        # #         result['link'] = os.path.join(request.url_root, 'data', servertype, datasetname)
        # #         #result['serviceurl'] = os.path.join(app.config['GEOSERVER'], datasetname, "ows?service=WFS&version=1.0.0&request=GetCapabilities")
        # #         result['serviceurl'] = app.config['GEOSERVER'] + "/" + datasetname + "/" + "wms?service=WMS&version=1.1.0&request=GetCapabilities"
        # #         result['servicetype'] = 'WMS'
        # #
        # #
        # #     else:   # either thredds or regular server; make distinction between 1 or more files
        # #
        # #         if len(files) == 1:
        # #             result['function'] = 'download'
        # #             filename, fileExtension = os.path.splitext(f)
        # #
        # #             if servertype == 'regular':
        # #                 if fileExtension == ".zip":
        # #                     result['format'] = 'application/zip'
        # #
        # #                 result['link'] = os.path.join(request.url_root, 'data', servertype, datasetname, f)
        # #
        # #             if servertype == 'thredds':
        # #
        # #                 # check if geoserver is online
        # #                 if (checkConnection(app.config['THREDDS_SERVER'],
        # #                     "Failed to connect to the THREDDS server at " + app.config['THREDDS_SERVER'] + \
        # #                     ". Please contact the system administrator or upload files to the regular server.")) == False:
        # #                     return redirect(url_for('uploadData'))
        # #
        # #                  # use '/'.join instead of os.path.join because the threddsclient apparently can't handle the result of the os.path.join..
        # #                 downloadUrl = '/'.join((app.config['THREDDS_SERVER'], datasetname, 'catalog.xml'))
        # #
        # #                 result['link'] = threddsclient.opendap_urls(downloadUrl)[0] + ".html"
        # #                 result['serviceurl'] = threddsclient.opendap_urls(downloadUrl)[0]
        # #                 result['servicetype'] = 'OPeNDAP'
        # #
        # #         if len(files) > 1:
        # #             result['function'] = 'information'
        # #
        # #             if servertype == 'regular':
        # #                 result['link'] = os.path.join(request.url_root, 'data', servertype, datasetname)
        # #
        # #             if servertype == 'thredds':
        # #                 # check if geoserver is online
        # #                 if (checkConnection(app.config['THREDDS_SERVER'],
        # #                     "Failed to connect to the THREDDS server at " + app.config['THREDDS_SERVER'] + \
        # #                     ". Please contact the system administrator or upload files to the regular server.")) == False:
        # #                     return redirect(url_for('uploadData'))
        # #
        # #                 result['link'] = os.path.join(app.config['THREDDS_SERVER'], datasetname, 'catalog.html')
        # endregion
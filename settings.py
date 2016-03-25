__author__ = 'beekhuiz'
import os

settings = {}
settings['SECRET_KEY'] = 'dfhlklasfjka'
my_dir = os.path.dirname(__file__)
settings['DEVELOP'] = True
   
settings['ZIP_DOWNLOAD_ALL_FOLDER']= 'zippeddownload'
settings['THREDDS_SERVER'] = "http://dl-ng003.xtr.deltares.nl/thredds/catalog/thredds/thredds" #os.path.join(my_dir, 'static/repos')
settings['GEOSERVER'] = "http://192.168.66.132:8080/geoserver"
settings['GEOSERVER_ADMIN'] = "admin"
settings['GEOSERVER_PASS'] = "geoserver"
settings['GEOSERVER_DATA_DIR'] = "file:////var/lib/tomcat/webapps/geoserver/data/data"  # CHANGE FOR REAL VERSION

if settings['DEVELOP']:
    settings['BASE_UPLOAD_FOLDER'] = os.path.join(my_dir, 'static/repos')  # FOR DEVELOPMENT
else:
    settings['BASE_UPLOAD_FOLDER'] = '/data'  # FOR SERVER

settings['MAX_CONTENT_LENGTH'] = 99 * 1000 * 1024 * 1024
settings['USE_REPOSITORY'] = False

# not used at the moment; all files are ok
settings['ALLOWED_THREDDS_EXTENSIONS'] = set(['nc'])
settings['IGNORED_FILES'] = set(['.gitignore'])

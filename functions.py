__author__ = 'beekhuiz'

def formatFileSize(bytes):
    if bytes >= 1000000000:
        return "{0:.2f}".format(float(bytes) / 1000000000.0) + ' GB'

    if bytes >= 1000000:
        return "{0:.2f}".format(float(bytes) / 1000000.0) + ' MB'

    return "{0:.2f}".format(float(bytes) / 1000.0) + ' KB'




# TEST THREDDS CRAWLER

# from thredds_crawler.crawl import Crawl
# c = Crawl("http://dl-tc008.xtr.deltares.nl:8080/thredds/catalog/thredds/catalog.xml", select=[".*"])
# print c.datasets

# THREDDSCLIENT
# import threddsclient
# urls = threddsclient.download_urls('http://dl-tc008.xtr.deltares.nl:8080/thredds/catalog/thredds/netcdftest/catalog.xml')
# urls = threddsclient.opendap_urls('http://dl-tc008.xtr.deltares.nl:8080/thredds/catalog/thredds/netcdftest/catalog.xml')


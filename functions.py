__author__ = 'beekhuiz'

def formatFileSize(bytes):
    if bytes >= 1000000000:
        return "{0:.2f}".format(float(bytes) / 1000000000.0) + ' GB'

    if bytes >= 1000000:
        return "{0:.2f}".format(float(bytes) / 1000000.0) + ' MB'

    return "{0:.2f}".format(float(bytes) / 1000.0) + ' KB'


import os

class uploadfile():
    def __init__(self, name, datasetFoldername, mimetype=None,size=None, not_allowed_msg=''):
        self.name = name
        self.datasetFoldername = datasetFoldername
        self.mimetype = mimetype
        self.size = size
        self.not_allowed_msg = not_allowed_msg
        self.dir = "{}/{}".format(datasetFoldername, name)
        self.url = "data/{}/{}".format(datasetFoldername, name)

    def get_file(self):
        if self.mimetype != None:
            # POST an normal file
            if self.not_allowed_msg == '':
                return {"name": self.name,
                        "datasetFoldername": self.datasetFoldername,
                        "mimetype": self.mimetype,
                        "size": self.size,
                        "dir": self.dir,
                        "url": self.url,}

            # File type is not allowed
            else:
                return {"error": self.not_allowed_msg,
                        "name": self.name,
                        "datasetFoldername": self.datasetFoldername,
                        "mimetype": self.mimetype,
                        "size": self.size,}
        
        # GET file from disk
        else:
            return {"name": self.name,
                    "datasetFoldername": self.datasetFoldername,
                    "size": self.size,
                    "dir": self.dir,
                    "url": self.url,}

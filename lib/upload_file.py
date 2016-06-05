import os

class uploadfile():
    def __init__(self, name, datasetFoldername, datatype= None, mimetype=None,size=None, not_allowed_msg=''):
        self.name = name
        self.datasetFoldername = datasetFoldername
        self.datatype = datatype
        self.mimetype = mimetype
        self.size = size
        self.not_allowed_msg = not_allowed_msg
        self.dir = "{}/{}".format(datasetFoldername, name)
        self.url = "data/{}/{}".format(datasetFoldername, name)
        self.delete_url = "delete/{}/{}".format(datasetFoldername, name)
        self.delete_type = "DELETE"

    def get_file(self):
        if self.mimetype != None:
            # POST an normal file
            if self.not_allowed_msg == '':
                return {"name": self.name,
                        "datasetFoldername": self.datasetFoldername,
                        "datatype": self.datatype,
                        "mimetype": self.mimetype,
                        "size": self.size,
                        "dir": self.dir,
                        "url": self.url, 
                        "deleteUrl": self.delete_url, 
                        "deleteType": self.delete_type,}

            # File type is not allowed
            else:
                return {"error": self.not_allowed_msg,
                        "name": self.name,
                        "datasetFoldername": self.datasetFoldername,
                        "datatype": self.datatype,
                        "mimetype": self.mimetype,
                        "size": self.size,}
        
        # GET file from disk
        else:
            return {"name": self.name,
                    "datasetFoldername": self.datasetFoldername,
                    "size": self.size,
                    "datatype": self.datatype,
                    "dir": self.dir,
                    "url": self.url, 
                    "deleteUrl": self.delete_url, 
                    "deleteType": self.delete_type,}

import os

class uploadfile():
    def __init__(self, name, servertype, datasetFoldername, type=None, size=None, not_allowed_msg=''):
        self.name = name
        self.servertype = servertype
        self.datasetFoldername = datasetFoldername
        self.type = type
        self.size = size
        self.not_allowed_msg = not_allowed_msg
        self.dir = "{}/{}/{}".format(servertype, datasetFoldername, name)
        self.url = "data/{}/{}/{}".format(servertype, datasetFoldername, name)
        self.delete_url = "delete/{}/{}/{}".format(servertype, datasetFoldername, name)
        self.delete_type = "DELETE"

    def get_file(self):
        if self.type != None:
            # POST an normal file
            if self.not_allowed_msg == '':
                return {"name": self.name,
                        "servertype": self.servertype,
                        "datasetFoldername": self.datasetFoldername,
                        "type": self.type,
                        "size": self.size,
                        "dir": self.dir,
                        "url": self.url, 
                        "deleteUrl": self.delete_url, 
                        "deleteType": self.delete_type,}

            # File type is not allowed
            else:
                return {"error": self.not_allowed_msg,
                        "name": self.name,
                        "servertype": self.servertype,
                        "datasetFoldername": self.datasetFoldername,
                        "type": self.type,
                        "size": self.size,}
        
        # GET file from disk
        else:
            return {"name": self.name,
                    "servertype": self.servertype,
                    "datasetFoldername": self.datasetFoldername,
                    "size": self.size,
                    "dir": self.dir,
                    "url": self.url, 
                    "deleteUrl": self.delete_url, 
                    "deleteType": self.delete_type,}

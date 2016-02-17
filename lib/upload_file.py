import os

class uploadfile():
    def __init__(self, name, servertype, dataset, type=None, size=None, not_allowed_msg=''):
        self.name = name
        self.servertype = servertype
        self.dataset = dataset
        self.type = type
        self.size = size
        self.not_allowed_msg = not_allowed_msg
        self.url = "{}/{}/{}".format(servertype, dataset, name)
        self.delete_url = "delete/{}/{}/{}".format(servertype, dataset, name)
        self.delete_type = "DELETE"

    def get_file(self):
        if self.type != None:
            # POST an normal file
            if self.not_allowed_msg == '':
                return {"name": self.name,
                        "servertype": self.servertype,
                        "dataset": self.dataset,
                        "type": self.type,
                        "size": self.size, 
                        "url": self.url, 
                        "deleteUrl": self.delete_url, 
                        "deleteType": self.delete_type,}

            # File type is not allowed
            else:
                return {"error": self.not_allowed_msg,
                        "name": self.name,
                        "servertype": self.servertype,
                        "dataset": self.dataset,
                        "type": self.type,
                        "size": self.size,}
        
        # GET file from disk
        else:
            return {"name": self.name,
                    "servertype": self.servertype,
                    "dataset": self.dataset,
                    "size": self.size, 
                    "url": self.url, 
                    "deleteUrl": self.delete_url, 
                    "deleteType": self.delete_type,}

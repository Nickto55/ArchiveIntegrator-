import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from CTkMessagebox import CTkMessagebox

from  scr.config_assets.receiver_config import ReceiverConfig



class ConfigArchiveIntegrator:
    def __init__(self):
        self.data_base = ReceiverConfig()
        self.cel_bd = 'ArchiveIntegrator'

    def get_all_config_program(self):
        self.data_base.load()
        return self.data_base.data.get(self.cel_bd, '')

    def set_config_progrm(self,key,data):
        if key in self.data_base.data.get(self.cel_bd,'').keys():
            self.data_base.data[self.cel_bd][key]=data
            self.data_base.save()
            self.data_base.load()

if __name__=="__main__":
    app = ConfigArchiveIntegrator()
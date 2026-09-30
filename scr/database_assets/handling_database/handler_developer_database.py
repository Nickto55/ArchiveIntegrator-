import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scr.database_assets.receiver_db import ReceiverDataBase


class DeveloperDatabase:
    def __init__(self):
        self.data_base = ReceiverDataBase(name_file_db='developer_database.json')
        self.name_dict = 'programs'

    def get_all_db_program(self):
        self.data_base.load()
        return self.data_base.data.get(self.name_dict, '')

    def set_db_progrm(self, key, data):
        if key in self.data_base.data.get(self.name_dict, '').keys():
            self.data_base.data[self.name_dict][key] = data
            self.data_base.save()
            self.data_base.load()

    def get_program_data(self, program_name):
        self.data_base.load()
        return self.data_base.data[self.name_dict].get(program_name, '')

    def set_program_db(
            self
            , name_repo=''
            , name_program=''
            , date_change=''
            , last_version=''
            , git_url=None
    ):
        """
        :param name_repo    :
        :param name_program :
        :param date_change  :
        :param last_version :
        :param git_url      :
        """
        if name_repo in self.data_base.data[self.name_dict].keys():

            bd_name_program = self.data_base.data[self.name_dict][name_repo].get('name', '')
            bd_date_change = self.data_base.data[self.name_dict][name_repo].get('target', '')
            bd_last_version = self.data_base.data[self.name_dict][name_repo].get('date relise', '')
            bd_git_url = self.data_base.data[self.name_dict][name_repo].get('git url', '')

            if name_program == '' and bd_name_program != '': name_program = bd_name_program
            if date_change == '' and bd_date_change != '': date_change = bd_date_change
            if last_version == '' and bd_last_version != '': last_version = bd_last_version
            if git_url is None and not bd_git_url is None: last_version = bd_last_version

        data_program = {
            f'{name_repo}': {
                'name': name_program
                , 'date change': date_change
                , 'last version': last_version
                , 'git url': git_url
            }
        }

        self.data_base.data[self.name_dict].update(data_program)
        self.data_base.save()
        self.data_base.load()


if __name__ == "__main__":
    app = DeveloperDatabase()

    print(app.get_program_data(program_name='dskljtest'))

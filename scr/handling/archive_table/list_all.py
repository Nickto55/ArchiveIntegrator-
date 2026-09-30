import os
import sys
import git

import pandas as pd

from sys import version_info

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scr.excel_assets.readers.excel_reader import ExcelReader
from scr.config_assets.handling_config.handler_program_config import ConfigMainProgram
from scr.database_assets.handling_database.handler_db_program import DataBaseProgramData
from scr.config_assets.handling_config.handler_archive_integrator import ConfigArchiveIntegrator


def get_git_remote_url_gitpython(local_path):
    try:
        repo = git.Repo(local_path)
        remote_url = repo.remotes.origin.url
        return remote_url
    except git.exc.InvalidGitRepositoryError:
        return "Ошибка: Указанная директория не является Git-репозиторием."
    except AttributeError:
        return "Ошибка: У репозитория нет удаленного источника (remote) с именем 'origin'."


class HandlerMainSheet:
    def __init__(self, path_to_tabel, config_archive_integrator=None):
        self.config_archive_integrator = config_archive_integrator if not pd.isna(
            config_archive_integrator) else ConfigArchiveIntegrator()
        self.db_program_data = DataBaseProgramData()
        self.path_to_tabel = path_to_tabel
        self.config_program = ConfigMainProgram()

        self.data_main_list_table = {}

    def main(self):
        self.load_main_list()
        self.generated_list_program()

        return self.generete_sheet()

    def get_data_main_list(self):
        self.load_main_list()
        return self.data_main_list_table

    def load_main_list(self):
        if pd.isna(self.path_to_tabel): print('list_all, load_main_list, Программа передала пустой  self.path_to_table')
        reader = ExcelReader(self.path_to_tabel, sheet_name='All programs')
        self.data_main_list_table = reader.get_dict_all_data()

    def generated_list_program(self):
        self.load_main_list()
        for num_row, row in self.data_main_list_table.items():
            name_program = row.get('Название программы', '')
            version_program = row.get('Версия')
            name_repo = os.path.basename(row.get('Ком', '')).replace('.git', '')
            if pd.isna(name_repo) or name_repo == '':
                name_repo = row.get('Наим. Репо.', '')

            try:
                url = get_git_remote_url_gitpython(
                    os.path.join(self.config_archive_integrator.get_all_config_program().get('path to project dir', ''),
                                 name_repo))
            except:
                url = ''

            comment_row = row.get('Ком.', '')
            if pd.isna(comment_row): comment_row = ''
            target = row.get('Цель выполнения программы', '')
            if pd.isna(target): target = ''
            date_relise = row.get('Дата разработки', '')
            if pd.isna(date_relise): date_relise = ''

            self.db_program_data.set_program_db(
                name_repo=name_repo
                , program_name=name_program
                , comment=comment_row
                , last_version=version_program
                , url_git=url
                , target=target
                , date_relise=date_relise
            )

    def generete_sheet(self):
        data_return = {}
        data_db = self.db_program_data.get_all_db_program()

        for num_row_db, row_db in data_db.items():
            row_return = {
                'Название программы'            : row_db.get('name', '')
                , 'Наим. Репо.'                 : row_db.get('name repo', '')
                , 'Версия'                      : row_db.get('last version', '')
                , 'Дата разработки'             : row_db.get('date relise', '')
                , 'Цель выполнения программы'   : row_db.get('target', '')
                , 'Ссылка на репо.'             : row_db.get('url git', '')
                , 'Ком.'                        : row_db.get('comment', '')
            }
            data_return[len(data_return)] = row_return

        return data_return


if __name__ == "__main__":
    app = HandlerMainSheet(
        path_to_tabel=r"C:\Users\yakovlev_nd\Desktop\Tests\ArchiveIntegrator\program — копия.xlsx")
    app.main()

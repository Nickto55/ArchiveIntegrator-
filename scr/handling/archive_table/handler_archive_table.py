import os
import sys
import git

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scr.handling.archive_table.list_all import HandlerMainSheet
from scr.excel_assets.enters.excel_enter_filter import ExcelDataInserter
from scr.handling.archive_table.generated_list_program import GeneratedListArchive

from scr.config_assets.handling_config.handler_program_config import ConfigMainProgram
from scr.config_assets.handling_config.handler_archive_integrator import ConfigArchiveIntegrator

from scr.database_assets.handling_database.handler_db_program import  DataBaseProgramData
from scr.database_assets.handling_database.handler_developer_database import  DeveloperDatabase

def get_git_remote_url_gitpython(local_path):
    try:
        repo = git.Repo(local_path)
        remote_url = repo.remotes.origin.url
        return remote_url
    except git.exc.InvalidGitRepositoryError:
        return "Ошибка: Указанная директория не является Git-репозиторием."
    except AttributeError:
        return "Ошибка: У репозитория нет удаленного источника (remote) с именем 'origin'."


class MainHandlerArchiveTabel:
    def __init__(self):
        self.path_to_tabel = None
        self.data_main_list_table = {}

        self.config_program = ConfigMainProgram()
        self.config_archive = ConfigArchiveIntegrator()

        self.database_program = DataBaseProgramData()
        self.database_archive = DeveloperDatabase()

        self.path_to_archive = self.config_archive.get_all_config_program().get('path to archive','')
        self.path_to_project_program = self.config_archive.get_all_config_program().get('path to project dir','')


    def main(self, path_to_tabel):
        self.path_to_tabel = path_to_tabel

        main_sheet = HandlerMainSheet(path_to_tabel)
        data = main_sheet.main()

        other_sheets = GeneratedListArchive(
            config_archive_integrator=ConfigArchiveIntegrator()
            , path_to_tabel=path_to_tabel
            , data_table=main_sheet.get_data_main_list()
        )

        writer = ExcelDataInserter(path_to_tabel)
        writer.insert_data({'': data}, sheet_name='All programs')

        other_sheets.genereted_sheets()

    def update_database(self):

        for name_repo in os.listdir(self.path_to_archive):
            path_to_programm_dirt = os.path.join(self.path_to_archive, name_repo)
            path_to_project_dirt = self.path_to_project_program
            # get_git_remote_url_gitpython()
            print(path_to_project_dirt)
            # print(path_to_programm_dirt, get_git_remote_url_gitpython(path_to_programm_dirt))


        # self.database_program.set_program_db(
        #     name_repo
        #     , url_git=''
        #     , comment=''
        #     , last_version=''
        #     , program_name=''
        #     , target=''
        #     , date_relise=''
        # )


if __name__ == "__main__":
    app = MainHandlerArchiveTabel()
    # app.update_database()
    app.main(
        path_to_tabel=r"C:\Users\yakovlev_nd\Desktop\Tests\ArchiveIntegrator\program — копия.xlsx"
    )


import os.path

from scr.config_assets.handling_config.handler_program_config import ConfigMainProgram
from scr.config_assets.handling_config.handler_archive_integrator import ConfigArchiveIntegrator

from scr.database_assets.handling_database.handler_developer_database import DeveloperDatabase
from scr.database_assets.handling_database.handler_db_program import DataBaseProgramData

from scr.handling.handler_compiled_program import CompiledProgramHandler
from scr.handling.archive_table.handler_archive_table import MainHandlerArchiveTabel


class ArchiveIntegrator:
    def __init__(self):
        self.config_program = ConfigMainProgram()
        self.config_archive_integrator = ConfigArchiveIntegrator()

        self.database_handler_program = DataBaseProgramData()
        self.database_handler_developer = DeveloperDatabase()

        self.dict_program_and_version = None

    def main_update_pivot_tabel(self):
        """
        Функция для запуска обновления сводной таблици
        :return:
        """
        self.update_excel_tabel()

    def main_update_archive(self, dict_program_and_version: dict):
        """
        Функция для запуска обновления архива
        :param dict_program_and_version : {
                repository_name : version
            }
        """
        if len(dict_program_and_version) < 1:
            print(f'archive_integrator. Порграмма передала пустой словарь. {dict_program_and_version}')
            return

        self.dict_program_and_version = dict_program_and_version

        self.update_excel_tabel()
        self.update_arhive()
        self.update_excel_tabel()

    def update_arhive(self):
        data_link_repository = {}

        for name_repository, row in self.database_handler_program.get_all_db_program().items():
            data_link_repository[name_repository] = os.path.join(
                self.config_archive_integrator.get_all_config_program().get('path to project dir', '')
                , name_repository
            )

        for name_repozitory, version in self.dict_program_and_version.items():
            handler_update_arhive = CompiledProgramHandler()
            handler_update_arhive.main(
                program_path=data_link_repository.get(name_repozitory)
                , version=version
            )

            self.database_handler_developer.set_program_db(
                name_repo=name_repozitory
                , last_version=version
            )

            self.database_handler_program.set_program_db(
                name_repo=name_repozitory
                , last_version=version
            )

    def update_excel_tabel(self):
        path_to_tabel = self.config_archive_integrator.get_all_config_program().get('path to tabel', '')

        handler_update_archive_tabel = MainHandlerArchiveTabel()
        handler_update_archive_tabel.main(path_to_tabel=path_to_tabel)


if __name__ == '__main__':
    app = ArchiveIntegrator()
    app.main_update_pivot_tabel()
    # app.main_update_archive(
    #     dict_program_and_version={
    #         'DatabaseMigrationSoftware': 'v32123.213.12.'
    #     }
    # )
    # app.main_update_pivot_tabel()
    # name_repozitory = ''`
    #
    # while name_repozitory != '0':
    #     name_repozitory = input('Имя репозитория программы: ')
    #     version_program = input('Новая версия программы: ')
    #
    #     data = {name_repozitory:version_program}
    #
    #     app = ArchiveIntegrator()
    #     app.main(data)



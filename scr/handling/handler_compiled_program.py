import os
from pathlib import Path

from scr.handling.file_transfer import FileTransfer
from scr.handling.archiving_process_handler import ArchivingProcessHandlerZIP
from scr.database_assets.handling_database.handler_developer_database import DeveloperDatabase
from scr.config_assets.handling_config.handler_archive_integrator import ConfigArchiveIntegrator


class CompiledProgramHandler:
    def __init__(self, number_of_programs_to_update=None, data_new_version=None):
        """
        Класс для архивирования последних изменённых программ
        :param number_of_programs_to_update: Колличество последних изменённых программ для архивирования
        :param data_new_version: Словарь для присвоения внеочерёдной версии программы
        """
        self.config_archive_integrator = ConfigArchiveIntegrator()
        self.handler_developer_database = DeveloperDatabase()

        self.number_of_programs_to_update = number_of_programs_to_update
        self.data_new_version = data_new_version

        self.path_to_basic_dir_project = self.config_archive_integrator.get_all_config_program().get(
            'path to project dir'
            , ''
        )

        self.last_time_update_file = 0.0
        self.name_archived_file = None

    def file_search_engine(self, program_path):
        if not program_path is None:
            if not 'dist' in os.path.normpath(program_path).split('\\'):
                if not 'dist' in os.listdir(program_path):
                    print('Нет папки dist ')
                    return None
                program_path = os.path.join(
                    program_path
                    , 'dist'
                )
            list_data = os.listdir(program_path)
        else:
            data_programm_time = {}
            list_path_dir_in_basic_dir_project = []
            for name_preositories in [repo for repo in os.listdir(self.path_to_basic_dir_project)]:
                if os.path.isdir(os.path.join(self.path_to_basic_dir_project, name_preositories)):
                    list_path_dir_in_basic_dir_project.append(
                        os.path.join(self.path_to_basic_dir_project, name_preositories))
            if len(list_path_dir_in_basic_dir_project) == 0: return None
            for repo_name in os.listdir(self.path_to_basic_dir_project):
                path_to_repo = os.path.join(self.path_to_basic_dir_project, repo_name)
                if os.path.isdir(path_to_repo):
                    directory_change_time = os.path.getmtime(path_to_repo)
                    data_programm_time.update(
                        {
                            directory_change_time: repo_name
                        }
                    )

            max_change_time = max(data_programm_time.keys())
            program_path = os.path.join(self.path_to_basic_dir_project, data_programm_time.get(max_change_time, ''))
            if not 'dist' in os.listdir(program_path):
                print('Нет папки dist ')
                return None
            program_path = os.path.join(program_path, 'dist')
            list_data = os.listdir(program_path)

        data_programm_time_finish_file = {}
        for name_file in list_data:
            if Path(name_file).suffix[1:] in ['exe']:
                path_to_file = os.path.join(program_path, name_file)
                directory_change_time = os.path.getmtime(path_to_file)
                data_programm_time_finish_file.update(
                    {
                        directory_change_time: name_file
                    }
                )
        max_change_time = max(data_programm_time_finish_file.keys())
        return_path = os.path.join(program_path, data_programm_time_finish_file.get(max_change_time, ''))

        self.last_time_update_file = max_change_time
        return return_path

    def main(self, program_path=None, name_repo=None):
        name_repo = os.path.basename(program_path) if name_repo is None else name_repo
        program_path = self.file_search_engine(program_path=program_path)
        if program_path is None: return

        archivator_zip = ArchivingProcessHandlerZIP(program_path)
        self.name_archived_file = archivator_zip.main()

        self.archive_packaging(name_repo)

    def archive_packaging(self, repository_name):
        data = self.handler_developer_database.get_all_db_program()
        print(repository_name)

        if not repository_name in data.keys():
            print(f'handler_compiled_program. В базе данных нет {repository_name}')
            return
        if self.name_archived_file is None:
            print(f'handler_compiled_program. self.name_archived_file is None {self.name_archived_file}')
            return

        program_name = data[repository_name].get('name', '')

        version = data[repository_name].get('last version', '')

        try:
            Path(version).mkdir(parents=True, exist_ok=True)
        except Exception as error_:
            print(f'handler_compiled_program, archive_packaging. Ошибка при создании папки версии')
            print(f'{error_}')
            return

        handler_file_thansfer = FileTransfer()

        try:
            handler_file_thansfer.transfer(self.name_archived_file, version)
        except Exception as error_:
            print(f'handler_compiled_program, archive_packaging. Ошибка при переноса архива в папку версии')
            print(f'{error_}')
            return

        path_to_archive = self.config_archive_integrator.get_all_config_program().get('path to archive', '')
        path_to_archive_dir = os.path.join(path_to_archive, program_name)

        if not program_name in os.listdir(path_to_archive):
            print(f'Создана директория в архиве: {path_to_archive_dir}')

            try:
                Path(str(path_to_archive_dir)).mkdir(parents=True, exist_ok=True)
            except Exception as error_:
                print('Ошибка при создании')
                print(error_)
                return

        handler_file_thansfer.transfer(version, path_to_archive_dir)
        try:
            handler_file_thansfer.transfer(version, path_to_archive_dir)
        except Exception as error_:
            print(f'Ошибка при переносе zip файла в архив')
            print(error_)
            return

        print(f'Успешно перенесено в архив')


if __name__ == '__main__':
    app = CompiledProgramHandler()
    app.main(r"C:\Users\yakovlev_nd\PycharmProjects\ManagerBAM")

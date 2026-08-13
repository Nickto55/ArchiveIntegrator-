import os

from scr.database_assets.handling_database.handler_db_program import DataBaseProgramData
from scr.database_assets.handling_database.handler_developer_database import DeveloperDatabase
from scr.config_assets.handling_config.handler_archive_integrator import ConfigArchiveIntegrator


class ProgramVersionIdentifier:
    def __init__(self):
        self.config_archive_integrator = ConfigArchiveIntegrator()
        self.handler_developer_database = DeveloperDatabase()
        self.handler_database_program = DataBaseProgramData()

        self.path_to_archive = self.config_archive_integrator.get_all_config_program().get('path to archive', '')

    def calculating_data_for_database(self):
        list_programm_in_archive = os.listdir(self.path_to_archive)
        data_time_create_arhive_version = {}

        for name_repository in list_programm_in_archive:
            path_to_repository = os.path.join(self.path_to_archive, name_repository)
            list_version = os.listdir(path_to_repository)
            list_int_version = []

            for version in list_version:
                if version[0] == 'v' or version[0] == 'V':
                    try:
                        list_int_version.append(version)
                    except:
                        pass

            if len(list_int_version) > 0:
                data_time_create_arhive_version.update(
                    {
                        name_repository: {
                            max(list_version):
                                {
                                    os.path.getmtime(path_to_repository)
                                }
                        }
                    }
                )

        return data_time_create_arhive_version

    def update_database(self, data):

        for name_repo, row in data.items():
            for version, date_change_set in row.items():
                if len(list(date_change_set)) > 0:
                    database_program = self.handler_database_program.get_all_db_program()

                    data_name_repo_progamm = {}
                    for name_repositoru_in_database, row in database_program.items():
                        data_name_repo_progamm.update(
                            {
                                row.get('name', ''): name_repositoru_in_database
                            }
                        )

                    self.handler_developer_database.set_program_db(
                        name_repo=data_name_repo_progamm.get(name_repo, '')
                        , name_program=name_repo
                        , date_change=list(date_change_set)[0]
                        , last_version=version
                    )

    def merge_database(self):
        for name_repozitory, row in self.handler_developer_database.get_all_db_program().items():
            print(name_repozitory, row)

            # database program
            if name_repozitory in self.handler_database_program.get_all_db_program().keys():
                self.handler_database_program.set_program_db(
                    name_repo=name_repozitory
                    , program_name=row.get('name', '')
                    , last_version=row.get('last version', '')
                )

                self.handler_developer_database.set_program_db(
                    name_repo=name_repozitory
                    , git_url=self.handler_database_program.get_program_data(name_repozitory).get('url git', '')
                )

    def main(self):
        self.merge_database()

        if __name__ == '__main__':
            app = ProgramVersionIdentifier()
            app.main()

import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scr.excel_assets.enters.excel_enter_filter import ExcelDataInserter
from scr.database_assets.handling_database.handler_db_program import DataBaseProgramData
from scr.config_assets.handling_config.handler_archive_integrator import ConfigArchiveIntegrator


class GeneratedListArchive:
    def __init__(self, config_archive_integrator, path_to_tabel, data_table=None):
        self.path_to_tabel = path_to_tabel

        self.db_program_data = DataBaseProgramData()

        self.config_archive_integrator = config_archive_integrator if not pd.isna(config_archive_integrator) else ConfigArchiveIntegrator()
        self.data_table = self.db_program_data.get_all_db_program() if not data_table is None else self.db_program_data.get_all_db_program()

        self.path_to_archive = self.config_archive_integrator.get_all_config_program().get('path to archive')
        self.exception_program = self.config_archive_integrator.get_all_config_program().get('exception program')

        self.list_programm_in_archive = os.listdir(self.path_to_archive)

    def generated_list_program(self, name_program):
        return_data = {}
        data_no_reversed = []

        try:
            if name_program in self.exception_program:
                list_in_dir2 = os.listdir(str(os.path.join(self.path_to_archive, name_program)))
                for file_or_dir2 in list_in_dir2:
                    list_in_dir = os.listdir(str(os.path.join(self.path_to_archive, name_program, file_or_dir2)))
                    for file_or_dir in list_in_dir:
                        full_file_or_dir = os.path.join(self.path_to_archive, name_program, file_or_dir2, file_or_dir)
                        if os.path.isdir(full_file_or_dir):
                            data_no_reversed.append(
                                {
                                    'program': file_or_dir2
                                    , 'version': os.path.join(self.path_to_archive, name_program, file_or_dir2,
                                                              file_or_dir)
                                    , "data": ", ".join(f.name for f in Path(str(full_file_or_dir)).iterdir())
                                    , "time": str(datetime.fromtimestamp(os.path.getctime(full_file_or_dir)))[:19]
                                    , '  back  ': ''
                                }
                            )

            else:
                list_in_dir = os.listdir(str(os.path.join(self.path_to_archive, name_program)))
                for file_or_dir in list_in_dir:
                    full_file_or_dir = os.path.join(self.path_to_archive, name_program, file_or_dir)
                    if os.path.isdir(full_file_or_dir):
                        data_no_reversed.append(
                            {
                                'version': os.path.join(self.path_to_archive, name_program, file_or_dir)
                                , "data": ", ".join(f.name for f in Path(str(full_file_or_dir)).iterdir())
                                , "time": str(datetime.fromtimestamp(os.path.getctime(full_file_or_dir)))[:19]
                                , '  back  ': ''
                            }
                        )
        except:
            pass
        data_no_reversed.reverse()
        for row in data_no_reversed:
            return_data[len(return_data)] = row

        return return_data

    def genereted_sheets(self):
        writer = ExcelDataInserter(self.path_to_tabel)
        for num_row, row in self.data_table.items():
            name_program = row.get('name', '')

            data = self.generated_list_program(name_program=name_program)
            writer.insert_data(
                data={'': data}
                , sheet_name=name_program
            )


if __name__ == '__main__':

    app = GeneratedListArchive(
        config_archive_integrator=None
        , path_to_tabel=r"C:\Users\yakovlev_nd\Desktop\Tests\ArchiveIntegrator\program — копия.xlsx"
    )
    app.genereted_sheets()

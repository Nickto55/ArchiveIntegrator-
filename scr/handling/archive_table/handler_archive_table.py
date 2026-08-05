import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scr.config_assets.handling_config.handler_program_config import ConfigMainProgram
from scr.config_assets.handling_config.handler_archive_integrator import ConfigArchiveIntegrator
from scr.handling.archive_table.generated_list_program import GeneratedListArchive
from scr.handling.archive_table.list_all import HandlerMainSheet
from scr.excel_assets.enters.excel_enter_filter import ExcelDataInserter


class MainHandlerArchiveTabel:
    def __init__(self):
        self.config_program = ConfigMainProgram()
        self.data_main_list_table = {}
        self.path_to_tabel = None

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


if __name__ == "__main__":
    app = MainHandlerArchiveTabel()
    app.main(
        path_to_tabel=r"C:\Users\yakovlev_nd\Desktop\Tests\ArchiveIntegrator\program — копия.xlsx"
    )

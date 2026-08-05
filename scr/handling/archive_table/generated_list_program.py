import sys
import os
import pandas as pd
from pathlib import Path
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scr.config_assets.handling_config.handler_archive_integrator import ConfigArchiveIntegrator
from scr.database_assets.handling_database.handler_db_program import DataBaseProgramData
from scr.excel_assets.enters.excel_enter_filter import ExcelDataInserter


class GeneratedListArchive:
    def __init__(self, config_archive_integrator, path_to_tabel, data_table):
        self.config_archive_integrator = config_archive_integrator if not pd.isna(
            config_archive_integrator) else ConfigArchiveIntegrator()
        self.path_to_tabel = path_to_tabel
        self.db_program_data = DataBaseProgramData()
        self.data_table = self.db_program_data.get_all_db_program()
        self.path_to_archive = self.config_archive_integrator.get_all_config_program().get('path to archive')
        self.exception_program = self.config_archive_integrator.get_all_config_program().get('exception program')

        self.list_programm_in_archive = os.listdir(self.path_to_archive)

    def generated_list_program(self, name_program):
        return_data = {}
        data_no_reversed = []
        try:
            if name_program in self.exception_program:
                list_in_dir2 = os.listdir(os.path.join(self.path_to_archive, name_program))
                for file_or_dir2 in list_in_dir2:
                    list_in_dir = os.listdir(os.path.join(self.path_to_archive, name_program, file_or_dir2))
                    for file_or_dir in list_in_dir:
                        full_file_or_dir = os.path.join(os.path.join(self.path_to_archive, name_program, file_or_dir2),
                                                        file_or_dir)
                        if os.path.isdir(full_file_or_dir):
                            data_no_reversed.append(
                                {
                                    'program': file_or_dir2
                                    , 'version': os.path.join(self.path_to_archive, name_program, file_or_dir2,
                                                              file_or_dir)
                                    , "data": ", ".join(f.name for f in Path(full_file_or_dir).iterdir())
                                    , "time": str(datetime.fromtimestamp(os.path.getctime(full_file_or_dir)))[:19]
                                    , '  back  ': ''
                                }
                            )

            else:
                # print(name_program,)
                list_in_dir = os.listdir(os.path.join(self.path_to_archive, name_program))
                for file_or_dir in list_in_dir:
                    full_file_or_dir = os.path.join(os.path.join(self.path_to_archive, name_program), file_or_dir)
                    if os.path.isdir(full_file_or_dir):
                        data_no_reversed.append(
                            {
                                'version': os.path.join(self.path_to_archive, name_program, file_or_dir)
                                , "data": ", ".join(f.name for f in Path(full_file_or_dir).iterdir())
                                , "time": str(datetime.fromtimestamp(os.path.getctime(full_file_or_dir)))[:19]
                                , '  back  ': ''
                            }
                        )
        except:
            pass
        data_no_reversed.reverse()
        for row in data_no_reversed:
            return_data[len(return_data)] = row
        # for ids, asd in return_data.items():
        #     print('     ', ids, asd)
        return return_data

    def genereted_sheets(self):
        writer = ExcelDataInserter(self.path_to_tabel)
        for num_row, row in self.data_table.items():
            name_program = row.get('name', '')

            data = self.generated_list_program(name_program=name_program)
            writer.insert_data(data={'': data}, sheet_name=name_program)


if __name__ == '__main__':
    app = GeneratedListArchive(
        config_archive_integrator=None
        , path_to_tabel=r"C:\Users\yakovlev_nd\Desktop\Tests\ArchiveIntegrator\program — копия.xlsx"
        , data_table={
            0: {'Название программы': 'Database migration software', 'Груп': 'nan',
                'Наим. Репо.': 'DatabaseMigrationSoftware', 'Цель выполнения программы': '-', 'Версия': 'v1.0.1',
                'Дата разработки': 'May 21, 2026', 'Входные данные': 'nan', 'Ссылка на репо.': 404.0,
                'Ком.': 'Проект в архиве'},
            1: {'Название программы': 'Dse Order Manager', 'Груп': 'nan', 'Наим. Репо.': 'DseOrderManager',
                'Цель выполнения программы': 'Программа для вытягивания из годового отчета дсе и наименование',
                'Версия': 'v0.2.0', 'Дата разработки': 'Jul 8, 2026', 'Входные данные': 'Годовой отчет',
                'Ссылка на репо.': 404.0, 'Ком.': 'Проект в архиве, после слияния с SQL order engine'},
            2: {'Название программы': 'change of surnames', 'Груп': 'nan', 'Наим. Репо.': 'hange-of-surnames',
                'Цель выполнения программы': "Программа для заполнения\\обновления столбца с фамилиями таблице 'УП без ИНС' из файла сгенерированного CNCprog",
                'Версия': 'v0.0.2', 'Дата разработки': 'Jul 17, 2026', 'Входные данные': "УП без ИНС',  CNCprog",
                'Ссылка на репо.': 404.0, 'Ком.': 'nan'},
            3: {'Название программы': 'GuiCNCFileCheckingProgram', 'Груп': 'nan',
                'Наим. Репо.': 'GuiCNCFileCheckingProgram',
                'Цель выполнения программы': 'Графический интерфейс для CNCFileCheckingProgram', 'Версия': 'v2.0.3',
                'Дата разработки': 'May 21, 2026', 'Входные данные': 'nan', 'Ссылка на репо.': 404.0, 'Ком.': 'nan'},
            4: {'Название программы': 'CNCFileCheckingProgram', 'Груп': 'nan', 'Наим. Репо.': 'CNCFileCheckingProgram',
                'Цель выполнения программы': 'Сканиерование локальных папок по станкам и создание сводной таблицы ',
                'Версия': 'v1.6.0', 'Дата разработки': 'Jul 10, 2025', 'Входные данные': 'nan',
                'Ссылка на репо.': 404.0, 'Ком.': 'Проект в архиве'},
            5: {'Название программы': 'Bam manager', 'Груп': 'nan', 'Наим. Репо.': 'Bam manager',
                'Цель выполнения программы': 'Программа для обработки (2012, СЗ, ПЖ, ЧПУ без инструмента) в сводную табл.',
                'Версия': 'v1.6.3', 'Дата разработки': 'Jun 3, 2026',
                'Входные данные': '2012, ДСЕ по СЗ,ЧПУ без инструмента,Проблемы и задачи УП и технологии',
                'Ссылка на репо.': 404.0, 'Ком.': 'nan'},
            6: {'Название программы': 'DSE Parser', 'Груп': 'nan', 'Наим. Репо.': 'DSE Parser',
                'Цель выполнения программы': 'Программа для парсинга и сопоставления данных из Excel-файлов изделий и деталей\xa0',
                'Версия': 'v1.5.0', 'Дата разработки': 'Jul 22, 2026',
                'Входные данные': 'Список переводов 28.05.xlsx, Файлы отчетов по дсе: -ер6.212.112.xls -ер7.756.090.xls -… , 26.01.01-12.31.xlsx',
                'Ссылка на репо.': 404.0, 'Ком.': 'nan'},
            7: {'Название программы': 'DseForSzAndNotifications', 'Груп': 'nan',
                'Наим. Репо.': 'DseForSzAndNotifications',
                'Цель выполнения программы': 'Программа для фильтрации и группировки данных из Excel по рабочим центрам (РЦ).',
                'Версия': 'v1.4.1', 'Дата разработки': 'May 28, 2026', 'Входные данные': 'nan',
                'Ссылка на репо.': 404.0, 'Ком.': 'Проект в архиве'},
            8: {'Название программы': 'DSESearchProgram', 'Груп': 'nan', 'Наим. Репо.': 'DSESearchProgram',
                'Цель выполнения программы': '-', 'Версия': 'v1.0.4', 'Дата разработки': 'Jul 17, 2025',
                'Входные данные': 'nan', 'Ссылка на репо.': 404.0, 'Ком.': 'Проект в архиве'},
            9: {'Название программы': 'Good Morning', 'Груп': 'nan', 'Наим. Репо.': 'ReportConversionProgram',
                'Цель выполнения программы': 'Программа для конвертации исходных Excel-таблиц и автоматического составления новых отчетов на основе полученных данных.',
                'Версия': 'v2.0.1', 'Дата разработки': 'Jul 8, 2026', 'Входные данные': 'nan', 'Ссылка на репо.': 404.0,
                'Ком.': 'nan'},
            10: {'Название программы': 'SQL order engine', 'Груп': 'nan', 'Наим. Репо.': 'BamParserSQL',
                 'Цель выполнения программы': 'Программа для создания сводной таблицы из базы данных, после слияния с dse order может самостоятельно обрабатывать отчет',
                 'Версия': 'v1.1.5', 'Дата разработки': 'Jul 30, 2026', 'Входные данные': 'Годовой отчет',
                 'Ссылка на репо.': 404.0, 'Ком.': 'nan'},
            11: {'Название программы': 'Start v10 (Data Wave)', 'Груп': 'nan',
                 'Наим. Репо.': 'program_displaying_data_on_machines',
                 'Цель выполнения программы': 'Программа для просмотра\\создания папок дсе по станкам ',
                 'Версия': 'v10.1.12', 'Дата разработки': 'Jun 4, 2026',
                 'Входные данные': 'Программа имеет конфиг который можно использовать на нескольких комп.',
                 'Ссылка на репо.': 404.0, 'Ком.': 'Проблема с утечкой памяти не решена, но снижена'},
            12: {'Название программы': 'ToolCheckerProgram', 'Груп': 'nan', 'Наим. Репо.': 'ToolCheckerProgram',
                 'Цель выполнения программы': 'Программа для созданияя табл. инструментов (сколько на складе)',
                 'Версия': 'v1.1.1', 'Дата разработки': 'Aug 13, 2025', 'Входные данные': 'nan',
                 'Ссылка на репо.': 404.0, 'Ком.': 'Проект в архиве'},
            13: {'Название программы': 'INS Checker', 'Груп': 'nan', 'Наим. Репо.': 'INS_Checker',
                 'Цель выполнения программы': '-', 'Версия': 'v1.3.0', 'Дата разработки': 'Nov 17, 2025',
                 'Входные данные': 'nan', 'Ссылка на репо.': 404.0, 'Ком.': 'Проект в архиве'},
            14: {'Название программы': 'TelegrammBolt', 'Груп': 'nan', 'Наим. Репо.': 'TelegrammBolt',
                 'Цель выполнения программы': 'Bolt - Система связи преимущественно через телеграмм бота и сайт',
                 'Версия': 'v3.0.3', 'Дата разработки': 'Apr 17, 2026', 'Входные данные': 'СТРАДАТЬ',
                 'Ссылка на репо.': 404.0, 'Ком.': 'Проект в архиве'},
            15: {'Название программы': 'YpMapper', 'Груп': 'nan', 'Наим. Репо.': 'YpMapper',
                 'Цель выполнения программы': 'Программа для создания смежной таблицы по данным из Отчетов по УП',
                 'Версия': 'v0.0.3', 'Дата разработки': 'May 21, 2026', 'Входные данные': '-', 'Ссылка на репо.': 404.0,
                 'Ком.': 'Проект в архиве'},
            16: {'Название программы': 'nan', 'Груп': 'nan', 'Наим. Репо.': 'nan', 'Цель выполнения программы': 'nan',
                 'Версия': 'nan', 'Дата разработки': 'nan', 'Входные данные': 'nan', 'Ссылка на репо.': 'nan',
                 'Ком.': 'nan'},
            17: {'Название программы': 'nan', 'Груп': 'nan', 'Наим. Репо.': 'nan', 'Цель выполнения программы': 'nan',
                 'Версия': 'nan', 'Дата разработки': 'nan', 'Входные данные': 'nan', 'Ссылка на репо.': 'nan',
                 'Ком.': 'nan'},
            18: {'Название программы': 'nan', 'Груп': 'nan', 'Наим. Репо.': ' ', 'Цель выполнения программы': 'nan',
                 'Версия': 'nan', 'Дата разработки': 'nan', 'Входные данные': 'nan', 'Ссылка на репо.': 'nan',
                 'Ком.': 'nan'}
        }
    )
    app.genereted_sheets()

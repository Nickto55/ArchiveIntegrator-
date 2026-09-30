import os
import zipfile


class ArchivingProcessHandlerZIP:
    def __init__(self, path_to_the_archived_path):
        """
        Класс для работы с созданием ZIP архивов
        :param path_to_the_archived_path: Путь к .exe файлу
        """
        self.path_to_the_archived_path = path_to_the_archived_path
        self.name_archived_file = f'{os.path.basename(path_to_the_archived_path)}.zip'

    def main(self, name_archived_file=None, path_to_the_archived_path=None):
        """
        :param name_archived_file       : Имя которое присвоится к архиву
        :param path_to_the_archived_path: Путь к новому файлу для архивации
        :return:
        """

        if not path_to_the_archived_path is None:
            self.path_to_the_archived_path = path_to_the_archived_path
            self.name_archived_file = f'{os.path.basename(path_to_the_archived_path)}.zip'
        if not name_archived_file is None:
            if not name_archived_file[-4:] == '.zip': name_archived_file += '.zip'
            self.name_archived_file = name_archived_file

        self.arhiving_zip()
        return self.name_archived_file

    def arhiving_zip(self):
        if os.path.exists(self.path_to_the_archived_path):
            with zipfile.ZipFile(self.name_archived_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(self.path_to_the_archived_path, arcname=os.path.basename(self.path_to_the_archived_path))
            print(f"Файл успешно заархивирован в {self.name_archived_file}")
        else:
            print(f"Ошибка: Файл {self.path_to_the_archived_path} не найден.")


if __name__ == '__main__':
    app = ArchivingProcessHandlerZIP(
        path_to_the_archived_path=r"C:\Users\yakovlev_nd\Desktop\Tests\ArchiveIntegrator\GoodMorning.exe"
    )
    app.main()

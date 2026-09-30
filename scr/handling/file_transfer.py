import shutil
import os.path

from scr.config_assets.handling_config.handler_archive_integrator import ConfigArchiveIntegrator

class FileTransfer:
    def __init__(self):
        """
        Класс переноса файлов
        """
        self.config_archive_integrator = ConfigArchiveIntegrator()
        self.path_to_archive = self.config_archive_integrator.get_all_config_program().get('path to archive','')

    def transfer(self, path_to_file, path_to_dir):
        shutil.move(path_to_file, path_to_dir)

if __name__=='__main__':
    app = FileTransfer()
    app.transfer('v1.6.3-TEST', os.path.join(ConfigArchiveIntegrator().get_all_config_program().get('path to archive',''), 'Bam manager'))

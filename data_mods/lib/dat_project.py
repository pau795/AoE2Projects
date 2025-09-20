from abc import abstractmethod, ABC
from pathlib import Path

from genieutils.datfile import DatFile

from multimedia_generator import constants


class DatProject(ABC):

    def __init__(self, output_directory: Path, dat_file: DatFile = None):
        self.dat_file = DatFile.parse(constants.AOE_DAT_FILE_PATH) if dat_file is None else dat_file
        self.output_directory = output_directory
        self.dat_file_name = "empires2_x2_p1.dat"

    @abstractmethod
    def process(self):
        pass

    def convert(self):
        self.process()
        self.dat_file.save(self.output_directory / self.dat_file_name)
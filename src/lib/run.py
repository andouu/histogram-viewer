import enum
import aenum

from dataclasses import dataclass
from enum import Enum
from aenum import MultiValueEnum
from ROOT import TFile

class CrystalType(Enum):
    Na22 = enum.auto()
    Co60 = enum.auto()
    Tmp = enum.auto()

class PeakType(MultiValueEnum):
    SINGLE = CrystalType.Na22 # insert other RunTypes if needed, e.g. SINGLE = RunType.Na22, RunType.foo
    DOUBLE = CrystalType.Co60
    TRIPLE = aenum.auto()

@dataclass
class Run():
    name: str
    path: str
    
    @property
    def run_number(self):
        run_number_clean = self.name.removeprefix("run00")
        run_number_as_int = int(run_number_clean)
        return run_number_as_int

    @property
    def crystal_type(self):
        t_file = TFile.Open(self.path, "r")
        t_tree = t_file.Get("T")
        branches = [key.GetName() for key in t_tree.GetListOfBranches()]
        type = None
        if "Q2" in branches:
            type = CrystalType.Co60
        else:
            type = CrystalType.Na22

        t_file.Close()
        return type
    
    @property
    def peak_type(self):
        for attribute in PeakType:
            if self.crystal_type in PeakType(attribute).values:
                return attribute
        return None
    
    @property
    def peak_search_range(self) -> tuple:
        match self.crystal_type:
            case CrystalType.Na22:
                return (-20, -0.1)
            case CrystalType.Co60:
                return (-25, -15)

        return (-400, 400)
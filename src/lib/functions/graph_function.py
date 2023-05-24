import streamlit as st

from abc import ABC, abstractmethod
from ROOT import TFile
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any
from ..run import Run

class AltairDataType(Enum):
    QUANTITATIVE = "Q"
    ORDINAL = "O"
    NOMINAL = "N"
    TEMPORAL = "T"
    GEOJSON = "G"

@dataclass
class Selector():
    name: str
    func: Callable[[TFile, Run], Any]
    data_type: AltairDataType

class GraphingFunction(ABC):
    name: str = "Graphing Function"

    def __init__(self) -> None:
        self.get_x: Selector = None
        self.get_y: Selector = None

        self.x = []
        self.y = []

    def sidebar(self):
        pass

    def on_start(self):
        pass

    def on_processed(self):
        pass

    def on_end(self):
        pass

    def accumulate(self, runs: list[Run]):
        self.runs = runs
        self.on_start()

        self.t_files = [TFile.Open(run.path, "r") for run in runs]
        progress_bar = st.sidebar.progress(0.0, text="Reading TFiles...")
        processed_count = 0
        for t_file, run in zip(self.t_files, runs):
            x = self.get_x(t_file=t_file, run=run) if self.get_x else None
            y = self.get_y(t_file=t_file, run=run) if self.get_y else None

            self.x.append(x)
            self.y.append(y)

            processed_count += 1
            progress_bar.progress(processed_count / len(self.t_files), text=f"Processed {processed_count} out of {len(self.t_files)} runs")
            self.on_processed()

        self.on_end()

    def graph(self):
        pass
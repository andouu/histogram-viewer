import streamlit as st

from abc import ABC, abstractmethod
from ROOT import TFile

class SelectorAccumulator(ABC):
    @property
    @abstractmethod
    def name() -> str:
        pass

    def __init__(self):
        self.processed_count = 0
        self.x = []
        self.y = []
        self._result = None

    @abstractmethod
    def _set_result(self):
        pass

    def get_result(self):
        return self._result

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_process(self):
        pass

    @abstractmethod
    def on_complete(self):
        pass

    def accumulate(self, run_list):
        t_files = self._runs_as_t_files(run_list)
        self.selectors = self._t_files_as_selectors(t_files, run_list)
        
        progress_bar = st.sidebar.progress(0.0, text="Reading TFiles...")
        for selector in self.selectors:
            self.on_process()
            selector.process_events()
            
            self.processed_count += 1
            progress_bar.progress(self.processed_count / len(self.selectors), text=f"Processed {self.processed_count} out of {len(self.selectors)} runs")

        self._set_result()
        self.on_complete()

    def _runs_as_t_files(self, run_list):
        return [TFile.Open(run_data[1], "r") for run_data in run_list]
    
    @abstractmethod
    def _t_files_as_selectors(self, t_files):
        pass
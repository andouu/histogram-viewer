import streamlit as st

from abc import ABC, abstractmethod
from dataclasses import dataclass

class Selector(ABC):
    @property
    @abstractmethod
    def name() -> str:
        pass

    @property
    @abstractmethod
    def read_object() -> str:
        pass

    @abstractmethod
    def get_x(self):
        pass

    @abstractmethod
    def get_y(self):
        pass

    @abstractmethod
    def get_xy(self):
        pass

    def __init__(self, t_file):
        self.t_file = t_file

        self.processed_count = 0

    def process_events(self):
        obj = self.t_file.Get(self.read_object)
        for event in obj:
            self.on_process(event)
            self.processed_count += 1

        self.on_complete()

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_process(self, event):
        pass

    @abstractmethod
    def on_complete(self):
        pass
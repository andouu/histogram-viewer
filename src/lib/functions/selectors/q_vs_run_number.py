import numpy as np

from ...selector import Selector

class QvsRunNumberSelector(Selector):
    name = "Q vs. Run #"
    read_object = "DRS0 (EVENT ID = 1)"

    def __init__(self, t_file, run_name):
        super().__init__(t_file)
        self.x = []
        self.y = run_name

    def get_x(self):
        return np.mean(self.x[0])

    def get_y(self):
        return self.y
    
    def get_xy(self):
        return (self.get_x(), self.get_y())

    def on_start(self):
        pass

    def on_process(self, event):
        self.x.append(event.charge)

    def on_complete(self):
        pass
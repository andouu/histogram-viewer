import streamlit as st
import numpy as np

from ROOT import TF1, TObject
from ...selector import Selector

class QvsRunXSelector(Selector):
    name = "Q vs. Run x"
    read_object = None

    def __init__(self, t_file, run_name):
        super().__init__(t_file)
        self.channel_1_peak_bin = None
        self.run_name = run_name
        self.run_x = None
        self.channel_1_mus = ()
        self.channel_3_mus = ()

    def get_x(self):
        return (self.run_x, self.run_name)

    def get_y(self):
        return {
            "Channel 1": self.channel_1_mus,
            "Channel 3": self.channel_3_mus
        }
    
    def get_xy(self):
        return (self.get_x(), self.get_y())
    
    def _fit(self, channel):
        histogram = self.t_file.Get(f"channel_{channel}_histogram")

        peak_1_range = (8.71, 9.69) if channel == 1 else (31, 35)
        peak_2_range = (9.86, 10.8) if channel == 1 else (35, 40)
        
        def _get_bounds(search_range):
            bin_width = histogram.GetBinWidth(0)
            def _get_center_guess(search_range):
                lower_bound_bin = histogram.FindBin(search_range[0])
                upper_bound_bin = histogram.FindBin(search_range[1]) + 1
                max_value_bin = np.argmax([histogram.GetBinContent(i) for i in range(lower_bound_bin, upper_bound_bin)]) + lower_bound_bin
                return bin_width * max_value_bin

            center = _get_center_guess(search_range)
            return (center * 0.94, center * 1.04)

        left_peak_bounds = _get_bounds(peak_1_range)
        right_peak_bounds = _get_bounds(peak_2_range)
        
        def _get_mu(bounds):
            histogram.Fit("gaus", "LQ0", "", bounds[0], bounds[1])
            f = histogram.GetFunction("gaus")
            f.ResetBit(TF1.kNotDraw)
            histogram.Write(histogram.GetName(), TObject.kOverwrite)
            if not f:
                st.write("no?? " + str(bounds))
                st.write("channel: " + str(channel))
            return f.GetParameter(1)
        
        return (
            _get_mu(left_peak_bounds),
            _get_mu(right_peak_bounds)
        )
    
    def _get_run_x(self):
        inpt_tree = self.t_file.Get("INPT")
        measurement_counts = {}
        for entry in inpt_tree:
            data = entry.data
            measurement = data[1]
            if measurement in measurement_counts:
                measurement_counts[measurement] += 1
            else:
                measurement_counts[measurement] = 1

        highest_count = -1
        highest_count_measurement = None
        for measurement, count in measurement_counts.items():
            if count > highest_count:
                highest_count = count
                highest_count_measurement = measurement
        
        return highest_count_measurement

    def on_start(self):
        self.run_x = self._get_run_x()
        self.channel_1_mus = self._fit(1)
        self.channel_3_mus = self._fit(3)
    
    def on_process(self, event):
        pass

    def on_complete(self):
        pass
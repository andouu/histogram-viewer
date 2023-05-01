import streamlit as st
import numpy as np

from ...selector import Selector

class QvsRunNumberSelector(Selector):
    name = "Q vs. Run #"
    read_object = None

    def __init__(self, t_file, run_name):
        super().__init__(t_file)
        self.channel_1_peak_bin = None
        self.run_name = run_name
        self.channel_1_mu = 0
        self.channel_3_mu = 0

    def get_x(self):
        return self.run_name

    def get_y(self):
        return (self.channel_1_mu, self.channel_3_mu)
    
    def get_xy(self):
        return (self.get_x(), self.get_y())
    
    def _fit(self, channel, expander_label, debug=False):
        histogram = self.t_file.Get(f"channel_{channel}_histogram")
        num_bins = histogram.GetNbinsX()
        bin_width = histogram.GetBinWidth(0)
        histogram_content = [histogram.GetBinContent(i) for i in range(histogram.FindBin(0) + 1, num_bins + 1)]
        channel_peak_bin = np.argmax(histogram_content)

        lower_bound = bin_width * channel_peak_bin * 0.96
        upper_bound = bin_width * channel_peak_bin * 1.04
        histogram.Fit("gaus", "0Q", "", lower_bound, upper_bound)
        
        f = histogram.GetFunction("gaus")
        const, mu, sigma = f.GetParameter(0), f.GetParameter(1), f.GetParameter(2)
        e_const, e_mu, e_sigma = f.GetParError(0), f.GetParError(1), f.GetParError(2)
        ndf, chi2, prob = f.GetNDF(), f.GetChisquare(), f.GetProb()

        if not debug:
            return mu
        
        with st.expander(expander_label):
            col_1, col_2, col_3 = st.columns(3)
            with col_1:
                st.text("Peak: " + str(bin_width * channel_peak_bin))
            with col_2:
                st.text("Bin Width: " + str(bin_width))
            with col_3:
                st.text("Num Bins: " + str(num_bins))

            col_4, col_5 = st.columns(2)
            with col_4:
                st.latex("LB: " + str(lower_bound))
            with col_5:
                st.latex("UB: " + str(upper_bound))

            col_6, col_7, col_8 = st.columns(3)
            with col_6:
                st.text("Const: " + str(const))
            with col_7:
                st.latex(r"\mu: " + str(mu))
            with col_8:
                st.latex(r"\sigma: " + str(sigma))

            col_9, col_10, col_11 = st.columns(3)
            with col_9:
                st.text("E Const: " + str(e_const))
            with col_10:
                st.latex(r"\mu_{error}: " + str(e_mu))
            with col_11:
                st.latex(r"\sigma_{error}: " + str(e_sigma))

            col_12, col_13, col_14 = st.columns(3)
            with col_12:
                st.text("NDF: " + str(ndf))
            with col_13:
                st.latex(r"\chi^2: " + str(chi2))
            with col_14:
                st.latex(f"P: " + str(prob))

        return mu

    def on_start(self):
        debug = False
        if debug:
            channel_1_tab, channel_2_tab = st.tabs(["Channel 1", "Channel 3"])
            with channel_1_tab:
                self.channel_1_mu = self._fit(1, expander_label=self.run_name)
            with channel_2_tab:
                self.channel_3_mu = self._fit(3, expander_label=self.run_name)
        else:
            self.channel_1_mu = self._fit(1, expander_label=self.run_name)
            self.channel_3_mu = self._fit(3, expander_label=self.run_name)
    
    def on_process(self, event):
        pass

    def on_complete(self):
        pass
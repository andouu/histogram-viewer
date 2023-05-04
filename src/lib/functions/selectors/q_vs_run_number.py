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
        self.channel_1_mus = ()
        self.channel_3_mus = ()

    def get_x(self):
        return self.run_name

    def get_y(self):
        return {
            "Channel 1": self.channel_1_mus,
            "Channel 3": self.channel_3_mus
        }
    
    def get_xy(self):
        return (self.get_x(), self.get_y())
    
    def _fit(self, channel, debug=False):
        histogram = self.t_file.Get(f"channel_{channel}_histogram")

        peak_1_range = (5.2, 7.2) if channel == 1 else (31, 35)
        peak_2_range = (8.5, 10.8) if channel == 1 else (35, 40)
        
        def _get_bounds(search_range):
            bin_width = histogram.GetBinWidth(0)
            def _get_center_guess(search_range):
                lbb = histogram.FindBin(search_range[0])
                upb = histogram.FindBin(search_range[1]) + 1
                max_value_bin = np.argmax([histogram.GetBinContent(i) for i in range(lbb, upb)]) + lbb
                # st.write(f"lbb: {lbb}; x: {lbb * bin_width}")
                # st.write(f"upb: {upb}; x: {upb * bin_width}")
                # st.write(f"mvb: {max_value_bin}; x: {bin_width * max_value_bin}; value: {histogram.GetBinContent(int(max_value_bin))}")
                return bin_width * max_value_bin

            center = _get_center_guess(search_range)
            return (center * 0.94, center * 1.04)

        left_peak_bounds = _get_bounds(peak_1_range)
        right_peak_bounds = _get_bounds(peak_2_range)
        
        def _get_mu(bounds):
            histogram.Fit("gaus", "0Q", "", bounds[0], bounds[1])
            f = histogram.GetFunction("gaus")
            if not f:
                st.write("no?? " + str(bounds))
                st.write("channel: " + str(channel))
            return f.GetParameter(1)
        
        return (
            _get_mu(left_peak_bounds),
            _get_mu(right_peak_bounds)
        )

        # if not debug:
        #     return mu
        
        # with st.expander(expander_label):
        #     col_1, col_2, col_3 = st.columns(3)
        #     with col_1:
        #         st.text("Peak: " + str(bin_width * channel_peak_bin))
        #     with col_2:
        #         st.text("Bin Width: " + str(bin_width))
        #     with col_3:
        #         st.text("Num Bins: " + str(num_bins))

        #     col_4, col_5 = st.columns(2)
        #     with col_4:
        #         st.latex("LB: " + str(lower_bound))
        #     with col_5:
        #         st.latex("UB: " + str(upper_bound))

        #     col_6, col_7, col_8 = st.columns(3)
        #     with col_6:
        #         st.text("Const: " + str(const))
        #     with col_7:
        #         st.latex(r"\mu: " + str(mu))
        #     with col_8:
        #         st.latex(r"\sigma: " + str(sigma))

        #     col_9, col_10, col_11 = st.columns(3)
        #     with col_9:
        #         st.text("E Const: " + str(e_const))
        #     with col_10:
        #         st.latex(r"\mu_{error}: " + str(e_mu))
        #     with col_11:
        #         st.latex(r"\sigma_{error}: " + str(e_sigma))

        #     col_12, col_13, col_14 = st.columns(3)
        #     with col_12:
        #         st.text("NDF: " + str(ndf))
        #     with col_13:
        #         st.latex(r"\chi^2: " + str(chi2))
        #     with col_14:
        #         st.latex(f"P: " + str(prob))

    def on_start(self):
        self.channel_1_mus = self._fit(1)
        self.channel_3_mus = self._fit(3)
    
    def on_process(self, event):
        pass

    def on_complete(self):
        pass
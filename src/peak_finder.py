import ROOT
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

from lib.files import root_files_to_runs
from lib.plot import q_branch_to_dataframe
from lib.run import Run, PeakType
from scipy.signal import find_peaks
from pprint import pprint
from alive_progress import alive_bar
from multiprocessing import Pool, cpu_count
from concurrent.futures import ProcessPoolExecutor, as_completed

runs = root_files_to_runs()

starting_run = 313
ending_run = 690

runs_to_analyze: list[Run] = runs[starting_run - 313 : ending_run - 313 + 1]

def _single_mu(run: Run):
    t_file = ROOT.TFile.Open(run.path)
    data = q_branch_to_dataframe(t_file)
    t_file.Close()
    histogram, bin_edges = np.histogram(data.charges.tolist(), bins=128)
    max_count_bin_index = np.argmax(histogram)

    mu_guess = (bin_edges[max_count_bin_index] + bin_edges[max_count_bin_index]) / 2
    return mu_guess

def _multi_mu(run: Run):
    t_file = ROOT.TFile.Open(run.path)
    data: pd.DataFrame = q_branch_to_dataframe(t_file)
    t_file.Close()

    search_range = run.peak_search_range
    data = data[data.charges.between(left=search_range[0], right=search_range[1])]

    histogram, bin_edges = np.histogram(data.charges, bins=128, density=True)

    x_axis = np.linspace(bin_edges.min(), bin_edges.max(), 128)
    kde = stats.gaussian_kde(data.values.ravel())
    kde_curve = kde.pdf(x_axis)

    peaks, _ = find_peaks(kde_curve)
    peak_coordinates = [(bin_edges[peak], histogram[peak]) for peak in peaks]
    peak_coordinates.sort(key=lambda coord: coord[1], reverse=True)
    two_peaks = peak_coordinates[0:2]

    return [coordinate[0] for coordinate in two_peaks]

def get_peaks(run: Run):
    if run.peak_type is PeakType.SINGLE:
        return _single_mu(run)
    else:
        return _multi_mu(run)

def return_run(run):
    return run

def detect_peaks():
    MULTIPROCESS = True

    with alive_bar(len(runs_to_analyze)) as bar:
        def on_finish(run: Run, result):
            print(f"{run.name} ({run.peak_type}): Peaks: {result}")
            bar()

        if MULTIPROCESS:
            with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
                for run in runs_to_analyze:
                    executor.submit(_single_mu, run).add_done_callback(lambda future: on_finish(run, future.result()))
        else:
            for run in runs_to_analyze:
                peaks = get_peaks(run)
                on_finish(run, peaks)

def kde_method():
    run = runs_to_analyze[699-313]
    t_file = ROOT.TFile.Open(run.path)
    df = q_branch_to_dataframe(t_file)
    df = df[df.charges.between(left=run.peak_search_range[0], right=run.peak_search_range[1])]
    
    histogram, bin_edges = np.histogram(df.charges, bins=128, density=True)
    x = np.linspace(bin_edges.min(), bin_edges.max(), 128)
    plt.figure(figsize=(8, 6))
    plt.bar(bin_edges[:-1], histogram, width=np.diff(bin_edges), ec="k", align="edge", label="histogram")

    kde = stats.gaussian_kde(df.values.ravel())
    curve = kde.pdf(x)
    plt.plot(x, curve, lw=2, c="C3", label="KDE")

    peaks, _ = find_peaks(curve)
    peak_coordinates = [(bin_edges[peak], histogram[peak]) for peak in peaks]
    peak_coordinates.sort(key=lambda coord: coord[1], reverse=True)
    two_peaks = peak_coordinates[0:2]
    plt.plot([c[0] for c in two_peaks], [c[1] for c in two_peaks], "r+")

    plt.legend()
    plt.show()

def main():
    # detect_peaks()
    # print("Done")
    # kde_method()
    run = runs[-1]
    t_file = ROOT.TFile.Open(run.path, "read")

if __name__ == "__main__":
    main()
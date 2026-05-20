'''
plotter for binpacking project with matplot\
15 minutes starting at 1 item files
'''

import csv
import time
import matplotlib as mp
import numpy as np
import pandas as pd

def plot_outof_csv(filename, title):
    item_counts = []
    algo_times = []

    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader) #skip the labels
        for row in reader:
            item_counts.append(int(row[0]))
            algo_times.append(float(row[1]))

    plt.plot(item_counts, algo_times)
    plt.xlabel("Items Count")
    plt.ylabel("Time (seconds)")
    plt.title(title)
    plt.savefig(title + ".png")
    plt.clf()
    
    
def main():
    plot_outof_csv("bnb_15_minute_run.csv", "BNB OVER 15")
    plot_outof_csv("bnbffd_15_minute_run.csv", "BNBFFD OVER 15")
    plot_outof_csv("ffd_15_minute_run.csv", "FFD OVER 15")

if __name__ == "__main__":
    main()

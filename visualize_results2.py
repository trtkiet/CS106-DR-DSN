import h5py
from matplotlib import pyplot as plt
import argparse
import os
import os.path as osp
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', type=str, required=True,
                    help="path to h5 file containing summarization results")
args = parser.parse_args()

h5_res = h5py.File(args.path, 'r')
keys = h5_res.keys()

for key in keys:
    score = h5_res[key]['score'][...]
    machine_summary = h5_res[key]['machine_summary'][...]
    gtscore = h5_res[key]['gtscore'][...]
    fm = h5_res[key]['fm'][()]
    
    step = len(machine_summary) // len(gtscore)

    # plot score vs gtscore
    fig, axs = plt.subplots(2)
    n = len(gtscore)
    axs[0].bar(range(n), gtscore, color=['red' if machine_summary[i] else 'gray' for i in range(0, len(machine_summary), step)])
    axs[0].set_xlim(0, n)
    axs[0].set_yticklabels([])
    axs[0].set_xticklabels([])
    axs[1].set_title("video {} F-score {:.1%}".format(key, fm))
    axs[1].bar(range(n), score, color=['blue' if machine_summary[i] else 'gray' for i in range(0, len(machine_summary), step)])
    axs[1].set_xlim(0, n)
    axs[1].set_ylim(min(score), max(score))
    axs[1].set_yticklabels([])
    axs[1].set_xticklabels([])
    fig.savefig(osp.join(osp.dirname(args.path), 'score_' + key + '.png'), bbox_inches='tight')
    plt.close()

    print("Done video {}. # frames {}.".format(key, len(machine_summary)))

h5_res.close()
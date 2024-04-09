import os
import re
import argparse
import numpy as np
import pandas as pd


def clean_data(indir, outdir):
    file_list = os.listdir(indir)
    try:
        file_list.remove('.DS_Store')
    except:
        pass

    os.makedirs(outdir, exist_ok=True)

    for file in file_list:
        outfile = os.path.join(outdir, file)
        if os.path.exists(outfile):
            continue
        contents = pd.read_csv(os.path.join(indir, file))
        print(contents.head())

    return


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--input', type=str, required=True)
    argparser.add_argument('--output', type=str, required=True)
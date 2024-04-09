import os
import re
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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
        # print(contents.head())

        def get_centre(x,y,w,h):
            return x + w/2, y + h/2
        
        df = pd.DataFrame(columns=['frame', 'x', 'y'])
        df['frame'] = contents['frame']

        for index, row in contents.iterrows():
            x, y = get_centre(row['x'], row['y'], row['w'], row['h'])
            df.loc[index, 'x'] = round(x, 2)
            df.loc[index, 'y'] = round(y, 2)

        print(df.head())

        df.to_csv(outfile, index=False)

    return



def plot(df, outdir):

    fig, ax = plt.subplots(figsize=(3.3, 1.9))
    # norm df 
    ax.plot(df['x'], df['y'], color='black', linewidth=0.5)
    ax.set_xlim(0, 3.3)
    ax.set_ylim(0, 1.9)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(outdir, dpi=300)
    plt.close()



def plotter(indir, outdir):
    file_list = os.listdir(indir)
    try:
        file_list.remove('.DS_Store')
    except:
        pass

    os.makedirs(outdir, exist_ok=True)

    for file in file_list:
        outfile = os.path.join(outdir, file.split('.')[0] + '.png') 
        if os.path.exists(outfile):
            continue
        contents = pd.read_csv(os.path.join(indir, file))
        contents['x'] = (contents['x'] / 1920)*3.3
        contents['y'] = (contents['y'] / 1080)*1.9

        print(contents.head())

        plot(contents, outdir)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--input', type=str, required=True)
    argparser.add_argument('--output', type=str, required=True)
    argparser.add_argument('--plot', type=str, required=True)


    args = argparser.parse_args()
    # clean_data(args.input, args.output)
    
    plotter(args.output, args.plot)

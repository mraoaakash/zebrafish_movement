import os
import re
import math
import argparse
import numpy as np
import pandas as pd
from celluloid import Camera
import matplotlib.pyplot as plt



def zscore_using_apply(x, window):
    def zscore_func(x):
        return (x[-1] - x[:-1].mean())/x[:-1].std(ddof=0)
    return x.rolling(window=window+1).apply(zscore_func)

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

    # fig, ax = plt.subplots(figsize=(3.3, 1.9))
    # # norm df 
    # ax.plot(df['x'], df['y'], color='black', linewidth=0.5)
    # ax.set_xlim(0, 3.3)
    # ax.set_ylim(0, 1.9)
    # ax.axis('off')
    # plt.tight_layout()
    # plt.savefig(outdir, dpi=300)
    # plt.close()

    fig, ax = plt.subplots()

    ax.plot(df['frame'], df['x'], color='black', linewidth=0.5)
    ax.plot(df['frame'], df['y'], color='blue', linewidth=0.5)

    plt.tight_layout()
    plt.savefig(outdir, dpi=300)
    plt.close()

    print(zscore_using_apply(df['x'], 50))

def naremover(df):
    # Fills the 0 values in the dataframe with successive values before and after the 0 values
    df = df.replace(0, np.nan)
    df = df.interpolate(method='linear', limit_direction='both')
    return df

def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def cleaner(df):
    leng = len(df)
    # print(leng)

    # convert to 0
    threshold_y = 1080-214
    indices = list(df.index[df['y']>threshold_y])
    if len(indices)>0:
        # print(indices)
        df.loc[indices,:]=0

    for j in range(10):
        for i in range (1, leng-3,1):
            if df.iloc[i]['x']==0 or df.iloc[i+1]['x']==0:
                continue
            dist = calculate_distance(df.iloc[i]['x'], df.iloc[i]['y'], df.iloc[i+1]['x'], df.iloc[i+1]['y'])
            if dist >10:
                df.at[i+1,'x'] = 0
                df.at[i+1,'y'] = 0

    return df



def plotter(indir, outdir):
    file_list = os.listdir(indir)
    try:
        file_list.remove('.DS_Store')
    except:
        pass

    os.makedirs(outdir, exist_ok=True)

    for file in file_list:
        outfile = os.path.join(outdir, file.split('.')[0] + '.png') 
        # if os.path.exists(outfile):
        #     continue
        contents = pd.read_csv(os.path.join(indir, file))
        contents = cleaner(contents)
        contents = naremover(contents)
        contents['x'] = (contents['x'] / 1920)*3.3
        contents['y'] = (contents['y'] / 1080)*1.9

        print(contents.head())

        plot(contents, outfile)



if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--input', type=str, required=True)
    argparser.add_argument('--output', type=str, required=True)
    argparser.add_argument('--plot', type=str, required=True)


    args = argparser.parse_args()
    # clean_data(args.input, args.output)
    
    plotter(args.output, args.plot)

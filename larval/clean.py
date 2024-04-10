import os
import re
import math
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d




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

def smooth(X,Y):
    x , y = X, Y
    # moving average
    t = np.linspace(0, 1, len(x))
    t2 = np.linspace(0, 1, 100)

    x2 = np.interp(t2, t, x)
    y2 = np.interp(t2, t, y)
    sigma = 0.01
    x3 = gaussian_filter1d(x2, sigma)
    y3 = gaussian_filter1d(y2, sigma)

    x4 = np.interp(t, t2, x3)
    y4 = np.interp(t, t2, y3)
    return x4, y4


def plot(df, outdir):

    fig, ax = plt.subplots()
    # norm df 
    ax.plot(df['x'], df['y'], color='black', linewidth=0.5)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(outdir.replace('.png', '_track.png'), dpi=300)
    plt.close()

    X = np.array(df['x'].values)
    Y = np.array(df['y'].values)

    fig, ax = plt.subplots()

    ax.plot(df['frame'], X, color='black', linewidth=0.5)
    ax.plot(df['frame'], Y, color='blue', linewidth=0.5)

    plt.tight_layout()
    plt.savefig(outdir, dpi=300)
    plt.close()


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

    for j in range(2):
        for i in range (1, leng-2,1):
            if df.iloc[i]['x']==0 or df.iloc[i+1]['x']==0:
                continue
            dist = calculate_distance(df.iloc[i]['x'], df.iloc[i]['y'], df.iloc[i+1]['x'], df.iloc[i+1]['y'])
            if dist >50:
                # delete the row entirely
                df.drop(df.index[i], inplace=True)
    
    df_reset = pd.DataFrame(columns=['frame', 'x', 'y'])
    df_reset['frame'] = range(1, len(df)+1)
    for index, row in df.iterrows():
        df_reset.loc[index, 'x'] = row['x']
        df_reset.loc[index, 'y'] = row['y']

    df = naremover(df_reset)

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

        plot(contents, outfile.replace('.png', '_unsmooth.png'))
        # X,Y = smooth(np.array(contents['x']).astype(int), np.array(contents['y']).astype(int))

        # contents['x'] = X
        # contents['y'] = Y

        # print(contents.head())
        # plot(contents, outfile)




if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--input', type=str, required=True)
    argparser.add_argument('--output', type=str, required=True)
    argparser.add_argument('--plot', type=str, required=True)


    args = argparser.parse_args()
    # clean_data(args.input, args.output)
    
    plotter(args.output, args.plot)

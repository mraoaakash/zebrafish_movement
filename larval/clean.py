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
        # print(contents.head())

        def get_centre(x,y,w,h):
            return x + w/2, y + h/2
        
        df = pd.DataFrame(columns=['frame', 'x', 'y'])

        for index, row in contents.iterrows():
            x, y = get_centre(row['x'], row['y'], row['w'], row['h'])
            df_temp = pd.DataFrame({'frame': row['frame'], 'x': x, 'y': y},ignore_index=True)
            df = pd.concat([df, df_temp])
        

        print(df_temp.head())



    return


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--input', type=str, required=True)
    argparser.add_argument('--output', type=str, required=True)

    args = argparser.parse_args()
    clean_data(args.input, args.output)
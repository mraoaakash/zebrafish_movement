from ultralytics import YOLO
import os 
import cv2
import argparse
import numpy as np
import pandas as pd
import multiprocessing as mp
from multiprocessing.pool import Pool

# fish_name = 'rsec-left'

def runner(pre_post,video_path_src, modelpath,savepath, outpath=None):
    video_list = os.listdir(video_path_src)
    try:
        video_list.remove('.DS_Store')
    except:
        pass

    print(video_list)

    for fish_name in video_list:
        fish_name = fish_name.split('.')[0]
        if fish_name == '.DS_Store':
            continue
        video_path = f'{video_path_src}/{fish_name}.mp4'
        print(video_path)
        procesed = os.listdir(savepath)
        processed = [i.split('.')[0] for i in procesed]
        if fish_name in processed:
            continue
            pass


        os.makedirs(savepath, exist_ok=True)
        model = YOLO(modelpath)
        print(model)

        cap = cv2.VideoCapture(video_path)
        if outpath is not None:
            out = cv2.VideoWriter(f'{outpath}/{fish_name}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (1920, 1080))
        
        results = []

        df = pd.DataFrame(columns=['frame', 'x', 'y', 'w', 'h'])
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_arr = np.arange(0, num_frames+1, 1)
        df["frame"] = frame_arr

        # Loop through the video frames
        counter = 0
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()


            if success:
                # Run YOLOv8 tracking on the frame, persisting tracks between frames
                results = model.track(frame, persist=False)
                boxes = results[0].boxes.xywh.cpu().numpy()

                if len(boxes) > 0:
                    boxes = boxes[0]
                    df.loc[counter] = [counter, boxes[0], boxes[1], boxes[2], boxes[3]]
                else:
                    df.loc[counter] = [counter, 0, 0, 0, 0]


                # Visualize the results on the frame
                annotated_frame = results[0].plot()

                # Write the frame to the output video
                out.write(annotated_frame)


                # Display the annotated frame
                # cv2.imshow("YOLOv8 Tracking", annotated_frame)


                # Break the loop if 'q' is {pre_post}ssed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                # Break the loop if the end of the video is reached
                break
            counter += 1

        # Release the video capture object and close the display window
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        df.to_csv(f'{savepath}/{fish_name}.csv', index=False)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--pre_post', type=str, help='pre or post')
    argparser.add_argument('--video_path', type=str, help='path to video')
    argparser.add_argument('--modelpath', type=str, help='path to model')
    argparser.add_argument('--savepath', type=str, help='path to save')
    argparser.add_argument('--outpath', type=str, help='path to save', default=None)
    args = argparser.parse_args()
    runner(args.pre_post, args.video_path, args.modelpath, args.savepath, args.outpath)
    # runner('pre', 'data/pre_intervention/
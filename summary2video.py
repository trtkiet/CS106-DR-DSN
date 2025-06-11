import h5py
import cv2
import os
import os.path as osp
import numpy as np
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('-p', '--path', type=str, required=True, help="path to h5 result file")
# parser.add_argument('-d', '--frm-dir', type=str, required=True, help="path to frame directory")
# parser.add_argument('-i', '--idx', type=int, default=0, help="which key to choose")
# parser.add_argument('--fps', type=int, default=30, help="frames per second")
# parser.add_argument('--width', type=int, default=640, help="frame width")
# parser.add_argument('--height', type=int, default=480, help="frame height")
# parser.add_argument('--save-dir', type=str, default='log', help="directory to save")
# parser.add_argument('--save-name', type=str, default='summary.mp4', help="video name to save (ends with .mp4)")
# args = parser.parse_args()

def create_summary_video(key, source_video_path, machine_summary, output_folder):
    print(len(machine_summary))
    # Loop through each video in source_video_folder
    
    output_video_path = os.path.join(output_folder, f"{key}_summary.mp4")
    # Open the video file
    cap = cv2.VideoCapture(source_video_path)
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Check if the frame is selected in the summary
        if machine_summary[frame_count]:
            out.write(frame)
        frame_count += 1
    print('frame_count:', frame_count)
    cap.release()
    out.release()

def frm2video(frm_dir, summary, vid_writer):
    for idx, val in enumerate(summary):
        print(val)
        if val == 1:
            # here frame name starts with '000001.jpg'
            # change according to your need
            frm_name = str(idx+1).zfill(6) + '.jpg'
            frm_path = osp.join(frm_dir, frm_name)
            frm = cv2.imread(frm_path)
            frm = cv2.resize(frm, (args.width, args.height))
            vid_writer.write(frm)

if __name__ == '__main__':
    if not osp.exists(args.save_dir):
        os.mkdir(args.save_dir)
    vid_writer = cv2.VideoWriter(
        osp.join(args.save_dir, args.save_name),
        cv2.VideoWriter_fourcc(*'MP4V'),
        args.fps,
        (args.width, args.height),
    )
    h5_res = h5py.File(args.path, 'r')
    keys = [key for i, key in enumerate(h5_res.keys()) if i == args.idx]
    summary = []
    for key in keys:
        summary.append(h5_res[key]['machine_summary'][:])
    h5_res.close()
    frm2video(args.frm_dir, summary, vid_writer)
    vid_writer.release()
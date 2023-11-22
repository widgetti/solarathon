import cv2
import numpy as np
import solara as sl
import pandas as pd

from PIL import Image


def process_video_pose(video_name):

    frames_annotated = {}
    frames_keypoints = {}
    frame_idx = 0
    
    cap = cv2.VideoCapture(video_name)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = VideoProcessor.model(Image.fromarray(frame))

        if results is not None:
            for result in results:
                frames_keypoints[frame_idx] = result.keypoints.xy
                for x, y in np.squeeze(np.array(result.keypoints.xy)):
                    cv2.circle(frame, (int(x), int(y)), 2, (255, 0, 0), -1)
                frames_annotated[frame_idx] = frame
                frame_idx += 1

    return frames_annotated, frames_keypoints


class VideoProcessor:

    video_frame = sl.reactive(0)
    analysis_types = ['Pose', 'Track', 'Detect']
    analysis_type = sl.reactive('')
    model = None
    name = sl.reactive("")

    raw_frames = []
    processed_frames = []
    processed_data = []

    active_frame = sl.reactive(np.zeros((10, 10)).astype(int))

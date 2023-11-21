import cv2
import solara as sl
import tempfile
from PIL import Image
import numpy as np
from ultralytics import YOLO

from solara.components.file_drop import FileInfo

from solarathon.components.video_analysis import VideoProcessor, process_video_pose


def load_model(value):
    if value == 'Pose':
        VideoProcessor.model = YOLO('yolov8n-pose.pt')
    else:
        return None

@sl.component
def Page():

    file_received, set_file_received = sl.use_state("No file uploaded")

    def on_file(file: FileInfo):
        set_file_received(f'New file: {file["name"]}')

        with tempfile.NamedTemporaryFile() as temp:
            temp.write(file["data"])
            VideoProcessor.name.value = temp.name
            set_file_received(f'Temp file: {temp.name}')
            frames_annotated = {}
            frames_keypoints = {}
            frame_idx = 0
            
            cap = cv2.VideoCapture(temp.name)

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

    def process_video():
        return

    with sl.Column() as main:
        with sl.Sidebar():
            sl.FileDrop(label='Please provide a video to analyse.', lazy=False, on_file=on_file)
            sl.Select(label='Type of analysis', values=VideoProcessor.analysis_types, value=VideoProcessor.analysis_type, on_value=load_model)
            with sl.Column():
                sl.Button(label='Start analysis', on_click=process_video)

        sl.Markdown(str(VideoProcessor.analysis_type.value))
        sl.Info(file_received)

    return main

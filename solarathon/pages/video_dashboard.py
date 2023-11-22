import os
import cv2
import solara as sl
import tempfile
from PIL import Image
import numpy as np
from ultralytics import YOLO
import plotly.express as px
import pandas as pd

from solara.components.file_drop import FileInfo

from solarathon.components.video_analysis import VideoProcessor, process_video_pose


def load_model(value):
    if value == 'Pose':
        VideoProcessor.model = YOLO('yolov8n-pose.pt')
    elif value == 'Detect':
        VideoProcessor.model = YOLO('yolov8s.pt')
    else:
        return None

@sl.component
def FrameViewer():

    selection_data, set_selection_data = sl.use_state(None)
    click_data, set_click_data = sl.use_state(None)
    hover_data, set_hover_data = sl.use_state(None)
    unhover_data, set_unhover_data = sl.use_state(None)
    deselect_data, set_deselect_data = sl.use_state(None)

    fig = px.imshow(VideoProcessor.active_frame.value)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(width=600, height=600)
    sl.FigurePlotly(
        fig, on_selection=set_selection_data, on_click=set_click_data, on_hover=set_hover_data, on_unhover=set_unhover_data, on_deselect=set_deselect_data,
    )

@sl.component
def KeypointViewer():

    selection_data, set_selection_data = sl.use_state(None)
    click_data, set_click_data = sl.use_state(None)
    hover_data, set_hover_data = sl.use_state(None)
    unhover_data, set_unhover_data = sl.use_state(None)
    deselect_data, set_deselect_data = sl.use_state(None)

    # min_val = 1 if VideoProcessor.video_frame.value == 0 else VideoProcessor.video_frame.value
    # current_coords = np.concatenate(VideoProcessor.processed_data)[:min_val]
    # for point_idx in range(current_coords.shape[1]):
    #     fig=px.line(x=current_coords[:, point_idx, 0], y=current_coords[:, point_idx, 1])

    mask_frame = VideoProcessor.processed_data_df['frame'] < VideoProcessor.video_frame.value
    mask_keypoints_nonzero = (VideoProcessor.processed_data_df['coord0'] > 0) | (VideoProcessor.processed_data_df['coord1'] > 0) 
    fig=px.line(VideoProcessor.processed_data_df[mask_frame & mask_keypoints_nonzero], x='coord0', y='coord1', color='keypoint')
    fig.update_layout(width=600, height=600)
    fig.update_xaxes(range=[0, VideoProcessor.active_frame.value.shape[1]])
    fig.update_yaxes(range=[0, VideoProcessor.active_frame.value.shape[0]])

    sl.FigurePlotly(
        fig, on_selection=set_selection_data, on_click=set_click_data, on_hover=set_hover_data, on_unhover=set_unhover_data, on_deselect=set_deselect_data,
    )
    return

@sl.component
def DashboardControls():
    return


@sl.component
def Page():

    file_received, set_file_received = sl.use_state(False)
    file_status, set_file_status = sl.use_state('No file received.')
    analysis_status, set_analysis_status = sl.use_state('Analysis has not started. Please upload a video and press "Start analysis"!')
    frame_progress, set_frame_progress = sl.use_state(0.0)

    def on_file(file: FileInfo):
        set_file_status(f'New file: {file["name"]}')

        # Create temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(file["data"])
        temp_file.close()

        # Read video
        video = cv2.VideoCapture(temp_file.name)
        frames = []
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # Get the total number of frames

        for frame_index in range(frame_count):
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)  # Seek to the specific frame
            ret, frame = video.read()  # Read the frame
            if ret:
                frames.append(frame)

        # Store frames
        VideoProcessor.raw_frames = frames
        # Remove temp file
        os.remove(temp_file.name)


    def process_video():

        if VideoProcessor.analysis_type.value == 'Pose':
            processed_data = []
            processed_frames = []
            complete_df = pd.DataFrame()
            for frame_idx, frame in enumerate(VideoProcessor.raw_frames):
                set_frame_progress(np.round(100 * (1+frame_idx)/len(VideoProcessor.raw_frames)))
                # Interestingly, if the frames are saved in BGR it works fine
                # but if we convert to RGB on loading, it crashes at frame 95
                results = VideoProcessor.model(Image.fromarray(frame))

                if results is not None:
                    for result in results:
                        kpoints = result.keypoints
                        sample_df = pd.DataFrame(np.squeeze(np.array(kpoints.xy)), columns=['coord0', 'coord1'])
                        sample_df['frame'] = frame_idx
                        sample_df['keypoint'] = np.arange(np.squeeze(np.array(kpoints.xy)).shape[0])
                        complete_df = pd.concat([complete_df, sample_df], axis=0, ignore_index=True)
                        processed_data.append(np.array(kpoints.xy))
                        for (x, y) in np.squeeze(np.array(kpoints.xy)):
                            cv2.circle(frame, (int(x), int(y)), 1, (0, 0, 255), -1)
                        processed_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            VideoProcessor.processed_data = processed_data
            VideoProcessor.processed_frames = processed_frames
            VideoProcessor.processed_data_df = complete_df
            VideoProcessor.active_frame.value = processed_frames[VideoProcessor.video_frame.value]


    def update_frame(value):
        VideoProcessor.active_frame.value = VideoProcessor.processed_frames[value]

    # Interface
    with sl.Column() as main:
        with sl.Sidebar():
            sl.Markdown('### Video upload:')
            sl.Info(file_status)
            sl.FileDrop(label='Please provide a video to analyse.', lazy=False, on_file=on_file)
            
            sl.Select(label='Type of analysis', values=VideoProcessor.analysis_types, value=VideoProcessor.analysis_type, on_value=load_model)
            with sl.Column():
                sl.Button(label='Start analysis', on_click=process_video)

                if frame_progress == 0:
                    sl.Warning(label=analysis_status)
                elif (frame_progress > 0) and (frame_progress < 99.5):
                    set_analysis_status(f'Running analysis: {int(frame_progress)} %')
                    sl.Info(label=analysis_status)
                elif frame_progress >= 99.5:
                    set_analysis_status('Analysis complete!')
                    sl.Success(label=analysis_status)
                sl.ProgressLinear(value=frame_progress, color="blue")

        if frame_progress >= 99.5:
            with sl.GridFixed(columns=2):
                FrameViewer()
                KeypointViewer()
                sl.SliderInt(label='Frame:', min=0, max=len(VideoProcessor.raw_frames)-1, value=VideoProcessor.video_frame, on_value=update_frame)


    return main

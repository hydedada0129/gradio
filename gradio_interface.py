import gradio as gr

def process_video(video):
    """
    This function just returns the input video for demonstration.
    You can replace it with your actual video processing logic.
    """
    return video

with gr.Blocks() as demo:
    gr.Markdown("## Video Upload and Playback")

    with gr.Row():
        with gr.Column(scale=1):
            video_input = gr.Video(label="Upload Video")
        with gr.Column(scale=1):
            video_output = gr.Video(label="Output")  # Add playable=True

    video_input.upload(process_video, outputs=video_output)

if __name__ == "__main__":
    demo.launch()

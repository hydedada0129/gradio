#%%
import gradio as gr
import speech_recognition as sr

def process_video(video):
    """
    This function just returns the input video for demonstration.
    You can replace it with your actual video processing logic.
    """
    return video

def recognize_audio(video):
    """
    Performs audio recognition on the video using speech_recognition.
    """
    r = sr.Recognizer()

    try:
        with sr.AudioFile(video) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

with gr.Blocks() as demo:
    gr.Markdown("## Video Upload and Playback")

    with gr.Row():
        with gr.Column(scale=1):
            video_input = gr.Video(label="Upload Video")
        with gr.Column(scale=1):
            video_output = gr.Video(label="Output")  # Playable is supported in Gradio 4.44.1
            audio_output = gr.Textbox(label="Audio Recognition")

    video_input.upload(process_video, outputs=video_output)
    video_input.upload(recognize_audio, outputs=audio_output)

if __name__ == "__main__":
    demo.launch()
#%%

import gradio as gr
import speech_recognition as sr
import os

def process_video(video):
    """
    This function just returns the input video for demonstration.
    You can replace it with your actual video processing logic.
    """
    return video

def recognize_audio(video):
    """
    Performs audio recognition on the video using speech_recognition.
    """
    r = sr.Recognizer()

    # Save the video to a temporary file (for compatibility with speech_recognition)
    # temp_audio_file = "temp_audio.wav"
    temp_audio_file = os.path.join(os.getcwd(), "temp_audio.wav")  # Use current directory
    os.system(f"ffmpeg -i {video} -vn -acodec copy {temp_audio_file}")

    try:
        with sr.AudioFile(temp_audio_file) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"
    finally:
        os.remove(temp_audio_file)  # Clean up the temporary file

with gr.Blocks() as demo:
    gr.Markdown("## Video Upload and Playback")

    with gr.Row():
        with gr.Column(scale=1):
            video_input = gr.Video(label="Upload Video")
        with gr.Column(scale=1):
            video_output = gr.Video(label="Output")  # No playable=True here
            audio_output = gr.Textbox(label="Audio Recognition")

    video_input.upload(process_video, outputs=video_output)
    video_input.upload(recognize_audio, outputs=audio_output)

if __name__ == "__main__":
    demo.launch()

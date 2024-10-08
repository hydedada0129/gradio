# import os
# import speech_recognition as sr
# from pydub import AudioSegment
# import time
# from datetime import timedelta
# from pydub import AudioSegment
# from pydub.utils import which
# import gradio as gr

# ffmpeg_path = which("ffmpeg")  # Get the path to ffmpeg
# AudioSegment.converter = ffmpeg_path  # Set the path

# # 1. audio recognition
# # 將秒數格式化為 時:分:秒
# def format_time(seconds):
#     return str(timedelta(seconds=round(seconds)))

# # 進行語音辨識並顯示時間軸，並將結果寫入文字檔案
# def recognize_audio_in_chunks(wav_file, output_txt, chunk_length_ms=5000):
#     recognizer = sr.Recognizer()
#     audio = AudioSegment.from_wav(wav_file)
#     chunks = len(audio) // chunk_length_ms  # 計算總共有多少段

#     # 建立輸出文字檔案
#     with open(output_txt, "w", encoding="utf-8") as f:
#         print(f"音檔總長度: {len(audio) / 1000} 秒，將音訊檔切割成 {chunks} 段，每段約 {chunk_length_ms / 1000} 秒")
#         f.write(f"音檔總長度: {format_time(len(audio) / 1000)}\n")
#         f.write(f"每段約 {chunk_length_ms / 1000} 秒\n\n")

#         for i in range(0, len(audio), chunk_length_ms):
#             start_time = i / 1000  # 將時間轉為秒
#             end_time = (i + chunk_length_ms) / 1000 if i + chunk_length_ms <= len(audio) else len(audio) / 1000

#             # 將這段音訊儲存為臨時檔案
#             chunk_audio = audio[i:i + chunk_length_ms]
#             chunk_file = f"chunk_{i // chunk_length_ms}.wav"
#             chunk_audio.export(chunk_file, format="wav")

#             # 開始辨識該段音訊
#             with sr.AudioFile(chunk_file) as source:
#                 audio_data = recognizer.record(source)

#                 try:
#                     print(f"辨識中：第 {i // chunk_length_ms + 1} 段 ({format_time(start_time)} - {format_time(end_time)})")
#                     text = recognizer.recognize_google(audio_data, language="zh-TW")
#                     print(f"時間段 {format_time(start_time)} - {format_time(end_time)}: {text}")
#                     f.write(f"時間段 {format_time(start_time)} - {format_time(end_time)}: {text}\n")
#                 except sr.UnknownValueError:
#                     print(f"時間段 {format_time(start_time)} - {format_time(end_time)}: 無法辨識")
#                     f.write(f"時間段 {format_time(start_time)} - {format_time(end_time)}: 無法辨識\n")
#                 except sr.RequestError as e:
#                     print(f"語音辨識服務發生錯誤: {e}")
#                     f.write(f"時間段 {format_time(start_time)} - {format_time(end_time)}: 語音辨識錯誤 ({e})\n")

#             # 刪除臨時檔案
#             os.remove(chunk_file)

# def process_audio(audio_file):
#     """Processes the uploaded audio file."""
#     # Set output file name based on the input file
#     base_filename = os.path.splitext(os.path.basename(audio_file.name))[0]
#     output_txt = f"{base_filename}_transcription_Google2.txt"

#     # Perform audio recognition
#     recognize_audio_in_chunks(audio_file.name, output_txt)

#     # Read the output transcription
#     with open(output_txt, "r", encoding="utf-8") as f:
#         transcription = f.read()

#     # Return the transcription
#     return transcription

# # Create Gradio interface
# interface = gr.Interface(
#     fn=process_audio,
#     inputs=gr.Audio(label="Upload Audio"),
#     outputs=gr.Textbox(label="Extracted Text"),
#     title="Audio Transcription"
# )

# # Launch Gradio
# if __name__ == "__main__":
#     #input_mp4 = "your_MP4_file"  # 你的 MP4 檔案名稱
#     input_wav = "test_short_wav.wav"  # 你的 WAV 檔案名稱
#     # 自動將輸入的 MP4 檔案名稱轉換為輸出的 WAV 和 TXT 檔案名稱，保持一致
#     base_filename = os.path.splitext(os.path.basename(input_wav))[0]  # 取得不帶副檔名的檔案名稱
#     #output_wav = f"{base_filename}_output_google2.wav"  # 輸出的 WAV 檔案
#     output_txt = f"{base_filename}_transcription_Google2.txt"  # 輸出的文字檔案

#     # 記錄整個程式的開始時間
#     total_start_time = time.time()

#     # Step 2: 辨識 WAV 檔案並顯示時間軸，並將結果寫入文字檔
#     recognize_start_time = time.time()
#     recognize_audio_in_chunks(input_wav, output_txt, chunk_length_ms=5000)
#     recognize_end_time = time.time()
#     print(f"語音辨識花費時間: {format_time(recognize_end_time - recognize_start_time)}")

#     # 計算總花費時間
#     total_end_time = time.time()
#     total_time = total_end_time - total_start_time
#     print(f"整個程式總共花費時間: {format_time(total_time)}")
#     interface.launch()

#%%
import os
import speech_recognition as sr
from pydub import AudioSegment
import time
from datetime import timedelta
from pydub import AudioSegment
from pydub.utils import which
import gradio as gr

ffmpeg_path = which("ffmpeg")  # Get the path to ffmpeg
AudioSegment.converter = ffmpeg_path  # Set the path

# 1. audio recognition
# 將秒數格式化為 時:分:秒
def format_time(seconds):
    return str(timedelta(seconds=round(seconds)))

# 進行語音辨識並顯示時間軸，並將結果寫入文字檔案
def recognize_audio_in_chunks(wav_file, output_txt, chunk_length_ms=5000):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav(wav_file)
    chunks = len(audio) // chunk_length_ms  # 計算總共有多少段

    # 建立輸出文字檔案
    with open(output_txt, "w", encoding="utf-8") as f:
        print(f"音檔總長度: {len(audio) / 1000} 秒，將音訊檔切割成 {chunks} 段，每段約 {chunk_length_ms / 1000} 秒")
        f.write(f"音檔總長度: {format_time(len(audio) / 1000)}\n")
        f.write(f"每段約 {chunk_length_ms / 1000} 秒\n\n")

        for i in range(0, len(audio), chunk_length_ms):
            start_time = i / 1000  # 將時間轉為秒
            end_time = (i + chunk_length_ms) / 1000 if i + chunk_length_ms <= len(audio) else len(audio) / 1000

            # 將這段音訊儲存為臨時檔案
            chunk_audio = audio[i:i + chunk_length_ms]
            chunk_file = f"chunk_{i // chunk_length_ms}.wav"
            chunk_audio.export(chunk_file, format="wav")

            # 開始辨識該段音訊
            with sr.AudioFile(chunk_file) as source:
                audio_data = recognizer.record(source)

                try:
                    print(f"辨識中：第 {i // chunk_length_ms + 1} 段 ({format_time(start_time)} - {format_time(end_time)})")
                    text = recognizer.recognize_google(audio_data, language="zh-TW")
                    print(f"時間段 {format_time(start_time)} - {format_time(end_time)}: {text}")
                    f.write(f"時間段 {format_time(start_time)} - {format_time(end_time)}: {text}\n")
                except sr.UnknownValueError:
                    print(f"時間段 {format_time(start_time)} - {format_time(end_time)}: 無法辨識")
                    f.write(f"時間段 {format_time(start_time)} - {format_time(end_time)}: 無法辨識\n")
                except sr.RequestError as e:
                    print(f"語音辨識服務發生錯誤: {e}")
                    f.write(f"時間段 {format_time(start_time)} - {format_time(end_time)}: 語音辨識錯誤 ({e})\n")

            # 刪除臨時檔案
            os.remove(chunk_file)

def process_audio(audio_file):
    """Processes the uploaded audio file."""
    # Set output file name based on the input file
    base_filename = os.path.splitext(os.path.basename(audio_file.name))[0]
    output_txt = f"{base_filename}_transcription_Google2.txt"

    # Perform audio recognition
    recognize_audio_in_chunks(audio_file.name, output_txt)

    # Read the output transcription
    with open(output_txt, "r", encoding="utf-8") as f:
        transcription = f.read()

    # Return the transcription
    return transcription

# Create Gradio interface
interface = gr.Interface(
    fn=process_audio,
    inputs=gr.Audio(label="Upload Audio"),
    outputs=gr.Textbox(label="Extracted Text"),
    title="Audio Transcription"
)

# Define the function to handle the audio recognition process
def run_audio_recognition():
    input_wav = "/home/oem/anaconda3/envs/speech_to_speech/codes/backend/gradio/test_short_wav.wav"  # Your WAV file name

    # Automatically convert the input MP4 file name to the output WAV and TXT file names, keeping them consistent
    base_filename = os.path.splitext(os.path.basename(input_wav))[0]  # Get the file name without extension
    output_txt = f"{base_filename}_transcription_Google2.txt"  # Output text file

    # Record the start time of the entire program
    total_start_time = time.time()

    # Step 2: Recognize the WAV file, display the timeline, and write the results to a text file
    recognize_start_time = time.time()
    recognize_audio_in_chunks(input_wav, output_txt, chunk_length_ms=5000)
    recognize_end_time = time.time()
    print(f"Speech recognition took: {format_time(recognize_end_time - recognize_start_time)}")

    # Calculate the total time taken
    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    print(f"Total program time: {format_time(total_time)}")

# Launch Gradio
if __name__ == "__main__":
    # Run the audio recognition
    run_audio_recognition()
    interface.launch()
# %%

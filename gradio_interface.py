#%%
import os
import speech_recognition as sr
from pydub import AudioSegment
import time
from datetime import timedelta
from pydub import AudioSegment
from pydub.utils import which
from deep_translator import GoogleTranslator  # Import the deep_translator library
from gtts import gTTS

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


def translate_text(text):
    """Translates text using Google Translate."""
    try:
        translator = GoogleTranslator(source='auto', target='en')  # Assuming you want to translate to English
        translation = translator.translate(text)
        return translation
    except Exception as e:
        print(f"Translation error: {e}")
        return "Translation failed"


def run_audio_recognition_and_translation():
    input_wav = "test_short_wav.wav"  # Your WAV file name

    # Automatically convert the input MP4 file name to the output WAV and TXT file names, keeping them consistent
    base_filename = os.path.splitext(os.path.basename(input_wav))[0]  # Get the file name without extension
    output_txt = f"{base_filename}_transcription_Google2.txt"  # Output text file
    output_en_txt = f"{base_filename}_translation_en.txt"  # Output translated text file

    # Record the start time of the entire program
    total_start_time = time.time()

    # Step 2: Recognize the WAV file, display the timeline, and write the results to a text file
    recognize_start_time = time.time()
    recognize_audio_in_chunks(input_wav, output_txt, chunk_length_ms=5000)
    recognize_end_time = time.time()
    print(f"Speech recognition took: {format_time(recognize_end_time - recognize_start_time)}")

    # Read the output transcription
    with open(output_txt, "r", encoding="utf-8") as f:
        transcription = f.read()

    # Translate the text
    translated_text = translate_text(transcription)

    # Print the results
    print(f"Transcription: {transcription}")
    print(f"Translation: {translated_text}")

    # Save the translated text to a file
    with open(output_en_txt, "w", encoding="utf-8") as f:
        f.write(translated_text)
    print(f"Translated text saved to: {output_en_txt}")

    # Calculate the total time taken
    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    print(f"Total program time: {format_time(total_time)}")

    # Below is the text you want to add
    # (It will be appended to the translation)
    additional_text = "This is some extra text to be added to the translation!"
    translated_text = translated_text + "\n" + additional_text

    # Save the updated translation
    with open(output_en_txt, "a", encoding="utf-8") as f:
        f.write(additional_text)
    print(f"Updated translated text saved to: {output_en_txt}")
    
    #input for extracting story text
    story_text = extract_story_text(output_en_txt)

    output_file_path = "extracted_story_en.txt"  # Replace with your desired output file name

    #save to a new txt file
    save_story_text(story_text, output_file_path)
    print(f"Story text saved to: {output_file_path}")

    read_text_file(output_file_path)

def extract_story_text(file_path):
    """Extracts the story text from the provided file, excluding timestamps and other metadata."""
    story_text = ""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            # Check if the line starts with "Time period"
            if line.startswith("Time period"):
                # Extract the story text after the colon
                # story_text += line.split(": ", 1)[1].strip() + " "
                story_text += line.split(": ", 1)[1].strip() + "\n"
    return story_text.strip()

def save_story_text(story_text, output_file_path):
    """Saves the extracted story text to a new text file."""
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(story_text)

# Read and speak the translated text
def read_text_file(file_path):
    try:
        # Open and read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Use gTTS to convert text to speech
        tts = gTTS(text=text, lang='en')  # Assuming English language
        tts.save("output.mp3")  # Save the audio to a file

        print("Audio file saved as output.mp3")

        # # Use speech synthesis to read the text
        # engine.say(text)
        # engine.runAndWait()

    except FileNotFoundError:
        print("File not found, please check the file path.")
    except Exception as e:
        print(f"Error occurred: {e}")

    # Read and speak the translated text
    # read_text_file(output_en_txt)

if __name__ == "__main__":
    


# def read_text_file(file_path):
#     try:
#         # Open and read the file
#         with open(file_path, 'r', encoding='utf-8') as file:
#             text = file.read()

#         # Use gTTS to convert text to speech
#         tts = gTTS(text=text, lang='en')  # Assuming English language
#         tts.save("output.mp3")  # Save the audio to a file

#         print("Audio file saved as output.mp3")

#         # # Use speech synthesis to read the text
#         # engine.say(text)
#         # engine.runAndWait()

#     except FileNotFoundError:
#         print("File not found, please check the file path.")
#     except Exception as e:
#         print(f"Error occurred: {e}")

# Launch the process
# if __name__ == "__main__":
#     # run_audio_recognition_and_translation()
#     read_text_file('/home/oem/anaconda3/envs/speech_to_speech/codes/backend/gradio/test_short_wav_translation_en.txt')

# def extract_story_text(file_path):
#     """Extracts the story text from the provided file, excluding timestamps and other metadata."""
#     story_text = ""
#     with open(file_path, 'r', encoding='utf-8') as f:
#         lines = f.readlines()
#         for line in lines:
#             # Check if the line starts with "Time period"
#             if line.startswith("Time period"):
#                 # Extract the story text after the colon
#                 # story_text += line.split(": ", 1)[1].strip() + " "
#                 story_text += line.split(": ", 1)[1].strip() + "\n"
#     return story_text.strip()

# def save_story_text(story_text, output_file_path):
#     """Saves the extracted story text to a new text file."""
#     with open(output_file_path, 'w', encoding='utf-8') as f:
#         f.write(story_text)

# Example usage:
# file_path = "test_short_wav_translation_en.txt"  # Replace with your file path
# story_text = extract_story_text(file_path)
# output_file_path = "extracted_story.txt"  # Replace with your desired output file name

# save_story_text(story_text, output_file_path)
# print(f"Story text saved to: {output_file_path}")
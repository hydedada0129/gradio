import os
import speech_recognition as sr
from pydub import AudioSegment
import time
from datetime import timedelta
from pydub import AudioSegment
from pydub.utils import which
from deep_translator import GoogleTranslator

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

def translate_file(source_file, target_file):
    try:
        # 檢查目標文件路徑的寫入權限
        if not os.access(os.path.dirname(target_file), os.W_OK):
            print(f"無法寫入目標目錄：{os.path.dirname(target_file)}，請確認權限。")
            return

        translator = GoogleTranslator(source='auto', target='en')
        with open(source_file, 'r', encoding='utf-8') as f:
            text = f.read()

        translation = translator.translate(text)

        # 直接覆蓋目標檔案
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(translation)

        print(f"翻譯完成，結果已寫入 {target_file}")

        # **Return the translated text**
        return translation  

    except FileNotFoundError:
        print(f"文件 {source_file} 不存在")
    except Exception as e:
        print(f"發生錯誤：{e}")

# Add the permission-changing function
def change_permissions(directory):
    """Changes permissions of all .txt files in a directory to owner write permissions."""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            os.chmod(filepath, 0o666)  # Change to 0o666 to only grant write permissions to the owner
            print(f"Changed permissions of {filepath} to owner write")

if __name__ == "__main__":
    #input_mp4 = "short_video_1.mp4"  # 你的 MP4 檔案名稱
    input_wav = "short_video_1_output_google2.wav"  # 你的 WAV 檔案名稱
    # 自動將輸入的 MP4 檔案名稱轉換為輸出的 WAV 和 TXT 檔案名稱，保持一致
    base_filename = os.path.splitext(os.path.basename(input_wav))[0]  # 取得不帶副檔名的檔案名稱
    #output_wav = f"{base_filename}_output_google2.wav"  # 輸出的 WAV 檔案
    output_txt = f"{base_filename}_transcription_Google2.txt"  # 輸出的文字檔案
    output_en_txt = f"{base_filename}_transcription_Google2_en.txt"  # Output file for English translation

    # 記錄整個程式的開始時間
    total_start_time = time.time()

    # Step 2: 辨識 WAV 檔案並顯示時間軸，並將結果寫入文字檔
    recognize_start_time = time.time()
    recognize_audio_in_chunks(input_wav, output_txt, chunk_length_ms=5000)
    recognize_end_time = time.time()
    print(f"語音辨識花費時間: {format_time(recognize_end_time - recognize_start_time)}")

    # Change permissions of output files
    current_directory = os.getcwd()  # Get the current directory
    change_permissions(current_directory)

    # Translate the transcription
    translation = translate_file(output_txt, output_en_txt)
    print("Translated text:", translation)

    # 計算總花費時間
    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    print(f"整個程式總共花費時間: {format_time(total_time)}")
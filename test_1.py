import os
from deep_translator import GoogleTranslator

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

    except FileNotFoundError:
        print(f"文件 {source_file} 不存在")
    except Exception as e:
        print(f"發生錯誤：{e}")

# 設定文件路径
source_file = "source_ch.txt"
target_file = "target_en.txt"

translate_file(source_file, target_file)
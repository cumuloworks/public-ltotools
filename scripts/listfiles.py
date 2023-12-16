import os
import tkinter as tk
from tkinter import filedialog

def human_readable_size(size, decimal_places=1):
    size = float(size)  # sizeをfloat型に変換
    for unit in ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']:
        if size < 1024.0 or unit == 'YB':
            break
        size /= 1024.0
    if size.is_integer():
        return f"{size:.0f} {unit}"
    return f"{size:.{decimal_places}f} {unit}"

def list_files_with_human_readable_size(startpath, output_file):
    existing_files = set()
    if os.path.exists(output_file):
        with open(output_file, "r", encoding='utf-8') as f:
            for line in f:
                existing_files.add(line.split('   ')[-1].strip())

    with open(output_file, "a", encoding='utf-8') as f:
        for root, dirs, files in os.walk(startpath):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path not in existing_files:
                    size = os.path.getsize(file_path)
                    readable_size = human_readable_size(size)
                    f.write(f"{readable_size}   {file_path}\n")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # GUIを隠す

    # ディレクトリ選択ダイアログを表示
    directory_path = filedialog.askdirectory(title="ディレクトリを選択してください")

    # 出力ファイル選択ダイアログを表示
    output_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

    if directory_path and output_file_path:
        list_files_with_human_readable_size(directory_path, output_file_path)

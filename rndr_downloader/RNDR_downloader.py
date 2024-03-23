import tkinter as tk
from tkinter import filedialog
import os
import urllib.parse
import subprocess
import datetime
import time
from tqdm import tqdm
import threading

def monitor_download_progress(directory, expected_count, text_file_name, interval=0.2):
    dir_name = os.path.basename(directory)
    # ディレクトリ名とテキストファイル名をプログレスバーの説明として使用
    pbar = tqdm(total=expected_count, desc=f"{text_file_name} -> {dir_name}", unit="file", leave=False)
    while pbar.n < expected_count:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and not f.endswith('.aria2')]
        pbar.update(len(files) - pbar.n)
        time.sleep(interval)
    pbar.close()


def download_files(download_dir, urls, text_file_name):  # 引数にtext_file_nameを追加
    download_list_file = os.path.join(download_dir, "download_list.txt")
    with open(download_list_file, 'w') as f:
        for url in urls:
            f.write(url + '\n')

    command = f'aria2c -i "{download_list_file}" -d "{download_dir}" -x 16 -j 32 -c -q'
    subprocess.Popen(command, shell=True)

    monitor_thread = threading.Thread(target=monitor_download_progress, args=(download_dir, len(urls), text_file_name))
    monitor_thread.start()
    monitor_thread.join()

    os.remove(download_list_file)


def process_url_list(file_path):
    file_dir = os.path.dirname(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    text_file_name = os.path.basename(file_path)  # テキストファイルの完全な名前

    downloads = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        parsed_url = urllib.parse.urlparse(line.strip())
        query_params = urllib.parse.parse_qs(parsed_url.query)
        content_disposition = query_params.get('response-content-disposition', [''])[0]
        filename_in_url = ""

        if content_disposition:
            parts = content_disposition.split(';')
            for part in parts:
                if part.strip().startswith("filename="):
                    filename_in_url = part.split('=')[1].strip(' "')

        filename_removed = filename_in_url.replace(file_name, "").strip('_')
        directory = filename_removed.split('_')[0]

        download_dir = os.path.join(file_dir, file_name, directory)
        os.makedirs(download_dir, exist_ok=True)

        if download_dir not in downloads:
            downloads[download_dir] = []
        downloads[download_dir].append(line.strip())

    for dir, urls in downloads.items():
        download_files(dir, urls, text_file_name)  

def main():
    root = tk.Tk()
    root.withdraw()  # tkinterのメインウィンドウを表示しない

    file_paths = filedialog.askopenfilenames(title="ダウンロードするURLリストを含むテキストファイルを選択", filetypes=[("テキストファイル", "*.txt")])

    for file_path in file_paths:
        process_url_list(file_path)

if __name__ == "__main__":
    main()

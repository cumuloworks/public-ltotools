import tkinter as tk
import os
import urllib.parse
import subprocess
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(filetypes=[("テキストファイル", "*.txt")])

# テキストファイルのあるディレクトリを取得
file_dir = os.path.dirname(file_path)
file_name = os.path.splitext(os.path.basename(file_path))[0]

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

    # ダウンロード先ディレクトリをテキストファイルのあるディレクトリに設定
    download_dir = os.path.join(file_dir, file_name, directory)
    os.makedirs(download_dir, exist_ok=True)

    if download_dir not in downloads:
        downloads[download_dir] = []
    downloads[download_dir].append(line.strip())

for dir, urls in downloads.items():
    download_list_file = os.path.join(dir, "download_list.txt")
    with open(download_list_file, 'w') as f:
        for url in urls:
            f.write(url + '\n')

    command = f'aria2c -i "{download_list_file}" -d "{dir}" -x 16 -j 32 -c'
    subprocess.run(command, shell=True)

    os.remove(download_list_file)

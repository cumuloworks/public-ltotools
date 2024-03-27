import os
import unicodedata
from tkinter import Tk, messagebox
from tkinter.filedialog import askdirectory

def find_nfd_nfc_diff_files(directory):
    diff_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            nfc_version = unicodedata.normalize('NFC', file)
            if file != nfc_version:
                diff_files.append((os.path.join(root, file), os.path.join(root, nfc_version)))
    return diff_files

def rename_files(files_to_rename):
    for old_path, new_path in files_to_rename:
        os.rename(old_path, new_path)
        print(f"ファイル '{old_path}' を '{new_path}' にリネームしました。")

# ユーザーにディレクトリを選択させる
Tk().withdraw()  # Tkのルートウィンドウを非表示
selected_directory = askdirectory()

# ディレクトリが選択された場合、NFDとNFCが異なるファイルを検出
if selected_directory:
    files_to_rename = find_nfd_nfc_diff_files(selected_directory)
    if files_to_rename:
        print("NFD != NFC なファイルのリスト:")
        for old_path, new_path in files_to_rename:
            print(f"・{old_path} -> {new_path}")
        
        # ユーザーにリネームの確認を取る
        if messagebox.askyesno("リネーム確認", "上記のファイルをリネームしますか？"):
            rename_files(files_to_rename)
            print("指定されたファイルのリネームが完了しました。")
        else:
            print("リネーム処理はキャンセルされました。")
    else:
        print("NFDとNFCが異なるファイルは見つかりませんでした。")
else:
    print("ディレクトリが選択されませんでした。")

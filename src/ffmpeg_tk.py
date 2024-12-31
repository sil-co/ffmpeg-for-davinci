import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def select_input_file():
    """入力ファイルを選択するダイアログを表示"""
    file_path = filedialog.askopenfilename(
        title="入力ファイルを選択",
        filetypes=[("MP4ファイル", "*.mp4") ,("MOVファイル", "*.mov"), ("すべてのファイル", "*.*")]
    )
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def select_output_folder():
    """出力フォルダを選択するダイアログを表示"""
    folder_path = filedialog.askdirectory(title="出力フォルダを選択")
    if folder_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder_path)

def run_ffmpeg():
    """FFmpegコマンドを実行"""
    input_file = input_entry.get()
    output_folder = output_entry.get()

    if not input_file:
        messagebox.showerror("エラー", "入力ファイルを指定してください。")
        return

    # 出力フォルダが未選択の場合、入力ファイルと同じディレクトリを使用
    if not output_folder:
        output_folder = os.path.dirname(input_file)

    # 元のファイル名と拡張子を分離
    original_name, ext = os.path.splitext(os.path.basename(input_file))
    # 新しいファイル名を生成
    new_filename = f"{original_name}-ffmpeg{ext}"
    output_file = os.path.join(output_folder, new_filename)

    # FFmpegコマンドを構成
    command = [
        "ffmpeg",
        "-i", input_file,
        "-c:a", "copy",
        "-c:v", "copy",
        "-write_tmcd", "0",
        output_file
    ]

    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("成功", f"動画が正常に処理されました。\n出力ファイル: {output_file}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("エラー", f"FFmpegの実行中にエラーが発生しました。\n{e}")

# Tkinter GUIの構築
root = tk.Tk()
root.title("FFmpeg GUI")

# 入力ファイルの選択
tk.Label(root, text="入力ファイル:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
input_entry = tk.Entry(root, width=40)
input_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="選択", command=select_input_file).grid(row=0, column=2, padx=5, pady=5)

# 出力フォルダの選択
tk.Label(root, text="出力フォルダ:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
output_entry = tk.Entry(root, width=40)
output_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="選択", command=select_output_folder).grid(row=1, column=2, padx=5, pady=5)

# 実行ボタン
tk.Button(root, text="FFmpeg実行", command=run_ffmpeg, bg="blue", fg="white").grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()

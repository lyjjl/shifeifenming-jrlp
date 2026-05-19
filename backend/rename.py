import os
from pathlib import Path


def rename_brackets(folder_path):
    if not os.path.exists(folder_path):
        print(f"错误: 找不到文件夹 '{folder_path}'")
        return

    count = 0
    for filename in os.listdir(folder_path):
        if "[" in filename or "]" in filename:
            new_name = filename.replace("[", "(").replace("]", ")")

            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)

            try:
                os.rename(old_path, new_path)
                print(f"已重命名: {filename} -> {new_name}")
                count += 1
            except Exception as e:
                print(f"重命名 {filename} 时出错: {e}")

    print(f"\n处理完成！共修改了 {count} 个文件。")


if __name__ == "__main__":
    target_dir = str(Path(__file__).resolve().parent / "img")
    rename_brackets(target_dir)

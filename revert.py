# -*- coding: utf-8 -*-
"""还原 VS Code 中文语言包到官方原始状态（清除本项目写入的译文）。"""
import glob
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(HERE, "backup")
PACK_GLOB = os.path.join(os.path.expanduser("~"), ".vscode", "extensions",
                         "ms-ceintl.vscode-language-pack-zh-hans-*")


def main():
    dirs = [d for d in glob.glob(PACK_GLOB) if os.path.isdir(d)]
    if not dirs:
        sys.exit("未找到中文语言包")
    dirs.sort(key=lambda d: os.path.getmtime(os.path.join(d, "package.json")), reverse=True)
    ext = dirs[0]
    pack = os.path.join(ext, "translations", "main.i18n.json")
    bak = os.path.join(BACKUP_DIR, os.path.basename(ext) + "-main.i18n.json")
    if not os.path.exists(bak):
        sys.exit("没有对应版本的备份：%s\n语言包已升级时无法用旧备份还原，请在 VS Code 里重装该语言包。" % bak)

    shutil.copy2(bak, pack)
    print("已还原:", pack)

    clp = os.path.join(os.environ.get("APPDATA", ""), "Code", "clp")
    purged = 0
    if os.path.isdir(clp):
        for name in os.listdir(clp):
            if name.endswith(".zh-cn"):
                shutil.rmtree(os.path.join(clp, name), ignore_errors=True)
                purged += 1
    print(f"已清理语言包编译缓存 {purged} 个，请完全退出 VS Code 后重新打开。")


if __name__ == "__main__":
    main()

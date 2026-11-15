# -*- coding: utf-8 -*-
"""把本仓库的中文译文写入 VS Code 简体中文语言包，并清理语言包编译缓存。

用法：
    python apply.py

生效方式：执行后必须**完全退出 VS Code 再重新打开**（仅「重新加载窗口」不会重建缓存）。
"""
import glob
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OVERLAY = os.path.join(HERE, "zh_overlay.json")
BACKUP_DIR = os.path.join(HERE, "backup")
PACK_GLOB = os.path.join(os.path.expanduser("~"), ".vscode", "extensions",
                         "ms-ceintl.vscode-language-pack-zh-hans-*")


def find_pack():
    dirs = [d for d in glob.glob(PACK_GLOB) if os.path.isdir(d)]
    if not dirs:
        sys.exit("未找到中文语言包：%s\n请先在 VS Code 里安装「Chinese (Simplified) Language Pack」。" % PACK_GLOB)
    dirs.sort(key=lambda d: os.path.getmtime(os.path.join(d, "package.json")), reverse=True)
    return dirs[0]


def main():
    ext = find_pack()
    pack = os.path.join(ext, "translations", "main.i18n.json")
    print("语言包:", ext)

    # 首次运行备份原始文件
    os.makedirs(BACKUP_DIR, exist_ok=True)
    bak = os.path.join(BACKUP_DIR, os.path.basename(ext) + "-main.i18n.json")
    if not os.path.exists(bak):
        shutil.copy2(pack, bak)
        print("已备份原始文件:", os.path.relpath(bak, HERE))
    else:
        print("已有备份，跳过备份")

    overlay = json.load(open(OVERLAY, encoding="utf-8"))
    data = json.load(open(pack, encoding="utf-8-sig"))
    contents = data["contents"]

    added = updated = 0
    for mod, entries in overlay.items():
        cur = contents.setdefault(mod, {})
        for key, value in entries.items():
            if key in cur:
                if cur[key] != value:
                    updated += 1
            else:
                added += 1
            cur[key] = value

    json.dump(data, open(pack, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"写入完成：新增 {added} 条，覆盖 {updated} 条")

    # VS Code 会把语言包预编译缓存到 %APPDATA%\Code\clp\<hash>.zh-cn\，
    # 不清理的话改源文件不会生效（缓存按语言包 hash 命中）。
    clp = os.path.join(os.environ.get("APPDATA", ""), "Code", "clp")
    purged = 0
    if os.path.isdir(clp):
        for name in os.listdir(clp):
            if name.endswith(".zh-cn"):
                shutil.rmtree(os.path.join(clp, name), ignore_errors=True)
                purged += 1
    print(f"已清理语言包编译缓存 {purged} 个")
    print("请完全退出 VS Code 后重新打开，改动才会生效。")


if __name__ == "__main__":
    main()

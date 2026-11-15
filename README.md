# VS Code Chat / Agent 界面简体中文补全

VS Code 1.131 起内置 Chat 界面（Agent 会话、智能体模式、权限、沙盒、产物自动规则等）大量文案尚未包含在官方简体中文语言包里，界面会出现中英混排。

本仓库提供一份**本地补丁**：把缺失的译文写入已安装的中文语言包，让这些界面显示为中文。

- 覆盖 **10,535 条**文案、**815 个模块**
- 目标命名空间中文覆盖率：**99.5%**（剩余 75 条是 GitHub / MCP / URL 等品牌与技术串，不翻译）
- 不修改 VS Code 本体，只改语言包扩展下的一个 JSON 文件

## 用法

### 前置条件

| 项目 | 要求 |
|---|---|
| 语言包 | 已安装 **Chinese (Simplified) Language Pack**（`ms-ceintl.vscode-language-pack-zh-hans`），且 VS Code 界面语言为中文 |
| Python | 3.8 及以上，`python` 可在终端直接调用 |
| VS Code | 执行前建议**完全退出**，避免缓存文件被占用导致删除失败 |

### 第一步：获取代码

```bash
git clone https://github.com/angel12538/vscode-chat-zh-hans.git
cd vscode-chat-zh-hans
```

不想用 git 的话，在仓库页面点 **Code → Download ZIP**，解压后进入该目录执行后续命令即可。

### 第二步：写入译文

```bash
python apply.py
```

正常输出如下（路径随你的语言包版本变化）：

```text
语言包: C:\Users\<用户名>\.vscode\extensions\ms-ceintl.vscode-language-pack-zh-hans-1.131.xxxxxxxx
已备份原始文件: backup\ms-ceintl.vscode-language-pack-zh-hans-1.131.xxxxxxxx-main.i18n.json
写入完成：新增 10535 条，覆盖 0 条
已清理语言包编译缓存 1 个
请完全退出 VS Code 后重新打开，改动才会生效。
```

脚本做三件事：定位已安装的语言包（多版本时取最新）→ 合并译文并首次备份原文件到 `backup/` → 删除编译缓存。

重复执行是安全的，第二次会显示「新增 0 条，覆盖 10535 条」。

### 第三步：完全退出并重启 VS Code

关掉所有 VS Code 窗口，并在任务管理器中确认 `Code.exe` 进程数为 **0**；托盘或后台残留的进程也一并结束，然后重新打开 VS Code。

> 只按 `Ctrl+Shift+P` → 「重新加载窗口」**不会生效**，原因见下方「为什么重载不生效」。必须让主进程退出，缓存才会重建。

### 验证

打开 Chat 面板，点开「智能体模式」或权限菜单，应看到：

```text
智能体模式 / 权限 / 手动确认权限 / 辅助权限 / 全部允许 / 终端沙盒
```

设置页搜索 `@tag:chatPermissions`，沙盒那组设置也应是中文（「允许出站连接」「允许绕过沙盒」等）。

### 还原官方原状

```bash
python revert.py
```

同样需要完全退出 VS Code 后重新打开。该脚本用 `backup/` 里的原始文件覆盖回去，并清理编译缓存。

### 语言包更新之后

语言包自动更新会整体覆盖本项目写入的译文，表现为界面又出现英文。重新执行一次即可，脚本会自动匹配升级后的新目录：

```bash
python apply.py
```

### 常见问题

| 现象 | 处理 |
|---|---|
| `未找到中文语言包` | 先安装 Chinese (Simplified) Language Pack，或确认语言包未被禁用 |
| 重启后仍是英文 | 大多是没有完全退出（后台还有 `Code.exe`）；也可能是语言包刚升级，重跑 `apply.py` |
| `PermissionError` / 文件被占用 | 退出 VS Code 后再执行 |
| `revert.py` 提示没有对应备份 | 语言包已升级，旧备份版本不匹配；在 VS Code 里重装该语言包即可恢复官方状态 |
| 个别条目仍是英文 | 键名可能随 VS Code 版本变化而失效，属于已知情况，不影响稳定性 |

## 为什么重载不生效

VS Code 启动时会把语言包预编译成缓存：

```text
%APPDATA%\Code\clp\<语言包hash>.zh-cn\<版本hash>\nls.messages.json
```

该缓存的目录名来自 `languagepacks.json` 里登记的语言包 hash。只修改语言包的源文件 `main.i18n.json` 时 hash 不变，VS Code 会继续命中旧缓存，界面仍旧是英文。`apply.py` 会主动删除该缓存目录，所以必须完整重启进程才会重建。

## 覆盖范围

| 模块命名空间 | 说明 |
|---|---|
| `vs/workbench/contrib/chat/` | Chat 面板、输入框、消息渲染 |
| `vs/platform/agentHost/` | 智能体宿主、会话配置、沙盒设置 |
| `vs/sessions/` | Agent 会话列表、会话操作、横幅 |
| `vs/platform/artifactIntegrations/` | 产物自动规则 |
| `vs/workbench/contrib/terminalContrib/chatAgentTools/` | 终端工具与沙盒设置项 |

主要术语处理：

| 英文 | 译文 |
|---|---|
| Agent mode | 智能体模式 |
| Permissions | 权限 |
| Manual / Assisted / Allow all | 手动确认权限 / 辅助权限 / 全部允许 |
| Autopilot（智能体模式） | 自动驾驶 |
| Autopilot（产物自动化） | 自动规则 |
| Sandboxing for terminal | 终端沙盒 |
| Worktree | 工作树 |

品牌名不翻译：GitHub、Copilot、Codex、Claude、MCP、BYOK、URL、HTTP、Kerberos、Dev Tunnels、Dev Container、Docker、Agent Host、Agent Merge、SDK、CLI。

## 文件结构

```text
apply.py        写入译文 + 清理编译缓存
revert.py       还原官方原始文件
zh_overlay.json 译文数据（模块 → 键 → 中文）
backup/         首次 apply 时自动生成的原始文件备份
```

## 注意

1. **语言包自动更新会覆盖本项目写入的内容**，更新后重新执行 `python apply.py` 即可。
2. 语言包大版本升级后，`backup/` 中的旧备份与新版不匹配，`revert.py` 会拒绝执行，此时在 VS Code 里重装语言包即可恢复官方原状。
3. `zh_overlay.json` 的键名对应 VS Code 内部 NLS 模块与消息键，随 VS Code 版本演进可能失效；失效表现为部分条目仍显示英文，不影响稳定性。
4. 本项目为社区本地化补丁，与 Microsoft、OpenAI、GitHub 无关。

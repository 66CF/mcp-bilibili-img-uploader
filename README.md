# MCP Bilibili Img Uploader

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 简介
MCP Bilibili Img Uploader 是一个基于 MCP（Model Context Protocol）的服务器项目，它允许大语言模型（LLM）调用工具，将本地图片上传到 Bilibili 图床，并返回图片的永久 HTTPS 链接。该项目提供了标准化接口，方便与大语言模型集成，同时通过 Cookie 进行身份验证，确保上传操作的安全性。

## 功能特点
- **B站图床支持**：直接将本地图片上传至 Bilibili 图床。
- **直链生成**：上传成功后自动生成图片的永久 HTTPS 链接。
- **标准化接口**：基于 MCP 协议，便于大语言模型调用。
- **Cookie 身份验证**：使用 Bilibili 的 `SESSDATA` 和 `bili_jct` 进行身份验证。

## 鸣谢
本项目中 Bilibili API 交互的核心代码逻辑参考自 [bilibili-img-uploader](https://github.com/xlzy520/bilibili-img-uploader)。

## 系统要求
- Python 3.8 或更高版本。
- 用于安装 Python 包的 `pip`。
- 有效的 Bilibili 账户。
- MCP 客户端应用程序，如 [Claude for Desktop](https://www.claude.ai/download)。

## 快速开始

### 1. 获取代码
将服务器代码保存为 `bilibili_uploader.py`。

### 2. 安装依赖
打开终端，运行以下命令安装必要的包：
```bash
pip install "mcp[cli]" httpx
```

### 3. 获取 Bilibili Cookies
1. 在浏览器中登录 [www.bilibili.com](https://www.bilibili.com)。
2. 按 `F12`（或 Mac 上的 `Cmd + Option + I`）打开开发者工具。
3. 找到 `Application`（Chrome/Edge）或 `Storage`（Firefox）选项卡。
4. 在左侧菜单的 `Cookies` 下，选择 `https://www.bilibili.com`。
5. 找到并复制以下两项的 **Value**（值）：
    - `SESSDATA`
    - `bili_jct`

### 4. 运行服务器
在 `bilibili_uploader.py` 文件所在的目录打开终端，启动服务器：
```bash
python bilibili_uploader.py
```
服务器启动后将等待客户端连接。

### 5. 连接到 MCP 客户端（以 Claude for Desktop 为例）
1. 找到并打开 `claude_desktop_config.json` 配置文件：
    - **macOS**：`~/Library/Application Support/Claude/claude_desktop_config.json`
    - **Windows**：`%APPDATA%\Claude\claude_desktop_config.json`
2. 在文件中添加以下服务器配置，**务必将路径替换为你 `bilibili_uploader.py` 脚本的绝对路径**：
```json
{
    "mcpServers": {
        "bilibili-uploader": {
            "command": "python",
            "args": [
                "/path/to/your/project/bilibili_uploader.py"
            ]
        }
    }
}
```
3. 完全关闭并重启 Claude for Desktop 使配置生效。

### 6. 在对话中使用
- **第一步：设置 Cookies（每个会话只需一次）**
在客户端中与 LLM 对话，输入类似以下内容：
```plaintext
请设置我的 Bilibili Cookies。我的 SESSDATA 是 `your_sessdata_value_here`，bili_jct 是 `your_bili_jct_value_here`。
```
- **第二步：上传图片**
输入类似以下内容：
```plaintext
请把 `/Users/me/Desktop/photo.png` 这张图片上传到 Bilibili。
```
LLM 将调用工具完成上传，并返回图片的永久 HTTPS 链接。

## 代码结构
- `bilibili_uploader.py`：核心代码文件，实现了 MCP 服务器的初始化和两个工具函数 `set_bilibili_cookies` 和 `upload_image`。
- `README.md`：项目说明文档，包含项目简介、功能特点、系统要求、快速开始步骤等信息。
- `LICENSE`：项目使用的开源协议文件。

## 许可证
本项目采用 MIT License 许可，详情请见 [LICENSE](LICENSE) 文件。

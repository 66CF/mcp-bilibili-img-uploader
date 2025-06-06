# MCP Bilibili Img Uploader

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 简介
一个MCP（Model Context Protocol）服务器，能让大语言模型（LLM）调用工具将本地图片上传到Bilibili图床。

## 鸣谢
- Bilibili API 交互的核心代码逻辑参考自 [bilibili-img-uploader](https://github.com/xlzy520/bilibili-img-uploader)

## 功能特点
- B站图床
- 直链生成
- 基于 MCP 协议的标准化接口
- 基于 Cookie 的身份验证

## 系统要求
-   Python 3.8 or higher.
-   `pip` for installing Python packages.
-   An active Bilibili account.
-   An MCP client application, such as [Claude for Desktop](https://www.claude.ai/download).

## 快速开始
1.  **Clone the repository or save the script:**
    Save the server code as `bilibili_uploader.py`.
2.  **Install the required dependencies:**
    Open your terminal and run the following command to install the necessary packages.

    ```bash
    pip install "mcp[cli]" httpx
    ```

### 获取Bilibili Cookies
1.  在浏览器中登录 [www.bilibili.com](https://www.bilibili.com)。
2.  按 `F12` (或 Mac上的 `Cmd+Option+I`) 打开开发者工具。
3.  找到 `Application` (Chrome/Edge) 或 `Storage` (Firefox) 选项卡。
4.  在左侧菜单的 `Cookies` 下，选择 `https://www.bilibili.com`。
5.  找到并复制以下两项的 **Value** (值):
    *   `SESSDATA`
    *   `bili_jct`

### 运行服务器

在 `bilibili_uploader.py` 文件所在的目录打开终端，启动服务器：
```bash
python bilibili_uploader.py
```
服务器启动后将等待客户端连接。

### 连接到MCP客户端 (以Claude for Desktop为例)

1.  找到并打开 `claude_desktop_config.json` 配置文件：
    *   **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
    *   **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2.  在文件中添加以下服务器配置。**务必将路径替换为你 `bilibili_uploader.py` 脚本的绝对路径**。

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

3.  完全关闭并重启Claude for Desktop使配置生效。

### 在对话中使用

现在，你可以在客户端中通过与LLM对话来使用上传功能。

**第一步：设置Cookies（每个会话只需一次）**
> 请设置我的Bilibili Cookies。我的SESSDATA是 `your_sessdata_value_here`，bili_jct是 `your_bili_jct_value_here`。

**第二步：上传图片**
> 请把 `/Users/me/Desktop/photo.png` 这张图片上传到Bilibili。

LLM将调用工具完成上传，并返回图片的永久HTTPS链接。

# Bilibili Uploader MCP Server

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A Model Context Protocol (MCP) server that enables a Large Language Model (LLM) to upload images to Bilibili's image hosting service.

This server exposes tools that allow an LLM to authenticate using your Bilibili browser cookies and upload local image files, returning a direct, permanent HTTPS link. It works by replicating the API requests made by Bilibili's own web uploader.

## ✨ Features

-   **Upload Images**: Provides a tool to upload local images (`.jpg`, `.png`, `.gif`, etc.) to Bilibili's fast and reliable CDN.
-   **Cookie-Based Authentication**: Securely uses your Bilibili session cookies to authenticate with the API, without needing your username or password.
-   **Direct Link Generation**: Returns a clean, direct HTTPS URL to the uploaded image, ready for use in Markdown, HTML, or any other application.
-   **LLM Integration**: Built as an MCP server, allowing any compatible AI agent or application (like Claude for Desktop) to use its tools.

## ⚙️ Prerequisites

-   Python 3.8 or higher.
-   `pip` for installing Python packages.
-   An active Bilibili account.
-   An MCP client application, such as [Claude for Desktop](https://www.claude.ai/download).

## 🚀 Installation

1.  **Clone the repository or save the script:**
    Save the server code as `bilibili_uploader.py`.

2.  **Install the required dependencies:**
    Open your terminal and run the following command to install the necessary packages.

    ```bash
    pip install "mcp[cli]" httpx
    ```

## 🔑 Configuration: Getting Your Bilibili Cookies

To upload images, the server needs to authenticate as you. This is done using your browser's cookies. You only need to do this once, and then use the `set_bilibili_cookies` tool.

> **Warning:** Your cookies are sensitive credentials. Treat them like passwords and never share them with anyone.

1.  **Log in to Bilibili**: Open your web browser and log in to [www.bilibili.com](https://www.bilibili.com).
2.  **Open Developer Tools**: Press `F12` (or `Cmd+Option+I` on Mac) to open the developer tools.
3.  **Navigate to Cookies**:
    -   In Chrome/Edge: Go to the `Application` tab.
    -   In Firefox: Go to the `Storage` tab.
4.  **Find the Cookies**: In the left-hand menu, expand "Cookies" and select `https://www.bilibili.com`.
5.  **Copy the Values**: Find the following two cookies and copy their "Value" fields:
    -   `SESSDATA`
    -   `bili_jct`

You will use these values in the `set_bilibili_cookies` tool after starting the server.

## ⚡️ Usage

### Step 1: Run the Server

Open your terminal in the same directory as the `bilibili_uploader.py` file and run the server:

```bash
python bilibili_uploader.py
```

The server is now running and waiting for a client to connect.

### Step 2: Connect to an MCP Client

You need to connect this server to an MCP client. The example below is for Claude for Desktop.

1.  **Open Claude for Desktop Configuration**: Find and open the `claude_desktop_config.json` file.
    -   **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
    -   **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2.  **Add the Server Configuration**: Add the following JSON snippet to the file. **Make sure to replace `/path/to/your/project/bilibili_uploader.py` with the absolute path** to your script.

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

3.  **Restart Claude for Desktop**: Completely close and restart the application for the changes to take effect.

### Step 3: Authenticate in the Chat

Before you can upload, you must provide your cookies to the server using the `set_bilibili_cookies` tool. You can do this by asking the LLM in your chat interface.

**Example Prompt:**

> Please set my Bilibili cookies. My SESSDATA is `your_sessdata_value_here` and my bili_jct is `your_bili_jct_value_here`.

The LLM will call the tool, and you will see a confirmation message.

### Step 4: Upload an Image

Now you can ask the LLM to upload an image.

**Example Prompt:**

> Please upload the image located at `/Users/myuser/Desktop/my_awesome_photo.png` to Bilibili.

The LLM will call the `upload_image` tool, and if successful, it will return the direct URL to the uploaded image.

## 🛠️ Tool Reference

This server exposes the following tools to the LLM:

### `set_bilibili_cookies`

Sets the authentication cookies required for all upload operations.

-   **Arguments**:
    -   `sessdata` (string, required): The `SESSDATA` cookie value.
    -   `bili_jct` (string, required): The `bili_jct` cookie value, which acts as a CSRF token.
-   **Returns**:
    -   A string confirming that the cookies were set successfully.

### `upload_image`

Uploads a local image file to Bilibili's hosting service.

-   **Arguments**:
    -   `file_path` (string, required): The **absolute path** to the image file on your local machine.
-   **Returns**:
    -   A string containing the direct HTTPS URL of the uploaded image, or an error message if the upload failed.

## ⚠️ Disclaimer

-   This is an unofficial tool and is not affiliated with Bilibili.
-   The server relies on Bilibili's internal APIs, which may change at any time without notice, potentially breaking this tool.
-   You are responsible for the security of your own account. **Do not share your `SESSDATA` cookie with anyone.**

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

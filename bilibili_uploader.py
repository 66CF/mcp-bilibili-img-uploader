import httpx
import os
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP(
    "bilibili-uploader",
    "A server to upload images to Bilibili's image hosting service."
)

# In-memory storage for cookies for the current session.
bili_cookies = {
    "SESSDATA": None,
    "bili_jct": None,
}

@mcp.tool()
async def set_bilibili_cookies(sessdata: str, bili_jct: str) -> str:
    """
    Sets the Bilibili authentication cookies required for uploads. These can be
    retrieved from your browser's cookie storage after logging into bilibili.com.

    Args:
        sessdata: The SESSDATA cookie value from your Bilibili account.
        bili_jct: The bili_jct cookie value (CSRF token) from your Bilibili account.
    """
    global bili_cookies
    bili_cookies["SESSDATA"] = sessdata
    bili_cookies["bili_jct"] = bili_jct
    return "Bilibili cookies have been set successfully. You can now use the upload_image tool."

@mcp.tool()
async def upload_image(file_path: str) -> str:
    """
    Uploads a local image to the Bilibili image hosting service and returns its online URL.
    Requires set_bilibili_cookies to be called first.

    Args:
        file_path: The absolute path to the local image file.
    """
    global bili_cookies
    if not bili_cookies["SESSDATA"] or not bili_cookies["bili_jct"]:
        return "Error: Bilibili cookies are not set. Please call 'set_bilibili_cookies' first with your SESSDATA and bili_jct values."

    if not os.path.exists(file_path):
        return f"Error: File not found at the specified path: {file_path}"

    upload_url = "https://api.bilibili.com/x/upload/web/image"
    
    try:
        with open(file_path, "rb") as f:
            files = {'file': (os.path.basename(file_path), f, 'image/png')}
            # --- FIX IS HERE ---
            # Added the required 'bucket' parameter to the data payload.
            data = {
                'bucket': 'openplatform',
                'csrf': bili_cookies['bili_jct']
            }
            # --- END FIX ---
            cookies = {
                'SESSDATA': bili_cookies['SESSDATA'],
            }
            
            headers = {
                'Origin': 'https://www.bilibili.com',
                'Referer': 'https://www.bilibili.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    upload_url,
                    data=data,
                    files=files,
                    cookies=cookies,
                    headers=headers,
                    timeout=30.0
                )
                response.raise_for_status()
                
                response_data = response.json()
                
                if response_data.get("code") == 0:
                    location = response_data.get("data", {}).get("location")
                    if location:
                        https_url = location.replace("http://", "https://")
                        return f"Upload successful! URL: {https_url}"
                    else:
                        return f"Error: Upload succeeded but no 'location' field found in the response: {response_data}"
                elif response_data.get('message') == '请先登录':
                     return "Error: Authentication failed. The provided SESSDATA cookie may be invalid or expired. Please update it using 'set_bilibili_cookies'."
                else:
                    return f"Error: Bilibili API returned an error: {response_data.get('message', 'Unknown error')}"

    except httpx.HTTPStatusError as e:
        return f"HTTP Error: An error occurred while communicating with the Bilibili API. Status: {e.response.status_code}. Response: {e.response.text}"
    except Exception as e:
        return f"An unexpected error occurred during the upload process: {str(e)}"

if __name__ == "__main__":
    mcp.run()
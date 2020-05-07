#refer to docs at: https://pastebin.com/api
import requests
import pyperclip
import time

URL = "https://pastebin.com/api/api_post.php"
OPTION = "paste"

DEV_KEY: str = "token"  # your dev key, shown at https://pastebin.com/api
USER_KEY: str = "" #if your key is not set, execute generate_user_key() to cache it here. This is recommended by pastebin

# data limitations:
# guest - 10 pastes/24h, unlimited public, unlimited unlisted, no private
# free - 20 pastes/24h, unlimited public, 10 unlisted, 2 private
# pro - 250 pastes/24h, unlimited

def clipboard_to_link(name="sharedCode", language="python", private="0", expire="N"):
    clipboard = pyperclip.paste()
    if not clipboard:
        print("Error: Empty Paste")
        time.sleep(2)
        return
    else:
        data_dict = {
            "api_dev_key": DEV_KEY,
            "api_user_key": USER_KEY,  # if not set, post will get generated from guest account
            "api_option": "paste",
            "api_paste_code": clipboard,
            "api_paste_private": private,  # 0=public, 1=unlisted, 2=private
            "api_paste_expire_date": expire,
            "api_paste_format": language,
            "api_paste_name": name,
        }
        link = requests.post(URL, data=data_dict)

        if link.text.startswith("http"):
            pyperclip.copy(link.text)
            return link.text
        else:
            print(link.text)
            time.sleep(2)
            return


def generate_user_key(user_name, password):
    data_dict = {
        "api_dev_key": DEV_KEY,
        "api_user_name": user_name,
        "api_user_password": password
    }
    key = requests.post("https://pastebin.com/api/api_login.php", data=data_dict)
    return key.text


if __name__ == "__main__":
    clipboard_to_link()

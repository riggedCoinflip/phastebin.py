#refer to docs at: https://pastebin.com/api
import requests
import time
import json
import sys, getopt
import pyperclip

def setup():
    #setup needed for pastebin
    try:
        with open("keys.json", "r") as f:
            keys = json.load(f)
    except OSError:
        print("Couldn't open or find file 'keys.json'")
        print("A new file will be created")
    if any(("dev_key", "user_key")) not in keys:
        if "dev_key" not in keys:
            print("Your developer key is not set. You can find it on https://pastebin.com/api once you are logged in.")
            keys["dev_key"] = input("Please enter your developer key: ")
        if "user_key" not in keys:
            print("Couldn't find your user key. A new one will be generated. This requires your login data.")
            keys["user_key"] = generate_user_key(keys["dev_key"], input("username: "), input("password: "))
        with open("keys.json", "w") as f:
            json.dump(keys, f, indent=4)
    return keys

def generate_user_key(dev_key, user_name, password):
    data_dict = {
        "api_dev_key": dev_key,
        "api_user_name": user_name,
        "api_user_password": password
    }
    key = requests.post("https://pastebin.com/api/api_login.php", data=data_dict)
    return key.text

def pastebin(name="https://github.com/riggedCoinflip/phastebin.py", language="python", private="0", expire="1D"):
    # data limitations:
    # guest - 10 pastes/24h, unlimited public, unlimited unlisted, no private
    # free - 20 pastes/24h, unlimited public, 10 unlisted, 2 private
    # pro - 250 pastes/24h, unlimited

    keys = setup()

    clipboard = pyperclip.paste()
    if not clipboard:
        print("Error: Empty Paste")
        time.sleep(2)
        return
    elif not isinstance(clipboard, str):
        print("Error: Paste is not a String")
        time.sleep(2)
        return
    else:
        data_dict = {
            "api_dev_key": keys["dev_key"],
            "api_user_key": keys["user_key"],  # if not set, post will get generated from guest account
            "api_option": "paste",
            "api_paste_code": clipboard,
            "api_paste_private": private,  # 0=public, 1=unlisted, 2=private
            "api_paste_expire_date": expire,
            "api_paste_format": language,
            "api_paste_name": name,
        }
        link = requests.post("https://pastebin.com/api/api_post.php", data=data_dict)

        if link.text.startswith("http"):
            pyperclip.copy(link.text)
            return link.text
        else:
            print(link.text)
            time.sleep(2)
            return

def hastebin():
    #docs at https://github.com/seejohnrun/haste-server/wiki/POST-api
    url = "https://hastebin.com/documents"
    clipboard = pyperclip.paste()
    if not clipboard:
        print("Error: Empty Paste")
        time.sleep(2)
        return
    elif not isinstance(clipboard, str):
        print("Error: Paste is not a String")
        time.sleep(2)
        return
    else:
        link = requests.post(url, data=clipboard)
        if link:
            d = json.loads(link.text)
            key = d["key"]
            return_link = f"https://hastebin.com/{key}"
            pyperclip.copy(return_link)
            return return_link
        else:
            print("Error: Connection Timeout")
            time.sleep(2)
            return

def link_to_clipboard():
    paste = pyperclip.paste()
    if not paste:
        print("Error: Empty Paste")
        time.sleep(2)
        return
    elif not isinstance(paste, str):
        print("Error: Paste is not a String")
        time.sleep(2)
        return
    elif any(str(paste).startswith(x) for x in ("https://pastebin.com/", "pastebin.com/")):
        paste = str(paste).rsplit(r'/', 1)[-1]
        link = f"https://pastebin.com/raw/{paste}"
        response = requests.get(link)
        if response:
            print(response.text)
            pyperclip.copy(response.text)
            return response.text
        else:
            print("Error: Connection Timeout")
            time.sleep(2)
            return
    elif any(str(paste).startswith(x) for x in ("https://hastebin.com/", "hastebin.com/")):
        paste = str(paste).rsplit(r'/', 1)[-1]
        link = f"https://hastebin.com/documents/{paste}"
        response = requests.get(link)
        if response:
            d = json.loads(response.text)
            code = d["data"]
            print(code)
            pyperclip.copy(code)
            return code
        else:
            print("Error: Connection Timeout")
            time.sleep(2)
            return
    else:
        print(f"Error: Paste '{paste}'\n is not a (h/p)astebin link")
        time.sleep(2)
        return


if __name__ == "__main__": # needs to run with arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:p", ["copy=", "paste"])
        for opt, arg in opts:
            if opt in ("-c", "--copy"):
                if arg == "pastebin":
                    pastebin()
                elif arg == "hastebin":
                    hastebin()
                else:
                    raise getopt.GetoptError(f"Arg not allowed: {arg}")
            if opt in ("-p", "--paste"):
                link_to_clipboard()
    except getopt.GetoptError:
        print("phastebin.py { { -c | --copy } { pastebin | hastebin } } | { -p  | --paste } ")
        sys.exit(2)

import dload
import requests
import json
import os
import shutil

MINECRAFT_DIRECTORY = os.path.join(os.curdir, ".minecraft")
E2E_PROFILE_DIRECTORY = os.path.join(MINECRAFT_DIRECTORY, "profiles", "E2E")
PYMINELAUNCHER = os.path.join(os.curdir, "pyminelauncher", "pml.exe")

MODPACK_GITHUB_URL = "https://github.com/Nobody1902/e2e-modpack.git"

MODPACK_VERSION_URL = "https://raw.githubusercontent.com/Nobody1902/e2e-modpack/main/version.txt"
VERSION_FILE = os.path.join(os.curdir, "version.txt")
CURRENT_VERSION:str

def check_version()->bool:

    if not os.path.exists(VERSION_FILE):
        return False

    version = get_version()[0]

    print("Reading version file.")

    with open(VERSION_FILE) as f:
        CURRENT_VERSION = json.loads(f.read())["version"]
    

    print(f"Current version is '{CURRENT_VERSION}' and the latest is '{version}'")
    
    return CURRENT_VERSION == version

def get_version()->tuple[str, str]:
    response = requests.get(MODPACK_VERSION_URL)

    contents = response.content.decode()
    data = json.loads(contents)
    
    version = data["version"]
    minecraft_version = data["minecraft_version"]

    return (version, minecraft_version)

def download_modpack():
    print("Fetching modpack versions...")
    version = get_version()

    print("Downloading minecraft...")
    os.system(f"{PYMINELAUNCHER} create {version[1]} E2E")


    print("Downloading modpack - This may take a long time ...")
    abs_tmp_path = os.curdir + "\\"
    # download github repo
    modpack_path = dload.git_clone(MODPACK_GITHUB_URL, abs_tmp_path)

    shutil.copytree(os.path.join(modpack_path, "e2e-modpack-main", "modpack"), os.path.join(E2E_PROFILE_DIRECTORY, "game"), dirs_exist_ok=True)
    
    with open(VERSION_FILE, "w") as f:
        f.write(json.dumps({"version": version[0], "minecraft_version": version[1]}))
    
    shutil.rmtree(os.path.join(modpack_path, "e2e-modpack-main"))


if not check_version():
    download_modpack()

if not os.path.exists(os.path.join(os.curdir, "username.txt")):
    username = input("Enter your username: ")

    with open(os.path.join(os.curdir, "username.txt"), "w") as f:
        f.write(username)
    
    print(f"Set username to '{username}'.")
    print("You can change your username in the 'username.txt' file.")

with open(os.path.join(os.curdir, "username.txt"), "r") as f:
    username = f.read()

os.system(f"{PYMINELAUNCHER} launch E2E \"{username}\" 8192")
from pySmartDL import SmartDL
from TechZApi import TechZApi
import os


# Getting TechZApi Key

try:
    API_KEY = open("key.txt", "r").read().strip()
except:
    API_KEY = None

if not API_KEY or API_KEY == "":
    print("Enter Your TechZ Api Key (Get From https://t.me/TechZApiBot) ")
    API_KEY = input("Enter Your TechZ Api Key: ")
    with open("key.txt", "w") as f:
        f.write(API_KEY)

TechZApi = TechZApi(API_KEY)


# Getting Anime Name

while True:
    # Search Anime

    search = input("\nEnter Anime Name: ")
    if search == "":
        print(">> Anime Name Can't Be Empty")
        continue

    try:
        search = TechZApi.gogo_search(search)
    except Exception as e:
        print(">> Error: ", e)
        continue

    if len(search) == 0:
        print(">> Anime Not Found")
        continue
    else:
        break


# Select Anime

print("\n", "=" * 50, "\n\n>> Select Anime", sep="")
pos = 1
for i in search:
    print(f"{pos}. {i['title']}")
    pos += 1

while True:
    try:
        select = int(input("\nEnter Your Choice (1,2,3...): "))
        anime = search[select - 1]
        break
    except KeyboardInterrupt:
        print(">> Exiting...")
        exit()
    except:
        print(">> Invalid Choice")
        continue


# Episodes

title = anime.get("title")
episodes = TechZApi.gogo_anime(anime.get("id")).get("episodes")
print("\n", "=" * 50, "\n\n>> Select Episode", sep="")

for i in episodes:
    x, y = i.split("-episode-")
    print(f"Episode {y}")

while True:
    try:
        select = int(input("\nEnter Your Choice (1,2,3...): "))
        episode = episodes[select - 1]
        break
    except KeyboardInterrupt:
        print(">> Exiting...")
        exit()
    except:
        print(">> Invalid Choice")
        continue

# Episode Links


links = TechZApi.gogo_episode(episode).get("DL")
if links.get("SUB"):
    print("1. SUB")
if links.get("DUB"):
    print("2. DUB")

while True:
    try:
        select = int(input("Enter Your Choice (1,2): "))
        if select == 1:
            link = links.get("SUB")
            break
        elif select == 2:
            link = links.get("DUB")
            break
        else:
            print(">> Invalid Choice")
            continue
    except KeyboardInterrupt:
        print(">> Exiting...")
        exit()
    except:
        print(">> Invalid Choice")
        continue

print("\n", "=" * 50, "\n\n>> Select Quality", sep="")

pos = 1
for q in link.keys():
    print(f"{pos}. {q}")
    pos += 1

while True:
    try:
        select = int(input("Enter Your Choice (1,2,3...): "))
        quality = list(link.keys())[select - 1]
        break
    except KeyboardInterrupt:
        print(">> Exiting...")
        exit()
    except:
        print(">> Invalid Choice")
        continue

download_link = link.get(quality)

print("\n", "=" * 50, "\n\n>> Starting Download...\n", sep="")

dest = "./Downloads/"
path = (
    "./Downloads/"
    + title
    + "/"
    + episode.replace("-", " ").title()
    + " - "
    + quality
    + "p.mp4"
)
if not os.path.exists("./Downloads/"):
    os.mkdir("./Downloads")
if not os.path.exists("./Downloads/" + title):
    os.mkdir("./Downloads/" + title)

for i in range(3):
    try:
        obj = SmartDL(download_link, dest)
        obj.start()
        break
    except Exception as e:
        if "Destination path" in str(e):
            dest = str(e).split("'")[1]
            os.rename(dest, path)
            break
        print(">> Error: ", e)
        print("\n>> Retrying...")
        continue

print("\n", "=" * 50, "\n\n>> Downloaded Successfully")
os.rename(obj.get_dest(), path)
print(">> File Path: ", path)

input("Press Enter To Exit...")

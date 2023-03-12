import os
import asyncio
import aiofiles
import aiohttp
from TechZApi import TechZApi
import sys


# Getting TechZApi Key

try:
    API_KEY = open("key.txt", "r").read().strip()
except:
    API_KEY = None

if not API_KEY or API_KEY == "":
    print("Your TechZ Api Key (Get From https://telegram.me/TechZApiBot) ")
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
        ep_range = input(
            "\nEnter The Episodes You Want To Download (Ex 2, 3-8) || Enter * To Download All Episodes : "
        )
        if ep_range == "*":
            break
        if "-" not in ep_range:
            episodes = [episodes[int(ep_range) - 1]]
            break

        x, y = ep_range.split("-")
        episodes = episodes[(int(x) - 1) : int(y)]
        break
    except KeyboardInterrupt:
        print(">> Exiting...")
        exit()
    except:
        print(">> Invalid Choice")
        continue


# Audio

print("\n", "=" * 50, "\n\n>> Select Audio", sep="")

print("1. SUB")
print("2. DUB")

while True:
    try:
        select = int(input("Enter Your Choice (1,2): "))
        if select == 1:
            aud = "SUB"
            break
        elif select == 2:
            aud = "DUB"
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


# Quality

print("\n", "=" * 50, "\n\n>> Select Quality", sep="")

print("1. 360p")
print("2. 480p")
print("3. 720p")
print("4. 1080p")

while True:
    try:
        select = int(input("Enter Your Choice (1,2,3...): "))

        if select == 1:
            quality = "360"
        elif select == 2:
            quality = "480"
        elif select == 3:
            quality = "720"
        elif select == 4:
            quality = "1080"
        break
    except KeyboardInterrupt:
        print(">> Exiting...")
        exit()
    except:
        print(">> Invalid Choice")
        continue


# Getting Links

print("\n", "=" * 50, "\n\n>> Getting Download Urls...\n", sep="")


if not os.path.exists("./Downloads/"):
    os.mkdir("./Downloads")
if not os.path.exists("./Downloads/" + title):
    os.mkdir("./Downloads/" + title)

download_links = []

for i in episodes:
    try:
        url = TechZApi.gogo_episode(i).get("DL").get(aud).get(quality)
        path = (
            "./Downloads/"
            + title
            + "/"
            + i.replace("-", " ").title()
            + " - "
            + quality
            + "p.mp4"
        )
        download_links.append((path, url))
        print(">> Got Download Link Of: ", i)
    except Exception as e:
        print(">> Failed To Get Download Link Of: ", i)
        continue

# Downloader

print("\n", "=" * 50, "\n\n>> Batch Download Started...\n", sep="")

status = {}


async def download(session, name, url):
    async with session.get(url) as response:
        total = response.content_length / 1024
        done = 0
        async with aiofiles.open(name, "wb") as f:
            async for data in response.content.iter_chunked(1024):
                status[name] = round(done / total * 100, 2)
                done += 1
                await f.write(data)


def clear_line(n=1):
    LINE_UP = "\033[1A"
    LINE_CLEAR = "\x1b[2K"
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)


async def progress():
    while True:

        text = (
            "=" * 50
            + f"\n\n>> AniDL || Downloading {title} {aud} {quality}p : {ep_range}\n\n"
        )
        n = 2
        x = 0

        for k, v in sorted(status.items(), key=lambda x: x[0]):
            file = k.split("/")[-1]
            percent = f"v %" if v < 100 else "Completed"

            if x == 0:
                text += "File Name".center(len(file)) + " : Progress\n\n"
                n += 2
                x = 1

            text += f"{file} : {percent}\n"
            n += 1

        clear_line(n + 3)
        print(text)
        await asyncio.sleep(5)


async def main():
    global pos
    tasks = [progress()]
    session = aiohttp.ClientSession()

    for i in download_links:
        task = asyncio.create_task(download(session, i[0], i[1]))
        tasks.append(task)
        pos += 1

    await asyncio.gather(*tasks)
    await session.close()


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
    loop.run_until_complete(loop.shutdown_asyncgens())
finally:
    loop.close()

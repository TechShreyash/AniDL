import asyncio, aiohttp, os
from Utils.File import convertFilePath
from Utils.TechZApi import TechZApi
from Utils.Downloader import startM3U8Download, resetCache
from Utils.FFmpeg import ConvertTsToMp4

TechZApi = TechZApi()

# Getting Anime Name

while True:
    # Search Anime

    search = input("\nEnter Anime Name: ")
    if search == "":
        print(">> Anime Name Can't Be Empty")
        continue

    try:
        search = TechZApi.gogo_search(search.lower())
    except Exception as e:
        print(">> Error: ", e)
        continue

    if len(search) == 0:
        print(">> Anime Not Found")
        continue
    else:
        break


# Select Anime

print("\n", "=" * 50)
print("\n>> Select Anime\n")
pos = 1
print("-" * 53)
print("|" + "Index".center(10) + "|" + "Anime Name".center(40) + "|")
print("-" * 53)
for i in search:
    print("|" + str(pos).center(10) + "|" + str(i.get("title")).center(40) + "|")
    pos += 1
print("-" * 53)

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
anime = TechZApi.gogo_anime(anime.get("id"))["results"]
episodes = anime["episodes"]

print("\n", "=" * 50)
print("\n>> Select Episode\n", sep="")
print(f"Episode 1 - {len(episodes)} Are Available")

while True:
    try:
        print(
            "\nEnter The Episodes You Want To Download (Ex 2, 3-8) || Enter * To Download All Episodes"
        )
        ep_range = input("\nEpisodes To Download : ")
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

print("\n", "=" * 50)


# Download
async def StartDownload():
    resetCache()
    try:
        os.mkdir(convertFilePath(f"./Downloads/{anime.get('name')}"))
    except:
        pass
    session = aiohttp.ClientSession()
    print(
        "\nEnter Number Of Workers To Parallel Download (Recommended: 4,8,16) - Depends On Your Internet Speed/PC Specs (CPU Cores)"
    )
    workers = int(input("\nNo. Of Workers: "))
    print("\n>> Downloading Episodes")

    for ep in episodes:
        episode_id = ep[1]
        ep = ep[0]
        try:
            anime['name']= anime['name'].replace("/", " ").replace("\\",'')
            print(f"\n\n>> Downloading Episode {ep} - {quality}p")
            data = TechZApi.gogo_episode(episode_id)["results"]
            file = data["stream"]["sources"][0]["file"]
            await startM3U8Download(session, file, quality, workers)
            print(f">> Episode {ep} - {quality}p Downloaded")
            filepath = convertFilePath(
                f"./Downloads/{anime.get('name')}/{anime.get('name')} - Episode {ep} - {quality}p.mp4"
            )
            ConvertTsToMp4(filepath)
            resetCache()
        except Exception as e:
            print("Failed To Download Episode", ep)
            print(">> Error: ", e)
            continue
    await session.close()


asyncio.run(StartDownload())

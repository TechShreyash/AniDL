import aiohttp, asyncio, aiofiles, os

folder_path = "./Downloads/temp/"


async def startM3U8Download(session, url, quality, workers):
    print(">> Getting Download Links")
    path = "/".join(url.split("/")[:-1]) + "/"

    async with session.get(url) as response:
        resp = await response.text()

    quality = []
    for i in resp.split("\n"):
        if i.startswith("ep"):
            quality.append((i.split(".")[3], path + i.strip()))

    for i in quality:
        if i[0] == "1080":
            file = i[1]

    async with session.get(file) as response:
        resp = await response.text()

    chunks = []
    for i in resp.split("\n"):
        if i.startswith("ep"):
            chunks.append(path + i.strip())

    TOTAL = len(chunks)

    chunkSize = TOTAL // workers
    chunkList = []
    for i in range(workers - 1):
        chunkList.append(chunks[:chunkSize])
        chunks = chunks[chunkSize:]

    chunkList.append(chunks)

    tasks = [progress(TOTAL)]
    pos = 1
    for i in chunkList:
        tasks.append(downloadChunks(pos, session, i))
        pos += 1

    await asyncio.gather(*tasks)


chunksDownloaded = 0
sizeDownloaded = 0


def resetCache():
    global chunksDownloaded, sizeDownloaded
    chunksDownloaded = 0
    sizeDownloaded = 0
    try:
        os.mkdir("./Downloads")
    except:
        pass
    try:
        os.mkdir(folder_path)
    except:
        pass

    files = os.listdir(folder_path)
    for file in files:
        os.remove(folder_path + file)


def clearLine(n=1):
    for i in range(n):
        print("\033[1A\x1b[2K", end="")


async def progress(TOTAL):
    global chunksDownloaded, sizeDownloaded
    x = 0
    c = 0
    t = 0

    print("-" * 88)
    print(
        "|"
        + "Chunks Downloaded".center(21)
        + "|"
        + "Chunks/sec".center(14)
        + "|"
        + "Size Downloaded".center(19)
        + "|"
        + "Speed".center(15)
        + "|"
        + "Time Left".center(13)
        + "|"
    )
    print("-" * 88 + "\n\n")

    while True:
        if chunksDownloaded == TOTAL:
            break

        speed = round((sizeDownloaded - x) / (1024 * 1024 * 2), 2)  # per sec
        speed2 = round((chunksDownloaded - c) / 2)  # per sec
        if speed2 == 0:
            speed2 = 1
        time = round(((TOTAL - chunksDownloaded) / speed2) / 60, 2)  # in min
        size = round(sizeDownloaded / (1024 * 1024))  # in MB

        clearLine(2)
        print(
            "|"
            + f"{chunksDownloaded}/{TOTAL}".center(21)
            + "|"
            + f"{speed2} Chunks".center(14)
            + "|"
            + f"{size} MB".center(19)
            + "|"
            + f"{speed} MB/s".center(15)
            + "|"
            + f"{time} min".center(13)
            + "|"
        )
        print("-" * 88)
        x = sizeDownloaded
        c = chunksDownloaded

        await asyncio.sleep(2)


async def downloadChunks(pos, session: aiohttp.ClientSession, chunks):
    global chunksDownloaded, sizeDownloaded

    async with aiofiles.open(f"{folder_path}{pos}.ts", "ab") as f:
        for i in chunks:
            async with session.get(i) as response:
                resp = await response.read()

            await f.write(resp)

            sizeDownloaded += len(resp)
            chunksDownloaded += 1

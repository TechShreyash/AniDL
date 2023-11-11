import subprocess
import os, re


def get_total_frames(video_file):
    command = [
        "ffmpeg",
        "-i",
        video_file,
        "-map",
        "0:v:0",
        "-c",
        "copy",
        "-f",
        "null",
        "-",
    ]

    result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

    x = result.stderr
    while "frame" in x:
        x = x[x.find("frame") + 6 :]
    x = x[: x.find("fps")].strip()
    return int(x)


def ConvertTsToMp4(path):
    print("\n>> Converting To Mp4")
    TOTAL_FRAMES = 0
    with open("./Downloads/temp/files.txt", "w") as f:
        for i in os.listdir("./Downloads/temp"):
            if i.endswith(".ts"):
                TOTAL_FRAMES += get_total_frames("./Downloads/temp/" + i)
                f.write(f"file '{i}'\n")

    command = "ffmpeg -f concat -safe 0 -i ./Downloads/temp/files.txt -c copy ./Downloads/temp/output.mp4 -y".split()
    process = subprocess.Popen(command, stderr=subprocess.PIPE)

    progress_regex = re.compile(r"frame=\s*(\d+)")

    while True:
        output = process.stderr.readline()
        if process.poll() is not None:
            break

        # Extract progress information using the regex
        match = progress_regex.search(output.decode("utf-8"))
        if match:
            frame_number = int(match.group(1))
            percent = round((frame_number * 50) / TOTAL_FRAMES)
            print("=" * percent + f"> {percent*2} %", end="\r")

    process.wait()
    percent = 50
    print("=" * percent + f"> {percent*2} %", end="\r")
    print("\nConversion complete.")

    try:
        os.remove(path)
    except:
        pass
    os.rename("./Downloads/temp/output.mp4", path)

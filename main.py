"""
Import Modules
"""

import requests
import os
import sys


def api_request(query: str = "") -> list:
    baseUrl = "https://lrclib.net/api/search?q="
    headers = {"Content-Type": "application/json"}
    url = baseUrl + query
    completeUrl = url.replace(" ", "+").replace(",", "+").replace("、", "+")

    response = requests.get(completeUrl, headers=headers)
    data = response.json()
    return data


def write_lrc(file: str, lyrics: str) -> None:
    fileName = f"{file}.lrc"
    try:
        os.remove(fileName)
        with open(fileName, "x") as f:
            f.write(f"{lyrics}\n")
    except Exception:
        with open(fileName, "x") as f:
            f.write(f"{lyrics}\n")


def get_audio_file() -> list:
    allFiles = os.listdir(os.getcwd())
    audioFiles = []
    try:
        for file in range(0, len(allFiles)):
            if allFiles[file].endswith((".opus", ".mp3", ".wav")):
                audioFiles.append(
                    allFiles[file].rstrip(".opus").rstrip(".mp3").rstrip(".wav")
                )
    except Exception:
        print("Error: No audio files")
    return audioFiles


def testing(data):
    new_query = f"{data[0].get('artistName')} {data[0].get('name')}"
    resend_query = new_query.replace(" ", "+").replace(",", "+").replace("、", "+")
    with open("output.json", "wx") as f:
        f.write(str(data[0]))


def get_lyrics(query="") -> str:
    try:
        data = api_request(query)
        if len(data) == 0:
            print(f"No results for: {query}")
            return ""
        else:
            newData = []
            for n in range(0, 4):
                if not data[n].get("syncedLyrics"):
                    n -= 1
                    continue
                newData.append(data[n])
                results = f"""\nResult no.{n}
                \nName: {data[n].get("name")}
                \nArtist(s): {data[n].get("artistName")}
                \n{data[n].get("syncedLyrics")}\n """
                print(results)
            try:
                selection = abs(int(input("Select result: ")) - 1)
                print(newData[selection].get("syncedLyrics"))
                write_lrc(query, newData[selection].get("syncedLyrics"))
                return newData[selection].get("syncedLyrics")
            except Exception as e:
                print(e)
                return "No valid lyrics"
    except Exception as e:
        print(f"Error: {e}")
        return ""


try:
    if sys.argv[1].endswith(("opus", "mp3", "wav")):
        get_lyrics(sys.argv[1].rstrip(".opus").rstrip(".mp3").rstrip(".wav"))
    elif sys.argv[1] == "scan":
        files = get_audio_file()
        for n in files:
            get_lyrics(n)
    elif sys.argv[1] is IndexError:
        query = input("search: ")
        get_lyrics(query)
    else:
        get_lyrics(sys.argv[1])
except IndexError:
    query = input("search: ")
    get_lyrics(query)
except KeyboardInterrupt or RuntimeError:
    print("\nProgram interupted")
except Exception as e:
    print(e)

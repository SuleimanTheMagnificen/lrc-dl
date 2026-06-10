import requests
import os


class Client:
    """lrc downloader client powered by lrclib"""

    def __init__(self) -> None:
        pass

    """FUnction handling api requests to the lrclib API"""

    def api_request(self, query: str = "") -> list:
        baseUrl = "https://lrclib.net/api/search?q="
        headers = {"Content-Type": "application/json"}
        url = baseUrl + query
        completeUrl = url.replace(" ", "+").replace(",", "+").replace("、", "+")

        response = requests.get(completeUrl, headers=headers)
        data = response.json()
        return data

    """Scans the current directory for the audio files to be processed"""

    def get_audio_file(self, path: str = ".") -> list:
        allFiles = os.listdir(path)
        audioFiles = []
        try:
            for file in range(0, len(allFiles)):
                if allFiles[file].endswith((".opus", ".mp3", ".wav")):
                    audioFiles.append(
                        allFiles[file].rstrip(".opus").rstrip(".mp3").rstrip(".wav")
                    )
            if len(audioFiles) == 0:
                print("Error: No audio files")
        except Exception:
            print("Error: No audio files")
        return audioFiles

    """Returns string object of lyrics from data JSON"""

    def get_lyrics(self, query="") -> str:
        try:
            data = self.api_request(query)
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
                    self.write_lrc(query, newData[selection].get("syncedLyrics"))
                    return newData[selection].get("syncedLyrics")
                except Exception as e:
                    print(e)
                    return "No valid lyrics"
        except Exception as e:
            print(f"Error: {e}")
            return ""

    def write_lrc(self, file: str, lyrics: str) -> None:
        fileName = f"{file}.lrc"
        try:
            os.remove(fileName)
            with open(fileName, "x") as f:
                f.write(f"{lyrics}\n")
        except Exception:
            with open(fileName, "x") as f:
                f.write(f"{lyrics}\n")

    def __repr__(self) -> str:
        return "lrc downloader client powered by lrclib"

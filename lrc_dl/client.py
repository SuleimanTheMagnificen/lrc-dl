import requests
import os
from utils import Utils


class Client:
    """lrc downloader client powered by lrclib"""

    eligible_flags = ["--c. --current, -m, --manual", "--no-download"]
    extensions = (".opus", ".mp3", ".wav")
    utils = Utils()

    def __init__(self) -> None:
        pass

    """FUnction handling api requests to the lrclib API"""

    def api_request(self, queries: dict = {}) -> list[dict]:
        baseUrl = "https://lrclib.net/api/"
        headers = {"Content-Type": "application/json"}
        url = f"{baseUrl}search?"
        for key, value in queries.items():
            if not value:
                continue
            url += f"{key}={value}&"
        completeUrl = (
            url.replace(" ", "&20")
            .replace(",", "+")
            .replace("、", "+")
            .replace("`", "%60")
            .rstrip("&")
        )

        response = requests.get(completeUrl, headers=headers)
        data = response.json()
        return data

    """Searches for the audio file name"""

    def get_audio_file(self, path: str = ".") -> list:
        allFiles = os.listdir(path)
        audioFiles = []
        try:
            for file in range(0, len(allFiles)):
                if allFiles[file].endswith(self.extensions):
                    fileName: str = self.utils.remove_ext(allFiles[file])["fileName"]
                    print(f"Found {fileName} in {path}")
                    audioFiles.append(fileName)
            if len(audioFiles) == 0:
                print("No audio files")
        except Exception as e:
            print(f"Error: {e} during audio retrieval")
        return audioFiles

    """Scans the current directory for audio files"""

    def scan_folder(self, path: str = ".", flags: list = []) -> None:
        allFiles: list[str] = os.listdir(path)
        audioFiles: list[str] = []
        folders: list[str] = []
        try:
            """Loops through files and folders"""
            for file in range(0, len(allFiles)):
                if allFiles[file].endswith(self.extensions):
                    audioFiles.append(allFiles[file])
                    fileName: str = self.utils.remove_ext(allFiles[file])["fileName"]
                    print(f"Found {fileName} in {path}")
                    metadata = self.utils.get_song_data(f"{path}/{allFiles[file]}")
                    print(metadata)
                    if "--no-download" not in flags:
                        self.get_lyrics(queries=metadata, path=path, flags=flags)
                elif os.path.isdir(allFiles[file]):
                    folders.append(allFiles[file])
            """Check current flags"""
            """Recursively checks each folder in current directory"""
            if ("-c" or "--current") not in flags:
                for folder in folders:
                    self.scan_folder(folder, flags=flags)
            else:
                self.get_audio_file(path=path)
                return
            if len(audioFiles) == 0:
                print(f"No audio files in {path}")
                return
        except Exception as e:
            print(f"Error: {e} during folder scan")

    """Returns string object of lyrics from data JSON"""

    def get_lyrics(
        self,
        queries: dict = {"q": "No track name inserted"},
        path: str = "",
        flags: list = [],
    ) -> str:
        if "track_name" not in queries:
            queries["track_name"] = queries["q"]
        else:
            queries["q"] = queries["track_name"]
        try:
            data: list[dict] = self.api_request(queries)
            newData = []
            entry = {}
            if len(data) == 0:
                print(f"No results for: {queries['track_name']}")
                return f"No results for: {queries['track_name']}"

            try:
                num = 0
                for n in range(0, 4):
                    num += 1
                    if not data[n].get("syncedLyrics"):
                        num -= 1
                        continue
                    newData.append(data[n])
                    results = f"""\nResult no.{num}
                    \nName: {data[n].get("name")}
                    \nArtist(s): {data[n].get("artistName")}
                    \n{data[n].get("syncedLyrics")}\n """
                    if ("-m" or "--manual") in flags:
                        print(results)
                        selection = abs(int(input("Select result: ")) - 1)
                        entry = newData[selection]
                        print(entry["syncedLyrics"])
                    else:
                        """Default behavior: take first result"""
                        entry = newData[0]
                if ("--no-download") not in flags:
                    self.utils.write_lrc(
                        songName=queries["track_name"],
                        path=path,
                        lyrics=entry["syncedLyrics"],
                    )
                return str(entry["syncedLyrics"])
            except Exception as e:
                print(f"Error: {e}, lyrics for {queries['track_name']} not retrieved")
                return ""

        except Exception as e:
            print(f"Error: {e} during lyrics retrieval")
            return ""

    def __repr__(self) -> str:
        return "lrc downloader client powered by lrclib"

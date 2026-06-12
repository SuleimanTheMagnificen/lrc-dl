import requests
import os


class Client:
    """lrc downloader client powered by lrclib"""

    eligible_flags = ["--c. --current, -m, --manual", "--no-download"]
    extensions = (".opus", ".mp3", ".wav")

    def __init__(self) -> None:
        pass

    """FUnction handling api requests to the lrclib API"""

    def api_request(self, query: str = "") -> list[dict]:
        baseUrl = "https://lrclib.net/api/search?q="
        headers = {"Content-Type": "application/json"}
        url = baseUrl + query
        completeUrl = url.replace(" ", "+").replace(",", "+").replace("、", "+")

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
                    fileName: str = self.remove_ext(allFiles[file])["fileName"]
                    print(f"Found {fileName} in {path}")
                    audioFiles.append(fileName)
            if len(audioFiles) == 0:
                print("No audio files")
        except Exception as e:
            print(f"Error: {e}")
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
                    fileName: str = self.remove_ext(allFiles[file])["fileName"]
                    print(f"Found {fileName} in {path}")
                    audioFiles.append(fileName)
                    if "--no-download" not in flags:
                        lyrics = self.get_lyrics(fileName, flags)
                        self.write_lrc(fileName, path, lyrics)
                elif os.path.isdir(allFiles[file]):
                    folders.append(allFiles[file])
            """Check current flags"""
            """Recursively checks each folder in current directory"""
            if ("-c" or "--current") not in flags:
                for folder in folders:
                    self.scan_folder(folder, flags=flags)
            else:
                self.get_audio_file(path=".")
                return
            if len(audioFiles) == 0:
                print(f"No audio files in {path}")
                return
        except Exception as e:
            print(f"Error: {e}")

    """Returns string object of lyrics from data JSON"""

    def get_lyrics(self, query="", flags: list = []) -> str:
        try:
            data: list[dict] = self.api_request(query)
            if len(data) == 0:
                print(f"No results for: {query}")
                return f"No results for: {query}"
            else:
                if ("-m" or "--manual") in flags:
                    try:
                        newData = []
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
                            print(results)
                        selection = abs(int(input("Select result: ")) - 1)
                        print(newData[selection].get("syncedLyrics"))
                        return str(newData[selection].get("syncedLyrics"))
                    except Exception as e:
                        print(e)
                        return "No valid lyrics"
                else:
                    print("test")
                    return data[0]["syncedLyrics"]
        except Exception as e:
            print(f"Error: {e}")
            return ""

    """Removes music file extensions"""

    def remove_ext(self, file: str) -> dict:
        name, ext = os.path.splitext(file)
        result: dict[str, str] = {"fileName": name, "fileExtension": ext}
        return result

    """Writes lyrics to an lrc file"""

    def write_lrc(self, songName: str, path: str = ".", lyrics: str = "") -> None:
        fileName = f"{songName}.lrc"
        try:
            filePath: str = f"{path}/{fileName}"
            print(filePath)
            # os.remove(filePath)
            with open(filePath, "x") as f:
                f.write(f"{lyrics}\n")
        except Exception as e:
            print(f"Error: {e}")

    """"Checks vaidity of flags"""

    def flag_check(self, flags: list = []):
        check = True
        for flag in flags:
            if flag not in self.eligible_flags:
                print(f"Error: non-valid flag '{flag}'")
                check = False
                return check
        return check

    def __repr__(self) -> str:
        return "lrc downloader client powered by lrclib"

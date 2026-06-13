import os
import ffmpeg


class Utils:
    """Utillity functions to simplify client code"""

    def __init__(self):
        pass

    """"Checks vaidity of flags"""

    def flag_check(self, eligible_flags: list = [], flags: list = []):
        check = True
        for flag in flags:
            if flag not in eligible_flags:
                print(f"Error: non-valid flag '{flag}'")
                check = False
                return check
        return check

    """Uses ffmpeg to extract metadata from audio files for better search"""

    def get_song_data(self, file: str = "", flags={}) -> dict:
        """Overrides metadata with user input"""
        """NOTE: To maintain functionality, key names must be as maintained follows"""
        metadata: dict[str, str] = {
            "track_name": "",
            "artist_name": "",
            "album_name": "",
        }
        print(file)
        try:
            if ("-m" or "--manual") in flags or not file:
                """Entry to mark user input"""
                metadata["track_name"] = input("title: ")
                metadata["artist_name"] = input("artist: ")
                metadata["album_name"] = input("album: ")
                return metadata
            media: dict = ffmpeg.probe(file)["streams"][0]
            metadata["track_name"] = media["tags"]["title"]
            metadata["artist_name"] = media["tags"]["artist"]
            metadata["album_name"] = media["tags"]["album"]
            return metadata
        except Exception as e:
            print(f"Error: {e}")
            return {}

    """Removes music file extensions"""

    def remove_ext(self, file: str) -> dict:
        name, ext = os.path.splitext(file)
        result: dict[str, str] = {"fileName": name, "fileExtension": ext}
        return result

    """Writes lyrics to an lrc file"""

    def write_lrc(
        self, songName: str = "output", path: str = ".", lyrics: str = ""
    ) -> None:
        fileName = f"{songName}.lrc"
        try:
            filePath: str = f"{path}/{fileName}"
            with open(filePath, "x") as f:
                f.write(f"{lyrics}\n")
        except Exception as e:
            print(f"Error: {e}")

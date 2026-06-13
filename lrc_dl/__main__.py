import sys
from client import Client
from utils import Utils


def main():
    client = Client()
    utils = Utils()
    args = sys.argv[1:]
    if len(args) != 0:
        if args[0].endswith(("opus", "mp3", "wav")):
            client.get_lyrics(
                {"q": sys.argv[1].rstrip(".opus").rstrip(".mp3").rstrip(".wav")},
                flags=args[1:],
            )
        elif args[0] == "scan":
            if not Utils.flag_check(client.eligible_flags, args[1:]):
                return
            client.scan_folder(flags=args[1:])
        elif args[0].startswith("-"):
            if not utils.flag_check(client.eligible_flags, args[0:]):
                return
            print(
                "Search for music lyrics by track, artist, and album/nPress enter if you don't want to insert any"
            )
            data = utils.get_song_data("", flags=["-m"])
            client.get_lyrics(data, flags=args[0:])
        else:
            lyrics = client.get_lyrics({"q": args[0]}, flags=args[1:])
            utils.write_lrc(lyrics, flags=args[1:])
    else:
        print(
            "Search for music lyrics by track, artist, and album/nPress enter if you don't want to insert any"
        )
        data = Utils.get_song_data("", flags=["-m"])
        client.get_lyrics(data, flags=["-m"])


if __name__ == "__main__":
    main()

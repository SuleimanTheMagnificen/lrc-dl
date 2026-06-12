import sys
from client import Client


def main():
    client = Client()
    args = sys.argv[1:]
    if len(args) != 0:
        if args[0].endswith(("opus", "mp3", "wav")):
            client.get_lyrics(sys.argv[1].rstrip(".opus").rstrip(".mp3").rstrip(".wav"))
        elif args[0] == "scan":
            if not client.flag_check(args[1:]):
                return
            client.scan_folder(flags=args[1:])
        elif args[0].startswith("-"):
            if not client.flag_check(args[0:]):
                return
            query: str = input("Search: ")
            client.get_lyrics(query, flags=args[0:])
        else:
            client.get_lyrics(args[0], flags=args[1:])
    else:
        query: str = input("Search: ")
        client.get_lyrics(query, flags=["-m"])


if __name__ == "__main__":
    main()

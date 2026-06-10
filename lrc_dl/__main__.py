import sys
from client import Client


def main():
    client = Client()
    args = sys.argv[1:]
    if len(args) != 0:
        if args[0].endswith(("opus", "mp3", "wav")):
            client.get_lyrics(sys.argv[1].rstrip(".opus").rstrip(".mp3").rstrip(".wav"))
        elif args[0] == "scan":
            files: list = client.get_audio_file()
            for n in files:
                client.get_lyrics(n)
        else:
            client.get_lyrics(args[0])
    else:
        query: str = input("Search: ")
        client.get_lyrics(query)


if __name__ == "__main__":
    main()

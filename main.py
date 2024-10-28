import os
import re

from yt_dlp import YoutubeDL
from pydub import AudioSegment

# TODO: это для windows, реализовать также для unix
os.environ["PATH"] += ';' + os.path.realpath('./ffengine')


def audio_download(url_address: str) -> tuple[int, str, dict, str]:
    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        'outtmpl': 'audio_source',
        # 'ffmpeg_location': os.path.realpath('./ffengine/ffmpeg.exe'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            # 'preferredquality': '192'
        }]
    }

    with YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([url_address])

        info = ydl.extract_info(url_address, download=False)
        title: str = info.get("title", None)
        time_line: dict = info.get("chapters", None)

    print(f"{'-' * 50}\nAudio Downloaded Successfully!!!\n{'-' * 50}")
    return error_code, title, time_line, "audio_source.mp3"


def audio_redactor(file_path: str, title_name: str, time_line: dict | None):
    title_name = ''.join(re.split(r'[.,:;!?@#$%^&`~|*/=+-]', title_name))
    title_name = ' '.join(title_name.split())

    # TODO: проверка на существование папки
    os.mkdir(title_name)

    # AudioSegment.converter = os.path.realpath('./ffengine/ffmpeg.exe')
    # AudioSegment.ffprobe = os.path.realpath('./ffengine/ffprobe.exe')

    if time_line:
        count_compositions = len(time_line)
        curr_composition = 0

        for composition in time_line:
            curr_composition += 1
            print(f"{'-' * 50}\nCreate audio #{composition["title"]}\n"
                  f"Please Wait...\nPROGRESS {curr_composition}/{count_compositions}\n{'-' * 50}")

            try:
                start_time = int(composition["start_time"]) * 1000
                end_time = int(composition["end_time"]) * 1000

                composition_title = ''.join(re.split(r'[\\`~|/]', composition["title"]))
                composition_title = ' '.join(composition_title.split())
                composition_file = str(curr_composition) + '. ' + composition_title + '.mp3'

                # TODO: получается, что в цикле она каждый раз инициализируется?
                audio_file = AudioSegment.from_mp3(os.path.join(os.getcwd(), file_path))
                song = audio_file[start_time:end_time]

                song_file_path = os.path.join(os.getcwd(), title_name, composition_file)
                song.export(song_file_path, format='mp3')

                print(f"{'-' * 50}\n#{composition["title"]} Created!\n{'-' * 50}")
            except Exception as e:
                print(f"{'-' * 50}\nAn error occurred while creating the {composition["title"]}:\n{e}\n{'-' * 50}")

    else:
        # TODO: разработать логику когда тайм-лайны отсутствуют
        pass

    os.remove("audio_source.mp3")


def main():
    url_address_for_video: str = input("Введите ссылку для скачивания: ")
    print()

    error, album_title, audio_time_line, source_file = audio_download(url_address_for_video)

    if not error:
        audio_redactor(source_file, album_title, audio_time_line)


if __name__ == "__main__":
    main()

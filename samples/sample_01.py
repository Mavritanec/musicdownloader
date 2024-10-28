import os

print()
print(os.getcwd())
print(os.path.join(os.getcwd(), './ffengine/ffmpeg.exe'))
print(os.path.realpath('../ffengine/ffmpeg.exe'))
print(type(os.path.realpath('../ffengine/ffmpeg.exe')))

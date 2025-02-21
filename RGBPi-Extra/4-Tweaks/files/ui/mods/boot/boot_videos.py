import os
import subprocess

def gen_video():
    playlist_file = '/tmp/boot_video_playlist.m3u'
    video_directory = os.path.join(os.path.dirname(__file__), 'videos')
    video_files = []

    for root, dirs, files in os.walk(video_directory):
        for file in files:
            video_files.append(os.path.join(root, file))

    if video_files:
        with open(playlist_file, 'w') as playlist:
            for video_file in video_files:
                playlist.write(f"{video_file}\n")

    return playlist_file

def play_videos():
    playlist_file = gen_video()
    if os.path.exists(playlist_file):
        cvlc_command = [
            'cvlc',
            '--fullscreen',
            '--play-and-exit',
            '--no-osd',
            '--quiet',
            '--aout=alsa',
            playlist_file
        ]
        with open(os.devnull, 'w') as devnull:
            subprocess.run(cvlc_command, stdout=devnull, stderr=devnull)

if __name__ == "__main__":
    play_videos()

from backend.domain.photo.entity import Photo
from backend.domain.video.port import IVideoCreator, Video
import subprocess

# ffmpeg -framerate 4 -pattern_type glob -i '691302564/*.png' \
#  -stream_loop -1 -i logo.apng -filter_complex "[1:v]scale=100:100[tmp];[0:v][tmp]overlay=shortest=1:x=20:y=10 [vid]" \
#  -stream_loop -1 -i ./happy-202230.mp3 -filter:a "volume=0.3" \
#  -shortest -map [vid] -map 2:a -c:v libx264 -pix_fmt yuv420p \
#  -f mp4 -movflags frag_keyframe+empty_moov pipe:1 >out3.mp4


class FfmpegVideoCreator(IVideoCreator):
    def create_video(self, photos: list[Photo], fps: int = 4) -> Video:
        input = bytearray()
        for p in photos:
            input += p
        command = [
            "ffmpeg",
            "-framerate",
            str(fps),
            "-f",
            "image2pipe",
            "-i",
            "pipe:0",
            "-stream_loop",
            "-1",
            "-i",
            "./resources/logo.apng",
            "-filter_complex",
            "[1:v]scale=100:100[tmp];[0:v][tmp]overlay=shortest=1:x=20:y=10 [vid]",
            "-stream_loop",
            "-1",
            "-i",
            "./resources/happy-202230.mp3",
            "-filter:a",
            "volume=0.3",
            "-shortest",
            "-map",
            "[vid]",
            "-map",
            "2:a",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-f",
            "mp4",
            "-movflags",
            "frag_keyframe+empty_moov",
            "pipe:1",
        ]
        process = subprocess.run(command, input=input, capture_output=True)
        assert process.returncode == 0
        return process.stdout

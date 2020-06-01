"""Main module."""

import datetime
from pytimeparse.timeparse import timeparse

from moviepy.editor import concatenate_videoclips, TextClip, CompositeVideoClip

from tqdm import tqdm

from .video_sources import auto_video_source


def get_duration(string):
    """Convert time string to proper object."""
    secs = timeparse(string)
    return datetime.timedelta(seconds=secs)


def parse_input(fname):
    """Parse in put file."""
    with open(fname) as fd:
        for line in fd.readlines():
            if line.lstrip().startswith('#'):
                continue

            url, start, end = line.split()
            yield auto_video_source(url), get_duration(start), get_duration(end)


def assemble_clip(video):
    """Modify single clip."""
    clip = video.clip

    # overlay video information
    # TODO: set maximal length
    # max_len = 50
    txt = f'{video.title}\n({video.author})'#[:max_len].ljust(max_len)

    txt_clip = (TextClip(
        txt,
        fontsize=72, font='Impact-Normal',
        color='white', stroke_color='black', stroke_width=3,
        align='West'
    ).set_position((0, 0))
     .set_duration(clip.duration)
     .resize(width=clip.w))

    final_clip = CompositeVideoClip([clip, txt_clip])

    # fix audio bugs
    # final_clip.audio_fadein(0.01).audio_fadeout(0.01)

    return final_clip


def merge_videos(video_list, output_file):
    """Merge multiple clips into single one."""
    clip_list = [assemble_clip(v) for v in video_list]
    final_clip = concatenate_videoclips(clip_list)
    final_clip.write_videofile(
        str(output_file),
        temp_audiofile='fubar.m4a', audio_codec='aac')


def handle(input_file, output_file, temp_dir):
    """Aggregate functionality."""
    input_ = list(parse_input(input_file))
    temp_dir.mkdir(parents=True, exist_ok=True)

    video_list = []
    for i, (vid, start, end) in enumerate(tqdm(
        input_, desc='Processing clips'
    )):
        vid.load()

        fname = temp_dir / f'out_{i:03}_{vid.id_}.mp4'
        vid.save_snippet(fname, start, end)

        video_list.append(vid)

    merge_videos(video_list, output_file)

"""Define all sources which can provide videos."""

import os
from urllib.parse import urlparse
from abc import ABC, abstractmethod

import sh
from pytube import YouTube

from moviepy.editor import VideoFileClip

from tqdm import tqdm


class Video(ABC):
    """Abstract base class."""

    def __init__(self, url):
        self.url = url

        self.fname = None

    @abstractmethod
    def load(self):
        ...

    @abstractmethod
    def save_snippet(self, fname, start, end):
        ...

    @property
    @abstractmethod
    def id_(self):
        ...

    @property
    @abstractmethod
    def title(self):
        ...

    @property
    @abstractmethod
    def author(self):
        ...

    @property
    @abstractmethod
    def stream_url(self):
        ...

    @property
    def clip(self):
        assert self.fname is not None
        return VideoFileClip(str(self.fname))

    def save_snippet(self, fname, start, end):
        if os.path.exists(fname):
            tqdm.write(f'Cached "{fname}"')
        else:
            dur = end - start

            # extract relevant section from video (without download whole video)
            cmd = sh.ffmpeg.bake(
                '-y',
                '-ss', start,
                '-i', self.stream_url,
                '-t', dur,
                # '-to', dur,
                '-c', 'copy',
                fname)

            # tqdm.write(str(cmd))
            cmd()

            # cut to correct duration because previous ffmpeg command
            # creates a video with still frames at the end
            # TODO: figure out why this is happening
            sh.ffmpeg(
                '-y',
                '-i', fname,
                '-t', dur,
                'tmp.mp4'
            )
            sh.mv('tmp.mp4', fname)

        self.fname = fname


class LocalVideo(Video):
    """Handle videos from local filesystem."""
    def load(self):
        pass

    @property
    def id_(self):
        return self.url.replace('/', '_')

    @property
    def title(self):
        return os.path.basename(self.url)

    @property
    def author(self):
        return 'local'

    @property
    def stream_url(self):
        return self.url


class YoutubeVideo(Video):
    """Handle videos from YouTube."""

    def load(self):
        self.yt = YouTube(self.url)

    @property
    def id_(self):
        return self.yt.video_id

    @property
    def title(self):
        return self.yt.title

    @property
    def author(self):
        return self.yt.author

    @property
    def stream_url(self):
        # high quality
        stream = self.yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        # low quality
        # stream = self.yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().last()

        return stream.url


def auto_video_source(url):
    """Automatically detect correct video source for given url."""
    if os.path.exists(url):
        return LocalVideo(url)

    o = urlparse(url)
    if o.netloc == 'www.youtube.com':
        return YoutubeVideo(url)

    raise RuntimeError(f'No source wrapper found for "{url}"')

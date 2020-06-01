# clypper

[![image](https://img.shields.io/pypi/v/clypper.svg)](https://pypi.python.org/pypi/clypper)

Rapidly create supercuts from various video sources.


## Installation

```python
pip install clypper
```


## Usage

A text file specifying the video source url as well as start and end timestamps can be converted to a supercut using a single command:

```bash
$ cat input.txt
https://www.youtube.com/watch?v=dQw4w9WgXcQ 0:43 0:44
https://www.youtube.com/watch?v=o0u4M6vppCI 1:55 1:59
$ clypper -i input.txt -o supercut.mp4
[..]
$ file supercut.mp4
supercut.mp4: ISO Media, MP4 Base Media v1 [IS0 14496-12:2003]
```


## Developer notes

### Making a new release

```bash
$ bump2version patch # minor major
$ poetry publish --build
```

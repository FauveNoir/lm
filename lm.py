#!/usr/bin/env python
# -*- coding: utf-8 -*-
# frdepartment : mainfile
#!/usr/bin/python

import os, sys, subprocess, shlex, re
from   subprocess import call
from   tabulate   import tabulate
from   optparse   import OptionParser
import argparse
import magic
import os.path

def extractTag(track,tag):
    if tag == 'genre':
        charToSortBy='tag:genre='
    if tag == 'author':
        charToSortBy='tag:artist='
    if tag == 'album':
        charToSortBy='tag:album='
    if tag == 'title':
        charToSortBy='tag:title='
    if tag == 'number':
        charToSortBy='tag:track='

    cleeningTag= re.compile(re.escape(charToSortBy), re.IGNORECASE)

    extractTagCmd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', track]
    fullTagOutput = subprocess.Popen(extractTagCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    (stdout, stderr) = fullTagOutput.communicate()

    for line in stdout.split('\n'):
        if charToSortBy in line.lower():
            return cleeningTag.sub('', line)


def getAuthorName(track):
    return extractTag(track,"author")

def getAlbumName(track):
    return extractTag(track,"album")

def getTrackName(track):
    return extractTag(track,"title")

def getTrackNumber(track):
    return extractTag(track,"number")

def getGenre(track):
    return extractTag(track,"genre")

analysedFiles=sys.argv
#del analysedFiles[0]

allTracks=[]

audioMimetype=[
"audio/x-flac", "audio/ogg", "audio/mpeg", "audio/MPA", "audio/mpa-robust", "audio/mp3", "audio/aac", "audio/aacp", "audio/x-aac", "audio/x-m4a", "audio/x-m4p", "audio/x-m4b", "audio/mp4", "audio/mp4a", "audio/mp4a-latm", "audio/mpga", "audio/mpeg4-generic", "audio/3gpp", "audio/3gpp2", "audio/mp4", "audio/x-mpegurl", "audio/vorbis"
]

for track in analysedFiles:
    if os.path.isfile(track):
        if magic.from_file(track, mime=True) in audioMimetype:
            allTracks.append([getTrackName(track), getTrackNumber(track), getAuthorName(track), getAlbumName(track), getGenre(track)])

usage = "usage: %prog [ [--author] [--genre] [--album] [--track] ]… [--header] <file>…"
parser = OptionParser(usage=usage, version="lm 0.1")


parser.add_option("-a", "--author", help="Sort by author",          default=False, action="store_true", dest="author")
parser.add_option("--genre",  help="Sort by genre",           default=False, action="store_true", dest="genre")
parser.add_option("--album",  help="Sort by album",           default=False, action="store_true", dest="album")
parser.add_option("--track",  help="Sort by number of track", default=False, action="store_true", dest="track")
parser.add_option("--header", help="Display a header information on the top of lit", default=False, action="store_true", dest="header")

(options, args) = parser.parse_args()


if options.track:
    allTracks.sort(key=lambda x: x[1])
if options.author:
    allTracks.sort(key=lambda x: x[2])
if options.album:
    allTracks.sort(key=lambda x: x[3])
if options.genre:
    allTracks.sort(key=lambda x: x[4])

if options.header:
    print tabulate(allTracks, headers=["Title", "Track", "Author", "Album", "Genre"])
else:
    print tabulate(allTracks, tablefmt="plain")

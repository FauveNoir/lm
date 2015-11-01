#!/usr/bin/env python
# -*- coding: utf-8 -*-
# frdepartment : mainfile
#!/usr/bin/python

import os, sys, subprocess, shlex, re
from subprocess import call

def extractTag(track,tag):
    if tag == "genre":
        charToSortBy="TAG:GENRE="
    if tag == "author":
        charToSortBy="TAG:ARTIST="
    if tag == "album":
        charToSortBy="TAG:ALBUM="
    if tag == "number":
        charToSortBy="TAG:track="

    cmd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', track]
    fullTagOutput = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    fullTagOutput = fullTagOutput

    for line in fullTagOutput:
        if charToSortBy in line:
            return line.replace(charToSortBy, "")


def getAuthorName(track):
    return extractTag(track,"author")

def getAlbumName(track):
    return extractTag(track,"album")

def getTrackName(track):
    return extractTag(track,"author")

def getTrackNumber(track):
    return extractTag(track,"number")

def getGenre(track):
    return extractTag(track,"genre")

analysedFiles=sys.argv

allTracks=[]

for track in sys.argv:
    allTracks.append([getTrackName(track), getTrackNumber(track), getAuthorName(track), getAlbumName(track), getGenre(track)])

#print allTracks

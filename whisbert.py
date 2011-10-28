#!/usr/bin/env python

import time
import glob
import whisper
import eventlet
import os
from ernie import mod, start
from calendar import timegm
from string import join

def create(path, retentions,  overwrite=False, xFilesFactor=0.5, aggregationMethod='average'):
    archives = [whisper.parseRetentionDef(str(timePerPoint)+":"+str(timeToStore))
            for (timePerPoint, timeToStore) in retentions]
    if len(retentions) == 0:
        raise Exception("No Retention given")

    if overwrite and os.path.exists(path):
        print 'Overwriting existing file: %s' % path
        os.unlink(path)

    p = path.split("/")[:-1]
    p = join(p, os.path.sep)
    if not os.path.exists(p):
        os.makedirs(p)

    whisper.create(path + '.wsp', archives, xFilesFactor, aggregationMethod)
    return True

def update(path, datapoints):
    nrOfPoints = len(datapoints),
    if nrOfPoints == 1:
        (timestamp, value) = datapoints[0]
        timestamp = timegm(timestamp.timetuple())
        whisper.update(path, value, timestamp)
    elif nrOfPoints > 1:
        whisper.update_many(path + '.wsp', [
            (timegm(t.timetuple()), v) for (t,v) in datapoints])
    else:
        raise Exception("No Datapoint given")

    return True

def single_fetch(whisperFile, fromTime, untilTime):
    return whisper.fetch(whisperFile, fromTime, untilTime)

pile = eventlet.GreenPile()
def fetch(path, fromTime, untilTime=None):
    fromTime = timegm(fromTime.timetuple())

    if untilTime != None:
        untilTime =  timegm(untilTime.timetuple())

    arrayOfValues = []
    arrayOfTimeInfos = []
    files = glob.glob(path + ".wsp")
    for i in range(len(files)):
        pile.spawn(single_fetch, files[i], fromTime, untilTime)

    for (timeInfo, values) in pile:
        arrayOfValues.append(values)
        arrayOfTimeInfos.append(timeInfo)

    if arrayOfTimeInfos.count(arrayOfTimeInfos[0]) == len(arrayOfTimeInfos):
        values = [sum(v) for v in zip(*arrayOfValues)]
        (start, end, step) = arrayOfTimeInfos[0]
        return (start, end, step, values)
    else:
        return False

mod('whisbert').fun('create', create)
mod('whisbert').fun('update', update)
mod('whisbert').fun('fetch', fetch)

if __name__ == "__main__":
    start()

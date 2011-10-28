import unittest
import whisbert
import os
import shutil
import datetime
import time

timestamp = int(time.time())
data = []
nrOfMetrics = 10
tmp_path = "/tmp/wsp"
metric1 = tmp_path + "/a/b/c/1"
metric2 = tmp_path + "/a/b/d/1"

class TestWhisper(unittest.TestCase):

    def setUp(self):
        self.assertTrue(whisbert.create(metric1, [(1, nrOfMetrics)]))
        self.assertTrue(whisbert.create(metric2, [(1, nrOfMetrics)]))

        for i in range(nrOfMetrics):
            data.append((datetime.datetime.fromtimestamp(timestamp -1), i))

    def tearDown(self):
        shutil.rmtree(tmp_path)

    def testSingleUpdate(self):
        for d in data:
            whisbert.update(metric1, [d])
            whisbert.update(metric2, [d])

    def testMultiUpdate(self):
        whisbert.update(metric1, data)
        whisbert.update(metric2, data)

    def testFetch(self):
        mystart = timestamp - nrOfMetrics
        (_, _, _, values) = whisbert.fetch(metric1,
                datetime.datetime.fromtimestamp(mystart),
                datetime.datetime.fromtimestamp(timestamp))
        for i in range(len(values)):
            self.assertEquals(values[i], i)

    def testQueryFetch(self):
        mystart = timestamp - nrOfMetrics
        (_, _, _, values) = whisbert.fetch(tmp_path + "/a/*/*/1",
                datetime.datetime.fromtimestamp(mystart),
                datetime.datetime.fromtimestamp(timestamp))
        for i in range(len(values)):
            self.assertEquals(values[i], i+i) # we got the summed results of the two metrices

if __name__ == '__main__':
    unittest.main()


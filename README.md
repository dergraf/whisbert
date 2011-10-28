Whisbert - A [BERT-RPC](http://bert-rpc.org/) Interface for Round Robin DB [Whisper](http://graphite.wikidot.com/whisper)
==========================================================
Whisbert uses the [Ernie BERT-RPC Server](https://github.com/mojombo/ernie) together with the [python-ernie](http://github.com/tylerneylon/python-ernie) connector.

Installation
------------
In order to use Whisbert you need to install <code>Ernie</code> first. Have a look at the [Ernie Project](https://github.com/mojombo/ernie) for the installation requirements and instructions. Once Ernie is installed, you are able to install Whisbert:

You can either clone this repository and installing the dependencies, eventlet, python-bert, and python-ernie by yourself, or use <code>pip</code> which will fetch and install all the dependencies.
  
<code>pip install git+git://github.com/dergraf/whisbert.git</code>

This will also install <code>example.ernie.config</code> which is needed to run Ernie:

<code>ernie -c /path/to/example.ernie.config<code>
  
Exported BERT Remote Procedure Calls (RPC)
------------------------------------------
###hisbert.create(binary(), list(tuple(int(), int())), bool(), float(), atom())
<code>whisbert.create(path, retentions, overwrite=False, xFilesFactor=0.5, aggregationMethod='average')</code>

####path:
Absolute Path to the whisper file being created. One whisper file contains all the metrics and aggregates them according to the specified retentions.

####retentions
List of retention tuples <code>(timePerPoint, timeToStore)</code>. In order to store some metric with minutely precision for 30 days, then at 15 minute precision for 10 years, we need to specify the following retention list: 
<code>[(60,43200), (900, 350400)]</code>

####overwrite=False
Specifies if we are allowed to overwrite an existing whisper file.

####xFilesFactor=0.5
Specifies the fraction of data points in a propagation interval that must have known values for a propagation to occur.

####aggregationMethod='average'
Specifies the function to use when propagating data. Takes either 'average', 'sum', 'last', 'max', or 'min'. 

###whisbert.update(binary(), list(tuple(time(), int() | float())))
<code>whisbert.update(path, datapoints)</code>

####path: same as above

####datapoints
List of datapoint tuples <code>(timestamp, value)</code>

###whisbert.fetch(binary(), time(), time()) 
<code>whisbert.fetch(query, fromTime, untilTime=Now)</code>

####query: 
Specifies the path to the whisper file. The difference to the path parameter seen above , the query may contain wildcards resulting in more than one whisper file. These files are concurrently fetched (eventlet) and the results are cumulated.

####fromTime:
Starttime for the range-query

####untilTime:
Endtime for the range-query, defaults to Now

Advanced Topics
---------------
Ernie does not support persistent connections at the moment, which can really slow down the whole system if you have many update and fetch requests for Whisbert. I provide a [fork of Ernie](http://github.com/dergraf/ernie/tree/persistent_conns) that should solve this problem. 

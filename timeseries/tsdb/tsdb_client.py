import asyncio
from .tsdb_serialization import serialize, LENGTH_FIELD_LENGTH, Deserializer
from .tsdb_ops import *
from .tsdb_error import *
import time
import numpy as np
import scipy

"""
Constructor for the TimeSeries class.

Parameters
----------
times: sequence
    Monotonically increasing sequence of times at which the values \
    were collected
values: sequence
    The ordered sequence of data points

Raises
------
TypeError
    Raises the error if the input data is not an iterable or if it \
    contains any type that is not numerical

Notes
-----
PRE: times is sorted in monotonically increasing order and has \
matching indices to values
"""


class TSDBClient(object):
    """
    The client. This could be used in a python program, web server, or REPL!
    """
    def __init__(self, port=9999, test=False):
        """
        Initializes the Client class

        Parameters
        ----------
        port: integer
            Port on which the client sent data to the server
        test: Boolean
            Flag that indicates whether the script is being run in test mode
        """

        self.port = port
        self.test = test

    def insert_ts(self, primary_key, ts):
        """
        Inserts a timeseries into the database

        Parameters
        ----------
        primary_key: string
            PK for the row being inserted
        ts: TimeSeries
            Timeseries object being inserted into the database
        """

        json_dict = typemap["insert_ts"](primary_key, ts).to_json()
        msg = serialize(json_dict)
        self._send(msg)
        # your code here, construct from the code in tsdb_ops.py

    def delete(self, primary_key):
        """
        Deletes a timeseries in the database

        Parameters
        ----------
        primary_key: string
            PK for the row being deleted
        """
        json_dict = typemap["delete_ts"](primary_key).to_json()
        msg = serialize(json_dict)
        print ('Deleting:', msg)
        self._send(msg)

    def upsert_meta(self, primary_key, metadata_dict):
        """
        Upserts data columns corresponding to the PK in the database

        Parameters
        ----------
        primary_key: string
            PK for the row being upserted
        metadata_dict: dictionary
            Key-Value pairs indicating data column and value being upserted
        """
        json_dict = typemap["upsert_meta"](primary_key, metadata_dict).to_json()
        print("C> msg", json_dict)
        msg = serialize(json_dict)
        self._send(msg)
        # your code here

    def select(self, metadata_dict={}, fields=None, additional=None):
        """
        Selects a number of rows from the database and returns it to the user

        Parameters
        ----------
        metadata_dict: dictionary
            Key-Value pairs with data column as key and the predicates applied \
            for filtering as values
        fields: list
            List of fields to be sent back to the user
        additional: dictionary
            Two key-value pairs - 1) sort_by as key with field as value (along\
            with an indicator for ascending vs descending) and limit \
            as key and an integer as value indicating number of rows in the \
            output)

        Returns
        -------
        OrderedDict, representing rows of the database. Key as primary key and \
        value being another OrderedDict with the fields requested
        """
        json_dict = typemap["select"](metadata_dict, fields, additional).to_json()
        msg = serialize(json_dict)
        return self._send(msg)
        # YOUR CODE HERE

    def augmented_select(self, proc, target, arg=None, metadata_dict={}, additional=None):
        """
        Selects a number of rows from the database and runs the specified \
        stored proc on those rows. Outputs the results of the stored proc to \
        the user

        Parameters
        ----------
        proc: string
            specifies which stored proc to run on the query results (list of \
            possible stored procs in the procs folder in the package)
        target: list
            list of target fields to which the stored proc values are bound; \
            these are not fields in the database
        arg:
            any argument that the user wants to send for the stored proc \
            calculation
        metadata_dict: dictionary
            Key-Value pairs with data column as key and the predicates applied \
            for filtering as values
        additional: dictionary
            Two key-value pairs - 1) sort_by as key with field as value (along\
            with an indicator for ascending vs descending) and limit \
            as key and an integer as value indicating number of rows in the \
            output)

        Returns
        -------
        Dictionary, representing rows of the database. Key as primary key and \
        value being another Dictionary with the fields calculated bound to the \
        target specified
        """
        print("HEEEREEE")
        json_dict = typemap["augmented_select"](proc, target, arg, metadata_dict, additional).to_json()
        msg = serialize(json_dict)
        return self._send(msg)
        # your code here

    def add_trigger(self, proc, onwhat, target, arg):
        """
        Ties a trigger to a database command

        Parameters
        ----------
        proc: string
            specifies which stored proc to run on the query results (list of \
            possible stored procs in the procs folder in the package)
        onwhat: string
            specifies which database command the trigger needs to be added to
        target: list
            list of target fields to which the stored proc values are bound; \
            these are fields that will be upserted into the database
        arg:
            any argument that the user wants to send for the stored proc \
            calculation
        """
        json_dict = typemap["add_trigger"](proc, onwhat, target, arg).to_json()
        msg = serialize(json_dict)
        self._send(msg)
        # YOUR CODE HERE

    def remove_trigger(self, proc, onwhat):
        """
        Removes existing trigger tied to a database command

        Parameters
        ----------
        proc: string
            specifies which stored proc needs to be removed from list of \
            existing triggers
        onwhat: string
            specifies which database command the trigger needs to be removed \
            from
        """
        json_dict = typemap["remove_trigger"](proc, onwhat).to_json()
        msg = serialize(json_dict)
        self._send(msg)
        # YOUR CODE HERE

    def _tsmaker(self, m, s, j):
        "returns metadata and a time series in the shape of a jittered normal"
        meta = {}
        meta['order'] = int(np.random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]))
        meta['blarg'] = int(np.random.choice([1, 2]))
        t = np.arange(0.0, 1.0, 0.01)
        v = scipy.stats.norm.pdf(t, m, s) + j*np.random.randn(100)
        return meta, ts.TimeSeries(t, v)

    def populate_db(self, numElem = 50, numVp = 5):

        # add a trigger. notice the argument. It does not do anything here but
        # could be used to save a shlep of data from client to server.
        self.add_trigger('junk', 'insert_ts', None, 'db:one:ts')
        # our stats trigger
        self.add_trigger('stats', 'insert_ts', ['mean', 'std'], None)
        # Set up 50 time series
        mus = np.random.uniform(low=0.0, high=1.0, size=50)
        sigs = np.random.uniform(low=0.05, high=0.4, size=50)
        jits = np.random.uniform(low=0.05, high=0.2, size=50)

        # dictionaries for time series and their metadata
        tsdict = {}
        metadict = {}
        for i, m, s, j in zip(range(numElem), mus, sigs, jits):
            meta, tsrs = self._tsmaker(m, s, j)
            # the primary key format is ts-1, ts-2, etc
            pk = "ts-{}".format(i)
            tsdict[pk] = tsrs
            meta['vp'] = -1  # augment metadata with a boolean asking if this is a  VP.
            metadict[pk] = meta

        # choose 5 distinct vantage point time series
        vpkeys = ["ts-{}".format(i) for i in np.random.choice(range(numElem), size=numVp, replace=False)]
        for i in range(numVp):
            # add 5 triggers to upsert distances to these vantage points
            self.add_trigger('corr', 'insert_ts', ["d_vp-{}".format(i)], tsdict[vpkeys[i]])
            # change the metadata for the vantage points to have meta['vp']=True
            metadict[vpkeys[i]]['vp'] = i
        # Having set up the triggers, now insert the time series, and upsert the metadata
        for k in tsdict:
            self.insert_ts(k, tsdict[k])
            time.sleep(1)
            self.upsert_meta(k, metadict[k])

    def find_similar(self, query, k_nearest = 1):
        all_vps = self.select({'vp':{'>=':0}}, ['vp'])[1]
        print ('allvps:', all_vps)
        res = self.augmented_select('corr', ['dist'], query, {'vp': {'>=':0}})
        # print(res)
        # # 1b: choose the lowest distance vantage point
        # # you can do this in local code
        print("REEEES", res)
        d_res = res[1]
        print("D_REEEES", res[1])
        sorted_res = []
        for k, v in d_res.items():
            sorted_res.append((v['dist'], k))

        sorted_res.sort()
        best_D, best_vp = sorted_res[0]

        get_vp_idx = all_vps[best_vp]['vp']
        # D_vp = vpkeys.index(sorted_res[0][1])
        # print (sorted_res, 'D = ', best_D, 'pk = ', best_vp, 'vp_idx = ', get_vp_idx)

        # # Step 2: find all time series within 2*d(query, nearest_vp_to_query)
        # # this is an augmented select to the same proc in correlation
        res2 = self.augmented_select('corr', ['dist'], query, {'d_vp-{}'.format(get_vp_idx): {'<=': 2*best_D}})
        # print (res2)
        # # 2b: find the smallest distance amongst this ( or k smallest)
        d_res = res2[1]
        sorted_res = []
        for k, v in d_res.items():
            sorted_res.append( (v['dist'], k) )

        sorted_res.sort()
        D = sorted_res[0][0]
        D_k = sorted_res[0][1]
        print (sorted_res, 'D = ', D, 'D_k = ', D_k)
        nearestwanted = [sorted_res[i][1] for i in range(min(k_nearest, len(sorted_res)))]
        print ('Sorted res:', sorted_res)
        return nearestwanted

    # Feel free to change this to be completely synchronous
    # from here onwards. Return the status and the payload
    async def _send_coro(self, msg, loop, test=False):
        """
        Asynchronously sends messages to the server

        Parameters
        ----------
        msg: bytes
            Data from the database serialized into bytes for transmission
        loop: asyncio event loop
            provides a handle to the asyncio framework for this method
        test: boolean
            Flag that indicates whether the script is being run in test mode

        Returns
        -------
        Tuple, with status indicating success of message transmission and \
        actual payload
        """
        if self.test:
            return TSDBStatus(0), {}
        # set up connection with server
        reader, writer = await asyncio.open_connection('localhost', self.port, loop=loop)
        # send data across
        writer.write(msg)
        # get back payload from database
        data = await reader.read()
        # process payload
        deserializer = Deserializer()
        deserializer.append(data)
        data_json = {}

        sleep_count = 0
        while not deserializer.ready():
            time.sleep(0.05)
            sleep_count += 1
            if sleep_count > 30:
                raise TimeoutError

        data_json = deserializer.deserialize()
        status = data_json["status"]
        payload = data_json["payload"]
        if payload is not None:
            payload_keys = payload.keys()
        else:
            payload_keys = payload
        writer.close()
        print('C> status: ' + str(TSDBStatus(status)))
        print('C> payload: ' + str(payload_keys))
        print('-----------')
        # print("writing")
        # your code here - remember to figure out the async part
        return TSDBStatus(status), payload

    # call `_send` with a well formed message to send.
    # once again replace this function if appropriate
    def _send(self, msg):
        """
        Calls async method to send data to server

        Parameters
        ----------
        msg: bytes
            Data from the database serialized into bytes for transmission

        Returns
        -------
        Tuple, with status indicating success of message transmission and \
        actual payload
        """
        # loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        coro = asyncio.ensure_future(self._send_coro(msg, loop))
        loop.run_until_complete(coro)
        return coro.result()

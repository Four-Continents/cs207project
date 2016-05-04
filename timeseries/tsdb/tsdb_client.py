import asyncio
from .tsdb_serialization import serialize, LENGTH_FIELD_LENGTH, Deserializer
from .tsdb_ops import *
from .tsdb_error import *
import time


class TSDBClient(object):
    """
    The client. This could be used in a python program, web server, or REPL!
    """
    def __init__(self, port=9999, test=False):
        self.port = port
        self.test = test

    def insert_ts(self, primary_key, ts):
        json_dict = typemap["insert_ts"](primary_key, ts).to_json()
        msg = serialize(json_dict)
        self._send(msg)
        # your code here, construct from the code in tsdb_ops.py

    def upsert_meta(self, primary_key, metadata_dict):
        json_dict = typemap["upsert_meta"](primary_key, metadata_dict).to_json()
        print("C> msg", json_dict)
        msg = serialize(json_dict)
        self._send(msg)
        # your code here

    def select(self, metadata_dict={}, fields=None, additional=None):
        json_dict = typemap["select"](metadata_dict, fields, additional).to_json()
        msg = serialize(json_dict)
        return self._send(msg)
        # YOUR CODE HERE

    def augmented_select(self, proc, target, arg=None, metadata_dict={}, additional=None):
        json_dict = typemap["augmented_select"](proc, target, arg, metadata_dict, additional).to_json()
        msg = serialize(json_dict)
        return self._send(msg)
        # your code here

    def add_trigger(self, proc, onwhat, target, arg):
        json_dict = typemap["add_trigger"](proc, onwhat, target, arg).to_json()
        msg = serialize(json_dict)
        self._send(msg)
        # YOUR CODE HERE

    def remove_trigger(self, proc, onwhat):
        json_dict = typemap["remove_trigger"](proc, onwhat).to_json()
        msg = serialize(json_dict)
        self._send(msg)
        # YOUR CODE HERE

    # Feel free to change this to be completely synchronous
    # from here onwards. Return the status and the payload
    async def _send_coro(self, msg, loop, test=False):
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
        if deserializer.ready():
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
        loop = asyncio.get_event_loop()
        coro = asyncio.ensure_future(self._send_coro(msg, loop))
        loop.run_until_complete(coro)
        return coro.result()

from tsdb import TSDBClient
import timeseries as ts
import numpy as np
import time
import scipy.stats
from collections import OrderedDict
import flask
from flask import Flask, url_for, request
from timeseries import TimeSeries
import json
import procs
from importlib import import_module
# from scipy.stats import norm

app = Flask(__name__)

empty_schema = {'pk': {'convert': lambda x: x, 'index': True},
                'ts': {'convert': lambda x: x, 'index': None},
                'order': {'convert': int, 'index': 1},
                'blarg': {'convert': int, 'index': 1}}

client = TSDBClient(30000)

@app.route('/')
def index():
    pass

@app.route('/select')
def select():
    md = request.args.get('md', '')
    fields = request.args.get('fields', '')
    additional = request.args.get('additional', '')

    split_md = md.split(',')
    md = dict(zip(split_md[::2], split_md[1::2])) if md else None


    fields = fields.split(',') if fields else None

    split_additional = additional.split(',')
    additional = dict(zip(split_additional[::2], split_additional[1::2])) or None

    _, results =  client.select(md, fields=fields, additional=additional)

    return '<pre>'+ json.dumps(results, indent=4, separators=(',', ': '))+'</pre>'



@app.route('/insert', methods=['POST'])
def insert():
    #Allows you to instert a time series in json format
    re = request.json
    data = json.loads(re)

    pk = list(data.keys())[0]
    times = list(data.values())[0]['ts']['times']
    values = list(data.values())[0]['ts']['values']

    ts = TimeSeries(times, values)

    client.insert_ts(pk, ts)
    return 'OK'

@app.route('/upsert_meta', methods=['POST'])
def upsert_meta():
    #Allows you to instert a time series in json format
    re = request.json
    data = json.loads(re)

    md = list(data.values())[0]

    pk = list(data.keys())[0]

    client.upsert_meta(pk, md)
    return 'OK'     

@app.route('/augmented_select', methods=['POST'])
def augmented_select():
    re = request.json
    data = json.loads(re)

    md = data["md"] if "md" in data else None
    additional = data["additional"] if "additional" in data else None
    proc = data["proc"] 
    target = data["target"]
    arg = data["arg"] if "arg" in data else None

    # self, proc, target, arg=None, metadata_dict={}, additional=None)
    _, result = client.augmented_select(proc, target, arg, md, additional)
    print("RESULT", type(result))
    print(result)

    # return flask.jsonify(**result)
    return json.dumps(result, indent=4, separators=(',', ': '))
    # return '<pre>'+ json.dumps(result, indent=4, separators=(',', ': '))+'</pre>'
     

# if __name__ == '__main__':
#     empty_schema = {'pk': {'convert': lambda x: x, 'index': None}}
#     db = DictDB(empty_schema, 'pk')
#     TSDBServer(db).run()

from collections import OrderedDict
import flask
from flask import Flask, url_for, request
from .dictdb import DictDB
from timeseries import TimeSeries
import json
import procs
from importlib import import_module
import re


app = Flask(__name__)

empty_schema = {'pk': {'convert': lambda x: x, 'index': True},
                'ts': {'convert': lambda x: x, 'index': None},
                'order': {'convert': int, 'index': 1},
                'blarg': {'convert': int, 'index': 1}}

db = DictDB(empty_schema, 'pk')

@app.route('/')
def index():
    pass

@app.route('/select')
def select():
	md = request.args.get('md', '')
	fields = request.args.get('fields', '')
	additional = request.args.get('additional', '')

	split_md = md.split(',')
	md = dict(zip(split_md[::2], split_md[1::2]))

	
	if len(list(md.values()))>0:
		params = re.findall('\d+|\D+',list(md.values())[0])
		md2 = {}
		filt = {}
		filt[params[0]] = int(params[1])
		md2[list(md.keys())[0]] =  filt
		md = md2

	fields = fields.split(',') if fields else []

	split_additional = additional.split(',')
	additional = dict(zip(split_additional[::2], split_additional[1::2])) or None


	loids, fields = db.select(md, fields, additional)
	if fields is not None:
		new_fields = []
		for f_d in fields:
			f_d = {k: v.to_json() if hasattr(v, 'to_json') else v
			       for k, v in f_d.items()}
			print(f_d)
			new_fields.append(f_d)
		d = OrderedDict(zip(list(map(str, loids)), new_fields))
	else:
		d = OrderedDict((str(k), {}) for k in loids)

	return  flask.jsonify(**d)

@app.route('/augmented_select', methods=['POST'])
def augmented_select():
	re = request.json
	data = json.loads(re)

	md = data['md']
	additional = data["additional"]
	proc = data["proc"]
	target = data["target"]
	arg = data["arg"]

	loids, fields = db.select(md, None, additional)
	mod = import_module('procs.' + proc)
	storedproc = getattr(mod, 'proc_main')

	results = []
	for pk in loids:
		row = db.rows[pk]
		result = storedproc(pk, row, arg)
		results.append(dict(zip(target, result)))


	return flask.jsonify(**dict(zip(loids, results)))
       
	
	# loids, fields = db.select(md, fields, additional)
	# if fields is not None:
	# 	new_fields = []
	# 	for f_d in fields:
	# 		f_d = {k: v.to_json() if hasattr(v, 'to_json') else v
	# 		       for k, v in f_d.items()}
	# 		print(f_d)
	# 		new_fields.append(f_d)
	# 	d = OrderedDict(zip(list(map(str, loids)), new_fields))
	# else:
	# 	d = OrderedDict((str(k), {}) for k in loids)

	# return  flask.jsonify(**d)


@app.route('/insert', methods=['POST'])
def insert():
	#Allows you to instert a time series in json format
	re = request.json
	data = json.loads(re)

	pk = list(data.keys())[0]
	times = list(data.values())[0]['ts']['times']
	values = list(data.values())[0]['ts']['values']

	ts = TimeSeries(times, values)

	db.insert_ts(pk, ts)
	return 'OK'

@app.route('/upsert_meta', methods=['DELETE'])
def upsert_meta():
	#Allows you to instert a time series in json format
	re = request.json
	data = json.loads(re)

	md = list(data.values())[0]

	pk = list(data.keys())[0]

	db.upsert_meta(pk, md)
	print(md)
	return 'OK'
# from flask import Flask, url_for, request

# app = Flask(__name__)
# @app.route('/')
# def index(): pass



# @app.route('/select	')
# def select():
# 	md = request.args.get('md', '')
# 	fields = request.args.get('fields', '')
# 	additional = request.args.get('additional', '')
# 	loids, fields = self.server.db.select(op['md'], op['fields'], op['additional'])
#     self._run_trigger('select', loids)




# if __name__ == '__main__':
#     empty_schema = {'pk': {'convert': lambda x: x, 'index': None}}
#     db = DictDB(empty_schema, 'pk')
#     TSDBServer(db).run()

from collections import OrderedDict
import flask
from flask import Flask, url_for, request
from .dictdb import DictDB
from timeseries import TimeSeries


app = Flask(__name__)

empty_schema = {'pk': {'convert': lambda x: x, 'index': None},
                'ts': {'convert': lambda x: x, 'index': None}}
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

@app.route('/insert')
def insert():
	pk = request.args.get('pk', None)
	times = request.args.get('times', '')
	values = request.args.get('values', '')

	times = times.split(',') if times else []
	times = list(map(float, times))

	values = values.split(',') if values else []
	values = list(map(float, values))

	if not pk or not times or not values:
		return 'Error, the input must be...', 400

	ts = TimeSeries(times, values)
	pk = int(pk)

	db.insert_ts(pk, ts)
	return 'OK'

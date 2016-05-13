import timeseries as ts

async def main(pk, row, arg):
    # print("[[[[[[[[[[[STATS]]]]]]]]]]]]", pk, row, arg)
    damean = ts.TimeSeries(row['ts']['times'], row['ts']['values']).mean()
    dastd = ts.TimeSeries(row['ts']['times'], row['ts']['values']).std()
    return [damean, dastd]


def proc_main(pk, row, arg):
    """
    including pk and arg because of call in tsdb_server.py
    """
    damean = ts.TimeSeries(row['ts']['times'], row['ts']['values']).mean()
    dastd = ts.TimeSeries(row['ts']['times'], row['ts']['values']).std()
    return [damean, dastd]

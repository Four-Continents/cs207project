import timeseries as ts

async def main(pk, row, arg):
    # print("[[[[[[[[[[[STATS]]]]]]]]]]]]", pk, row, arg)
    print("PARA LA MEAN",ts.TimeSeries(row['ts']['times'], row['ts']['values']))
    damean = ts.TimeSeries(row['ts']['times'], row['ts']['values']).mean()
    dastd = ts.TimeSeries(row['ts']['times'], row['ts']['values']).std()
    return [damean, dastd]


def proc_main(pk, row, arg):
    """
    including pk and arg because of call in tsdb_server.py
    """
    damean = row['ts'].mean()
    print("MEAN",damean)
    dastd = row['ts'].std()
    print("STD",std)
    return [damean, dastd]

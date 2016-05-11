import asyncio
async def main(pk, row, arg):
    #print("[[[[[[[[[[[STATS]]]]]]]]]]]]", pk, row, arg)
    damean = row['ts'].mean()
    dastd = row['ts'].std()
    return [damean, dastd]

def proc_main(pk, row, arg):
    """
    including pk and arg because of call in tsdb_server.py
    """
    damean = row['ts'].mean()
    dastd = row['ts'].std()
    return [damean, dastd]

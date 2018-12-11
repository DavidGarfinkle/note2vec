import pandas as pd
from vis.analyzers.indexers.noterest import MultiStopIndexer
from vis.models.indexed_piece import Importer
from music21.musedata.base40 import pitchToBase40

def _to_base40(float_or_str):
    event = str(float_or_str).lower()

    if event in ('rest', 'nan'):
        return event
    else:
        return pitchToBase40(event)

def pointset(file_path):
    ip = Importer(file_path)
    df = ip.get_data('multistop')

    if len(df) == 0:
        raise Exception("Pointset is empty!")

    # Convert pitch names to Base40
    df40 = df['noterest.MultiStopIndexer'].applymap(_to_base40)

    # Save the offset index as columnar data
    df40['offset'] = df40.index

    series = [df40[[str(i), 'offset']].rename(columns={str(i): 'pitch'}) for i in range(len(df40.columns) - 1)]

    pointset = pd.concat(series, ignore_index = 1)
    pointset = pointset[(pointset.pitch != 'nan') & (pointset.pitch != 'rest')]
    pointset = pointset.sort(['offset', 'pitch'])
    pointset = pointset.reset_index(drop=True)

    return pointset


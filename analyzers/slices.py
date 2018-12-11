import math

def slices(notes_df):

    # Each slice is one quarterLength
    duration = notes_df.iloc[-1].offset
    numslices = int(math.ceil(duration / 4))

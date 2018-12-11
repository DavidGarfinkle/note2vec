import sys
sys.path.append('/home/dgarfinkle/note2vec')
import os
from indexers import pointset

def main():
    musdir = sys.argv[1]
    outdir = sys.argv[2]

    for doc in os.listdir(musdir):
        fullpath = os.path.join(musdir, doc)

        print("Indexing {}".format(doc))
        df = pointset(fullpath)

        docname, doctype = os.path.splitext(doc)
        outpath = os.path.join(outdir, docname + '.pkl')
        print("Pickling to {}".format(outpath))
        df.to_pickle(outpath)

if __name__ == "__main__":
    main()

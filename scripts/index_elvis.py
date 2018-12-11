import sys
sys.path.append('/usr/share/smr-db/note2vec')
import os
import json
import shutil
from indexers import pointset

class Piece():
    def __init__(self, basepath):
        name, ext = os.path.splitext(basepath)
        info = name.split('_')

        self.id = int(info[0])
        self.name = "_".join(info[1:-1])
        self.ext = ext
        self.format = ext[1:]

        # JSON
        keys = ['name', 'format']
        data = { key: getattr(self, key) for key in keys }
        data['collection'] = 'elvis'
        self.json = { self.id: data }

def is_piece(basepath):
    return basepath[0] == '0'

def main():
    musdir = sys.argv[1]
    outdir = sys.argv[2]

    with open(os.path.join(outdir, 'data.json'), 'a') as f:

        for doc in (d for d in os.listdir(musdir) if is_piece(d)):
            print("Indexing {}".format(doc))
            fullpath = os.path.join(musdir, doc)
            piece = Piece(doc)

            try:
                df = pointset(fullpath)
            except Exception as e:
                print(e)
                continue

            # Write to music/ and index/
            mus_outpath = os.path.join(outdir, 'music', str(piece.id)) + piece.ext
            ind_outpath = "{}.csv".format(os.path.join(outdir, 'index', str(piece.id)))
            print("Writing to {}, {}".format(mus_outpath, ind_outpath))
            shutil.copyfile(fullpath, mus_outpath)
            df.to_csv(ind_outpath, sep='\t', index_col='index')

            # Update data.json
            f.write(json.dumps(piece.json) + '\n')

if __name__ == '__main__':
    main()

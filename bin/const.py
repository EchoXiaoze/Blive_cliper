from enum import Enum
from pathlib import Path

# path=os.path.dirname(sys.argv[0]).replace('/','\\')

class Dirs(Enum):
    records: Path = "录播"
    clips: Path = "切片"
    former_rec: Path = "往期录播"
    former_clips: Path = "往期切片"





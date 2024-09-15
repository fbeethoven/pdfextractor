from  pathlib import Path
import os 


PROJ_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR: str = os.path.join(PROJ_ROOT, "data")
REFERENCE_DIR: str = os.path.join(PROJ_ROOT, "references")

TRANSLATE_URL_BASE: str = "https://translate.googleapis.com/translate_a/single"
TRANSLATE_URL: str = f"{TRANSLATE_URL_BASE}?client=gtx&sl=pl&tl=en&dt=t&q="

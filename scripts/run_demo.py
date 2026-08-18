import json
from pathlib import Path
from authority_cut import run_demo
r=run_demo(); print(json.dumps(r,indent=2)); Path('results/controlled-demo.json').write_text(json.dumps(r,indent=2)+'\n')

import sys
from pathlib import Path

package_dir = Path(__file__).parent.joinpath('..', 'src').resolve()
sys.path.insert(0, str(package_dir))

import textgrid_explorer

textgrid_explorer.main()

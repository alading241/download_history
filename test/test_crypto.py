

import os
import sys
CURRENTURL = os.path.dirname(__file__)
sys.path.append(os.path.dirname(CURRENTURL))

from gl.gl import SavePassword



data = SavePassword().readcrypto()
print(data)
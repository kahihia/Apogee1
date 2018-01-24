# this allows the setting folder to look like a module

# base is loaded first
from .base import *

# production will override base
from .production import *

# local will override production and base
# not sure why it's in a try block
try:
	from .local import *
except:
	pass
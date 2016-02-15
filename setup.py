from distutils.core import setup
import py2exe

setup(console=['main.py'])

# windows = [{
#             "script":"myprogram.pyw",
#             "icon_resources": [(1, "myicon.ico")],
#             "dest_base":"myprogram"
#             }]
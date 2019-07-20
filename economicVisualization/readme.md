How to deploy visualization:

docker run -it -p 5006:5006 -v "pathToVol\vol":/out danielperezr88/bokeh-python3:latest /bin/bash

bokeh serve --show econ_vix.py
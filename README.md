# SpatialProteomicsQC
This is a quality control tool for spatial proteomics data that has been developed in the Borner lab. Primary results illustrating the functionality of the tool have been published [here](https://doi.org/10.1101/2021.11.09.467934) and presented [here](https://www.youtube.com/watch?v=dUrOxYHJihc). The graphical user interface is available at https://domqc.bornerlab.org. Alternatively you can clone this repository and run the user interface locally or use the provided functionaility in custom pyhton code. If you encounter any issues with the website or the code please let us know through the issues on this repository and if you have any unanswered questions regarding the science behind it don't hesitate to contact us directly.

## Disclaimer
While the code base underlying this tool has been reviewed thoroughly the interface is still in an unpolished state. Therefore we recommend sanity checking results from the interface and running clean sessions, i.e. only upload data you want to compare in that session and reload the page if you want to switch to a different project. As we will update the webpage from time to time it might be down for short intervals of time.

## Running locally
To run the app locally create a new python environment (>=3.7.6) clone the repository and install the package:
```
python3 -m venv path/to/env
source path/to/env/bin/activate

git clone https://github.com/valbrecht/SpatialProteomicsQC

pip install .
```
If any pip installations fail due to external dependencies missing (e.g. zlib requirement for Pillow installation from source on python 3.6, or Microsoft Visual C++ 14 on windows) try installing that library using a binary file, thereby avoiding the dependency:
```
pip install --only-binary :all: Pillow
```

Then you can run a panel serve command from the command line:
```
cd webapp
panel serve QCtool.py
```

Alternatively you can install jupyter and open the jupyter notebook and run the app directly. This will allow you to load files >80MB through the commented code cells at the end of the file.

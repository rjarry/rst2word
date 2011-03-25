rmdir /S /Q dist
python setup.py sdist
python setup.py bdist_wininst
rmdir /S /Q build

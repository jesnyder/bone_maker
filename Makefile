DEFAULT_GOAL:  pythonanalysis

.PHONY: pythonanalysis
pythonanalysis:
	pip install --upgrade -r requirements.txt
	python3  code/python/c0000_main.py

.PHONY: install dev test lint doctor gen serve docker

install:
	pip install -e .

dev:
	pip install -e ".[all]"

test:
	python -m unittest discover -s tests -v

lint:
	python -m py_compile photonforge/*/*.py

doctor:
	photonforge doctor

gen:
	photonforge gen "一只戴红围巾的柴犬，冬日清晨，柔和逆光，4k，电影感" --provider mock

serve:
	photonforge serve --port 8000

docker:
	docker build -t photonforge:latest .

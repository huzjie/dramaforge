PY ?= python

all: compile test doctor

compile:
	$(PY) -m compileall -q dramaforge

test:
	$(PY) -m unittest discover -s tests -t .

doctor:
	$(PY) -m dramaforge.doctor

bench:
	$(PY) -m dramaforge.cli bench --config configs/default.yaml

synth:
	$(PY) -m dramaforge.cli synth --config configs/default.yaml --text "你好，欢迎收听今天的播客。"

serve:
	$(PY) -m dramaforge.cli serve --config configs/default.yaml

.PHONY: all compile test doctor bench synth serve

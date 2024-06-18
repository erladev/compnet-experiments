all: combined-plot-ex2.svg combined-plot-ex3.svg combined-plot-ex4.svg


combined-plot-ex3.svg: ex3/csv/*.csv plots_combined.py
	python3 plots_combined.py --output $@ --ref ex3/csv/demon.csv --t0 --no_ref_for=ex3/csv/edon-laptop.csv ex3/csv/*.csv


combined-plot-%.svg: %/csv/*.csv plots_combined.py
	python3 plots_combined.py --output $@ --ref $*/csv/demon.csv --t0 $*/csv/*.csv


clean:
	rm -fr combined-plot-ex*.svg
all: combined-plot-ex2.png combined-plot-ex3.png combined-plot-ex4.png plot-ex5.png


combined-plot-ex3.png: ex3/csv/*.csv plots_combined.py
	python3 plots_combined.py --output $@ --markers=ex3/markers.csv --ref ex3/csv/demon.csv --t0 --no_ref_for=ex3/csv/edon-laptop.csv ex3/csv/*.csv


combined-plot-ex2.png: ex2/csv/*.csv plots_combined.py
	python3 plots_combined.py --output $@ --ref ex2/csv/demon.csv --t0 ex2/csv/*.csv

combined-plot-ex4.png: ex4/csv/*.csv plots_combined.py
	python3 plots_combined.py --output $@ --ref ex4/csv/demon.csv --t0 ex4/csv/*.csv

plot-ex5.png: ex5/*.csv plots_combined.py
	python3 plots_combined.py --output $@ ex5/*.csv

clean:
	rm -fr combined-plot-ex*.png
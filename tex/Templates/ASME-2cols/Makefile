# type "make" command in Unix to create asme2ej.pdf file 
all:
	latex asme2ej
	bibtex asme2ej
	latex asme2ej
	latex asme2ej
	dvips -o asme2ej.ps asme2ej
	ps2pdf asme2ej.ps asme2ej.pdf

clean:
	(rm -rf *.ps *.log *.dvi *.aux *.*% *.lof *.lop *.lot *.toc *.idx *.ilg *.ind *.bbl *blg)

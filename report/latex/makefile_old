# makefile for dvips

all:
	latex	main.tex 
	dvips	-Ppdf	-G0	main.dvi
	ps2pdf	main.ps
dvi: 
	latex	main.tex
ps:
	dvips	-Ppdf	-G0	main.dvi
		# the -G0 fixes the ligature problem.
pdf:
	ps2pdf	main.ps

clean:
	rm	main.aux
	rm	main.dvi
	rm	main.log
	rm	main.toc
	rm	main.ps
	rm	main.pdf


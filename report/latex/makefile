# makefile for dvips

all:
	latex	main.tex
	bibtex	main
	latex	main.tex
	latex	main.tex 
	dvips	main.dvi
	gs -dSAFER -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sPAPERSIZE=a4 -dPDFSETTINGS=/printer \-dCompatibilityLevel=1.3 -dMaxSubsetPct=100 -dSubsetFonts=true -dEmbedAllFonts=true \-sOutputFile=file.pdf main.ps 

clean:
	rm	main.aux
	rm	main.dvi
	rm	main.log
	rm	main.toc
	rm	main.ps
	rm	main.pdf


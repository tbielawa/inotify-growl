#!/usr/bin/make

clean:
	find . -type f -name "*~" -delete
	find . -type f -name "#*#" -delete
	find . -type f -name "*.py[co]" -delete

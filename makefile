CC = gcc
TAGRET = cheat
PROG = memory/bytes.c process/process.c
CFLAGS = -Iinclude

run:
	$(CC) -o $(TAGRET) $(PROG) $(CFLAGS)

clean:
	rm -rf *.o $(TAGRET)
	rm -rf $(TAGRET)

python:
	python3 tui/tui.py

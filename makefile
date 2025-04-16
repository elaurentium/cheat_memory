CC = gcc
TAGRET = cheat
PROG = memory/bytes.c memory/process.c

run:
	$(CC) -o $(TAGRET) $(PROG)

clean:
	rm -rf *.o $(TAGRET)
	rm -rf $(TAGRET)

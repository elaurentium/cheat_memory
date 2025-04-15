CC = gcc
OBJS = memory/proc.o memory/bytes.o
TAGRET = cheat
PROG = memory/bytes.c memory/process.c

$(TAGRET): $(OBJS)
	$(CC) -o $(TAGRET) $(OBJS)

memory/proc.o: memory/process.c
	$(CC) -c memory/process.c

memory/bytes.o: memory/bytes.c
	$(CC) -c memory/bytes.c

run:
	$(CC) -o $(TAGRET) $(PROG)

clean:
	rm -rf *.o $(TAGRET)
	rm -rf $(TAGRET)

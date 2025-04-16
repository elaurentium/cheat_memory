CC = gcc
OBJS = bin/proc.o bin/bytes.o
TAGRET = cheat
PROG = memory/bytes.c memory/process.c

$(TAGRET): $(OBJS)
	$(CC) -o $(TAGRET) $(OBJS)

bin/proc.o: memory/process.c
	$(CC) -c memory/process.c -o bin/proc.o

bin/bytes.o: memory/bytes.c
	$(CC) -c memory/bytes.c -o bin/bytes.o

run:
	$(CC) -o $(TAGRET) $(PROG)

clean:
	rm -rf bin/*.o $(TAGRET)
	rm -rf $(TAGRET)

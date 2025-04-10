run:
	gcc -o memo memory/memory.c
	g++ -o process memory/process.c

clean:
	rm -fr memo
	rm -fr process
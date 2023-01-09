all: 
	gcc -g -Wall -o pr4 pr4.c
	gcc -g -Wall -o pr4_p pr4_p.c -lpthread

pr4: pr4.c
	gcc -g -Wall -o pr4 pr4.c

pr4_p: pr4_p.c
	gcc -g -Wall -o pr4_p pr4_p.c -lpthread
	
clean:
	rm pr4 pr4_p

test:
	./pr4 test.txt 5 > serial.txt
	./pr4_p test.txt 5 2 1 > parallel.txt
	diff -y serial.txt parallel.txt 
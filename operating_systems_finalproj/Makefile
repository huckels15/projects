SRCS = $(wildcard *.c)
CFLGS = -Wall -Werror -D_FILE_OFFSET_BITS=64 -std=gnu99
OBJS = $(SRCS:.c=.o)
RHEL8HOSTS = wpwkddlth17619 wpwkddlth17620

all: grayfs

test: pathnames-test gfs-helper-test

clean:
	rm -f gfs-helper gfs-helper-test grayfs pathnames pathnames-test *.o

gfs-helper.o: gfs-helper.c gfs-helper.h grayfs.h pathnames.h utils.o
	gcc $(CFLGS) -c -o gfs-helper.o  gfs-helper.c

gfs-helper-test: gfs-helper.o pathnames.o utils.o gfs-helper.c
	gcc $(CFLGS) -o gfs-helper-test  gfs-helper.o gfs-helper-test.c pathnames.o utils.o

grayfs: grayfs.c grayfs.h gfs-helper.h pathnames.h utils.h gfs-helper.o pathnames.o utils.o
	gcc $(CFLGS) grayfs.c gfs-helper.o pathnames.o utils.o `pkg-config fuse3 --cflags --libs` -o grayfs
	@for host in $(RHEL8HOSTS) ; do \
		./checkbadhost.sh $$host ; \
	done;

pathnames.o: pathnames.c pathnames.h grayfs.h gfs-helper.h utils.h
	gcc $(CFLGS) -c -o pathnames.o pathnames.c

pathnames-test: pathnames.o utils.o pathnames-test.c
	gcc $(CFLGS) -o pathnames-test  pathnames-test.c pathnames.o utils.o

utils.o: utils.c utils.h
	gcc $(CFLGS) -c -o utils.o utils.c

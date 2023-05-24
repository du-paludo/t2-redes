# PROG = client server
# CC = gcc
# CFLAGS =
# OBJS = client.o server.o

# .PHONY: all debug clean purge

all: client

client: client.o deck.o
	gcc -o client client.o deck.o

# server: server.o
# 	gcc -o server server.o

client.o: client.c 
	gcc -c client.c

deck.o: deck.c
	gcc -c deck.c

# server.o: server.c
# 	gcc -c server.c

# %.o: %.c %.h
# 	$(CC) $(CFLAGS) -c $< -o $@

# $(PROG): % : $(OBJS) %.o
# 	$(CC) $(CFLAGS) -o $@ $^ $(LFLAGS)

clean:
	@rm -f *~ *.bak *.tmp

purge: clean
	@rm -f  $(PROG) $(PROG_AUX) *.o $(OBJS) core a.out
	@rm -f *.png marker.out *.log
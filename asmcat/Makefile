
NAME	=	cat
SRC	=	cat.s
OBJ	=	cat.o

all:
	nasm -felf64 $(SRC)
	ld -o $(NAME) $(OBJ)

re:	clean all

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)


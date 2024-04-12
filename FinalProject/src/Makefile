
COOKIE = PACBROS
SNAME  = server-node
HOST   = default
ROOM   = server

all: server client

%.beam: %.erl
	erlc $<

server: client_server.beam 
	@echo "client_server:server_start($(ROOM))." | erl -sname $(SNAME) -setcookie $(COOKIE)

client: client_server.beam 
	@echo "client_server:client_start('$(SNAME)@$(HOST)', $(ROOM))." \
		| erl -sname $(SNAME) -setcookie $(COOKIE)
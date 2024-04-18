
COOKIE = PACBROS
SNAME  = server-node
HOST   = default
STOP   = stopper
CLIENT = client
ROOM   = server

all: client_server.beam

%.beam: %.erl
	erlc $<

server: client_server.beam 
	(echo "client_server:server_start($(ROOM))."; cat; echo "client_server:server_done($(ROOM)).") | erl -sname $(SNAME) -setcookie $(COOKIE)

client: client_server.beam 
	@echo "client_server:client_start('$(SNAME)@$(HOST)', $(ROOM))." \
		| erl -sname $(CLIENT) -setcookie $(COOKIE)



clean: 
	rm *.beam
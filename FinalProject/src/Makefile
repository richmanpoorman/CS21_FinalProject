
COOKIE = PACBROS
SNAME  = server-node
HOST   = default
STOP   = stopper
CLIENT = client
ROOM   = server
PYTHON3 = python

all: python_lib client_server.beam

%.beam: %.erl
	erlc $<

server: client_server.beam 
	(echo "client_server:server_start($(ROOM), \"$(PYTHON3)\")."; cat; echo "client_server:server_done($(ROOM)).") | erl -sname $(SNAME) -setcookie $(COOKIE)

client: client_server.beam 
	@echo "client_server:client_start('$(SNAME)@$(HOST)', $(ROOM), \"$(PYTHON3)\")." \
		| erl -sname $(CLIENT) -setcookie $(COOKIE)

dependencies: python_lib

python_lib:
	$(PYTHON3) -m pip -q --exists-action i install --user pygame
	$(PYTHON3) -m pip -q --exists-action i install --user numpy
	$(PYTHON3) -m pip -q --exists-action i install --user erpy


clean: 
	rm *.beam
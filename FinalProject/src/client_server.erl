-module(client_server).

-record(server_state, {port, players, clock, baseThread}).
-record(user_state  , {port, server, clock, baseThread}).

-export([server_start/1, server_done/1, server_send_port/2, server_get_port/1, client_start/2, receive_base/0]).
-define(INPUT_UPDATE_CLOCK, 10).
-define(DISPLAY_UPDATE_CLOCK, 100).
%%% SERVER SIDE %%%

%%% Name    : server_start
%%% Purpose : Starts the server which hosts the game logic 
%%% Params  : (atom) ServerName := The name of the server to start 
%%% Return  : (bool) If the server was able to start or not
server_start(ServerName) -> 
    PythonSpawn = "python -u ../src/GameRunner.py",
    BaseThread  = self(),
    register(ServerName, spawn_link(fun () -> server_initialize(PythonSpawn, BaseThread) end)),
    output_line("Server Done").

%%% Name    : broadcast
%%% Purpose : Sends the message to all of the players connected to the server 
%%% Params  : (atom)         Command := The message type/name to send
%%%           (dict)         Data    := The data needed to execute the command 
%%%           (server_state) State   := The state of the erlang loop 
%%% Return  : (server_state) The state after broadcasting
broadcast(Command, Data, State) -> 
    SendMsg = fun (Player) -> Player ! {from_server, {self(), Command, Data}} end,
    Players = State#server_state.players,
    lists:foreach(SendMsg, Players),
    State. 

%%% Name    : server_initialize
%%% Purpose : Start of the thread which has the server 
%%% Params  : (str) PythonSpawn := The command to start the python logic module
%%%           (pid) BaseThread  := The base thread which called the function
%%% Return  : ok
server_initialize(PythonSpawn, BaseThread) -> 
    Port = open_port({spawn, PythonSpawn}, [binary, {packet,4}, use_stdio]),
    SelfPid = self(),
    Clock   = spawn_link(fun () -> server_clock(SelfPid) end),
    InitialState = #server_state{port = Port, players = [], clock = Clock, baseThread = BaseThread},
    server_loop(InitialState).

%%% Name    : server_loop
%%% Purpose : Waits for messages and sends them to the appropriate location
%%% Params  : (server_state) State := The state of the program at the time
%%% Return  : ok
server_loop(State) -> 
    receive
        {__Port, {data, EncodedData}} -> 
            {Command, Data} = binary_to_term(EncodedData),
            % output_format("received command: ~p", [Command]),
            NewState = server_send(Command, Data, State),
            case Command of 
                done -> ok;
                _    -> server_loop(NewState)
            end;
        {from_client, {Pid, Command, Msg}} -> 
            output_format("got command ~p from client", [Command]),
            NewState = server_receive(Pid, Command, Msg, State),
            server_loop(NewState);
        done -> 
            Port = State#server_state.port,
            send_port_message(self(), done, [], Port),
            broadcast(done, [], State),
            send_base(done, State),
            Port ! {self(), close},
            State#server_state.baseThread ! done,
            output_line("Received Done");
        clock -> 
            NewState = server_receive(self(), clock, [], State),
            server_loop(NewState);
        {py_port, Msg} ->
            Port = State#server_state.port, 
            send_port_message(self(), py_port, Msg, Port),
            server_loop(State);
        get_port -> 
            send_base(State#server_state.port, State),
            server_loop(State);
        {__Port, closed} -> 
            output_line("Port was closed ..."),
            ok;
        Msg -> 
            output_line("Got a bad message"),
            output_format("received command: ~p", [Msg]),
            NewState = server_receive(self(), 'bad_message', Msg, State),
            server_loop(NewState)
    end.

%%% Name    : server_send
%%% Purpose : Sends the message to the users after receiving info from the port
%%% Params  : (atom)         Command := The message type/name to send
%%%           (dict)         Data    := The data needed to execute the command 
%%%           (server_state) State   := The state of the erlang loop 
%%% Return  : (server_state) The state after broadcasting
server_send(Command, Data, State) ->
    broadcast(Command, Data, State).

%%% Name    : server_receive
%%% Purpose : Sends message to the port (which is the game logic module)
%%% Params  : (pid)          Pid     := The pid of the client sending the message
%%%           (atom)         Command := The message type/name the client sent 
%%%           (dict)         Data    := The data needed to execute the command 
%%%           (server_state) State   := The state of the erlang loop
%%% Return  : (server_state) The state after receiving the command
server_receive(Pid, Command, Msg, State) -> 
    Port = State#server_state.port,
    send_port_message(Pid, Command, Msg, Port), 
    case Command of 
        player_join -> 
            Players    = State#server_state.players,
            NewPlayers = [Pid | Players],
            State#server_state{players = NewPlayers};
        quit -> 
            Players    = State#server_state.players,
            NewPlayers = lists:delete(Pid, Players),
            State#server_state{players = NewPlayers};
        _ ->
            State
    end.

server_clock(LoopPid) ->
    LoopPid ! clock,
    receive 
        quit -> 
            % output_line("Clock quit"),
            ok
    after
        ?INPUT_UPDATE_CLOCK -> client_clock(LoopPid)
    end.


%%% Name    : server_done
%%% Purpose : Closes the server of the given name
%%% Params  : (atom) ServerName := Name of the server room
%%% Return  : done
server_done(ServerName) -> 
    whereis(ServerName) ! done. 

%%% Name    : server_send_port
%%% Purpose : Testing function which sends message from erlang across the port
%%% Params  : (atom) ServerName := The name of the server to go to
%%%           (str)  Msg        := Message for the game logic to receive 
%%% Return  : (N/A) 
server_send_port(ServerName, Msg) ->
    whereis(ServerName) ! {py_port, Msg}.

%%% Name    : server_get_port
%%% Purpose : Gets the port information about the server
%%% Params  : (atom) ServerName := The name of the server to investigate
%%% Return  : (port) The ports of the program
server_get_port(ServerName) -> 
    whereis(ServerName) ! get_port,
    receive 
        Msg -> Msg
    end. 


%%% CLIENT SIDE %%%

%%% Name    : client_start
%%% Purpose : Starts the client 
%%% Params  : (atom) The name of the server node
%%%           (atom) The room of the server on the server node
%%% Return  : (bool) True if the client successfully starts
client_start(ServerNode, ServerRoom) -> 
    output_line("client start"),
    PythonSpawn = "python -u ../src/ClientRunner.py",
    BaseThread  = self(),
    % Pid = spawn_link(fun () -> client_initalize(PythonSpawn, ServerNode, ServerRoom, BaseThread) end),
    % register(client, Pid).
    register(client, self()),
    client_initalize(PythonSpawn, ServerNode, ServerRoom, BaseThread),
    receive 
        quit -> ok 
    end. 

%%% Name    : client_initialize
%%% Purpose : Starts the client thread
%%% Params  : (str)  PythonString := The string command 
%%%           (atom) ServerNode   := The server node to join 
%%%           (atom) ServerRoom   := The server room on the node to join
%%% Return  : (N/A)
client_initalize(PythonSpawn, ServerNode, ServerRoom, BaseThread) ->
    Port    = open_port({spawn, PythonSpawn}, [binary, {packet,4}, use_stdio]),
    Server  = {ServerRoom, ServerNode}, 
    SelfPid = self(),
    Clock   = spawn_link(fun () -> client_clock(SelfPid) end),
    InitialState = #user_state{port = Port, server = Server, clock = Clock, baseThread = BaseThread},
    client_loop(InitialState),
    output_line("erlang client close").

%%% Name    : client_loop
%%% Purpose : Gets messages from the client and sends them out appropriately
%%% Params  : (server_state) State := Client loop state
%%% Return  : (N/A)
client_loop(State) -> 
    receive
        {__Port, {data, EncodedData}} -> 
            output_line("---GOT PORT RECEPTION---"),
            {Command, Data} = binary_to_term(EncodedData),
            output_format("Erlang sees command: ~p", [Command]),
            NewState = client_send(Command, Data, State),
            case Command of
                quit -> 
                    output_line("In quit reception"),
                    client_clock_stop(State),
                    State#user_state.baseThread ! quit, 
                    ok;
                _    -> client_loop(NewState)
            end;
        {from_server, {Pid, Command, Msg}} -> 
            % output_line("In server reception"),
            NewState = client_receive(Pid, Command, Msg, State),
            client_loop(NewState);
        clock -> 
            % output_line("erlang client clock caught by loop"),
            NewState = client_receive(self(), clock, [], State),
            client_loop(NewState);
        _  -> 
            output_line("In fall through reception"),
            client_loop(State)
    end. 

%%% Name    : post
%%% Purpose : Sends the message to the server
%%% Params  : (atom)       Command := The message type/name 
%%%           (dict)       Data    := The data to run the command 
%%%           (user_state) State   := The client loop state
%%% Return  : (user_state) The state after posting
post(Command, Data, State) -> 
    Server = State#user_state.server,
    Server ! {from_client, {self(), Command, Data}},
    State. 

%%% Name    : client_clock
%%% Purpose : Starts a loop that will wake up the client to send inputs periodically
%%% Params  : (pid) LoopPid := The pid of the client to alert
%%% Return  : (N/A)
client_clock(LoopPid) ->
    % output_format("erlang client clock send to erlang ~p", [LoopPid]),
    LoopPid ! clock,
    receive 
        quit -> 
            % output_line("Clock quit"),
            ok
    after
        ?INPUT_UPDATE_CLOCK -> client_clock(LoopPid)
    end.

    %%% CLIENT HELPERS %%%

%%% Name    : client_send
%%% Purpose : Sends the message to the port after receiving from the port
%%% Params  : (atom)       Command := The message type/name 
%%%           (dict)       Data    := The data to run the command 
%%%           (user_state) State   := The client loop state
%%% Return  : (user_state) The state after posting
client_send(Command, Data, State) -> 
    post(Command, Data, State).

%%% Name    : client_receive
%%% Purpose : Receives message from the server and sends it to the client python
%%% Params  : (pid)        Pid     := The pid the message is received from 
%%%           (atom)       Command := The command the server sent 
%%%           (data)       Msg     := The data to run the command 
%%%           (user_state) State   := The client loop state
%%% Return  : (user_state) The state after receiving
client_receive(Pid, Command, Msg, State) -> 
    Port = State#user_state.port,
    send_port_message(Pid, Command, Msg, Port),
    State.

%%% Name    : client_clock_stop
%%% Purpose : Stops the clock for message input
%%% Params  : (user_state) State := The loop state
%%% Return  : (N/A)
client_clock_stop(State) ->
    State#user_state.clock ! quit.

%%% MESSAGE PASSING HELPERS %%%

%%% Name    : send_port_message
%%% Purpose : Sends the message over the port
%%% Params  : (pid)  Pid     := The pid the data is received from
%%%           (atom) Command := The message name/type 
%%%           (atom) Msg     := The data to go along with the message
%%%           (port) Port    := The port to send the data over
%%% Return  : ok
send_port_message(Pid, Command, Msg, Port) -> 
    Port ! {self(), {command, term_to_binary({Pid, Command, Msg}) }},
    ok.

%%% Name    : send_base
%%% Purpose : Test function that sends the message to the server base thread
%%% Params  : (atom)         Msg   := The message to send
%%%           (server_state) State := Server loop state
%%% Return  : (N/A)
send_base(Msg, State) -> 
    State#server_state.baseThread ! Msg.

%%% Name    : receive_base
%%% Purpose : Receives messages on the server sent by send_base
%%% Params  : (None)
%%% Return  : (atom) The message sent from send_base
receive_base() -> 
    receive 
        Msg -> Msg 
    end.

%%% Name    : output_line
%%% Purpose : Prints the message out to the Test.txt file
%%% Params  : (atom) Msg := Message to print
%%% Return  : (N/A)
output_line(Msg) -> 
    output_format(Msg, []).

%%% Name    : output_format
%%% Purpose : Prints the message out to the Test.txt file with the formatting
%%% Params  : (atom) Msg   := Message to print
%%%           (list) Param := Parameters to substitute in
%%% Return  : (N/A)
output_format(Msg, Param) -> 
    file:write_file("Test.txt", io_lib:fwrite(Msg ++ "\n", Param), [append]).
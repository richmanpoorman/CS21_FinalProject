-module(client_server).

-record(server_state, {port, players, baseThread}).
-record(user_state  , {port, server, clock}).

-export([server_start/1, server_done/1, server_send_port/2, server_get_port/1, client_start/2, receive_base/0]).
-define(INPUT_UPDATE_CLOCK, 1000).
%%% SERVER SIDE %%%

%%% Name    : server_start
%%% Purpose : Starts the server which hosts the game logic 
%%% Params  : (atom) ServerName := The name of the server to start 
%%% Return  : (bool) If the server was able to start or not
server_start(ServerName) -> 
    PythonSpawn = "python -u ../src/GameLogic.py",
    register(ServerName, spawn_link(fun () -> server_initialize(PythonSpawn) end)).

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
%%% Return  : ok
server_initialize(PythonSpawn) -> 
    Port = open_port({spawn, PythonSpawn}, [binary, {packet,4}, use_stdio]),
    InitialState = #server_state{port = Port, players = [], baseThread = self()},
    server_loop(InitialState).

%%% Name    : server_loop
%%% Purpose : Waits for messages and sends them to the appropriate location
%%% Params  : (server_state) State := The state of the program at the time
%%% Return  : ok
server_loop(State) -> 
    receive
        {__Port, {data, EncodedData}} -> 
            {Command, Data} = binary_to_term(EncodedData),
            output_format("received command: ~p", [Command]),
            NewState = server_send(Command, Data, State),
            server_loop(NewState);
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
            ok;
        {py_port, Msg} ->
            Port = State#server_state.port, 
            send_port_message(self(), py_port, Msg, Port),
            server_loop(State);
        get_port -> 
            send_base(State#server_state.port, State),
            server_loop(State);
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
%%% Purpose : (atom) The name of the server node
%%%           (atom) 
%%% Params  : 
%%% Return  : 
client_start(ServerNode, ServerRoom) -> 
    output_line("client start"),
    PythonSpawn = "python -u ../src/ClientRunner.py",
    Pid = spawn_link(fun () -> client_initalize(PythonSpawn, ServerNode, ServerRoom) end),
    register(client, Pid).

%%% Name    : 
%%% Purpose : 
%%% Params  : 
%%% Return  : 
client_initalize(PythonSpawn, ServerNode, ServerRoom) ->
    Port    = open_port({spawn, PythonSpawn}, [binary, {packet,4}, use_stdio]),
    Server  = {ServerRoom, ServerNode}, 
    SelfPid = self(),
    Clock   = spawn_link(fun () -> client_clock(SelfPid) end),
    InitialState = #user_state{port = Port, server = Server, clock = Clock},
    client_loop(InitialState),
    output_line("erlang client close").

%%% Name    : 
%%% Purpose : 
%%% Params  : 
%%% Return  : 
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
                    ok;
                _    -> client_loop(NewState)
            end;
        {from_server, {Pid, Command, Msg}} -> 
            output_line("In server reception"),
            NewState = client_receive(Pid, Command, Msg, State),
            client_loop(NewState);
        clock -> 
            output_line("erlang client clock caught by loop"),
            NewState = client_receive(self(), clock, [], State),
            client_loop(NewState);
        _  -> 
            output_line("In fall through reception"),
            client_loop(State)
    end. 

%%% Name    : 
%%% Purpose : 
%%% Params  : 
%%% Return  : 
post(Command, Data, State) -> 
    Server = State#user_state.server,
    Server ! {from_client, {self(), Command, Data}},
    State. 

%%% Name    : 
%%% Purpose : 
%%% Params  : 
%%% Return  : 
client_clock(LoopPid) ->
    output_format("erlang client clock send to erlang ~p", [LoopPid]),
    LoopPid ! clock,
    receive 
        quit -> 
            output_line("Clock quit"),
            ok
    after
        ?INPUT_UPDATE_CLOCK -> client_clock(LoopPid)
    end.

    %%% CLIENT HELPERS %%%

%%% Name    : 
%%% Purpose : 
%%% Params  : 
%%% Return  : 
client_send(Command, Data, State) -> 
    post(Command, Data, State).

%%% Name    : 
%%% Purpose : 
%%% Params  : 
%%% Return  : 
client_receive(Pid, Command, Msg, State) -> 
    Port = State#user_state.port,
    send_port_message(Pid, Command, Msg, Port),
    State.

%%% Name    : 
%%% Purpose : 
%%% Params  : 
%%% Return  : 
client_clock_stop(State) ->
    State#user_state.clock ! quit.

%%% MESSAGE PASSING HELPERS %%%

%%% Name    : 
%%% Purpose : 
%%% Params  : 
%%% Return  : 
send_port_message(Pid, Command, Msg, Port) -> 
    Port ! {self(), {command, term_to_binary({Pid, Command, Msg}) }},
    ok.

%%% Name    : 
%%% Purpose : 
%%% Params  : 
%%% Return  : 
send_base(Msg, State) -> 
    State#server_state.baseThread ! Msg.

%%% Name    : 
%%% Purpose : 
%%% Params  : 
%%% Return  : 
receive_base() -> 
    receive 
        Msg -> Msg 
    end.

%%% Name    : 
%%% Purpose : 
%%% Params  : 
%%% Return  : 
output_line(Msg) -> 
    output_format(Msg, []).

%%% Name    : 
%%% Purpose : 
%%% Params  : 
%%% Return  : 
output_format(Msg, Param) -> 
    file:write_file("Test.txt", io_lib:fwrite(Msg ++ "\n", Param), [append]).
-module(client_server).

-record(server_state, {port, players, baseThread}).
-record(user_state  , {port, server}).

-export([server_start/1, server_done/1, server_send_port/2, server_get_port/1, client_start/2]).

%%% SERVER SIDE %%%
server_start(ServerName) -> 
    PythonSpawn = "python -u ../src/GameLogic.py",
    register(ServerName, spawn(fun () -> server_initialize(PythonSpawn) end)).

broadcast(Command, Data, State) -> 
    SendMsg = fun (Player) -> Player ! {from_server, {self(), Command, Data}} end,
    Players = State#server_state.players,
    lists:foreach(SendMsg, Players),
    State. 

server_initialize(PythonSpawn) -> 
    Port = open_port({spawn, PythonSpawn}, [binary, {packet,4}, use_stdio]),
    InitialState = #server_state{port = Port, players = [], baseThread = self()},
    server_loop(InitialState).

server_loop(State) -> 
    receive
        {__Port, {data, EncodedData}} -> 
            {Command, Data} = binary_to_term(EncodedData),
            NewState = server_send(Command, Data, State),
            server_loop(NewState);
        {from_client, {Pid, Command, Msg}} -> 
            NewState = server_receive(Pid, Command, Msg, State),
            server_loop(NewState);
        done -> 
            Port = State#server_state.port,
            send_port_message(self(), done, [], Port),
            broadcast(done, [], State),
            send_base(done, State),
            Port ! {self(), close};
        {py_port, Msg} ->
            Port = State#server_state.port, 
            send_port_message(self(), py_port, Msg, Port),
            server_loop(State);
        get_port -> 
            send_base(State#server_state.port, State),
            server_loop(State);
        Msg -> 
            NewState = server_receive(self(), 'bad_message', Msg, State),
            server_loop(NewState)
    end.

    %%% SERVER HELPERS %%%

server_send(Command, Data, State) ->
    broadcast(Command, Data, State).

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

server_done(ServerName) -> 
    whereis(ServerName) ! done. 

server_send_port(ServerName, Msg) ->
    whereis(ServerName) ! {py_port, Msg}.

send_base(Msg, State) -> 
    State#server_state.baseThread ! Msg.

server_get_port(ServerName) -> 
    whereis(ServerName) ! get_port,
    receive 
        Msg -> Msg
    end. 

%%% CLIENT SIDE %%%
client_start(ServerNode, ServerRoom) -> 
    PythonSpawn = "python -u ../src/ClientRunner.py",
    spawn(fun () -> client_initalize(PythonSpawn, ServerNode, ServerRoom) end).

client_initalize(PythonSpawn, ServerNode, ServerRoom) ->
    Port = open_port({spawn, PythonSpawn}, [binary, {packet,4}, use_stdio]),
    Server = {ServerRoom, ServerNode}, 
    InitialState = #user_state{port = Port, server = Server},
    client_loop(InitialState).

post(Command, Data, State) -> 
    Server = State#user_state.server,
    Server ! {from_client, {self(), Command, Data}},
    State. 

client_loop(State) -> 
    receive
        {__Port, {data, EncodedData}} -> 
            {Command, Data} = binary_to_term(EncodedData),
            client_send(Command, Data, State);
        {from_server, {Pid, Command, Msg}} -> 
            client_receive(Pid, Command, Msg, State)
    end. 

    %%% CLIENT HELPERS %%%

client_send(Command, Data, State) -> 
    NewState = post(Command, Data, State),
    case Command of 
        quit -> ok;
        _    -> client_loop(NewState)
    end.

client_receive(Pid, Command, Msg, State) -> 
    Port = State#user_state.port,
    send_port_message(Pid, Command, Msg, Port),
    case Command of 
        done -> ok;
        _    -> client_loop(State)
    end.


%%% MESSAGE PASSING HELPERS %%%
send_port_message(Pid, Command, Msg, Port) -> 
    Port ! {Pid, {command, term_to_binary({Pid, Command, Msg}) }},
    ok.
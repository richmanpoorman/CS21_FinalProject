-module(client_server).

-record(server_state, {port, players, baseThread}).
-record(user_state  , {port, server, clock}).

-export([server_start/1, server_done/1, server_send_port/2, server_get_port/1, client_start/2, receive_base/0]).
-define(INPUT_UPDATE_CLOCK, 1000).
%%% SERVER SIDE %%%
server_start(ServerName) -> 
    PythonSpawn = "python -u ../src/GameLogic.py",
    register(ServerName, spawn_link(fun () -> server_initialize(PythonSpawn) end)).

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
            output_format("received command: ~w", [Command]),
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
            output_format("received command: ~w", [Msg]),
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


server_get_port(ServerName) -> 
    whereis(ServerName) ! get_port,
    receive 
        Msg -> Msg
    end. 

%%% CLIENT SIDE %%%
client_start(ServerNode, ServerRoom) -> 
    output_line("client start"),
    PythonSpawn = "python -u ../src/ClientRunner.py",
    Pid = spawn_link(fun () -> client_initalize(PythonSpawn, ServerNode, ServerRoom) end),
    register(client, Pid).

client_initalize(PythonSpawn, ServerNode, ServerRoom) ->
    Port   = open_port({spawn, PythonSpawn}, [binary, {packet,4}, use_stdio]),
    Server = {ServerRoom, ServerNode}, 
    SelfPid = self(),
    Clock  = spawn_link(fun () -> client_clock(SelfPid) end),
    InitialState = #user_state{port = Port, server = Server, clock = Clock},
    client_loop(InitialState),
    output_line("erlang client close").

client_loop(State) -> 
    receive
        {__Port, {data, EncodedData}} -> 
            output_line("In port reception"),
            {Command, Data} = binary_to_term(EncodedData),
            NewState = client_send(Command, Data, State),
            case Command of
                quit -> self() ! quit;
                _    -> client_loop(NewState)
            end;
        {from_server, {Pid, Command, Msg}} -> 
            output_line("In server reception"),
            NewState = client_receive(Pid, Command, Msg, State),
            client_loop(NewState);
        quit -> 
            output_line("In quit reception"),
            client_clock_stop(State),
            ok;
        clock -> 
            output_line("erlang client clock caught by loop"),
            NewState = client_receive(self(), clock, [], State),
            client_loop(NewState);
        Msg  -> 
            output_line("In fall through reception"),
            output_format("~w", [Msg])
    end. 

post(Command, Data, State) -> 
    Server = State#user_state.server,
    Server ! {from_client, {self(), Command, Data}},
    State. 

client_clock(LoopPid) ->
    output_format("erlang client clock send to erlang ~p", [LoopPid]),
    LoopPid ! clock,
    receive 
        quit -> ok
    after
        ?INPUT_UPDATE_CLOCK -> client_clock(LoopPid)
    end.

    %%% CLIENT HELPERS %%%

client_send(Command, Data, State) -> 
    post(Command, Data, State).

client_receive(Pid, Command, Msg, State) -> 
    Port = State#user_state.port,
    send_port_message(Pid, Command, Msg, Port),
    State.

client_clock_stop(State) ->
    State#user_state.clock ! quit.

%%% MESSAGE PASSING HELPERS %%%
send_port_message(Pid, Command, Msg, Port) -> 
    Port ! {self(), {command, term_to_binary({Pid, Command, Msg}) }},
    ok.

send_base(Msg, State) -> 
    State#server_state.baseThread ! Msg.

receive_base() -> 
    receive 
        Msg -> Msg 
    end.

output_line(Msg) -> output_format(Msg, []).
output_format(Msg, Param) -> file:write_file("Test.txt", io_lib:fwrite(Msg ++ "\n", Param), [append]).
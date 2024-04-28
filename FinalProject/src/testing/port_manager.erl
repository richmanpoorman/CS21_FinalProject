-module(port_manager).

-record(server_state, {port, players}).
-record(user_state  , {port, server}).


%%% SERVER SIDE %%%
server_start(SpawnString) -> 
    Port = open_port({spawn, SpawnString}, [binary, {packet,4}, use_stdio]),
    InitialState = #server_state{port = Port, players = []},
    server_loop(InitialState). 

broadcast({Command, Data}, State) -> 
    SendMsg = fun ({Command, Data}, Player) -> 
        Player ! {self(), Command, Data},
    lists:foreach(SendMsg, State#server_state.players),
    State. 

server_loop(State) -> 
    receive
        {Port, {data, EncodedData}} -> 
            {Command, Data} = binary_to_term(EncodedData),
            server_send(Command, Data, State);
        {Pid, Command, Msg} -> 
            server_receive(Pid, Command, Msg, State)
    end.

    %%% SERVER HELPERS %%%

server_send(Command, Data, State) ->
    NewState = broadcast(done, Data, State),
    case Command of 
        done -> ok. 
        _    -> serverLoop(NewState)
    end.

server_receive(Pid, Command, Msg, State) -> 
    Port = State#server_state.port,
    send_port_message(Pid, Command, Msg, Port), 
    case Command of 
        player_join -> 
            Players    = State#server_state.players,
            NewPlayers = [Pid | Players]
            #server_state{port = Port, players = NewPlayers},
            server_loop(NewState);
        quit -> 
            Players    = State#server_state.players,
            NewPlayers = lists:delete(Pid, Players)
            #server_state{port = Port, players = NewPlayers},
            server_loop(NewState);
        _ ->
            server_loop(NewState).
    end.

%%% CLIENT SIDE %%%
client_start(SpawnString, ServerNode, ServerRoom) -> 
    Port = open_port({spawn, SpawnString}, [binary, {packet,4}, use_stdio]),
    Server = {ServerRoom, ServerNode}, 
    InitialState = #user_state{port = Port, server = Server},
    client_loop(InitialState).

post(Command, Data, State) -> 
    Server = State#user_state.server,
    Server ! {self(), Command, Data},
    State. 

client_loop(State) -> 
    
    receive
        {Port, {data, EncodedData}} -> 
            {Command, Data} = binary_to_term(EncodedData),
            client_send(Command, Data, State)
        {Pid, Command, Msg} -> 
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
    Port ! term_to_binary({Pid, Command, Msg}),
    ok.
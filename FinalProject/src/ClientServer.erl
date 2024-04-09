-module(client_server).
-behaviour(gen_server).

%% API
-export([start/1, stop/1, start_link/1]).
-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2, code_change/3]).
-record(state, {users}).


%%% CLIENT FUNCTIONS %%% 
join_game() -> ok. 

send_input(Server, Input) -> 
    gen_server:cast(Server, {input, Input}).

%%% SERVER FUNCTIONS %%%
stop(Name) ->
    gen_server:call(Name, stop).

start_link(Name) ->
    gen_server:start_link({local, Name}, ?MODULE, [], []).

init(_Args) ->
    {ok, #state{users = []}}.

%%% BROADCAST %%%
broadcastAll([Info | Rest], Users) -> 
    broadcast(Info, Users),
    broadcastAll(Rest, Users);
broadcastAll([], Users) -> 
    ok.  

broadcast(Information, [User | Users]) -> 
    User ! Information,
    broadcast(Information, Users);
broadcast(Information, []) -> 
    ok. 

%%% HANDLE CALL %%%
handle_call(stop, _From, State) ->
    {stop, normal, stopped, State};
handle_call(_Request, _From, State) ->
    {reply, ok, State}.

%%% HANDLE CAST %%%
handle_cast(_Msg, State) ->
    {noreply, State}.

%%% HANDLE OTHER %%%
handle_info(_Info, State) ->
    {noreply, State}.

%%% END %%%
terminate(_Reason, _State) ->
    ok.

%%% CODE CHANGE %%%
code_change(_OldVsn, State, _Extra) ->
    {ok, State}.

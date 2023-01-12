# GameNegotiatorServer
Server for game-negotiator
-----------------------------

Highly WIP;
The server-side of a tool for negotiating games between friends. The users download a client, which registers a url protocol.
Through a web interface those users can then click a url with a token included in its parameters.
The client on each users machine scans for games that are owned, *and* installed. This MVP only supports steam.
The client then sends this back to the server, which displays to all users a list of games, sorted by number of people who have them installed.

I had this idea to help me and my pals decide on games that we all had, on the fly. This is difficult because all of the various launchers make it difficult
to get an accurate list of games you have in common with other users.

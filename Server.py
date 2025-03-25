import socket
import select
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(5)
open_client_sockets = []

rPos = [4, 8]
bPos = [4, 0]
turn = 1
connected = True
won1 = False
won2 = False
move = "nothing"
player1 = server_socket
player2 = server_socket

while True:
    rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            if len(open_client_sockets) < 2:

                rPos = [4, 8]
                bPos = [4, 0]
                turn = 1
                connected = True
                move = "nothing"

                if len(open_client_sockets) == 0:
                    won1 = False
                    won2 = False
                    open_client_sockets.append(new_socket)
                    player1 = new_socket
                    new_socket.send("1")
                else:
                    open_client_sockets.append(new_socket)
                    player2 = new_socket
                    new_socket.send("2")
            else:
                new_socket.send("failed")
        else:
            data = current_socket.recv(1024)

            if data == "both?":
                if len(open_client_sockets) == 2:
                    current_socket.send("yes")
                else:
                    current_socket.send("no")
            else:
                if current_socket == player1:

                    if data == "turn?":
                        if won1 == True:
                            current_socket.send("Won")
                        elif won2 == True:
                            current_socket.send("Lost")
                        elif connected == False:
                            current_socket.send("quit")
                        elif turn == 1:
                            current_socket.send(move)
                        else:
                            current_socket.send("no")
                    else:
                        if data == "":
                            connected = False
                            open_client_sockets.remove(current_socket)
                            current_socket.close()

                        elif data == "0-1":
                            rPos[0] -= 1
                        elif data == "0+1":
                            rPos[0] += 1
                        elif data == "1-1":
                            rPos[1] -= 1
                        elif data == "1+1":
                            rPos[1] += 1

                        if rPos[1] == 0:
                            won1 = True
                            #open_client_sockets.remove(current_socket)
                            #current_socket.close()

                        turn = 2
                        move = data

                elif current_socket == player2:

                    if data == "turn?":
                        if won1 == True:
                            current_socket.send("Lost")
                        elif won2 == True:
                            current_socket.send("Won")
                        elif connected == False:
                            current_socket.send("quit")
                        elif turn == 2:
                            current_socket.send(move)
                        else:
                            current_socket.send("no")
                    else:
                        if data == "":
                            connected = False
                            open_client_sockets.remove(current_socket)
                            current_socket.close()

                        elif data == "0-1":
                            bPos[0] -= 1
                        elif data == "0+1":
                            bPos[0] += 1
                        elif data == "1-1":
                            bPos[1] -= 1
                        elif data == "1+1":
                            bPos[1] += 1

                        if bPos[1] == 8:
                            won2 = True
                            #open_client_sockets.remove(current_socket)
                            #current_socket.close()

                        turn = 1
                        move = data

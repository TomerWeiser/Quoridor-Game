import pygame
import socket
import time


pygame.init()

#colors

white = (255, 255, 255)
black = (0, 0, 0)
red = (225, 0, 0)
green = (0, 155, 0)
blue = (0, 0, 255)
lightBlue = (100, 255, 255)
brown = (128, 64, 0)

#screen size

width = 1000
height = 820

#pictures

background = pygame.image.load('Background.png')
instructions = pygame.image.load('instructions.png')
EnglishInstructions = pygame.image.load('Englishinstructions.png')
keys = pygame.image.load('keys.png')
EnglishKeys = pygame.image.load('Englishkeys.png')
board = pygame.image.load('Board.png')
PlayerR = pygame.image.load('RedSoldier.png')
PlayerB = pygame.image.load('BlueSoldier.png')
BothPlayers = pygame.image.load('BothPlayers.png')
HoriWall = pygame.image.load('HorizontalStick.png')
VertiWall = pygame.image.load('VerticalStick.png')

#sounds

MoveSound = pygame.mixer.Sound("move.wav")
WallSound = pygame.mixer.Sound("wall.wav")
WinSound = pygame.mixer.Sound("win.wav")
LoseSound = pygame.mixer.Sound("lose.wav")
ErrorSound = pygame.mixer.Sound("error.wav")

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Quoridor: by Tomer Weiser")

icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

#fonts

SmallGameFont = pygame.font.SysFont("Arial Black", 28)
BigGameFont = pygame.font.SysFont("Arial Black", 40)
SmallFont = pygame.font.SysFont("Tahoma", 50)
BigFont = pygame.font.SysFont("Tahoma", 100)


def Message(msg, color, yChange=0, size="small", xChange=0):
    if size == "small":
        text = SmallFont.render(msg, True, color)
    elif size == "big":
        text = BigFont.render(msg, True, color)
    elif size == "bigGame":
        text = BigGameFont.render(msg, True, color)
    elif size == "smallGame":
        text = SmallGameFont.render(msg, True, color)
    textRect = text.get_rect()
    textRect.center = (width / 2) + xChange, (height / 2) + yChange     #center of the screen + changes
    screen.blit(text, textRect)         #(the msg with the font, where to place it)


def Instructions():
    done = False
    lang = "h"
    part = "i"
    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_h:
                    lang = "h"
                if event.key == pygame.K_e:
                    lang = "e"
                if event.key == pygame.K_i:
                    part = "i"
                if event.key == pygame.K_k:
                    part = "k"

        screen.blit(background, (0, 0))
        Message("Instructions", black, -350, "big")
        Message("__________", black, -340, "big")
        Message("Press Esc to go back", blue, 360, "small", 260)
        if lang == "h":
            Message("Press E for english", blue, -250, "small", -280)
            if part == "i":
                Message("Press K to see the keys", blue, 300, "small", -240)
                screen.blit(instructions, (150, 200))
            elif part == "k":
                Message("Press I to see the instructions", blue, 300, "small", -150)
                screen.blit(keys, (150, 200))
        elif lang == "e":
            Message("Press H for hebrew", blue, -250, "small", -280)
            if part == "i":
                Message("Press K to see the keys", blue, 300, "small", -240)
                screen.blit(EnglishInstructions, (150, 200))
            elif part == "k":
                Message("Press I to see the instructions", blue, 300, "small", -150)
                screen.blit(EnglishKeys, (150, 200))
        pygame.display.update()



def MainMenu():
    intro = True
    while intro == True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    intro = False
                if event.key == pygame.K_i:
                    Instructions()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.blit(background, (0, 0))
        Message("Quoridor", black, -250, "big")
        Message("Created By Tomer Weiser", black, -150)
        Message("Press P to play", blue, -25, "small", -300)
        Message("Press I for Instructions", blue, 75, "small", -212)
        Message("Press Q to quit", blue, 175, "small", -300)
        pygame.display.update()




xDifference = 80
yDifference = 78
LeftXLimit = 67
UpYLimit = 64
RightXLimit = LeftXLimit + xDifference*8
DownYLimit = UpYLimit + yDifference*8

clock = pygame.time.Clock()


def Free(player, Pos, HoriPos, VertiPos, count, BeenList):

    if count > 100:
        return False

    for place in BeenList:
        if place == Pos:
            return False

    BeenList.append(Pos)

    if player == "1":
        if Pos[1] == 0:
            return True
    elif player == "2":
        if Pos[1] == 8:
            return True

    backup1 = Pos[0]
    backup2 = Pos[1]
    ret = False
    CantMove = False
    if Pos[0] < 8:
        for i in VertiPos:
            if i[0] == Pos[0] and i[1] == Pos[1]:
                CantMove = True
                break
        if CantMove == False:
            temp = [0,0]
            temp[0] = backup1+1
            temp[1] = backup2
            ret = Free(player, temp, HoriPos, VertiPos, count+1, BeenList)

    CantMove = False
    if Pos[0] > 0:
        for i in VertiPos:
            if i[0] == Pos[0] - 1 and i[1] == Pos[1]:
                CantMove = True
                break
        if CantMove == False:
            temp = [0,0]
            temp[0] = backup1-1
            temp[1] = backup2
            ret = ret or Free(player, temp, HoriPos, VertiPos, count+1, BeenList)

    CantMove = False
    if Pos[1] > 0:
        for i in HoriPos:
            if i[0] == Pos[0] and i[1] == Pos[1] - 1:
                CantMove = True
                break
        if CantMove == False:
            temp = [0,0]
            temp[0] = backup1
            temp[1] = backup2-1
            ret = ret or Free(player, temp, HoriPos, VertiPos, count+1, BeenList)

    CantMove = False
    if Pos[1] < 8:
        for i in HoriPos:
            if i[0] == Pos[0] and i[1] == Pos[1]:
                CantMove = True
                break
        if CantMove == False:
            temp = [0,0]
            temp[0] = backup1
            temp[1] = backup2+1
            ret = ret or Free(player, temp, HoriPos, VertiPos, count+1, BeenList)

    return ret


def GameLoop():
    xDifference = 81
    yDifference = 78
    LeftXLimit = 67
    UpYLimit = 64
    RightXLimit = LeftXLimit + xDifference * 8
    DownYLimit = UpYLimit + yDifference * 8

    rPos = [4,8]
    bPos = [4,0]
    change = "0"
    Status = "stay"
    press = "nothing"
    walls = 10
    HoriList = []          #64 137
    VertiList = []         #144 60
    HoriPos = []
    VertiPos = []
    finish = False

    MainMenu()
    my_socket = socket.socket()
    my_socket.connect(('127.0.0.1', 8000))
    player = my_socket.recv(1024)
    if player == "failed":
        screen.blit(background, (0, 0))
        Message("Connection failed", red, 0, "big")
        Message("Press Q to exit", blue, 360, "small", 320)
        pygame.display.update()
        pygame.mixer.Sound.play(ErrorSound)
        while finish == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        finish = True
    turn = "1"
    if player == "1":
        screen.blit(background, (0, 0))
        Message("Finding Game...", black, 0, "big")
        Message("Press M to go back to the menu", blue, 360, "small", 125)
        pygame.display.update()
        data = "no"
        while data != "yes":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    my_socket.send("")
                    my_socket.close()
                    data = "yes"
                    finish = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        my_socket.send("")
                        my_socket.close()
                        data = "yes"
                        finish = True
                        press = "m"

            if not finish:
                my_socket.send("both?")
                data = my_socket.recv(1024)


    while not finish:

        rPosPix = [LeftXLimit + (xDifference * rPos[0]), UpYLimit + (yDifference * rPos[1])]
        bPosPix = [LeftXLimit + (xDifference * bPos[0]), UpYLimit + (yDifference * bPos[1])]
        screen.blit(board, (0, 0))
        if rPos[0] == bPos[0] and rPos[1] == bPos[1]:
            screen.blit(BothPlayers, (rPosPix[0], rPosPix[1]))
            pygame.display.update()
        else:
            screen.blit(PlayerR, (rPosPix[0], rPosPix[1]))
            screen.blit(PlayerB, (bPosPix[0], bPosPix[1]))
            pygame.display.update()
        if len(HoriList) > 0:
            for i in HoriList:
                screen.blit(HoriWall, (i[0], i[1]))
        if len(VertiList) > 0:
            for i in VertiList:
                screen.blit(VertiWall, (i[0], i[1]))

        if player == turn:
            if player == "1":
                Message("Your", red, -350, "bigGame", 420)
                Message("Turn", red, -300, "bigGame", 420)
            elif player == "2":
                Message("Your", lightBlue, -350, "bigGame", 420)
                Message("Turn", lightBlue, -300, "bigGame", 420)
            Message("Walls Left:", brown, -50, "smallGame", 417)
            Message(str(walls), brown, 0, "smallGame", 417)
            screen.blit(HoriWall, (835,460))
            screen.blit(VertiWall, (911, 500))
            pygame.display.update()

            defaultxx = 835
            defaultxy = 460
            defaultyx = 911
            defaultyy = 500
            HoriPressed = False
            VertiPressed = False
            HoriWallTurn = False
            VertiWallTurn = False

            Lastturn = turn
            while turn == Lastturn:

                my_socket.send("both?")
                data = my_socket.recv(1024)
                if data == "no":
                    screen.blit(background, (0, 0))
                    Message("Opponent Left", red, -50, "big")
                    Message("Press Q to quit or M to go back to the menu", blue, 75, "small")
                    press = "nothing"
                    pygame.display.update()
                    my_socket.send("")
                    my_socket.close()
                    while press == "nothing":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                press = "q"
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                    press = "q"
                                if event.key == pygame.K_m:
                                    press = "m"
                    finish = True
                    Lastturn = -999


                OnTopOfA = False
                OnTopOfB = False
                CantMove = False
                mx, my = pygame.mouse.get_pos()
                if HoriPressed == True:
                    screen.blit(board, (0, 0))
                    if rPos[0] == bPos[0] and rPos[1] == bPos[1]:
                        screen.blit(BothPlayers, (rPosPix[0], rPosPix[1]))
                        pygame.display.update()
                    else:
                        screen.blit(PlayerR, (rPosPix[0], rPosPix[1]))
                        screen.blit(PlayerB, (bPosPix[0], bPosPix[1]))
                        pygame.display.update()
                    if len(HoriList) > 0:
                        for i in HoriList:
                            screen.blit(HoriWall, (i[0], i[1]))
                    if len(VertiList) > 0:
                        for i in VertiList:
                            screen.blit(VertiWall, (i[0], i[1]))

                    if player == "1":
                        Message("Your", red, -350, "bigGame", 420)
                        Message("Turn", red, -300, "bigGame", 420)
                    elif player == "2":
                        Message("Your", lightBlue, -350, "bigGame", 420)
                        Message("Turn", lightBlue, -300, "bigGame", 420)
                    Message("Walls Left:", brown, -50, "smallGame", 417)
                    Message(str(walls), brown, 0, "smallGame", 417)
                    screen.blit(VertiWall, (911, 500))

                    screen.blit(HoriWall, (mx, my))
                    pygame.display.update()

                if VertiPressed == True:
                    screen.blit(board, (0, 0))
                    if rPos[0] == bPos[0] and rPos[1] == bPos[1]:
                        screen.blit(BothPlayers, (rPosPix[0], rPosPix[1]))
                        pygame.display.update()
                    else:
                        screen.blit(PlayerR, (rPosPix[0], rPosPix[1]))
                        screen.blit(PlayerB, (bPosPix[0], bPosPix[1]))
                        pygame.display.update()
                    if len(HoriList) > 0:
                        for i in HoriList:
                            screen.blit(HoriWall, (i[0], i[1]))
                    if len(VertiList) > 0:
                        for i in VertiList:
                            screen.blit(VertiWall, (i[0], i[1]))

                    if player == "1":
                        Message("Your", red, -350, "bigGame", 420)
                        Message("Turn", red, -300, "bigGame", 420)
                    elif player == "2":
                        Message("Your", lightBlue, -350, "bigGame", 420)
                        Message("Turn", lightBlue, -300, "bigGame", 420)
                    Message("Walls Left:", brown, -50, "smallGame", 417)
                    Message(str(walls), brown, 0, "smallGame", 417)
                    screen.blit(HoriWall, (835, 460))

                    screen.blit(VertiWall, (mx, my))
                    pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        my_socket.send("")
                        my_socket.close()
                        finish = True
                        Lastturn = -999

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if mx > (defaultxx - 5) and mx < (defaultxx + 165) and my > (defaultxy - 5) and my < (defaultxy + 9) and walls > 0:
                                HoriPressed = True
                        if mx > (defaultyx - 5) and mx < (defaultyx + 9) and my > (defaultyy - 5) and my < (defaultyy + 165) and walls > 0:
                                VertiPressed = True


                    if event.type == pygame.MOUSEBUTTONUP:
                        if HoriPressed == True or VertiPressed == True:
                            if HoriPressed == True:
                                HoriPressed = False
                                VertiPressed = False
                                for i in range(mx-10, mx+10):
                                    if (i-64) % xDifference == 0 and i >= 64 and i <= (64 + xDifference*7):
                                        for j in range(my-10, my+10):
                                            if (j-137) % yDifference == 0 and j >= 137 and j <= (60 + yDifference*8):
                                                for wall in HoriList:
                                                    if (i == wall[0] or i == (wall[0] + xDifference) or i == (wall[0] - xDifference)) and (j == wall[1]):
                                                        OnTopOfA = True
                                                        break
                                                for wall in VertiList:
                                                    if (i+xDifference == wall[0]+1) and (j+1 == wall[1]+yDifference):
                                                        OnTopOfB = True
                                                        break
                                                if OnTopOfA == False and OnTopOfB == False:
                                                    HoriPos.append([(i-64)/xDifference, (j-60)/yDifference])
                                                    HoriPos.append([1 + ((i-64)/xDifference), (j-60)/yDifference])
                                                    if Free("1", rPos, HoriPos, VertiPos, 0, []) and Free("2", bPos, HoriPos, VertiPos, 0, []):
                                                        HoriList.append([i, j])
                                                        pygame.mixer.Sound.play(WallSound)
                                                        HoriWallTurn = True
                                                        break
                                                    else:
                                                        del HoriPos[-1]
                                                        del HoriPos[-1]
                                        break

                                if HoriWallTurn == True:
                                    walls -= 1
                                    if turn == "1":
                                        turn = "2"
                                        change = "h," + str(HoriList[-1][0]) + "," + str(HoriList[-1][1])
                                    elif turn == "2":
                                        turn = "1"
                                        change = "h," + str(HoriList[-1][0]) + "," + str(HoriList[-1][1])

                                else:
                                    screen.blit(board, (0, 0))
                                    if rPos[0] == bPos[0] and rPos[1] == bPos[1]:
                                        screen.blit(BothPlayers, (rPosPix[0], rPosPix[1]))
                                        pygame.display.update()
                                    else:
                                        screen.blit(PlayerR, (rPosPix[0], rPosPix[1]))
                                        screen.blit(PlayerB, (bPosPix[0], bPosPix[1]))
                                        pygame.display.update()
                                    if len(HoriList) > 0:
                                        for i in HoriList:
                                            screen.blit(HoriWall, (i[0], i[1]))
                                    if len(VertiList) > 0:
                                        for i in VertiList:
                                            screen.blit(VertiWall, (i[0], i[1]))

                                    if player == "1":
                                        Message("Your", red, -350, "bigGame", 420)
                                        Message("Turn", red, -300, "bigGame", 420)
                                    elif player == "2":
                                        Message("Your", lightBlue, -350, "bigGame", 420)
                                        Message("Turn", lightBlue, -300, "bigGame", 420)
                                    Message("Walls Left:", brown, -50, "smallGame", 417)
                                    Message(str(walls), brown, 0, "smallGame", 417)
                                    screen.blit(VertiWall, (defaultyx, defaultyy))
                                    screen.blit(HoriWall, (defaultxx, defaultxy))
                                    pygame.display.update()

                            elif VertiPressed == True:
                                HoriPressed = False
                                VertiPressed = False
                                for i in range(mx-10, mx+10):
                                    if (i-144) % xDifference == 0 and i >= 144 and i <= (64 + xDifference*8):
                                        for j in range(my-10, my+10):
                                            if (j-60) % yDifference == 0 and j >= 60 and j <= (60 + yDifference*7):
                                                for wall in VertiList:
                                                    if (i == wall[0]) and (j == wall[1] or j == (wall[1] + yDifference) or j == (wall[1] - yDifference)):
                                                        OnTopOfA = True
                                                        break
                                                for wall in HoriList:
                                                    if (j+yDifference == wall[1]+1) and (i+1 == wall[0]+xDifference):
                                                        OnTopOfB = True
                                                        break
                                                if OnTopOfA == False and OnTopOfB == False:
                                                    VertiPos.append([(i-64)/xDifference, (j-60)/yDifference])
                                                    VertiPos.append([(i-64)/xDifference, 1 + ((j-60)/yDifference)])
                                                    if Free("1", rPos, HoriPos, VertiPos, 0, []) and Free("2", bPos, HoriPos, VertiPos, 0, []):
                                                        VertiList.append([i, j])
                                                        pygame.mixer.Sound.play(WallSound)
                                                        VertiWallTurn = True
                                                        break
                                                    else:
                                                        del VertiPos[-1]
                                                        del VertiPos[-1]
                                        break

                                if VertiWallTurn == True:
                                    walls -= 1
                                    if turn == "1":
                                        turn = "2"
                                        change = "v," + str(VertiList[-1][0]) + "," + str(VertiList[-1][1])
                                    elif turn == "2":
                                        turn = "1"
                                        change = "v," + str(VertiList[-1][0]) + "," + str(VertiList[-1][1])

                                else:
                                    screen.blit(board, (0, 0))
                                    if rPos[0] == bPos[0] and rPos[1] == bPos[1]:
                                        screen.blit(BothPlayers, (rPosPix[0], rPosPix[1]))
                                        pygame.display.update()
                                    else:
                                        screen.blit(PlayerR, (rPosPix[0], rPosPix[1]))
                                        screen.blit(PlayerB, (bPosPix[0], bPosPix[1]))
                                        pygame.display.update()
                                    if len(HoriList) > 0:
                                        for i in HoriList:
                                            screen.blit(HoriWall, (i[0], i[1]))
                                    if len(VertiList) > 0:
                                        for i in VertiList:
                                            screen.blit(VertiWall, (i[0], i[1]))

                                    if player == "1":
                                        Message("Your", red, -350, "bigGame", 420)
                                        Message("Turn", red, -300, "bigGame", 420)
                                    elif player == "2":
                                        Message("Your", lightBlue, -350, "bigGame", 420)
                                        Message("Turn", lightBlue, -300, "bigGame", 420)
                                    Message("Walls Left:", brown, -50, "smallGame", 417)
                                    Message(str(walls), brown, 0, "smallGame", 417)
                                    screen.blit(VertiWall, (defaultyx, defaultyy))
                                    screen.blit(HoriWall, (defaultxx, defaultxy))
                                    pygame.display.update()


                    if event.type == pygame.KEYDOWN:
                        if turn == "1":
                            if event.key == pygame.K_UP and rPos[1] > 0:
                                for i in HoriPos:
                                    if i[0] == rPos[0] and i[1] == rPos[1]-1:
                                        CantMove = True
                                        break
                                if CantMove == False:
                                    rPos[1] -= 1
                                    pygame.mixer.Sound.play(MoveSound)
                                    turn = "2"
                                    change = "1-1"
                            elif event.key == pygame.K_DOWN and rPos[1] < 8:
                                for i in HoriPos:
                                    if i[0] == rPos[0] and i[1] == rPos[1]:
                                        CantMove = True
                                        break
                                if CantMove == False:
                                    rPos[1] += 1
                                    pygame.mixer.Sound.play(MoveSound)
                                    turn = "2"
                                    change = "1+1"
                            elif event.key == pygame.K_LEFT and rPos[0] > 0:
                                for i in VertiPos:
                                    if i[0] == rPos[0] - 1 and i[1] == rPos[1]:
                                        CantMove = True
                                        break
                                if CantMove == False:
                                    rPos[0] -= 1
                                    pygame.mixer.Sound.play(MoveSound)
                                    turn = "2"
                                    change = "0-1"
                            elif event.key == pygame.K_RIGHT and rPos[0] < 8:
                                for i in VertiPos:
                                    if i[0] == rPos[0] and i[1] == rPos[1]:
                                        CantMove = True
                                        break
                                if CantMove == False:
                                    rPos[0] += 1
                                    pygame.mixer.Sound.play(MoveSound)
                                    turn = "2"
                                    change = "0+1"

                        elif turn == "2":
                            if event.key == pygame.K_UP and bPos[1] > 0:
                                for i in HoriPos:
                                    if i[0] == bPos[0] and i[1] == bPos[1]-1:
                                        CantMove = True
                                        break
                                if CantMove == False:
                                    bPos[1] -= 1
                                    pygame.mixer.Sound.play(MoveSound)
                                    turn = "1"
                                    change = "1-1"
                            elif event.key == pygame.K_DOWN and bPos[1] < 8:
                                for i in HoriPos:
                                    if i[0] == bPos[0] and i[1] == bPos[1]:
                                        CantMove = True
                                        break
                                if CantMove == False:
                                    bPos[1] += 1
                                    pygame.mixer.Sound.play(MoveSound)
                                    turn = "1"
                                    change = "1+1"
                            elif event.key == pygame.K_LEFT and bPos[0] > 0:
                                for i in VertiPos:
                                    if i[0] == bPos[0] - 1 and i[1] == bPos[1]:
                                        CantMove = True
                                        break
                                if CantMove == False:
                                    bPos[0] -= 1
                                    pygame.mixer.Sound.play(MoveSound)
                                    turn = "1"
                                    change = "0-1"
                            elif event.key == pygame.K_RIGHT and bPos[0] < 8:
                                for i in VertiPos:
                                    if i[0] == bPos[0] and i[1] == bPos[1]:
                                        CantMove = True
                                        break
                                if CantMove == False:
                                    bPos[0] += 1
                                    pygame.mixer.Sound.play(MoveSound)
                                    turn = "1"
                                    change = "0+1"

                if turn != Lastturn and Lastturn != -999:
                    my_socket.send(change)

        else:
            if player == "1":
                Message("Opponent's", red, -350, "smallGame", 415)
                Message("Turn", red, -300, "smallGame", 415)
            elif player == "2":
                Message("Opponent's", lightBlue, -350, "smallGame", 415)
                Message("Turn", lightBlue, -300, "smallGame", 415)
            Message("Walls Left:", brown, -50, "smallGame", 417)
            Message(str(walls), brown, 0, "smallGame", 417)
            pygame.display.update()
            data = "no"
            while data == "no":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        finish = True
                        Status = "leave"
                        data = "leave"
                        my_socket.send("")
                        my_socket.close()
                        #screen.blit(background, (0, 0))
                        #Message("See you next time", green, 0, "big")
                        #pygame.display.update()
                if not finish:
                    my_socket.send("turn?")
                    data = my_socket.recv(1024)


            if Status != "leave":
                if data == "quit":
                    screen.blit(background, (0, 0))
                    Message("Opponent Left", red, -50, "big")
                    Message("Press Q to quit or M to go back to the menu", blue, 75, "small")
                    pygame.mixer.Sound.play(ErrorSound)
                    press = "nothing"
                    pygame.display.update()
                    my_socket.send("")
                    my_socket.close()
                    while press == "nothing":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                press = "q"
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                    press = "q"
                                if event.key == pygame.K_m:
                                    press = "m"
                    finish = True

                elif data == "Won":
                    screen.blit(background, (0, 0))
                    Message("You Win!!!", green, -50, "big")
                    Message("Press Q to quit or M to go back to the menu", blue, 75, "small")
                    pygame.mixer.Sound.play(WinSound)
                    press = "nothing"
                    pygame.display.update()
                    my_socket.send("")
                    my_socket.close()
                    while press == "nothing":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                press = "q"
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                    press = "q"
                                if event.key == pygame.K_m:
                                    press = "m"
                    finish = True

                elif data == "Lost":
                    screen.blit(background, (0, 0))
                    Message("You Lose...", red, -50, "big")
                    Message("Press Q to quit or M to go back to the menu", blue, 75, "small")
                    pygame.mixer.Sound.play(LoseSound)
                    press = "nothing"
                    pygame.display.update()
                    my_socket.send("")
                    my_socket.close()
                    while press == "nothing":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                press = "q"
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                    press = "q"
                                if event.key == pygame.K_m:
                                    press = "m"
                    finish = True

                else:
                    if player == "1":
                        LastPos = [0,0]
                        LastPos[0] = bPos[0]
                        LastPos[1] = bPos[1]
                        turn = "1"
                        if data == "0-1":
                            bPos[0] -= 1
                        elif data == "0+1":
                            bPos[0] += 1
                        elif data == "1-1":
                            bPos[1] -= 1
                        elif data == "1+1":
                            bPos[1] += 1
                        else:
                            pygame.mixer.Sound.play(WallSound)
                            value = data.split(",")
                            i = int(value[1])
                            j = int(value[2])
                            if value[0] == "h":
                                HoriList.append([i, j])
                                HoriPos.append([(i - 64) / xDifference, (j - 60) / yDifference])
                                HoriPos.append([1 + ((i - 64) / xDifference), (j - 60) / yDifference])
                            elif value[0] == "v":
                                VertiList.append([i, j])
                                VertiPos.append([(i - 64) / xDifference, (j - 60) / yDifference])
                                VertiPos.append([(i - 64) / xDifference, 1 + ((j - 60) / yDifference)])

                        if LastPos[0] != bPos[0] or LastPos[1] != bPos[1]:
                            pygame.mixer.Sound.play(MoveSound)

                    elif player == "2":
                        LastPos = [0,0]
                        LastPos[0] = rPos[0]
                        LastPos[1] = rPos[1]
                        turn = "2"
                        if data == "0-1":
                            rPos[0] -= 1
                        elif data == "0+1":
                            rPos[0] += 1
                        elif data == "1-1":
                            rPos[1] -= 1
                        elif data == "1+1":
                            rPos[1] += 1
                        else:
                            pygame.mixer.Sound.play(WallSound)
                            value = data.split(",")
                            i = int(value[1])
                            j = int(value[2])
                            if value[0] == "h":
                                HoriList.append([i, j])
                                HoriPos.append([(i - 64) / xDifference, (j - 60) / yDifference])
                                HoriPos.append([1 + ((i - 64) / xDifference), (j - 60) / yDifference])
                            elif value[0] == "v":
                                VertiList.append([i, j])
                                VertiPos.append([(i - 64) / xDifference, (j - 60) / yDifference])
                                VertiPos.append([(i - 64) / xDifference, 1 + ((j - 60) / yDifference)])

                        if LastPos[0] != rPos[0] or LastPos[1] != rPos[1]:
                            pygame.mixer.Sound.play(MoveSound)

    if press == "m":
        GameLoop()

    pygame.quit()
    quit()


GameLoop()
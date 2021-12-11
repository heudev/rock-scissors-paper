import random
import threading
import time


class tkmgame():
    player1 = None
    player2 = None
    currentplayer = None
    score = [0, 0]
    finishgame = False
    player1history = []
    player2history = []
    message = None
    gamemessage = None
    gameplaying = False
    thread = None
    thread2 = None
    exit_flag = False
    isexitdone = False
    resetbythread = False

    def timeoutcheck(self):
        while True:
            if self.exit_flag:
                self.isexitdone = True
                break
            historylen = len(self.player1history) + len(self.player2history)
            print("historylen:", historylen)
            time.sleep(180)
            print("ikincilen:", len(self.player1history) +
                  len(self.player2history))
            if len(self.player1history) + len(self.player2history) == historylen:
                self.resetbythread = True
                self.reset()
                print("Game reset")

    def timeout(self, status):
        if status == "start":
            self.exit_flag = False
            self.isexitdone = False
            self.thread = None
            if self.thread == None:
                self.thread = threading.Thread(target=self.timeoutcheck)
                if self.thread.is_alive() == False:
                    self.thread.start()
                    print("thread starting", self.thread.is_alive())
        if status == "stop":
            self.exit_flag = True

    def control(self):
        while True:
            time.sleep(1)
            if self.isexitdone:
                self.thread.join()
                print("thread:", self.thread.is_alive())
                self.exit_flag = False
                self.isexitdone = False
                self.thread = None

    def controlthread(self):
        if self.thread2 == None:
            self.thread2 = threading.Thread(target=self.control)
            self.thread2.start()

    def reset(self):
        self.player1 = None
        self.player2 = None
        self.currentplayer = None
        self.score = [0, 0]
        self.finishgame = False
        self.player1history = []
        self.player2history = []
        self.gamemessage = None
        self.timeout("stop")
        if self.resetbythread == False:
            self.setmessage("Game reset successful")
        self.resetbythread = False

    def getmessage(self):
        if self.message:
            keepmessage = self.message
            self.message = None
            return keepmessage

    def setmessage(self, value):
        self.message = value

    def getgamemessage(self):
        if self.gamemessage:
            keepmessage = self.gamemessage
            self.gamemessage = None
            return keepmessage

    def setgamemessage(self, value):
        self.gamemessage = value

    def tkmrandom(self):
        tkm = ["tas", "kagit", "makas"]
        return random.choice(tkm)

    def tkmcalculate(self, arg1, arg2):
        if arg1 == "tas" and arg2 == "tas":
            return "beraber"
        if arg1 == "tas" and arg2 == "kagit":
            return "player2"
        if arg1 == "tas" and arg2 == "makas":
            return "player1"
        if arg1 == "kagit" and arg2 == "tas":
            return "player1"
        if arg1 == "kagit" and arg2 == "kagit":
            return "beraber"
        if arg1 == "kagit" and arg2 == "makas":
            return "player2"
        if arg1 == "makas" and arg2 == "tas":
            return "player2"
        if arg1 == "makas" and arg2 == "kagit":
            return "player1"
        if arg1 == "makas" and arg2 == "makas":
            return "beraber"

    def scorecalculator(self):
        player1score = 0
        player2score = 0
        if len(self.player1history) == len(self.player2history):
            for player1, player2 in zip(self.player1history, self.player2history):
                result = self.tkmcalculate(player1, player2)
                if result == "player1":
                    player1score += 1
                if result == "player2":
                    player2score += 1
            self.score = [player1score, player2score]

    def startgame(self, player1, player2):
        if self.player1 and self.player2:
            self.setmessage("The game has already started")
            return
        self.player1 = player1
        self.player2 = player2
        self.currentplayer = random.choice([player1, player2])
        self.setgamemessage({
            "player1": player1,
            "player2": player2,
            "currentplayer": self.currentplayer
        })
        self.timeout("start")
        self.controlthread()

    def game(self, author):
        if self.player1 == None or self.player2 == None:
            self.setmessage("Please start game")
            return
        if author != self.player1 and author != self.player2:
            self.setmessage("You are not player")
            return

        if self.currentplayer == author:
            tkm = self.tkmrandom()
            if self.player1 == author:
                self.player1history.append(tkm)
                self.currentplayer = self.player2

            if self.player2 == author:
                self.player2history.append(tkm)
                self.currentplayer = self.player1

            self.scorecalculator()
            self.setgamemessage({
                "tkm": tkm,
                "score": self.score,
                "player1": self.player1,
                "player2": self.player2,
                "player1history": self.player1history,
                "player2history": self.player2history,
                "nextplayer": self.currentplayer
            })
        else:
            self.setmessage("You are not next player")
            return

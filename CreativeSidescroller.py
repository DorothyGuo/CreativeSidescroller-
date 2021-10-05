#################################################
# hw9.py
#
# Your name: Xiqiao Guo
# Your andrew id: xiqiaog
#################################################

import cs112_f19_week9_linter
from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import random

#################################################
# Bird Class and Subclasses
#################################################
class Bird(object):
    isMigrating = False

    @staticmethod
    def startMigrating():
        Bird.isMigrating = True
    
    @staticmethod
    def stopMigrating():
        Bird.isMigrating = False

    def __init__(self, species):
        self.species = species
        self.eggs = 0
    
    def fly(self):
        return "I can fly!"
    
    def countEggs(self):
        return self.eggs
    
    def layEgg(self):
        self.eggs += 1
    
    def __repr__(self):
        if self.eggs == 1:
            return f"{self.species} has {self.eggs} egg"
        else:
            return f"{self.species} has {self.eggs} eggs"
    
    def __eq__(self, other):
        return (isinstance(other, Bird) and (self.species == other.species))
    
    def __hash__(self):
        return hash(self.species)

class Penguin(Bird):
    def fly(self):
        return "No flying for me."
    
    def swim(self):
        return "I can swim!"

class MessengerBird(Bird):
    def __init__(self, species, message):
        super().__init__(species)
        self.message = message
    
    def deliverMessage(self):
        return self.message


#################################################
# runCreativeSidescroller
#################################################
# ignore_rest (The autograder ignores all code below here)
def runCreativeSidescroller():

    # This is the class that stores the player information
    class Player(object):
        def __init__(self, app):
            self.app = app
            self.spriteSheet = None
            self.loadPlayer("Left")
            self.playerWidth = self.spriteSheet[0].width
            self.playerHeight = self.spriteSheet[0].height
            self.playerX = self.app.width/2
            self.playerY = self.app.height - self.playerHeight
        
        # load the spritesheet of the player (left and right)
        def loadPlayer(self, direction):
            url = ("https://i.imgur.com/P81nSXL.png")
            spritestrip = self.app.loadImage(url)
            self.spriteSheet = []
            for i in range(3):
                if direction == "Left":
                    sprite = spritestrip.crop((5+50*i, 77, 35+50*i, 103))
                    scaledSprite = self.app.scaleImage(sprite, 2)
                    self.spriteSheet.append(scaledSprite)
                if direction == "Right":
                    sprite = spritestrip.crop((5+50*i, 121, 35+50*i, 154))
                    scaledSprite = self.app.scaleImage(sprite, 2)
                    self.spriteSheet.append(scaledSprite)

        def movePlayer(self):
            self.playerX += self.app.dx

    # This is the superclass of all classes that store the information of 
    # different falling pieces in the game
    class DroppingPieces(object):
        def __init__(self, app):
            self.app = app
            self.url = None
            self.pieceX = random.randint(-100, 600)
            self.pieceY = 0   # Top

        def __eq__(self, other):
            return (isinstance(other, DroppingPieces) and 
                    self.url == other.url)
        
        def __hash__(self):
            return hash(self.url)

        def loadPiece(self, scale):
            rawImage = self.app.loadImage(self.url)
            scaledImage = self.app.scaleImage(rawImage, scale)
            return scaledImage

        def dropPiece(self):
            self.pieceY += 10

    # The following four classes (Cake, chocolateCake, poison, fastPoison)
    # store the information like score, message, image, etc of different pieces
    class Cake(DroppingPieces):
        def __init__(self, app):
            super().__init__(app)
            url1 = "https://i.imgur.com/JL8TL4b.png"
            url2 = "https://i.imgur.com/6XW7qYB.png"
            url3 = "https://i.imgur.com/LK7RkLE.png"
            url4 = "https://i.imgur.com/0vSDP2E.png"
            self.url = random.choice([url1, url2, url3, url4])
            self.image = self.loadPiece(1/15)
            self.message = "tasty!"
            self.score = +1

    class chocolateCake(DroppingPieces):
        def __init__(self, app):
            super().__init__(app)
            self.url = "https://i.imgur.com/H4QgaZH.png"
            self.image = self.loadPiece(1/5)
            self.message = "Yummy!"
            self.score = +3

        # place the cake randomly on the screen
        def dropPiece(self):
            self.pieceX = random.randint(-100, 600)
            self.pieceY = random.randint(0, 400)

    class Poison(DroppingPieces):
        def __init__(self, app):
            super().__init__(app)
            url1 = "https://i.imgur.com/hWF2hkh.png"
            url2 = "https://i.imgur.com/Kxr0S8F.png"
            url3 = "https://i.imgur.com/FBq06d8.png"
            url4 = "https://i.imgur.com/ZAHnQFl.png"
            self.url = random.choice([url1, url2, url3, url4])
            if self.url == url2: scale = 1/5
            elif self.url == url3: scale = 1/5
            else: scale = 1/15
            self.image = self.loadPiece(scale)
            self.message = "oops!"
            self.score = -1

    class fastPoison(Poison):
        def __init__(self, app):
            super().__init__(app)
            self.score = -2
        
        def dropPiece(self):
            self.pieceY += 20
            
    # game modes
    # This is the starting screen of the game
    class SplashScreenMode(Mode):
        def appStarted(mode):
            url = "https://i.imgur.com/KXY9C9J.png"
            image = mode.loadImage(url)
            scaledImage = image.resize((500, 400))
            mode.image = scaledImage

        def redrawAll(mode, canvas):
            canvas.create_image(mode.width/2, mode.height/2, 
                                image=ImageTk.PhotoImage(mode.image))
            font = "Arial 20 bold"
            textMessage = '''
            Welcome to the game 'Eat or Die'! 
            In this game, move the player (with right or 
            left arrow)to catch the cake and avoid the 
            poison.
            Chocolate cake is a special food that you should 
            drag to the player if it appears (It's yummy!) 
            You can always press 'h' for help. Now, press any
            key to start the game!
            '''
            canvas.create_text(mode.width/2-20, mode.height/2, 
                                text=textMessage, font=font)

        # switch to gamemode
        def keyPressed(mode, event):
            mode.app.setActiveMode(mode.app.gameMode)

    # This is the major part of the game
    class GameMode(Mode):
        def appStarted(mode):
            mode.score = 0
            mode.dx = 0
            mode.dy = 0
            mode.player = Player(mode)
            mode.gameOver = False
            mode.scrollX = 0
            mode.scrollMargin = 50
            mode.pieceSet = set()
            mode.pieceList = []
            mode.initPiece()
            mode.drag = False
            mode.message = None
            mode.timeCounter = 0
            mode.cursorCx = mode.width/2
            mode.cursorCy = mode.height/2
            url1 = "https://i.imgur.com/kye5T9c.png"
            mode.gameOverImage = mode.loadImage(url1)
            url2 = "https://i.imgur.com/0E0kefS.png"
            cursorRawImage = mode.loadImage(url2)
            mode.cursorImage = mode.scaleImage(cursorRawImage, 1/8)
            url3 = "https://i.imgur.com/GlKrRbE.png"
            backgroundRawImage = mode.loadImage(url3)
            mode.backgroundImage = backgroundRawImage.resize((500, 400))

        def initPiece(mode):
            for i in range(2):
                cake1 = Cake(mode)
                cake2 = Cake(mode)
            while mode.checkIntersection(cake1, cake2):
                cake2 = Cake(mode)
            mode.pieceList.append(cake1)
            mode.pieceList.append(cake2)
            poison = Poison(mode)
            mode.pieceList.append(poison)

        # move the player, gethelp, get superhelp 
        def keyPressed(mode, event):
            if event.key == "Left":
                mode.player.loadPlayer("Left") # return a spritesheet 
                mode.dx = -5 
                mode.player.movePlayer()
            elif event.key == "Right":
                mode.player.loadPlayer("Right")
                mode.dx = +5
                mode.player.movePlayer()
            elif event.key == "h":
                mode.app.setActiveMode(mode.app.helpMode)
            elif event.key == "S":
                mode.doSuperHelp()
            # if out of scrollMargin, scroll the screen
            if ((mode.player.playerX <= mode.scrollMargin) or
                (mode.player.playerX >= mode.width-mode.scrollMargin)):
                mode.scrollX += mode.dx
        
        def doSuperHelp(mode):
            helpMessage = '''
            To play the game, simply move the player than pressing left or 
            right arrow. Try to catch the cake and avoid the poison. Get help 
            by pressing 'h'. Catching the cake gets you 1 point and catching 
            the chocolatecake gets you 3 points. Crashing into poison gets you
            1 point away and crashing into fastpoison gets you 2 points away. 
            If your score is negative or passes 20, the game is over. 
            '''
            print(helpMessage)
        
        # used to detect whether the user presses the chocolatecake
        def mousePressed(mode, event):
            if mode.pressInCake(event.x, event.y):
                mode.drag = True
                    
        # check whether the user presses inside the chocolatecake
        def pressInCake(mode, x, y):
            for piece in mode.pieceList:
                if type(piece) == chocolateCake:
                    (x0, y0, x1, y1) = mode.getObjectBound(piece)
            if ((x0 <= x) and (x <= x1) and (y >= y0) and (y <= y1)):
                return True
            else: return False
        
        # drag the chocolatecake to the player
        def mouseDragged(mode, event):
            if mode.drag:
                for piece in mode.pieceList:
                    if type(piece) == chocolateCake:
                        piece.pieceX = event.x
                        piece.pieceY = event.y

        # keep the player on the screen if necessary
        def makePlayerVisible(mode):
            x = mode.player.playerX
            if (x < mode.scrollX + mode.scrollMargin):
                mode.scrollX = x - mode.scrollMargin
            if (x > mode.scrollX + mode.width - mode.scrollMargin):
                mode.scrollX = x - mode.width + mode.scrollMargin
            
        # move the cursor following the real cursor
        def mouseMoved(mode, event):
            mode.cursorCx = event.x
            mode.cursorCy = event.y

        def timerFired(mode):
            mode.timeCounter += 1
            if not mode.gameOver:
                mode.makePlayerVisible
                mode.message = None
                mode.operatePiece()
                mode.makeNewPiece()
                mode.countScore()
                if mode.score >= 20:
                    mode.gameOver = True
        
        # initiate new falling pieces at different time
        def makeNewPiece(mode):
            if mode.timeCounter % 50 == 0:
                cake = Cake(mode)
                poison = Poison(mode)
                # avoid intersection
                while mode.checkIntersection(cake, poison):
                    cake = Cake(mode)
                mode.pieceList.append(cake)
                mode.pieceList.append(poison)
            if mode.timeCounter % 100 == 0:
                chocolatecake = chocolateCake(mode)
                fastpoison = fastPoison(mode)
                # avoid intersection
                while mode.checkIntersection(chocolatecake, fastpoison):
                    chocolatecake = chocolateCake(mode)
                mode.pieceList.append(chocolatecake)
                mode.pieceList.append(fastpoison)
        
        # make the pieces falling
        def operatePiece(mode):
            for piece in mode.pieceList:
                if type(piece) != chocolateCake:
                    piece.dropPiece()
                elif mode.timeCounter % 100 == 0:
                    piece.dropPiece()
                if piece.pieceY >= 800:
                    mode.pieceList.remove(piece)

        # check whether the user catches the cake or crashes into the poison,
        # and change the score accrodingly
        def countScore(mode):
            for piece in mode.pieceList:
                if mode.checkIntersection(mode.player, piece):
                    mode.score += piece.score
                    mode.pieceSet.add(piece)
                    mode.pieceList.remove(piece)
                if mode.score < 0:
                    mode.gameOver = True

        # Copied from: http://www.cs.cmu.edu/~112/notes/notes-
        # animations-part2.html#loadImageUsingUrl
        def checkIntersection(mode, object1, object2):
            (ax0, ay0, ax1, ay1) = mode.getObjectBound(object1)
            (bx0, by0, bx1, by1) = mode.getObjectBound(object2) # piece
            if ((ax1 >= bx0) and (bx1 >= ax0) and
                (ay1 >= by0) and (by1 >= ay0)):
                if type(object1) == Player:
                    # used to print the message carried by the pieces later
                    mode.message = object2.message
                return True
            else: return False
        
        # since Player is not the subclass of DroppingPieces, check 
        # independently
        def getObjectBound(mode, target):
            if  type(target) == Player:
                x0 = mode.player.playerX
                y0 = mode.player.playerY
                x1 = x0 + mode.player.playerWidth
                y1 = y0 + mode.player.playerHeight
            else:
                x0 = target.pieceX
                y0 = target.pieceY
                x1 = x0 + target.image.width
                y1 = y0 + target.image.height  
            return (x0, y0, x1, y1)        

        def redrawAll(mode, canvas):
            # draw the background
            canvas.create_image(mode.width/2, mode.height/2, 
                                image=ImageTk.PhotoImage(mode.backgroundImage))
            # draw pieces
            sx = mode.scrollX
            for piece in mode.pieceList:
                canvas.create_image(piece.pieceX + piece.image.width//2-sx, 
                                    piece.pieceY + piece.image.height//2,
                                    image=ImageTk.PhotoImage(piece.image))
            # draw player
            sprite = mode.player.spriteSheet[(mode.timeCounter % 3)] 
            cx = mode.player.playerX + mode.player.playerWidth//2
            cy = mode.player.playerY + mode.player.playerHeight//2
            canvas.create_image(cx-sx, cy, image=ImageTk.PhotoImage(sprite))
            # draw the score
            canvas.create_text(mode.width/2, 20, text=f"Score: {mode.score}", 
                                font="Arial 20")
            # draw the cursor
            canvas.create_image(mode.cursorCx, mode.cursorCy, 
                                image=ImageTk.PhotoImage(mode.cursorImage))
            # draw the message if message != None
            if mode.message != None:
                canvas.create_text(mode.width/2, 100, text=mode.message,
                                    font="Futura 20 bold", fill="deep pink")
            # draw the gameover screen. Display the pieces touched by the 
            # player
            if mode.gameOver:
                image = mode.gameOverImage
                canvas.create_image(mode.width/2, mode.height/2, 
                                    image=ImageTk.PhotoImage(image))
                interval = mode.width/len(mode.pieceSet)
                i = 0
                for piece in mode.pieceSet:
                    image = piece.image
                    canvas.create_image(50+i*interval, mode.height/2,
                                    image=ImageTk.PhotoImage(image))
                    i += 1

    class HelpMode(Mode):
        def appStarted(mode):
            url = "https://i.imgur.com/IASrFrQ.png"
            image = mode.loadImage(url)
            scaledImage = image.resize((500, 400))
            mode.image = scaledImage

        def redrawAll(mode, canvas):
            canvas.create_image(mode.width/2, mode.height/2, 
                                image=ImageTk.PhotoImage(mode.image))
            font="Arial 20 bold"
            textMessage = ''' 
            Hi! This is the help screen.
            To win the game, try to catch as much food as 
            possible and keep an eye on the poison!
            Also, pay attention to any cookie, which can earn 
            you more scores than cakes. Good luck!
            '''
            canvas.create_text(mode.width/2-20, mode.height/2, 
                                text=textMessage, font=font)

        def keyPressed(mode, event):
            mode.app.setActiveMode(mode.app.gameMode)

    class MyModalApp(ModalApp):
        def appStarted(app):
            app.splashMode = SplashScreenMode()
            app.gameMode = GameMode()
            app.helpMode = HelpMode()
            app.setActiveMode(app.splashMode)
            app.timerDelay = 300
        

    app = MyModalApp(width=500, height=400)

#################################################
# Test Functions
#################################################
def getLocalMethods(clss):
    import types
    # This is a helper function for the test function below.
    # It returns a sorted list of the names of the methods
    # defined in a class. It's okay if you don't fully understand it!
    result = [ ]
    for var in clss.__dict__:
        val = clss.__dict__[var]
        if (isinstance(val, types.FunctionType)):
            result.append(var)
    return sorted(result)

def testBirdClasses():
    print("Testing Bird classes...", end="")
    # A basic Bird has a species name, can fly, and can lay eggs
    bird1 = Bird("Parrot")
    assert(type(bird1) == Bird)
    assert(isinstance(bird1, Bird))
    assert(bird1.fly() == "I can fly!")
    assert(bird1.countEggs() == 0)
    assert(str(bird1) == "Parrot has 0 eggs")
    bird1.layEgg()
    assert(bird1.countEggs() == 1)
    assert(str(bird1) == "Parrot has 1 egg")
    bird1.layEgg()
    assert(bird1.countEggs() == 2)
    assert(str(bird1) == "Parrot has 2 eggs")
    tempBird = Bird("Parrot")
    assert(bird1 == tempBird)
    tempBird = Bird("Wren")
    assert(bird1 != tempBird)
    nest = set()
    assert(bird1 not in nest)
    assert(tempBird not in nest)
    nest.add(bird1)
    assert(bird1 in nest)
    assert(tempBird not in nest)
    nest.remove(bird1)
    assert(bird1 not in nest)
    assert(getLocalMethods(Bird) == ['__eq__','__hash__','__init__', 
                                     '__repr__', 'countEggs', 
                                     'fly', 'layEgg'])
    
    # A Penguin is a Bird that cannot fly, but can swim
    bird2 = Penguin("Emperor Penguin")
    assert(type(bird2) == Penguin)
    assert(isinstance(bird2, Penguin))
    assert(isinstance(bird2, Bird))
    assert(not isinstance(bird1, Penguin))
    assert(bird2.fly() == "No flying for me.")
    assert(bird2.swim() == "I can swim!")
    bird2.layEgg()
    assert(bird2.countEggs() == 1)
    assert(str(bird2) == "Emperor Penguin has 1 egg")
    assert(getLocalMethods(Penguin) == ['fly', 'swim'])
    
    # A MessengerBird is a Bird that carries a message
    bird3 = MessengerBird("War Pigeon", "Top-Secret Message!")
    assert(type(bird3) == MessengerBird)
    assert(isinstance(bird3, MessengerBird))
    assert(isinstance(bird3, Bird))
    assert(not isinstance(bird3, Penguin))
    assert(not isinstance(bird2, MessengerBird))
    assert(not isinstance(bird1, MessengerBird))
    assert(bird3.deliverMessage() == "Top-Secret Message!")
    assert(str(bird3) == "War Pigeon has 0 eggs")
    assert(bird3.fly() == "I can fly!")

    bird4 = MessengerBird("Homing Pigeon", "")
    assert(bird4.deliverMessage() == "")
    bird4.layEgg()
    assert(bird4.countEggs() == 1)
    assert(getLocalMethods(MessengerBird) == ['__init__', 'deliverMessage'])

    # Note: all birds are migrating or not (together, as one)
    assert(bird1.isMigrating == bird2.isMigrating == bird3.isMigrating == False)
    assert(Bird.isMigrating == False)

    bird1.startMigrating()
    assert(bird1.isMigrating == bird2.isMigrating == bird3.isMigrating == True)
    assert(Bird.isMigrating == True)

    Bird.stopMigrating()
    assert(bird1.isMigrating == bird2.isMigrating == bird3.isMigrating == False)
    assert(Bird.isMigrating == False)
    print("Done!")

testBirdClasses()
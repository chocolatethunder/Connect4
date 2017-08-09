import turtle as t
import random
import string
from copy import copy, deepcopy

# Global Variables
HEIGHT 		= 700 # Board's Height
WIDTH 		= 1100 # Board's WIDTH
CELLSIZE 	= 100 # Size of each cell on the gameboard
HALFCELL 	= CELLSIZE//2
GAMESTATE	= []  # Initial GAMESTATE
TURN		= " "  # Initilize empty TURN
DRAWSPEED 	= 2000
R			= "R" # Red Player
Y			= "Y" #Yellow Player
AIPEG           = " "

# Determine the number of columns and rows
TROWS 	= (HEIGHT//CELLSIZE)-1
TCOLS 	= (WIDTH//CELLSIZE)-4
	
#---------------------- START INITIAL DRAW AND SETUP FUNCTIONS --------------------

# This function is a GUI touch up. It makes sure the draw of the circle is padded nicely in the game board
def resetX():
	return ((0.75*CELLSIZE)/2)+5
	
#When the game is over the screen will display who won
#The winner parameter need to be carried because, it has multiple condition to display different messages
#The winner parameter is either R,Y,or None defined by the check fucntions below
def gameOver(winner):
	t.speed(DRAWSPEED)
	t.up()
	t.goto(WIDTH-(HALFCELL*1.60),HEIGHT-(CELLSIZE*6.5))
	if winner == R:
		t.color('red')
		t.write('Player Wins : R', True, 'right', font=('', 25, 'bold','normal'))
	elif winner == Y:
		t.color('green')
		t.write('Player Wins : Y', True, 'right', font=('', 25, 'bold','normal'))
	elif winner == None:
		t.color('black')
		t.write('The game is a Tie', True, 'right', font=('', 25, 'bold','normal'))



	
# Initialize and setup the coordinates for the screen and reset the grid from center to the bottom left
def intializeScreen():

	t.setup(WIDTH, HEIGHT)
	t.reset()
	t.setworldcoordinates(0,0,WIDTH,HEIGHT)
	t.hideturtle()
	
	startX = resetX()
	startY = 10
	
	# Once the screen is initialized start drawing the empty board
	drawBoard(startX,startY)
	
	#After the board is drawn start drawing the UI on the side
	drawUI()

# This function can draw the circular peg anywhere on the board
# 4 parameters: circle which calls the turtle function, using the coordinates from x & y
# And what color the peg will be, and smaller is a parameter that
# determes whether the game is over, and drawing the game over pegs
def drawPeg(circle,x,y,color,smaller):
	
	global pegSize
	if smaller != False:
		pegSize = (0.50*CELLSIZE)/2
	
		circle.hideturtle()
		circle.speed(DRAWSPEED)
		circle.begin_fill()
		circle.up()
		circle.goto(x,y)
		circle.down()
		circle.color(color)
		circle.circle(pegSize)
		circle.end_fill()
		circle.hideturtle()
	else:
		pegSize = (0.75*CELLSIZE)/2
		
		circle.hideturtle()
		circle.speed(DRAWSPEED)
		circle.begin_fill()
		circle.up()
		circle.goto(x,y)
		circle.down()
		circle.color(color)
		circle.circle(pegSize)
		circle.end_fill()
		circle.hideturtle()

# This function first draws the base board and draws the empty peg holes on it to create an empty game board
# startX and startY
def drawBoard(startX,startY):
	
	
	# Draw base grid	
	grid = t.Turtle()
	grid.speed(DRAWSPEED)
	grid.up()
	grid.goto(0,0)
	grid.down()
	grid.color("blue")
	grid.pensize(25)
	grid.left(90)
	
	for square in range(2):
		grid.begin_fill()
		grid.forward(HEIGHT)
		grid.right(90)
		grid.forward(WIDTH-(CELLSIZE*4))
		grid.right(90)
		grid.end_fill()
		
	circle 	= t.Turtle()

	setupGameState(TROWS,TCOLS)
	
	# Draw the columns and ROWS
	for row in range(TROWS):
		for col in range(TCOLS):
			drawPeg(circle,startX,startY,"white",False)
			startX = startX + CELLSIZE

		startX = resetX()
		startY = startY + CELLSIZE
	
	drawColLabels(startX,startY)

# Function that writes the labels of the title, description, saving, and loading.
def drawUI():
	ui = t.Turtle()
	ui.color("Blue")
	ui.hideturtle()
	ui.speed(DRAWSPEED)
	ui.penup()
	ui.goto(WIDTH-(CELLSIZE),HEIGHT-(CELLSIZE))
	ui.write("Connect", True, "right", font=('Arial', 50, 'italic', 'bold'))
	ui.goto(WIDTH-(CELLSIZE*0.6),HEIGHT -(CELLSIZE*1.5))
	ui.write("4",True, 'center', font=('Arial', 85, 'bold','italic'))
	
	intro_message = ['This is a game where you play TURN for TURN','with another player. The first player drops a piece', 'The second player drops a piece afterwards. This', 'process repeats unitl one player can connect 4 ', 'pieces vertically, horizontally, or diagonally']
	increment = HEIGHT-(CELLSIZE*2.5)
	for description in intro_message:
		ui.color("Black")
		ui.goto(WIDTH-CELLSIZE*1.85,increment)
		increment = increment - (CELLSIZE//4)
		ui.write(description,True, 'center' , font = ('Arial', 11 , 'bold', 'italic'))
	ui.goto(WIDTH-(HALFCELL*1.75),HEIGHT-(CELLSIZE*4))
	saveMessage = "Press the key [S] to save"
	ui.color("Dark Blue")
	ui.write(saveMessage,True,'right',font = ('Arial',14,'italic','bold'))
	ui.goto(WIDTH-(HALFCELL*0.75),(HEIGHT-(HALFCELL*9)))
	loadMessage = "Press the key [L] to load last save"
	ui.write(loadMessage,True,'right',font = ('Arial',14,'italic','bold'))
	

# Initialize and setup the GAMESTATE with empty moves filed in
def setupGameState(TROWS,TCOLS):	
	for col in range(TCOLS):
		GAMESTATE.append(col)
		GAMESTATE[col] = []
		for row in range(TROWS):
			GAMESTATE[col].append(row)
			GAMESTATE[col][row] = " "


# Draws the labes on top of the columns
# startX and startY are the starting coordinates to guide where to draw the labels
def drawColLabels(startX,startY):
	
	labels = string.ascii_uppercase
	pentip = t.Turtle()
	
	pentip.hideturtle()
	
	for col in range(TCOLS):
		pentip.penup()
		pentip.color("white")
		pentip.goto(startX,startY)
		pentip.write(labels[col], True, 'center', font=('', 50, 'bold','normal'))
		startX = startX + CELLSIZE

	startX = resetX()

# Randomly decides by default who goes first
def whoStarts(randomize=True):
	
	global TURN
	global AIPEG
	
	if randomize == True:
		dice = random.randint(0,1)
		if dice == 0:
			print("You are the Yellow Peg, you will be going first")
			AIPEG = R
			TURN = Y
			t.color('Blue')
			t.up()
			t.goto(WIDTH-(HALFCELL*2),HEIGHT -(CELLSIZE*6))
			t.write("You are going first!",True,'right',font=('Arial',15,'bold','normal'))
		if dice == 1:
			print("You are the Red Peg, you will be going second")
			AIPEG = Y
			TURN = Y
			aiTurn(GAMESTATE)
			t.color('Red')
			t.up()
			t.goto(WIDTH-(HALFCELL*2),HEIGHT -(CELLSIZE*6))
			t.write("You are going second!",True,'right',font=('Arial',15,'bold','normal'))

#---------------------- END INITIAL DRAW AND SETUP FUNCTIONS --------------------
			
#---------------------- START SUPER COMPLICATED AI ALGORITHMS --------------------

# AI Turn maker. More algorithms coming soon!
#The AI will choose its best option and make a valid move after the player clicks
#The parameter GAMESTATE is needed for the AI to look at the current board and make its best move

def aiTurn(GAMESTATE):
	aiChoice = (seekAndDestroy(GAMESTATE)*CELLSIZE)
	clicked(aiChoice,0)

# This function finds which of the columns has the highest heuristical value determined by the hVal and
# seekAndDestroy functions.
# Rating is a list containing the rows and cols and their heurestical value
# maxCol is returned to tell the AI which column to drop the next peg into
def findMaxCol(rating):
	
	max = 0
	maxCol = None
	
	for col in range(len(rating)):		
		for row in range(len(rating[col])):			
			if (max < rating[col][row]):
				max = rating[col][row]
				maxCol = col
				
	return maxCol

# This function creates a copy of the current gamestate. It then adds an AI peg to each column and determines
# the heurestical value of that move and stores it in bestmove.
# Gamestate is the current gamestate
# The function either returns the key (which is the column number) of the highest heuristical value stored in
# in moveHRating
def seekAndDestroy(GAMESTATE):
	
	global AIPEG
	
	tempGame = deepcopy(GAMESTATE)
	moveHRating = []
	bestmove = []
	
	for col in range(TCOLS):
		moveHRating.append(col)
		moveHRating[col] = []
		
		for row in range(len(tempGame[col])):
			moveHRating[col].append(row)
			
			if tempGame[col][row] == " ":
				tempGame[col][row] = AIPEG
				moveHRating[col][row] = hVal(tempGame)		
				
				if moveHRating[col][row] > 0:
					bestmove.append(findMaxCol(moveHRating))
				tempGame[col][row] = " "

	if (bestmove):
		return max(bestmove)
	else:
		return random.randint(0,TCOLS)

# This is the mathematical function that gives the AI a numerical heurestical value of each of it's next move
# It checks for how many 2 in a row, 3 in a row, and 4 in a row there will be in the theoretical boardstate.
# Boardstate is a hypothetical list of gamestate passed by seekAndDestroy function for evalluation
# Returns the heuristical value of each move.
def hVal(boardstate):
	
	global AIPEG	
	ai_fours 	= checkStreak(boardstate, AIPEG, 4)
	ai_threes	= checkStreak(boardstate, AIPEG, 3)
	ai_twos		= checkStreak(boardstate, AIPEG, 2)
	
	if AIPEG == Y:
		opponent = R
	else:
		opponent = Y
		
	player_fours = checkStreak(boardstate, opponent, 4)
	
	if player_fours > 0:
		return -10000
	else:
		return ai_fours*100000 + ai_threes*100 + ai_twos
	
# Checks for matching pegs and returns the count. Boardstate is hypothetical gamestate, player is the current
# player and streak is the number of pegs matching in a row to look for.
def checkStreak(boardstate, player, streak):
	count = 0
	for row in range(TROWS):
		for col in range(TCOLS):
			if boardstate[col][row].upper() == player.upper():				
				count += checkVerticalStreak(row, col, boardstate, streak)
				count += checkHorizontalStreak(row, col, boardstate, streak)
				count += checkDiagonalStreak(row, col, boardstate, streak)
				
	return count

# Checks for vertical matching streaks and returns the count
# Row and Col are the coordinated from which to start searching from. Boardstate is hypothetical gamestate,
# player is the current player and streak is the number of pegs matching in a row to look for.
def checkVerticalStreak(row, col, boardstate, streak):
	winCount = 0
	for step in range(row,TROWS):
		if boardstate[col][step].upper() == boardstate[col][row].upper():
			winCount += 1
		else:
			break
	
	if winCount >= streak:
		return True
	else:
		return False

# Checks for Horizontal matching streaks and returns the count
# Row and Col are the coordinated from which to start searching from. Boardstate is hypothetical gamestate,
# player is the current player and streak is the number of pegs matching in a row to look for.
def checkHorizontalStreak(row, col, boardstate, streak):
	winCount = 0
	for step in range(col,TCOLS):
		if boardstate[step][row].upper() == boardstate[col][row].upper():
			winCount += 1
		else:
			break
	
	if winCount >= streak:
		return True
	else:
		return False

# Checks for Diagonal matchin streaks and returns the count
# Row and Col are the coordinated from which to start searching from. Boardstate is hypothetical gamestate,
# player is the current player and streak is the number of pegs matching in a row to look for.
def checkDiagonalStreak(row, col, boardstate, streak):
	
	total = 0
	winCount = 0
	colstep = col
	
	for rowstep in range(row, TROWS):
		if colstep >= TCOLS:
			break
		elif boardstate[colstep][rowstep].upper() == boardstate[col][row].upper():
			winCount += 1
		else:
			break
		colstep += 1
		
	if winCount >= streak:
		total += 1
		
	total = 0
	winCount = 0
	colstep = col
	
	for rowstep in range(row, -1, -1):
		if colstep >= TCOLS:
			break
		elif boardstate[colstep][rowstep].upper() == boardstate[col][row].upper():
			winCount += 1
		else:
			break
		colstep += 1
		
	if winCount >= streak:
		total += 1
		
	return total
		

#----------------------  END SUPER COMPLICATED AI ALGORITHMS ---------------------

#---------------------- START PLAYER INTERACTION FUNCTIONS --------------------

# Translates user's clicks into Row
def getRow(y):
	return int((y//CELLSIZE))

# Translates user's clicks into TCOLS	
def getCol(x):	
	return int((x//CELLSIZE))

# The core of the game where the player's move is interpreted, checked, then inserted into
# the GAMESTATE and then displayed on screen.
def clicked(x,y):

	global TURN
	
	column 	= getCol(x)
	row     = getRow(y)
	
	if (checkBoardFull(GAMESTATE) == True):

		if (validMove(GAMESTATE,column,row) == True):
			
			if (displayMove(GAMESTATE,column,TURN) == True):
				
				winner = checkWin(GAMESTATE)
				
				if winner == False:
					if AIPEG == Y:
						if TURN == Y:
							TURN = R
						elif TURN == R:
							TURN = Y
							aiTurn(GAMESTATE)
					if AIPEG == R:
						if TURN == Y:
							TURN = R
							aiTurn(GAMESTATE)
						elif TURN == R:
							TURN = Y
						
				else:			
					print("Player Wins :",winner)
					gameOver(winner)
					#This is where the winscreen shows up
					t.exitonclick()
	else:
		gameOver(None)
	return False			

# This function translates the user's click move into a peg being drawn onto the game screen
def displayMove(GAMESTATE,column,TURN):

	if TURN == R:
		turncolour = "red"
	if TURN == Y:
		turncolour = "yellow"
	
	for row in range(len(GAMESTATE[column])):
		if GAMESTATE[column][row] == " ":
			GAMESTATE[column][row] = TURN
			circle = t.Turtle()
			drawPeg(circle,(column*CELLSIZE)+resetX(),(row*CELLSIZE)+10,turncolour,False)
			return True
			
	return False

#---------------------- END PLAYER INTERACTION FUNCTIONS --------------------


#---------------------- START VALIDATION FUNCTIONS --------------------

# Checks if the player has entered a valid move
# Takes the gamestate, column, and row
# Checks if the click is in a valid spot to place a peg
def validMove(GAMESTATE,column,row):
	
	if (row >= 0 and row < TROWS):
		if (column >= 0 and column < TCOLS):
			return True
	
	return False

# Checks if all the game's empty pegs have been filled
# Takes the gamestate to check whether the board is comepletely full
def checkBoardFull(GAMESTATE):
	for col in range(TCOLS):
		for row in range(TROWS):
			if GAMESTATE[col][row] == " ":
				return True
	return False

# Checks the GAMESTATE for a vertical win condition
# Takes the gamestate and goes through each column and row to see a vertical check
def checkRows(GAMESTATE):	
	for col in range(TCOLS):
		for row in range(TROWS):
			if GAMESTATE[col][row] != " " and row < (TROWS-3):
				if (GAMESTATE[col][row] == GAMESTATE[col][row+1] and \
					GAMESTATE[col][row] == GAMESTATE[col][row+2] and \
					GAMESTATE[col][row] == GAMESTATE[col][row+3]):
						winningPegs(row,col)
						winningPegs(row+1,col)
						winningPegs(row+2,col)
						winningPegs(row+3,col)
						return GAMESTATE[col][row]
	
	return False

# Checks the GAMESTATE for a horizontal win condition
#
def checkCols(GAMESTATE):
	for col in range(TCOLS):
		for row in range(TROWS):
			if GAMESTATE[col][row] != " " and col < (TCOLS-3):
				if (GAMESTATE[col][row] == GAMESTATE[col+1][row] and \
					GAMESTATE[col][row] == GAMESTATE[col+2][row] and \
					GAMESTATE[col][row] == GAMESTATE[col+3][row]):
						winningPegs(row,col)
						winningPegs(row,col+1)
						winningPegs(row,col+2)
						winningPegs(row,col+3)
						return GAMESTATE[col][row]
	
	return False
	
#Checks both bottom left to top right and top left to bottom right for a win condition
def checkDiag(GAMESTATE):
	
	# Checks / Pattern
	for col in range(TCOLS):
		for row in range(TROWS):
			if GAMESTATE[col][row] != " " and col < (TCOLS-3) and row < (TROWS-3):
				if (GAMESTATE[col][row] == GAMESTATE[col+1][row+1] and \
					GAMESTATE[col][row] == GAMESTATE[col+2][row+2] and \
					GAMESTATE[col][row] == GAMESTATE[col+3][row+3]):
						winningPegs(row,col)
						winningPegs(row+1,col+1)
						winningPegs(row+2,col+2)
						winningPegs(row+3,col+3)
						return GAMESTATE[col][row]
	
	# Checks \ Pattern
	for col in range(TCOLS):
		for row in range(TROWS):
			if GAMESTATE[col][row] != " " and col > 2 and row < (TROWS-3):
				if (GAMESTATE[col][row] == GAMESTATE[col-1][row+1] and \
					GAMESTATE[col][row] == GAMESTATE[col-2][row+2] and \
					GAMESTATE[col][row] == GAMESTATE[col-3][row+3]):
						winningPegs(row,col)
						winningPegs(row+1,col-1)
						winningPegs(row+2,col-2)
						winningPegs(row+3,col-3)
						return GAMESTATE[col][row]
	
	return False

#Checks the GAMESTATE to see if any of the win conditions are met and 
def checkWin(GAMESTATE):
	
	rowWin = checkRows(GAMESTATE)
	colWin = checkCols(GAMESTATE)
	diagWin = checkDiag(GAMESTATE)
	
	if rowWin != False:
		return rowWin
		
	if colWin != False:
		return colWin
	
	if diagWin != False:
		return diagWin
	
	return False

def winningPegs(row,col):
	circle = t.Turtle()
	turncolour = "Dark Blue"
	drawPeg(circle,col*CELLSIZE+resetX(),row*CELLSIZE+20,turncolour,True)
	
	
#---------------------- END VALIDATION FUNCTIONS --------------------


#---------------------- START SAVING GAME FUNCTIONS -----------------

#When prompted by function onkey [S] creates a file that puts the current GAMESTATE into the file
def saveGame():
	winner = checkWin(GAMESTATE)
	if winner != False:
		print ("Cannot save, there is already a winner. Please start a new game")
	
	else:
		saving = open('save.txt','w')
		for item in GAMESTATE:
			saving.write(''.join(item) + '\n')
		saving.write(AIPEG + '\n')
		saving.write(TURN)
		saving.close()
		t.up()
		t.goto(WIDTH-(HALFCELL*2),HEIGHT -(CELLSIZE*7))
		t.write("Game is now saved.",True,'right',font=('Arial',15,'bold','normal'))
		print ("Game is now saved.")

#The parameters "line" is being used to recreate the loaded GAMESTATE
#Before newstate is returned, newstate is being used to draw the old pegs before GAMESTATE is fully updated
def updateGamestate(line):
	global AIPEG
	global TURN
	newlist = []
	circle = t.Turtle()

	for i in range(len(line)-2):
		sublist = []
		for j in range(len(line[i])):
			sublist.append(line[i][j])
		newlist.append(sublist)
		
	AIPEG = line[len(line)-2]
	TURN = line[len(line)-1]
	print("Updated AIPEG and TURN")
	print("AIPEG is " +AIPEG+ " and TURN is " ,TURN)
	print ("It's your move!")
	
	newstate = newlist
	
	for column in range(len(newstate)):
		for row in range(len(newstate[column])):
			if newstate[column][row] == R:
				turncolour = "red"
				drawPeg(circle,(column*CELLSIZE)+resetX(),(row*CELLSIZE)+10,turncolour,False)
			elif newstate[column][row] == Y:
				turncolour = "yellow"
				drawPeg(circle,(column*CELLSIZE)+resetX(),(row*CELLSIZE)+10,turncolour,False)


	return newstate

#When prompted by function onkey [L], opens the save.txt file and goes through it, splitting it,
#and then sending it through the function updateGamestate
def loadGame():
	global GAMESTATE
	load = open('save.txt','r')
	line = load.read().splitlines()
	GAMESTATE = updateGamestate(line)
	print("Game is now loaded.")
	t.up()
	t.goto(WIDTH-(HALFCELL*2),HEIGHT -(CELLSIZE*5))
	t.write("Game is now loaded!", True,'right',font=('Arial',15,'bold','normal'))
	winner = checkWin(GAMESTATE)
		
		
#---------------------- END SAVING GAME FUNCTIONS -------------------
			
def main():
	intializeScreen()
	whoStarts(randomize=True)
	t.onscreenclick(clicked)
	t.onkey(saveGame,"s")
	t.onkey(loadGame,"l")
	t.listen()
	t.mainloop()
	

main()

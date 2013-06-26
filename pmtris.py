#!/usr/bin/env python

"""

Release under the terms of the GPL licence
You can get a copy of the license at http://www.gnu.org

Description: Poor Man's Tetris clone.

Cloned by: Matt Hersant (matt_hersant[at]yahoo[dot]com)

Why: Thought it would be fun!  And wanted to
see if I could do it all by myself.  That is,
without reading the code from other tetris
clones.  After all the backbone of this game
simply involves the manipulation of a 2d
array/list, right?  Update: wasn't able to do
this without doing an internet search for help
on the tetrimino rotation.

Stuff:
    - Consider using a 22 row board
    - Consider weighing random tetrimino selection
    - Add ghost tetrimino to bottom, so human knows
      where it will land

"""

try:
    import numpy
    import curses
    from sys import exit
    from random import choice 
    from time import time, sleep
    from signal import signal, SIGINT
except ImportError, err:
    print "Error Importing module. %s" % (err)
    exit(1)

##############################################
def signal_handler(signal, frame):
##############################################
    curses.endwin()
    exit(0)

##############################################
def logActiveCoordinates(board):
##############################################
    active_y_coordinates = []
    active_x_coordinates = []
    for [y_idx, y_val] in enumerate(board):
        for [x_idx, x_val] in enumerate(board[y_idx]):
            if x_val == 'x':
                active_y_coordinates.append(y_idx)
                active_x_coordinates.append(x_idx)
    return active_y_coordinates, active_x_coordinates

##############################################
if __name__=='__main__':
##############################################
    # Signal handler for sigint
    signal(SIGINT, signal_handler)

    # Map Color names to numbers.
    colormap = {                             \
        'BLACK'      : 1,  'BLUE'      : 2,  \
        'GREEN'      : 3,  'YELLOW'    : 4,  \
        'MAGENTA'    : 5,  'CYAN'      : 6,  \
        'WHITE'      : 7,  'RED'       : 8,  \
        'WHITE_TXT'  : 9,  'RED_TXT'   : 10, \
        'BLUE_TXT'   : 11, 'GREEN_TXT' : 12, \
    }

    # Define game tetriminos (game pieces)
    # data structure.  pos is list of 2d lists.
    # Each 2d list is a different two deminsional 
    # position.  Based on clockwise rotation.
    # We use this manner of declaration so that 
    # humans may easily read this code and make
    # changes to tetrimino layouts.
    tetriminos = {}
    tetriminos['o'] = {            \
        'pos' : [                  \
                    [1, 1],        \
                    [1, 1],        \
                ],                 \
        'clr' : colormap['YELLOW'] \
    }
    tetriminos['z'] = {            \
        'pos' : [                  \
                    [0, 0, 0],     \
                    [1, 1, 0],     \
                    [0, 1, 1],     \
                ],                 \
        'clr' : colormap['RED']    \
    }
    tetriminos['i'] = {            \
        'pos' : [                  \
                    [0, 0, 0, 0],  \
                    [1, 1, 1, 1],  \
                    [0, 0, 0, 0],  \
                    [0, 0, 0, 0],  \
                ],                 \
        'clr' : colormap['BLUE']   \
    }
    tetriminos['l'] = {            \
        'pos' : [                  \
                    [1, 0, 0],     \
                    [1, 0, 0],     \
                    [1, 1, 0],     \
                ],                 \
        'clr' : colormap['MAGENTA']\
    }
    tetriminos['j'] = {            \
        'pos' : [                  \
                    [0, 1, 0],     \
                    [0, 1, 0],     \
                    [1, 1, 0],     \
                ],                 \
        'clr' : colormap['WHITE']  \
    }
    tetriminos['s'] = {            \
        'pos' : [                  \
                    [0, 0, 0],     \
                    [0, 1, 1],     \
                    [1, 1, 0],     \
                ],                 \
        'clr' : colormap['GREEN']  \
    }
    tetriminos['t'] = {            \
        'pos' : [                  \
                    [0, 0, 0],     \
                    [1, 1, 1],     \
                    [0, 1, 0],     \
                ],                 \
        'clr' : colormap['CYAN']   \
    }

    tetrimino_positions = {}
    for i in tetriminos.keys():
        tetrimino_positions[i] = tetriminos[i]['pos']

    # The status of our board will live here.
    board = []

    # Define where our board will live.
    boardstartx = 1
    boardstarty = 1

    # Define where our scoreboard will live.
    scoreboardstartx = 15
    scoreboardstarty = 1
    scoreboardheight = 5
    scoreboardwidth  = 11

    # Define where our nextpieceboard will live.
    nextpieceboardstartx = 15
    nextpieceboardstarty = 8
    nextpieceboardheight = 5
    nextpieceboardwidth  = 11

    # The deminsions of the tetris grid.
    boardymin = 0
    boardymax = 20
    boardxmin = 0
    boardxmax = 10

    # Init board.
    templist = []
    for i in range(boardymin, boardymax):
        for j in range(boardxmin, boardxmax):
            templist.append('')
        board.append(templist)
        templist = []

    # Init curses.
    myscreen = curses.initscr()
    # Non blocking.
    myscreen.timeout(0)
    # Suppress the human's input.
    curses.noecho()
    # Disable line buffering.
    curses.cbreak()
    # Hide cursor.
    curses.curs_set(0)
    # Enable processing of arrow keys.
    myscreen.keypad(1)

    # Init colors.
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1,  curses.COLOR_BLACK,   curses.COLOR_BLACK)
    curses.init_pair(2,  curses.COLOR_BLUE,    curses.COLOR_BLUE)
    curses.init_pair(3,  curses.COLOR_GREEN,   curses.COLOR_GREEN)
    curses.init_pair(4,  curses.COLOR_YELLOW,  curses.COLOR_YELLOW)
    curses.init_pair(5,  curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(6,  curses.COLOR_CYAN,    curses.COLOR_CYAN)
    curses.init_pair(7,  curses.COLOR_WHITE,   curses.COLOR_WHITE)
    curses.init_pair(8,  curses.COLOR_RED,     curses.COLOR_RED)
    curses.init_pair(9,  curses.COLOR_WHITE,   curses.COLOR_BLACK)
    curses.init_pair(10, curses.COLOR_RED,     curses.COLOR_BLACK)
    curses.init_pair(11, curses.COLOR_BLUE,    curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_GREEN,   curses.COLOR_BLACK)

    # Create gamebox.
    gamebox = myscreen.derwin(                   \
        boardymax + 1,                           \
        boardxmax + 1,                           \
        boardstarty,                             \
        boardstartx,                             \
    )
    gamebox.border(0)

    # Create scoreboard.
    scoreboard = myscreen.derwin(                \
        scoreboardheight,                        \
        scoreboardwidth,                         \
        scoreboardstarty,                        \
        scoreboardstartx,                        \
    )

    # Create nextpiece.
    nextpieceboard = myscreen.derwin(            \
        nextpieceboardheight,                    \
        nextpieceboardwidth,                     \
        nextpieceboardstarty,                    \
        nextpieceboardstartx,                    \
    )

    scoreboard.refresh()
    nextpieceboard.refresh()

    # Keep track of the last time a piece was
    # forced down one row.  For simplicity sake,
    # we are using whole seconds.
    last_push_down = time()

    # Booleans
    blns = {}
    blns['rotate'] = False
    blns['blocking'] = False
    blns['push_left'] = False
    blns['push_right'] = False
    blns['force_down'] = False
    blns['collide_btm'] = False
    blns['init_active_piece'] = True

    # Declare our score.
    score = 0

    # Declare our current piece.
    which = ''

    # Declare our next piece.
    nextwhich = ''

    # Clear intro screen and start game.
    gamebox.erase()

    # Aguirre, the Wrath of God.
    # Begin our search for El Dorado.
    while True:
        # This block is run If we collide or we
        # need to init a new tetrimino.  
        if blns['collide_btm'] or blns['init_active_piece']:
            if not which:
                which = choice(tetriminos.keys())
                nextwhich = choice(tetriminos.keys())
            else:
                which = nextwhich
                nextwhich = choice(tetriminos.keys())
            blns['init_active_piece'] = True
            blns['collide_btm'] = False

        event = myscreen.getch()
        if event == ord('q'):
            curses.endwin()
            exit(0)
        elif event == ord('p'):
            # Handle pause/unpause.
            # NEED TO FREEZE PUSH TIME
            if not blns['blocking']:
                myscreen.timeout(-1)
                blns['blocking'] = True
            else:
                myscreen.timeout(0)
                blns['blocking'] = False
        elif event == curses.KEY_UP:
            blns['rotate'] = True
        elif event == curses.KEY_LEFT:
            blns['push_left'] = True
        elif event == curses.KEY_RIGHT:
            blns['push_right']= True
        elif event == curses.KEY_DOWN:
            blns['force_down']= True

        ##############################################
        # Initial draw of newly picked tetrimino.
        ##############################################
        if blns['init_active_piece']:
            position = tetriminos[which]['pos']
            tetrimino_positions[which] = position
            for [y_idx, y_val] in enumerate(position):
                for [x_idx, x_val] in reversed(list(enumerate(position[y_idx]))):
                    if position[y_idx][x_idx]:
                        if board[y_idx][x_idx + 3]:
                            # Can't init piece, game over.
                            curses.endwin()
                            exit(0)
                        else:
                            board[y_idx][x_idx + 3] = 'x'
            blns['init_active_piece'] = False

            nextpieceboard.clear()
            # Show the human the next piece.
            newposition = tetriminos[nextwhich]['pos']
            for [y_idx, y_val] in enumerate(newposition):
                for [x_idx, x_val] in reversed(list(enumerate(newposition[y_idx]))):
                    if newposition[y_idx][x_idx]:
                        nextpieceboard.addstr(                              \
                            y_idx + 1,                                      \
                            x_idx + 3,                                      \
                            'x',                                            \
                            curses.color_pair(tetriminos[nextwhich]['clr']) \
                        )
            nextpieceboard.addstr(                                          \
                0,                                                          \
                2,                                                          \
                'Next',                                                     \
                curses.color_pair(colormap['WHITE_TXT'])                    \
            )
            nextpieceboard.refresh()

            scoreboard.addstr(                                              \
                0,                                                          \
                2,                                                          \
                'Score',                                                    \
                curses.color_pair(colormap['WHITE_TXT'])                    \
            )
            scoreboard.addstr(                                              \
                1,                                                          \
                2,                                                          \
                str(score),                                                 \
                curses.color_pair(colormap['RED_TXT'])                      \
            )
            scoreboard.refresh()


        # Keep track of the location of our active piece.
        [ active_y_coordinates, active_x_coordinates ] = logActiveCoordinates(board)
        time_to_push = False
        if blns['force_down'] or (time() - last_push_down) > 1:
            time_to_push = True

        ##############################################
        # Check for collision with bottom.
        ##############################################
        for [y_idx, y_val] in enumerate(board):
            for [x_idx, x_val] in enumerate(board[y_idx]):
                if x_val == 'x':
                    if time_to_push:
                        if (y_idx + 1) >= boardymax:
                            blns['collide_btm'] = True
                    else:
                        # Can't collide with bottom, not pushing.
                        blns['collide_btm'] = False

        ##############################################
        # Determine if another piece is blocking the push down.
        ##############################################
        if time_to_push and not blns['collide_btm']:
            max_y = max(active_y_coordinates)
            if (max_y + 1) < boardymax:
                for [y_idx, y_val] in enumerate(active_y_coordinates):
                    x_val = active_x_coordinates[y_idx]
                    if board[y_val + 1][x_val] != 'x':
                        if board[y_val + 1][x_val]:
                            # There is a piece below us.
                            # Set artificial collide_btm.
                            blns['collide_btm'] = True

        ##############################################
        # Push left.
        ##############################################
        if blns['push_left'] and not blns['collide_btm']:
            ok_to_push = True
            min_x = min(active_x_coordinates)
            for [y_idx, y_val] in enumerate(active_y_coordinates):
                x_val = active_x_coordinates[y_idx]
                if (x_val - 1 > boardxmin):
                    if board[y_val][x_val - 1] != 'x':
                        if board[y_val][x_val - 1]:
                            ok_to_push = False
            if min_x <= boardxmin:
                ok_to_push = False
            if ok_to_push:
                for [y_idx, y_val] in enumerate(active_y_coordinates):
                    x_val = active_x_coordinates[y_idx]
                    board[y_val][x_val] = ''
                    board[y_val][x_val - 1] = 'x'
                # We've pushed, so we need to update coordinates.
                [ active_y_coordinates, active_x_coordinates ] = logActiveCoordinates(board)
            blns['push_left'] = False

        ##############################################
        # Push right.
        ##############################################
        if blns['push_right'] and not blns['collide_btm']:
            ok_to_push = True
            max_x = max(active_x_coordinates)
            for [y_idx, y_val] in reversed(list(enumerate(active_y_coordinates))):
                x_val = active_x_coordinates[y_idx]
                if (x_val + 1 < boardxmax):
                    if board[y_val][x_val + 1] != 'x':
                        if board[y_val][x_val + 1]:
                            ok_to_push = False
            if max_x >= (boardxmax - 1):
                ok_to_push = False
            if ok_to_push:
                for [y_idx, y_val] in reversed(list(enumerate(active_y_coordinates))):
                    x_val = active_x_coordinates[y_idx]
                    board[y_val][x_val] = ''
                    board[y_val][x_val + 1] = 'x'
                # We've pushed, so we need to update coordinates.
                [ active_y_coordinates, active_x_coordinates ] = logActiveCoordinates(board)
            blns['push_right'] = False

        ##############################################
        # Rotation.
        ##############################################
        if blns['rotate'] and not blns['collide_btm']:
            current_x_offset = min(active_x_coordinates)
            current_y_offset = min(active_y_coordinates)

            position = tetrimino_positions[which]
            prop_position = numpy.array(position)
            transposed = prop_position.T
            rotated = []
            for [y_idx, y_val] in enumerate(transposed):
                templist = []
                for [x_idx, x_val] in reversed(list(enumerate(transposed[y_idx]))):
                    templist.append(transposed[y_idx][x_idx])
                rotated.append(templist)

            ok_to_rotate = True
            new_y_coordinates = []
            new_x_coordinates = []
            for [y_idx, y_val] in enumerate(rotated):
                for [x_idx, x_val] in reversed(list(enumerate(rotated[y_idx]))):
                    if position[y_idx][x_idx]:
                        curses.endwin()
                        print 'y_idx => ' + str(y_idx)
                        print 'current_y_offset => ' + str(current_y_offset)
                        print 'x_idx => ' + str(x_idx)
                        print 'current_x_offset => ' + str(current_x_offset)
                        print ''
                        new_y_coordinates.append(y_idx + current_y_offset)
                        new_x_coordinates.append(x_idx + current_x_offset)

            if ok_to_rotate:
                for [y_idx, y_val] in enumerate(active_y_coordinates):
                    x_val = active_x_coordinates[y_idx]
                    board[y_val][x_val] = ''
                for [y_idx, y_val] in enumerate(new_y_coordinates):
                    x_val = new_x_coordinates[y_idx]
                    board[y_val][x_val] = 'x'
                tetrimino_positions[which] = rotated
                [ active_y_coordinates, active_x_coordinates ] = logActiveCoordinates(board)
                blns['init_active_piece'] = False

        ##############################################
        # Push down.
        ##############################################
        if not blns['collide_btm']:
            if time_to_push:
                for [y_idx, y_val] in reversed(list(enumerate(active_y_coordinates))):
                    x_val = active_x_coordinates[y_idx]
                    board[y_val][x_val] = ''
                    board[y_val + 1][x_val] = 'x'
                last_push_down = time()
                # We've pushed, so we need to update coordinates.
                [ active_y_coordinates, active_x_coordinates ] = logActiveCoordinates(board)
        # We're at the bottom, we need to replace x with the
        # key for the active tetrimino.
        else:
            for [y_idx, y_val] in enumerate(active_y_coordinates):
                x_val = active_x_coordinates[y_idx]
                board[y_val][x_val] = which

        ##############################################
        # Filled row check.
        ##############################################
        # Start from the bottom up.
        completed = []
        for [y_idx, y_val] in reversed(list(enumerate(board))):
            complete_row = True
            for [x_idx, x_val] in enumerate(board[y_idx]):
                if not board[y_idx][x_idx]:
                    complete_row = False
            if complete_row:
                completed.append(y_idx)

        # If human has filled a row. Delete it then add
        # a fresh one to the beginning.
        if completed:
            templist = []
            for i in range(boardxmin, boardxmax):
                templist.append('')
            for idx in completed:
                del(board[idx])
                board.insert(0, templist)
                score += (10 * len(completed))
            blns['init_active_piece'] = True

        # Reset booleans.
        blns['rotate'] = False
        blns['push_left'] = False
        blns['push_right'] = False
        blns['force_down']= False

        x = 0
        y = 0
    
        gamebox.erase()
        for outerrow in board:
            for innerrow in outerrow:
                piece = innerrow
                if innerrow == 'x':
                    piece = which
                color = False
                if not innerrow:
                    color = colormap['BLACK']
                else:
                    color = tetriminos[piece]['clr']
                gamebox.addstr(              \
                    y,                       \
                    x,                       \
                    innerrow,                \
                    curses.color_pair(color) \
                )
                x += 1
            y += 1
            x = 0
        gamebox.refresh()

        sleep(100/1000000.0)

curses.endwin()

# TODO
# DO TESTING TO ENSURE LINE FILL WORKS
# FOR EACH ITERATION OF BOTH THE LOGO AND 
# BOARD LOOPS, CHECK WINDOW SIZE TO MAKE
# SURE HUMAN HASN'T SHRUNK IT.

# just use dash and pipe or whatever for border
#nlines, ncols, beginy, beginx

# ROTATE 2D LIST +90
# 1. TRANSPOSE
# 2. REVERSE EACH ROW

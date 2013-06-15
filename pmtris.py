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
array/list, right?

Stuff:
    - Consider using a 22 row board
    - Consider weighing random tetrimino selection
    - Consider adding + grid markers on board (overlap)

"""

import curses
from sys import exit
from random import choice 
from time import time, sleep
from signal import signal, SIGINT

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
    tetriminos['o'] = {                               \
        'pos' : [                                     \
                    [[0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]], \
                ],                                    \
        'clr' : colormap['YELLOW']                    \
    }
    tetriminos['z'] = {                               \
        'pos' : [                                     \
                    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 0, 1, 1, 0, 0, 0]], \
                    #
                    [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]], \
                ],                                    \
        'clr' : colormap['RED']                       \
    }
    tetriminos['i'] = {                               \
        'pos' : [                                     \
                    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],  \
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], \
                    #
                    [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]], \
                ],                                    \
        'clr' : colormap['BLUE']                      \
    }
    tetriminos['l'] = {                               \
        'pos' : [                                     \
                    [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]], \
                    #
                    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]], \
                    #
                    [[0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]], \
                    #
                    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 1, 1, 1, 0, 0, 0, 0]], \
                ],                                    \
        'clr' : colormap['MAGENTA']                   \
    }
    tetriminos['j'] = {                               \
        'pos' : [                                     \
                    [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]], \
                    #
                    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 1, 1, 1, 0, 0, 0, 0]], \
                    #
                    [[0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]], \
                    #
                    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]], \
                ],                                    \
        'clr' : colormap['WHITE']                     \
    }
    tetriminos['s'] = {                               \
        'pos' : [                                     \
                    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0]], \
                    #
                    [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],  \
                     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]], \
                ],                                    \
        'clr' : colormap['GREEN']                     \
    }
    tetriminos['t'] = {                               \
        'pos' : [                                     \
                    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]], \
                    #
                    [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]], \
                    #
                    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 1, 1, 1, 0, 0, 0, 0]], \
                    #
                    [[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],  \
                     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]], \
                ],                                    \
        'clr' : colormap['CYAN']                      \
    }

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
    #grid = myscreen.derwin(22, 12, 5, 25)
    #nlines, ncols, beginy, beginx
    #grid.border(0)

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

    # The status of our board will live here.
    board = []

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

    # Init a dict to keep track of indexes.
    tetrimino_indexes = {}
    for i in tetriminos.keys():
        tetrimino_indexes[i] = 0

    logo = [            \
        ["  poor    "], \
        ["  man's   "], \
        ["  tetris  "], \
        ["          "], \
        ["   .   .  "], \
        [" ',     : "], \
        ["`. `.  .: "], \
        ["     `.:  "], \
        ["   ,.:'`. "], \
        ["  /'      "], \
        ["          "], \
        ["          "], \
        ["/\ rotate "], \
        ["<  left   "], \
        [">  right  "], \
        ["\/ slam   "], \
        ["          "], \
        ["[a] start "], \
        ["[p] pause "], \
        ["[q] quit  "], \
    ]

    logo_blink_time = time()
    logo_y_max = 3
    aart_y_max = 9
    glitz = [ 'WHITE_TXT', 'RED_TXT', 'BLUE_TXT', 'GREEN_TXT' ]
    glitz_idx = 0
    # Show the human our logo.
    while True:
        event = myscreen.getch()
        if event == ord('q'):
            curses.endwin()
            exit(0)
        if event == ord('a'):
            break
        # Starting coordinates. 
        x = 25
        y = 5
    
        myscreen.erase()
        for [y_idx, y_val] in enumerate(logo):
            for [x_idx, x_val] in enumerate(logo[y_idx]):
                color = colormap['WHITE_TXT']
                if y_idx <= logo_y_max:
                    if (time() - logo_blink_time) >= 2:
                        color = colormap['RED_TXT']
                        if (time() - logo_blink_time) >= 4:
                            logo_blink_time = time()
                myscreen.addstr(y, x, logo[y_idx][x_idx], curses.color_pair(color))
                x += 1
            y += 1
            x = 25
        myscreen.refresh()
        sleep(1000/1000000.0)

    # Keep track of the last time a piece was
    # forced down one row.  For simplicity sake,
    # we are using whole seconds.
    last_push_down = time()

    # Booleans
    blns = {}
    blns['slam'] = False
    blns['rotate'] = False
    blns['blocking'] = False
    blns['push_left'] = False
    blns['push_right'] = False
    blns['collide_btm'] = False
    blns['init_active_piece'] = True

    # Declare our current piece.
    which = ''

    # Clear intro screen and start game.
    myscreen.erase()

    # Aguirre, the Wrath of God.
    # Begin our search for El Dorado.
    while True:
        # This block is run If we collide or we
        # need to init a new tetrimino.  
        if blns['collide_btm'] or blns['init_active_piece']:
            which = choice(tetriminos.keys())
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
            blns['slam']= True

        ##############################################
        # Initial draw of newly picked tetrimino.
        ##############################################
        if blns['init_active_piece']:
            position = tetriminos[which]['pos'][0]
            for [y_idx, y_val] in enumerate(position):
                for [x_idx, x_val] in enumerate(position[y_idx]):
                    if position[y_idx][x_idx]:
                        if board[y_idx][x_idx]:
                            # Can't init piece, game over.
                            curses.endwin()
                            exit(0)
                        else:
                            board[y_idx][x_idx] = 'x'
            tetrimino_indexes[which] = 0
            blns['init_active_piece'] = False

        # x indicates the active tetrimino.
        # For each iteration of the infinite while loop,
        # we need to find the coordinates of the active piece.
        time_to_push = False
        if blns['slam'] or (time() - last_push_down) > 1:
            time_to_push = True
        [ active_y_coordinates, active_x_coordinates ] = logActiveCoordinates(board)

        ##############################################
        # Check for collision with bottom.
        ##############################################
        for [y_idx, y_val] in enumerate(board):
            for [x_idx, x_val] in enumerate(board[y_idx]):
                if x_val == 'x':
                    if time_to_push:
                        if (y_idx + 1) >= boardymax:
                            blns['collide_btm'] = True
                            blns['slam'] = False
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
                            blns['slam'] = False

        ##############################################
        # Push left.
        ##############################################
        if blns['push_left'] and not blns['collide_btm'] and not blns['slam']:
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
        if blns['push_right'] and not blns['collide_btm'] and not blns['slam']:
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
        if blns['rotate'] and not blns['collide_btm'] and not blns['slam']:
            index = tetrimino_indexes[which]
            if len(tetriminos[which]['pos']) > 1:
                index += 1
                if index > (len(tetriminos[which]['pos']) - 1):
                    index = 0
            position = tetriminos[which]['pos'][index]

            current_offset = min(active_x_coordinates)
            default_offset = boardxmax
            for [y_idx, y_val] in enumerate(position):
                for [x_idx, x_val] in enumerate(position[y_idx]):
                    if position[y_idx][x_idx]:
                        if x_idx < default_offset:
                            default_offset = x_idx

            curses.endwin()
            print 'hello world'
            temp_position = position
            # Equalize our offsets.
            # Chop away columns until offset is same
            # For each column chopped, add blank one to end.
            while current_offset != default_offset:
                print "DOING 0"
                if current_offset > default_offset:
                    print "DOING 1"
                    # Then we need to add a column to beginning and remove one from end.
                    for outerrow in temp_position:
                        outerrow.insert(0, 0)
                        outerrow.pop()
                    default_offset += 1
                else:
                    print "DOING 2"
                    # Then we need to remove a column from beginning and add one to end
                    for outerrow in temp_position:
                        outerrow.insert(-1, 0)
                        temp_position.pop(0)
                    default_offset -= 1

            #import pprint
            #pprint.pprint(temp_position)
            position = False
            temp_position = False
#
#            tetrimino_indexes[which] = index
#            #temp_y_coordinates = active_y_coordinates
#            #temp_x_coordinates = active_x_coordinates
#            # Rotate right... for each element in rotated_coordinates
#            # check active coordinates to see if we're clobbering a piece.
#            # We've rotated, so we need to update coordinates.
#
#            # ROTATION, DETERMIN PROPOSED COORDINATES, THEN CHECK FOR COLLISION
#            # WITH BOTTOM, RIGHT AND LEFT
#            [ active_y_coordinates, active_x_coordinates ] = logActiveCoordinates(board)

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

        # Reset booleans.
        blns['rotate'] = False
        blns['push_left'] = False
        blns['push_right'] = False

        # Starting coordinates. 
        x = 25
        y = 5
    
        myscreen.erase()
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
                myscreen.addstr(y, x, innerrow, curses.color_pair(color))
                x += 1
            y += 1
            x = 25
        myscreen.refresh()

        if not blns['slam']:
            sleep(1000/1000000.0)

curses.endwin()

# TODO
# DO TESTING TO ENSURE LINE FILL WORKS

# 408 431... min max breaks

#index => 1
#[[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]]
#index => 0
#[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
# [0, 0, 0, 1, 1, 0, 0, 0, 0, 0]]
#index => 1
#[[0, 0, 0], [0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]]
#index => 0
#[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
#index => 1
#[[0, 0, 0], [0, 0, 0], [0, 0, 0]]


# just use dash and pipe or whatever for border

#card game - Memory
import simplegui
import random


# helper function to initialize globals
def new_game():
    global serect_list, state, exposed, recent_card, turn_number
    turn_number = 0
    state = 0
    exposed = []
    recent_card = []
    
    for i in range(16):
        exposed.append(False)
    serect_list = range(8)
    serect_list.extend(serect_list)
    random.shuffle(serect_list)

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, exposed, recent_card, turn_number
    
    i = pos[0] // 50
    if exposed[i] == True:
        return
    else:
        exposed[i] = True
        turn_number += 1
        label.set_text("Turns = " + str(turn_number))
        if state == 0:
            recent_card.append(i)
            state = 1
        elif state == 1:
            recent_card.append(i)
            state = 2
        elif state == 2:
            card1,card2 = recent_card.pop(), recent_card.pop()
            if serect_list[card1] != serect_list[card2]:
                exposed[card1] = False
                exposed[card2] = False
            recent_card.append(i)
            state = 1
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global serect_list, i, recent_card, change
    width = range(0, 801, 50)
    list = range(16)
    for i in list:
        canvas.draw_polygon([[width[i],0],[width[i+1],0],
                             [width[i+1],100],[width[i],100]],2,"Red","Green")
        if exposed[i]:
            canvas.draw_line([width[i]+25, 0],[width[i]+25,100], 50, "Black")
            canvas.draw_text(str(serect_list[i]), [10 + 50 * i, 70], 60, "White")
        
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

from statistics import mode
from tkinter import *
from tkinter import font
from PIL import ImageTk, Image
from math import *
import os

#create window
root = Tk()
root.title("Calculator")
root.geometry('400x630')
root.resizable(width=False, height=False)
#canvas for the window
canvas = Canvas(root, height=630, width=400)
canvas.pack()

#NB!
#name "line" is the field where user input is appearing as numbers and operation signs

#GLOBAL SUPPORT VARIABLES
sign_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', '-', '×', '÷', '2', '√(', '.', '(', ')', 'sin(', 'cos('] #list of all signs to show on the line
math_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', '-', '*', '/', '**2', 'sqrt(', '*sqrt(', '.', '(', ')', 'sin(', 'cos('] #list of all signs that can be added to the 'mathline' list
standart_operation_sign_list = ['+', '-', '×', '÷'] #list of standart operation signs
all_animation_operation_sign_list = ['+', '-', '×', '÷', '2'] #list of operation signs for animation function
all_math_operation_sign_list = ['+', '-', '*', '/', '**2'] #list of operation signs for math function
all_trigonometry_sign_list = ['sin(', 'cos(']
line = [] #list of elements (labels) on the line
mathline = []
global equal_state
equal_state = False
global x
global error_state
error_state = False

#COLORS
BG_COLOR = 'white'
LINE_COLOR = 'white'
SIGN_COLOR = LINE_COLOR
BTN_COLOR = 'white'
BTN_HOVER_COLOR = '#DFDFDF'
#SIZE AND POSITION OF BLACK LINE
BLACK_LINE_HEIGHT = 1
BLACK_LINE_XPOS = 0
#SIZE AND POSITION OF THE LINE
LINE_YPOS = 154
LINE_H = 80
LINE_W = 400
#SIZES AND POSITIONS OF ELEMENTS ON THE LINE
LINE_ELEMENTS_SIZE_MULTIPLIER = 1.4 #to adjust for the font size increase
YPOS = 10 #default y
H = 30 #default objects height
NUM_W = 8 * LINE_ELEMENTS_SIZE_MULTIPLIER #width of numbers
POINT_W = 6 * LINE_ELEMENTS_SIZE_MULTIPLIER #width of point
OPERATION_W = 22 * LINE_ELEMENTS_SIZE_MULTIPLIER #width of operation signs
POWER2_W = 8 * LINE_ELEMENTS_SIZE_MULTIPLIER #width of power 2
POWER2_FONT = 'Times', 9
SQRT_W = 15 * LINE_ELEMENTS_SIZE_MULTIPLIER #width of square root
BRACKET_W = 6 * LINE_ELEMENTS_SIZE_MULTIPLIER #width of brackets
TRIGONOMETRY_W = 27 * LINE_ELEMENTS_SIZE_MULTIPLIER #width of trigonometry functions (sin, cos etc)
SIGN_FONT_SIZE = 14
SIGN_FONT_FONT = 'Times'
SIGN_FONT = SIGN_FONT_FONT, SIGN_FONT_SIZE
#ANSWER LINE
ANSWER_XPOS = 230
ANSWER_YPOS = 42
ANSWER_H = 40
ANSWER_W = 170
ANSWER_FONT = SIGN_FONT_FONT, SIGN_FONT_SIZE
ERROR_FONT = 'Helvetica', 14
#BUTTONS
BTN_W = 100 #width of buttons
BTN_H = 66 #high of buttons
BTN_FONT = 'Helvetica', 12
BTN_COLUMN_1 = 0
BTN_COLUMN_2 = 100
BTN_COLUMN_3 = 200
BTN_COLUMN_4 = 300
BTN_ROW_1 = 564
BTN_ROW_2 = 498
BTN_ROW_3 = 432
BTN_ROW_4 = 366
BTN_ROW_5 = 300
BTN_ROW_6 = 234

START_LABEL_XPOS = 10 #point from where the signs on the line are being created
INITIAL_ZERO_XPOS = 11 #position of initial zero
X_LINE_LIMIT = 350 #limits the amount of signs can be added to the line in pixels
SCI_NOTATION_POINT = 15 #point from which amount of digits in the answer programm converts number to a scientific notation
ROUND_PERCISION = 10 #rounding presicion of float answers

#print useful stuff in terminal
def terminal():
   print('1. initial_zero.winfo_exists:', initial_zero.winfo_exists())
   print('2. mode_state: ', mode_state)
   try:
      print('3. res_list:', res_list)
   except:
      print('3. res_list: None')
   print('4. equal_state:', equal_state)
   print('5. error_state:', error_state)
   try:
      print("6. res:", res)
   except NameError:
      print("6. res: None")
   try:
      print("7. res_show:", res_show) 
   except NameError:
      print("7. res_show: None")
   try:
      print('8. ans_btn_list:', ans_btn_list)
   except NameError:
      print('8. ans_btn_list: []')
   print('9. mathline:', mathline)
   print('10. line:', line)
   print('--------------------------------------------------------------------')

#animating function
def animation(btn):

   #support variables
   global initial_zero
   global equal_state
   global ans_xpos

   #remove answer label when user insert any sign ater last calculation to start a new calculation
   if equal_state is True:
      if btn in standart_operation_sign_list or btn == '^2' or btn == '√(' or btn == '.':
         print("OPERATING WITH THE ANSWER...")
      else:
         for i2 in sign_list:
            if btn == i2:
               equal_clear()       
   #remove initial zero
   initial_zero.destroy()

   #in case user tries to add numbers to a power2
   try:
      if type(btn) == int and mathline[-1]=='**2':
         return
   except:
      pass
   #in case if user tries to add operation to a operation
   try:
      if btn in all_animation_operation_sign_list and mathline[-1] in all_math_operation_sign_list and mathline[-1] != '**2':
         line[-1].destroy()
         del line[-1]
   except:
      pass
   #in case if user tries to add trigonometry operation to unexpected sign
   try:
      if btn in all_trigonometry_sign_list and mathline[-1] not in all_math_operation_sign_list:
         if mathline[-1] != '(':
            return
   except:
      pass

   #adding signs to the line
   for i in sign_list:
      if btn == i and type(i) == int and line[-1].winfo_x() < X_LINE_LIMIT: #for numbers
         line.append('')
         line[-1] = Label(line_frame, text=str(btn), font=(SIGN_FONT), bg=SIGN_COLOR)
         line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=YPOS, height=H, width=NUM_W)
      if btn == i and btn == '.' and line[-1].winfo_x() < X_LINE_LIMIT: #for point
         if equal_state is True: #to operate answer straightaway
            ans()
            line.append('')
            line[-1] = Label(line_frame, text=str(btn), font=(SIGN_FONT), bg=SIGN_COLOR)
            line[-1].place(x = ans_xpos, y=YPOS, height=H, width=POINT_W)         
         else:
            if len(mathline) == 0: #for adding point to initial 0 on the line
               animation(0)
               math(0)
               line.append('')
               line[-1] = Label(line_frame, text=str(btn), font=(SIGN_FONT), anchor='e', bg=SIGN_COLOR)
               line[-1].place(x = INITIAL_ZERO_XPOS + NUM_W, y=YPOS, height=H, width=POINT_W)
            else: #all other cases
               line.append('')
               line[-1] = Label(line_frame, text=str(btn), font=(SIGN_FONT), anchor='e', bg=SIGN_COLOR)
               line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=YPOS, height=H, width=POINT_W)
      if btn == i and btn in standart_operation_sign_list and line[-1].winfo_x() < X_LINE_LIMIT: #for operation signs
         if equal_state is True: #to operate answer straightaway
            ans()
            line.append('')
            line[-1] = Label(line_frame, text=str(btn), font=(SIGN_FONT), bg=SIGN_COLOR)
            line[-1].place(x = ans_xpos, y=YPOS, height=H, width=OPERATION_W)
         else:
            if equal_state is False and len(line) == 1: #if operation sign is the first appearing on the line, so it will be the same size as a digit
               line.append('')
               line[-1] = Label(line_frame, text=str(btn), font=(SIGN_FONT), bg=SIGN_COLOR)
               line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=YPOS, height=H, width=NUM_W+1)
            else: #other cases
               line.append('')
               line[-1] = Label(line_frame, text=str(btn), font=(SIGN_FONT), bg=SIGN_COLOR)
               line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=YPOS, height=H, width=OPERATION_W)     
      if btn == i and btn == '2' and line[-1].winfo_x() < X_LINE_LIMIT: #for power 2
         if equal_state is True: #to power 2 answer straightaway
            ans()
            line.append('')
            line[-1] = Label(line_frame, text=str(btn), font=(POWER2_FONT), anchor=NE, bg=SIGN_COLOR)
            line[-1].place(x = ans_xpos, y=YPOS, height=H, width=POWER2_W) 
         else: #other cases      
            line.append('')
            line[-1] = Label(line_frame, text=str(btn), font=(POWER2_FONT), anchor=NE, bg=SIGN_COLOR)
            line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=YPOS, height=H, width=POWER2_W)
      if btn == i and btn == '√(' and line[-1].winfo_x() < X_LINE_LIMIT: #for sqrt
         if equal_state is True: #to sqrt answer straightaway
            ans()
            line.append('')
            line[-1] = Label(line_frame, text=str(btn), font=(SIGN_FONT), bg=SIGN_COLOR)
            line[-1].place(x = ans_xpos, y=YPOS, height=H, width=SQRT_W) 
         else: #other cases        
            line.append('')
            line[-1] = Label(line_frame, text=str(btn), font=(SIGN_FONT), bg=SIGN_COLOR)
            line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=YPOS, height=H, width=SQRT_W)
      if btn == i and btn == '(' and line[-1].winfo_x() < X_LINE_LIMIT: #for right bracket
         line.append('')
         line[-1] = Label(line_frame, text=str(btn), font=(SIGN_FONT), bg=SIGN_COLOR)
         line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=YPOS, height=H, width=BRACKET_W)
      if btn == i and btn == ')' and line[-1].winfo_x() < X_LINE_LIMIT: #for left bracket
         line.append('')
         line[-1] = Label(line_frame, text=str(btn), font=(SIGN_FONT), bg=SIGN_COLOR)
         line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=YPOS, height=H, width=BRACKET_W)
      if btn == i and btn in all_trigonometry_sign_list:
         line.append('')
         line[-1] = Label(line_frame, text=str(btn), font=(SIGN_FONT), bg=SIGN_COLOR)
         line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=YPOS, height=H, width=TRIGONOMETRY_W)
   #clear the line
   if btn == 'C':
      line_clear()
      equal_clear()
   terminal()
   #remove last sign
   if btn == '⌫':
      if equal_state is False:
         backspace()
      elif equal_state is True: 
         equal_clear()
      terminal()

#math logic function
def math(btn):

   #support variables
   global answer_label
   global error_label
   global equal_state
   global res_math
   global res_list
   global res_show
   global error_state
   
   #in case if user tries to add numbers to a power2
   try:
      if type(btn) == int and mathline[-1]=='**2':
         return
   except IndexError:
      pass
   #in case if user tries to add operation to a operation
   try:
      if btn in all_math_operation_sign_list and mathline[-1] in all_math_operation_sign_list and mathline[-1] != '**2':
         del mathline[-1]
   except IndexError:
      pass
   #in case if user tries to add trigonometry operation to unexpected sign
   try:
      if btn in all_trigonometry_sign_list and mathline[-1] not in all_math_operation_sign_list:
         if mathline[-1] != '(':
            return
   except:
      pass
   #in case if user adds sqrt to an integer
   try:
      if btn == 'sqrt(' and type(mathline[-1]) == int:
         btn = '*sqrt('
   except:
      pass

   #adds numbers and operations to the 'mathline' list
   for i in math_list:
      #adding signs to mathline
      if btn==i and line[-1].winfo_x() < X_LINE_LIMIT:
         mathline.append(btn)

   #count answer, display it on the window and clear all lists
   if btn == '=' and equal_state is False:
      equal_state = True
      res_string = ''.join([str(item) for item in mathline]) #transform 'mathline' list to a string
      #create answer label
      try:
         res_math = eval(res_string) #transform string into math expression to count the answer
         #check if answer has .0 float and transform it to an integer
         try:
            if res_math.is_integer() == True: 
               res_math = int(res_math)
         except:
            pass
         #round answer with lot of decimals numbers
         if type(res_math) == float: 
            res_math = round(res_math, ROUND_PERCISION)
         #transform answer to a list
         res_list = [str(i) for i in str(res_math)] 
         if len(res_list) > SCI_NOTATION_POINT:
            res_show = sci_notation(res_math)
         else:
            res_show = res_math
         answer_label = Label(line_frame, text=str(res_show), font=(ANSWER_FONT), bg=LINE_COLOR)
         answer_label.place(x=ANSWER_XPOS, y=ANSWER_YPOS, height=ANSWER_H, width=ANSWER_W)           
      except: #for any mistakes
         error_label = Label(line_frame, text='Syntax ERROR', font=(ERROR_FONT), bg=LINE_COLOR)
         error_label.place(x=ANSWER_XPOS, y=ANSWER_YPOS, height=ANSWER_H, width=ANSWER_W)
         error_state = True
         print('ERROR')

   #terminal info
   terminal()

#'ans' button function
def ans():
   global res_math
   global ans_btn_list
   global res_list
   global ans_xpos
   global error_state
   ans_xpos = INITIAL_ZERO_XPOS

   if equal_state is False:
      #convert res to a list
      ans_btn_list = [str(i) for i in str(res_show)]
      for i in ans_btn_list:
         animation(i)
         math(i)

   if equal_state is True:
      if error_state is False:
         #clear everything
         equal_clear()
         initial_zero.destroy()

         #convert res to a list
         ans_btn_list = [str(i) for i in str(res_show)]

         #adding signs to the line
         for i in ans_btn_list:
            line.append('')
            line[len(line)-1] = Label(line_frame, text=str(i), font=(SIGN_FONT), bg=SIGN_COLOR)
            line[len(line)-1].place(x = ans_xpos, y=YPOS, height=H, width=NUM_W)
            ans_xpos+=NUM_W
            mathline.append(i)
      elif error_state is True:
         equal_clear()
      try:
         ans_btn_list.clear()
      except NameError:
         pass
      res_math = None


   #terminal
   terminal()

#represent huge or small numbers in scientific notation
def sci_notation(big_result):
   global sci_res
   try:
      e = format(big_result, '.6e')
   except OverflowError:
      sci_res = 'ERROR'
      return sci_res
   a = e.split('e')
   b = a[0].replace('0','')
   sci_res = b + 'e' + a[1]
   return sci_res

#clear functions
def equal_clear():
   #remove everything from the line
   global equal_state
   global res
   global initial_zero
   global error_state
   if equal_state is True and error_state is False:
      try:
         answer_label.destroy()
         error_label.destroy()
      except NameError:
         pass 
      try:
         for i in range(len(line)):
            if len(line) > 1:
               line[-1].destroy()
               del line[-1]
               mathline.clear()
      except NameError:
         pass
         res = 0
      #return initial zero back to the line
      if initial_zero.winfo_exists() == 0:
         initial_zero = Label(line_frame, text='0', font=(SIGN_FONT), bg=SIGN_COLOR)
         initial_zero.place(x=INITIAL_ZERO_XPOS, y=YPOS, height=H, width=NUM_W)
   elif error_state is True:
      error_label.destroy()
      for i in range(len(line)):
         if len(line) > 1:
            line[-1].destroy()
            del line[-1]
            mathline.clear()
      #return initial zero back to the line
      if initial_zero.winfo_exists() == 0:
         initial_zero = Label(line_frame, text='0', font=(SIGN_FONT), bg=SIGN_COLOR)
         initial_zero.place(x=INITIAL_ZERO_XPOS, y=YPOS, height=H, width=NUM_W)
      
   #bring equal_state back to default so new sign inputs don't make mistakes
   equal_state = False
   error_state = False
def line_clear():
   global res
   global initial_zero
   for i in range(len(line)):
      if len(line) > 1:
         line[-1].destroy()
         del line[-1]
         mathline.clear()
   res = 0
   #return initial zero back to the line
   if initial_zero.winfo_exists() == 0:
      initial_zero = Label(line_frame, text='0', font=(SIGN_FONT), bg=LINE_COLOR)
      initial_zero.place(x=INITIAL_ZERO_XPOS, y=YPOS, height=H, width=NUM_W)
def backspace():
   global initial_zero
   #remove last sign from the line
   if len(line) > 1:
      line[-1].destroy()
      del line[-1]
   if len(mathline) > 0:
      del mathline[-1]
   if len(line) == 1:
      if initial_zero.winfo_exists() == 0:
         initial_zero = Label(line_frame, text='0', font=(SIGN_FONT), bg=SIGN_COLOR)
         initial_zero.place(x=INITIAL_ZERO_XPOS, y=YPOS, height=H, width=NUM_W)

#window close function
def win_close(e): 
   root.destroy()

#convert path to image and resize it if needed
def img(img_name, width=0, lenght=0):
   #convert script path to image path
   def img_folder_path():
      path = __file__
      path_replaced = path.replace("\\", "/")
      path_transformed = path_replaced.replace('/calcapp.py', '/images/')
      return path_transformed

   image_path = img_folder_path() + img_name
   img_raw = Image.open(image_path)
   if width!=0 and lenght!=0:
      img_resized = img_raw.resize((width, lenght))
      img_done = ImageTk.PhotoImage(img_resized)
   else:
      img_done = ImageTk.PhotoImage(img_raw)
   return img_done

#images
bg_img = img('background.jpg', 400, 630) #background
btn_1_img = img('btn_1.jpg') #btn_1
btn_2_img = img('btn_2.jpg') #btn_1

#frame for the window
frame = Frame(root, bg=BG_COLOR)
frame.place(relwidth=1, relheight=1)
#canvas for the answer window
line_canvas = Canvas(root)
line_canvas.place(x=0, y=LINE_YPOS, height=LINE_H, width=LINE_W)
#frame for the answer window
line_frame = Frame(root, bg=LINE_COLOR)
line_frame.place(x=0, y=LINE_YPOS, height=LINE_H, width=LINE_W)
#small black line above buttons for design adjustment
black_line = Label(root, bg='black')
black_line.place(x=BLACK_LINE_XPOS, y=BTN_ROW_6-BLACK_LINE_HEIGHT, height=BLACK_LINE_HEIGHT, width=LINE_W)
#empty support label for signs on the line for them to start from
start_label = Label(line_frame, bg=SIGN_COLOR)
start_label.place(x=START_LABEL_XPOS, y=YPOS, height=0, width=0)
line.append(start_label)
#zero which stays initially on the line
global initial_zero
initial_zero = Label(line_frame, text='0', font=(SIGN_FONT), bg=LINE_COLOR)
initial_zero.place(x=INITIAL_ZERO_XPOS, y=YPOS, height=H, width=NUM_W)

#button bind functions
def button_hover(name):
   name['bg'] = BTN_HOVER_COLOR
def button_hover_leave (name):
   name['bg'] = BTN_COLOR
def bind(btn_name, mode, sign, mathsign, keyboard1='None', keyboard2='None'):
   #make button highligh
   btn_name.bind("<Enter>", lambda name: button_hover(name = btn_name))
   btn_name.bind("<Leave>", lambda name: button_hover_leave(name = btn_name))
   #bind action to keyboard key
   if mode == 'math':
      if keyboard1 != 'None':
         root.bind(keyboard1, lambda btn: math(btn=mathsign))
      if keyboard2 != 'None':
         root.bind(keyboard2, lambda btn: math(btn=mathsign))
   elif mode == 'both':
      if keyboard1 != 'None':
         root.bind(keyboard1, lambda btn: [animation(btn=sign), math(btn=mathsign)])
      if keyboard2 != 'None':
         root.bind(keyboard2, lambda btn: [animation(btn=sign), math(btn=mathsign)])

mode_state = 1
#buttons of mode 1
def buttons_mode1():
   global btn_power2
   global btn_sqroot
   #add new buttons
   btn_power2 = Button(frame, text='x^2', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation('2'), math('**2')])
   btn_power2.place (x=BTN_COLUMN_2, y=BTN_ROW_5, height=BTN_H, width=BTN_W)
   btn_power2.bind("<Enter>", lambda name: button_hover(name = btn_power2))
   btn_power2.bind("<Leave>", lambda name: button_hover_leave(name = btn_power2))
   btn_sqroot = Button(frame, text='√x', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation('√('), math('sqrt(')])
   btn_sqroot.place (x=BTN_COLUMN_3, y=BTN_ROW_5, height=BTN_H, width=BTN_W)
   btn_sqroot.bind("<Enter>", lambda name: button_hover(name = btn_sqroot))
   btn_sqroot.bind("<Leave>", lambda name: button_hover_leave(name = btn_sqroot))
#buttons of mode 2
def buttons_mode2():
   global btn_sin
   global btn_cos
   #add new buttons
   btn_sin = Button(frame, text='sin', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation('sin('), math('sin(')])
   btn_sin.place (x=BTN_COLUMN_2, y=BTN_ROW_5, height=BTN_H, width=BTN_W)
   btn_sin.bind("<Enter>", lambda name: button_hover(name = btn_sin))
   btn_sin.bind("<Leave>", lambda name: button_hover_leave(name = btn_sin))
   btn_cos = Button(frame, text='cos', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation('cos('), math('cos(')])
   btn_cos.place (x=BTN_COLUMN_3, y=BTN_ROW_5, height=BTN_H, width=BTN_W)
   btn_cos.bind("<Enter>", lambda name: button_hover(name = btn_cos))
   btn_cos.bind("<Leave>", lambda name: button_hover_leave(name = btn_cos))
#mode button functionality
def mode_switch():
   global mode_state
   if mode_state == 1:
      #destroy previous mode answers
      btn_power2.destroy()
      btn_sqroot.destroy()
      buttons_mode2()
      mode_state = 2
      return
   if mode_state == 2:
      #destroy previous mode answers
      btn_sin.destroy()
      btn_cos.destroy()
      buttons_mode1()
      mode_state = 1
      return

#buttons
buttons_mode1()
btn_1 = Button(frame, text='1', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation(1), math(1)])
btn_1.place(x=BTN_COLUMN_1, y=BTN_ROW_2, height=BTN_H, width=BTN_W)
bind(btn_1, 'both', 1, 1, '1')
btn_2 = Button(frame, text='2', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation(2), math(2)])
btn_2.place(x=BTN_COLUMN_2, y=BTN_ROW_2, height=BTN_H, width=BTN_W)
bind(btn_2, 'both', 2, 2, '2')
btn_3 = Button(frame, text='3', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation(3), math(3)])
btn_3.place (x=BTN_COLUMN_3, y=BTN_ROW_2, height=BTN_H, width=BTN_W)
bind(btn_3, 'both', 3, 3, '3')
btn_4 = Button(frame, text='4', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation(4), math(4)])
btn_4.place (x=BTN_COLUMN_1, y=BTN_ROW_3, height=BTN_H, width=BTN_W)
bind(btn_4, 'both', 4, 4, '4')
btn_5 = Button(frame, text='5', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation(5), math(5)])
btn_5.place (x=BTN_COLUMN_2, y=BTN_ROW_3, height=BTN_H, width=BTN_W)
bind(btn_5, 'both', 5, 5, '5')
btn_6 = Button(frame, text='6', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation(6), math(6)])
btn_6.place (x=BTN_COLUMN_3, y=BTN_ROW_3, height=BTN_H, width=BTN_W)
bind(btn_6, 'both', 6, 6, '6')
btn_7 = Button(frame, text='7', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation(7), math(7)])
btn_7.place (x=BTN_COLUMN_1, y=BTN_ROW_4, height=BTN_H, width=BTN_W)
bind(btn_7, 'both', 7, 7, '7')
btn_8 = Button(frame, text='8', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation(8), math(8)])
btn_8.place (x=BTN_COLUMN_2, y=BTN_ROW_4, height=BTN_H, width=BTN_W)
bind(btn_8, 'both', 8, 8, '8')
btn_9 = Button(frame, text='9', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation(9), math(9)])
btn_9.place (x=BTN_COLUMN_3, y=BTN_ROW_4, height=BTN_H, width=BTN_W)
bind(btn_9, 'both', 9, 9, '9')
btn_0 = Button(frame, text='0', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation(0), math(0)])
btn_0.place (x=BTN_COLUMN_2, y=BTN_ROW_1, height=BTN_H, width=BTN_W)
bind(btn_0, 'both', 0, 0, '0')
btn_plus = Button(frame, text='+', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation('+'), math('+')])
btn_plus.place (x=BTN_COLUMN_4, y=BTN_ROW_2, height=BTN_H, width=BTN_W)
bind(btn_plus, 'both', '+', '+', '+')
btn_minus = Button(frame, text='-', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation('-'), math('-')])
btn_minus.place (x=BTN_COLUMN_4, y=BTN_ROW_3, height=BTN_H, width=BTN_W)
bind(btn_minus, 'both', '-', '-', '-')
btn_multiplication = Button(frame, text='×', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation('×'), math('*')])
btn_multiplication.place (x=BTN_COLUMN_4, y=BTN_ROW_4, height=BTN_H, width=BTN_W)
bind(btn_multiplication, 'both', '×', '*', '*')
btn_division = Button(frame, text='÷', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation('÷'), math('/')])
btn_division.place (x=BTN_COLUMN_4, y=BTN_ROW_5, height=BTN_H, width=BTN_W)
bind(btn_division, 'both', '÷', '/', '/')
btn_equal = Button(frame, text='=', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: math('='))
btn_equal.place (x=BTN_COLUMN_4, y=BTN_ROW_1, height=BTN_H, width=BTN_W)
bind(btn_equal, 'math', '=', '=', '=', '<Return>')
btn_point = Button(frame, text='.', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation('.'), math('.')])
btn_point.place (x=BTN_COLUMN_3, y=BTN_ROW_1, height=BTN_H, width=BTN_W)
bind(btn_point, 'both', '.', '.', '.')
btn_backspace = Button(frame, text='⌫', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation('⌫')])
btn_backspace.place (x=BTN_COLUMN_4, y=BTN_ROW_6, height=BTN_H, width=BTN_W)
root.bind('<BackSpace>', lambda btn: animation(btn='⌫'))
btn_backspace.bind("<Enter>", lambda name: button_hover(name = btn_backspace))
btn_backspace.bind("<Leave>", lambda name: button_hover_leave(name = btn_backspace))
btn_clear = Button(frame, text='C', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation('C'), math('C')])
btn_clear.place (x=BTN_COLUMN_3, y=BTN_ROW_6, height=BTN_H, width=BTN_W)
bind(btn_clear, 'both', 'C', 'C', 'c', '<Delete>')
btn_Ans = Button(frame, text='Ans', bg=BTN_COLOR, font=(BTN_FONT), command=ans)
btn_Ans.place (x=BTN_COLUMN_1, y=BTN_ROW_1, height=BTN_H, width=BTN_W)
btn_Ans.bind("<Enter>", lambda name: button_hover(name = btn_Ans))
btn_Ans.bind("<Leave>", lambda name: button_hover_leave(name = btn_Ans))
btn_bracket_right = Button(frame, text='(', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation('('), math('(')])
btn_bracket_right.place (x=BTN_COLUMN_1, y=BTN_ROW_6, height=BTN_H, width=BTN_W)
bind(btn_bracket_right, 'both', '(', '(', '<(>')
btn_bracket_left = Button(frame, text=')', bg=BTN_COLOR, font=(BTN_FONT), command=lambda: [animation(')'), math(')')])
btn_bracket_left.place (x=BTN_COLUMN_2, y=BTN_ROW_6, height=BTN_H, width=BTN_W)
bind(btn_bracket_left, 'both', ')', ')', '<)>')
btn_mode = Button(frame, text='mode', bg=BTN_COLOR, font=(BTN_FONT), command=mode_switch)
btn_mode.place (x=BTN_COLUMN_1, y=BTN_ROW_5, height=BTN_H, width=BTN_W)
btn_mode.bind("<Enter>", lambda name: button_hover(name = btn_mode))
btn_mode.bind("<Leave>", lambda name: button_hover_leave(name = btn_mode))
root.bind('<Escape>', win_close)

print('--------------------------------------------------------------------')
terminal()

#making window stay opened
root.mainloop()

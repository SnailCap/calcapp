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
sign_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', '-', '×', '÷', '2', '^1/2', '.', '(', ')', 'sin(', 'cos('] #list of all signs to show on the line
math_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', '-', '*', '/', '**2', '**(1/2)', '.', '(', ')', 'sin(', 'cos('] #list of all signs that can be added to the 'mathline' list
standart_operation_sign_list = ['+', '-', '×', '÷'] #list of standart operation signs
all_animation_operation_sign_list = ['+', '-', '×', '÷', '2', '^1/2'] #list of operation signs for animation function
all_math_operation_sign_list = ['+', '-', '*', '/', '**2', '**(1/2)'] #list of operation signs for math function
all_trigonometry_sign_list = ['sin(', 'cos(']
line = [] #list of elements (labels) on the line
mathline = []
global equal_state
equal_state = 0
global x

global error_statek0
error_state = 0

#COLORS
bg_color = 'white'
line_color = 'white'
sign_color = line_color
btn_color = 'white'
btn_hover_color = '#DFDFDF'
#SIZE AND POSITION OF BLACK LINE
black_line_height = 1
black_line_xpos = 0
#SIZE AND POSITION OF THE LINE
line_ypos = 154
line_h = 80
line_w = 400
#SIZES AND POSITIONS OF ELEMENTS ON THE LINE
line_elements_size_multiplier = 1.4 #to adjust for the font size increase
ypos=10 #default y
h=30 #default objects height
num_w=8 * line_elements_size_multiplier #width of numbers
point_w=6 * line_elements_size_multiplier #width of point
operation_w=22 * line_elements_size_multiplier #width of operation signs
power2_w=8 * line_elements_size_multiplier #width of power 2
power2_font='Times', 9
sqrt_w = 30 * line_elements_size_multiplier #width of square root
bracket_w = 6 * line_elements_size_multiplier #width of brackets
trigonometry_w = 37 #width of trigonometry functions (sin, cos etc)
sign_font_size = 14
sign_font_font = 'Times'
sign_font = sign_font_font, sign_font_size
#ANSWER LINE
answer_xpos = 230
answer_ypos = 42
answer_h = 40
answer_w = 170
answer_font = sign_font_font, sign_font_size
error_font = 'Helvetica', 14
#BUTTONS
btn_w = 100 #width of buttons
btn_h = 66 #high of buttons
btn_font = 'Helvetica', 12
btn_column_1 = 0
btn_column_2 = 100
btn_column_3 = 200
btn_column_4 = 300
btn_row_1 = 564
btn_row_2 = 498
btn_row_3 = 432
btn_row_4 = 366
btn_row_5 = 300
btn_row_6 = 234

start_label_xpos = 10 #point from where the signs on the line are being created
initial_zero_xpos = 11 #position of initial zero
x_line_limit = 350 #limits the amount of signs can be added to the line in pixels
sci_notation_point = 15 #point from which amount of digits in the answer programm converts number to a scientific notation
round_precision = 12 #rounding presicion of float answers

#print useful stuff in terminal
print('--------------------------------------------------------------------')
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
   if equal_state == 1:
      if btn in standart_operation_sign_list or btn == '^2' or btn == '^1/2' or btn == '.':
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
      if btn == i and type(i) == int and line[-1].winfo_x() < x_line_limit: #for numbers
         line.append('')
         line[-1] = Label(line_frame, text=str(btn), font=(sign_font), bg=sign_color)
         line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=ypos, height=h, width=num_w)
      if btn == i and btn == '.' and line[-1].winfo_x() < x_line_limit: #for point
         if equal_state == 1: #to operate answer straightaway
            ans()
            line.append('')
            line[-1] = Label(line_frame, text=str(btn), font=(sign_font), bg=sign_color)
            line[-1].place(x = ans_xpos, y=ypos, height=h, width=point_w)         
         else:
            if len(mathline) == 0: #for adding point to initial 0 on the line
               animation(0)
               math(0)
               line.append('')
               line[-1] = Label(line_frame, text=str(btn), font=(sign_font), anchor='e', bg=sign_color)
               line[-1].place(x = initial_zero_xpos + num_w, y=ypos, height=h, width=point_w)
            else: #all other cases
               line.append('')
               line[-1] = Label(line_frame, text=str(btn), font=(sign_font), anchor='e', bg=sign_color)
               line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=ypos, height=h, width=point_w)
      if btn == i and btn in standart_operation_sign_list and line[-1].winfo_x() < x_line_limit: #for operation signs
         if equal_state == 1: #to operate answer straightaway
            ans()
            line.append('')
            line[-1] = Label(line_frame, text=str(btn), font=(sign_font), bg=sign_color)
            line[-1].place(x = ans_xpos, y=ypos, height=h, width=operation_w)
         else:
            if equal_state == 0 and len(line) == 1: #if operation sign is the first appearing on the line, so it will be the same size as a digit
               line.append('')
               line[-1] = Label(line_frame, text=str(btn), font=(sign_font), bg=sign_color)
               line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=ypos, height=h, width=num_w+1)
            else: #other cases
               line.append('')
               line[-1] = Label(line_frame, text=str(btn), font=(sign_font), bg=sign_color)
               line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=ypos, height=h, width=operation_w)     
      if btn == i and btn == '2' and line[-1].winfo_x() < x_line_limit: #for power 2
         if equal_state == 1: #to power 2 answer straightaway
            ans()
            line.append('')
            line[-1] = Label(line_frame, text=str(btn), font=(power2_font), anchor=NE, bg=sign_color)
            line[-1].place(x = ans_xpos, y=ypos, height=h, width=power2_w) 
         else: #other cases      
            line.append('')
            line[-1] = Label(line_frame, text=str(btn), font=(power2_font), anchor=NE, bg=sign_color)
            line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=ypos, height=h, width=power2_w)
      if btn == i and btn == '^1/2' and line[-1].winfo_x() < x_line_limit: #for sqrt
         if equal_state == 1: #to sqrt answer straightaway
            ans()
            line.append('')
            line[-1] = Label(line_frame, text=str(btn), font=(sign_font), bg=sign_color)
            line[-1].place(x = ans_xpos, y=ypos, height=h, width=sqrt_w) 
         else: #other cases        
            line.append('')
            line[-1] = Label(line_frame, text=str(btn), font=(sign_font), bg=sign_color)
            line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=ypos, height=h, width=sqrt_w)
      if btn == i and btn == '(' and line[-1].winfo_x() < x_line_limit: #for right bracket
         line.append('')
         line[-1] = Label(line_frame, text=str(btn), font=(sign_font), bg=sign_color)
         line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=ypos, height=h, width=bracket_w)
      if btn == i and btn == ')' and line[-1].winfo_x() < x_line_limit: #for left bracket
         line.append('')
         line[-1] = Label(line_frame, text=str(btn), font=(sign_font), bg=sign_color)
         line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=ypos, height=h, width=bracket_w)
      if btn == i and btn in all_trigonometry_sign_list:
         line.append('')
         line[-1] = Label(line_frame, text=str(btn), font=(sign_font), bg=sign_color)
         line[-1].place(x = line[-2].winfo_x() + line[-2].winfo_width(), y=ypos, height=h, width=trigonometry_w)
   #clear the line
   if btn == 'C':
      line_clear()
      equal_clear()
   terminal()
   #remove last sign
   if btn == '⌫':
      if equal_state == 0:
         backspace()
      elif equal_state == 1: 
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

   #adds numbers and operations to the 'mathline' list
   for i in math_list:
      #adding signs to mathline
      if btn==i and line[-1].winfo_x() < x_line_limit:
         mathline.append(btn)

   #count answer, display it on the window and clear all lists
   if btn == '=' and equal_state == 0:
      equal_state = 1
      res_string = ''.join([str(item) for item in mathline]) #transform 'mathline' list to a string
      #create answer label
      try:
         res_math = eval(res_string) #transform string into math expression to count the answer
         if type(res_math) == float:
            res_math = round(res_math, round_precision)
         res_list = [str(i) for i in str(res_math)] #transform answer to a list
         if len(res_list) > sci_notation_point:
            res_show = sci_notation(res_math)
         else:
            res_show = res_math
         answer_label = Label(line_frame, text=str(res_show), font=(answer_font), bg=line_color)
         answer_label.place(x=answer_xpos, y=answer_ypos, height=answer_h, width=answer_w)           
      except: #for any mistakes
         error_label = Label(line_frame, text='Syntax ERROR', font=(error_font), bg=line_color)
         error_label.place(x=answer_xpos, y=answer_ypos, height=answer_h, width=answer_w)
         error_state = 1
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
   ans_xpos = initial_zero_xpos

   if equal_state == 0:
      #convert res to a list
      ans_btn_list = [str(i) for i in str(res_show)]
      for i in ans_btn_list:
         animation(i)
         math(i)

   if equal_state == 1:
      if error_state == 0:
         #clear everything
         equal_clear()
         initial_zero.destroy()

         #convert res to a list
         ans_btn_list = [str(i) for i in str(res_show)]

         #adding signs to the line
         for i in ans_btn_list:
            line.append('')
            line[len(line)-1] = Label(line_frame, text=str(i), font=(sign_font), bg=sign_color)
            line[len(line)-1].place(x = ans_xpos, y=ypos, height=h, width=num_w)
            ans_xpos+=num_w
            mathline.append(i)
      elif error_state == 1:
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
   if equal_state == 1 and error_state == 0:
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
         initial_zero = Label(line_frame, text='0', font=(sign_font), bg=sign_color)
         initial_zero.place(x=initial_zero_xpos, y=ypos, height=h, width=num_w)
   elif error_state == 1:
      error_label.destroy()
      for i in range(len(line)):
         if len(line) > 1:
            line[-1].destroy()
            del line[-1]
            mathline.clear()
      #return initial zero back to the line
      if initial_zero.winfo_exists() == 0:
         initial_zero = Label(line_frame, text='0', font=(sign_font), bg=sign_color)
         initial_zero.place(x=initial_zero_xpos, y=ypos, height=h, width=num_w)
      
   #bring equal_state back to default so new sign inputs don't make mistakes
   equal_state = 0
   error_state = 0
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
      initial_zero = Label(line_frame, text='0', font=(sign_font), bg=line_color)
      initial_zero.place(x=initial_zero_xpos, y=ypos, height=h, width=num_w)
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
         initial_zero = Label(line_frame, text='0', font=(sign_font), bg=sign_color)
         initial_zero.place(x=initial_zero_xpos, y=ypos, height=h, width=num_w)

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
frame = Frame(root, bg=bg_color)
frame.place(relwidth=1, relheight=1)
#canvas for the answer window
line_canvas = Canvas(root)
line_canvas.place(x=0, y=line_ypos, height=line_h, width=line_w)
#frame for the answer window
line_frame = Frame(root, bg=line_color)
line_frame.place(x=0, y=line_ypos, height=line_h, width=line_w)
#small black line above buttons for design adjustment
black_line = Label(root, bg='black')
black_line.place(x=black_line_xpos, y=btn_row_6-black_line_height, height=black_line_height, width=line_w)
#empty support label for signs on the line for them to start from
start_label = Label(line_frame, bg=sign_color)
start_label.place(x=start_label_xpos, y=ypos, height=0, width=0)
line.append(start_label)
#zero which stays initially on the line
global initial_zero
initial_zero = Label(line_frame, text='0', font=(sign_font), bg=line_color)
initial_zero.place(x=initial_zero_xpos, y=ypos, height=h, width=num_w)

#button bind functions
def button_hover(name):
   name['bg'] = btn_hover_color
def button_hover_leave (name):
   name['bg'] = btn_color
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
   btn_power2 = Button(frame, text='x^2', bg=btn_color, font=(btn_font), command=lambda: [animation('2'), math('**2')])
   btn_power2.place (x=btn_column_2, y=btn_row_5, height=btn_h, width=btn_w)
   btn_power2.bind("<Enter>", lambda name: button_hover(name = btn_power2))
   btn_power2.bind("<Leave>", lambda name: button_hover_leave(name = btn_power2))
   btn_sqroot = Button(frame, text='√x', bg=btn_color, font=(btn_font), command=lambda: [animation('^1/2'), math('**(1/2)')])
   btn_sqroot.place (x=btn_column_3, y=btn_row_5, height=btn_h, width=btn_w)
   btn_sqroot.bind("<Enter>", lambda name: button_hover(name = btn_sqroot))
   btn_sqroot.bind("<Leave>", lambda name: button_hover_leave(name = btn_sqroot))
#buttons of mode 2
def buttons_mode2():
   global btn_sin
   global btn_cos
   #add new buttons
   btn_sin = Button(frame, text='sin', bg=btn_color, font=(btn_font), command=lambda: [animation('sin('), math('sin(')])
   btn_sin.place (x=btn_column_2, y=btn_row_5, height=btn_h, width=btn_w)
   btn_sin.bind("<Enter>", lambda name: button_hover(name = btn_sin))
   btn_sin.bind("<Leave>", lambda name: button_hover_leave(name = btn_sin))
   btn_cos = Button(frame, text='cos', bg=btn_color, font=(btn_font), command=lambda: [animation('cos('), math('cos(')])
   btn_cos.place (x=btn_column_3, y=btn_row_5, height=btn_h, width=btn_w)
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
btn_1 = Button(frame, text='1', bg=btn_color, font=(btn_font), command=lambda: [animation(1), math(1)])
btn_1.place(x=btn_column_1, y=btn_row_2, height=btn_h, width=btn_w)
bind(btn_1, 'both', 1, 1, '1')
btn_2 = Button(frame, text='2', bg=btn_color, font=(btn_font), command=lambda: [animation(2), math(2)])
btn_2.place(x=btn_column_2, y=btn_row_2, height=btn_h, width=btn_w)
bind(btn_2, 'both', 2, 2, '2')
btn_3 = Button(frame, text='3', bg=btn_color, font=(btn_font), command=lambda: [animation(3), math(3)])
btn_3.place (x=btn_column_3, y=btn_row_2, height=btn_h, width=btn_w)
bind(btn_3, 'both', 3, 3, '3')
btn_4 = Button(frame, text='4', bg=btn_color, font=(btn_font), command=lambda: [animation(4), math(4)])
btn_4.place (x=btn_column_1, y=btn_row_3, height=btn_h, width=btn_w)
bind(btn_4, 'both', 4, 4, '4')
btn_5 = Button(frame, text='5', bg=btn_color, font=(btn_font), command=lambda: [animation(5), math(5)])
btn_5.place (x=btn_column_2, y=btn_row_3, height=btn_h, width=btn_w)
bind(btn_5, 'both', 5, 5, '5')
btn_6 = Button(frame, text='6', bg=btn_color, font=(btn_font), command=lambda: [animation(6), math(6)])
btn_6.place (x=btn_column_3, y=btn_row_3, height=btn_h, width=btn_w)
bind(btn_6, 'both', 6, 6, '6')
btn_7 = Button(frame, text='7', bg=btn_color, font=(btn_font), command=lambda: [animation(7), math(7)])
btn_7.place (x=btn_column_1, y=btn_row_4, height=btn_h, width=btn_w)
bind(btn_7, 'both', 7, 7, '7')
btn_8 = Button(frame, text='8', bg=btn_color, font=(btn_font), command=lambda: [animation(8), math(8)])
btn_8.place (x=btn_column_2, y=btn_row_4, height=btn_h, width=btn_w)
bind(btn_8, 'both', 8, 8, '8')
btn_9 = Button(frame, text='9', bg=btn_color, font=(btn_font), command=lambda: [animation(9), math(9)])
btn_9.place (x=btn_column_3, y=btn_row_4, height=btn_h, width=btn_w)
bind(btn_9, 'both', 9, 9, '9')
btn_0 = Button(frame, text='0', bg=btn_color, font=(btn_font), command=lambda: [animation(0), math(0)])
btn_0.place (x=btn_column_2, y=btn_row_1, height=btn_h, width=btn_w)
bind(btn_0, 'both', 0, 0, '0')
btn_plus = Button(frame, text='+', bg=btn_color, font=(btn_font), command=lambda: [animation('+'), math('+')])
btn_plus.place (x=btn_column_4, y=btn_row_2, height=btn_h, width=btn_w)
bind(btn_plus, 'both', '+', '+', '+')
btn_minus = Button(frame, text='-', bg=btn_color, font=(btn_font), command=lambda: [animation('-'), math('-')])
btn_minus.place (x=btn_column_4, y=btn_row_3, height=btn_h, width=btn_w)
bind(btn_minus, 'both', '-', '-', '-')
btn_multiplication = Button(frame, text='×', bg=btn_color, font=(btn_font), command=lambda: [animation('×'), math('*')])
btn_multiplication.place (x=btn_column_4, y=btn_row_4, height=btn_h, width=btn_w)
bind(btn_multiplication, 'both', '×', '*', '*')
btn_division = Button(frame, text='÷', bg=btn_color, font=(btn_font), command=lambda: [animation('÷'), math('/')])
btn_division.place (x=btn_column_4, y=btn_row_5, height=btn_h, width=btn_w)
bind(btn_division, 'both', '÷', '/', '/')
btn_equal = Button(frame, text='=', bg=btn_color, font=(btn_font), command=lambda: math('='))
btn_equal.place (x=btn_column_4, y=btn_row_1, height=btn_h, width=btn_w)
bind(btn_equal, 'math', '=', '=', '=', '<Return>')
btn_point = Button(frame, text='.', bg=btn_color, font=(btn_font), command=lambda: [animation('.'), math('.')])
btn_point.place (x=btn_column_3, y=btn_row_1, height=btn_h, width=btn_w)
bind(btn_point, 'both', '.', '.', '.')
btn_backspace = Button(frame, text='⌫', bg=btn_color, font=(btn_font), command=lambda: [animation('⌫')])
btn_backspace.place (x=btn_column_4, y=btn_row_6, height=btn_h, width=btn_w)
root.bind('<BackSpace>', lambda btn: animation(btn='⌫'))
btn_backspace.bind("<Enter>", lambda name: button_hover(name = btn_backspace))
btn_backspace.bind("<Leave>", lambda name: button_hover_leave(name = btn_backspace))
btn_clear = Button(frame, text='C', bg=btn_color, font=(btn_font), command=lambda: [animation('C'), math('C')])
btn_clear.place (x=btn_column_3, y=btn_row_6, height=btn_h, width=btn_w)
bind(btn_clear, 'both', 'C', 'C', 'c', '<Delete>')
btn_Ans = Button(frame, text='Ans', bg=btn_color, font=(btn_font), command=ans)
btn_Ans.place (x=btn_column_1, y=btn_row_1, height=btn_h, width=btn_w)
btn_Ans.bind("<Enter>", lambda name: button_hover(name = btn_Ans))
btn_Ans.bind("<Leave>", lambda name: button_hover_leave(name = btn_Ans))
btn_bracket_right = Button(frame, text='(', bg=btn_color, font=(btn_font), command=lambda: [animation('('), math('(')])
btn_bracket_right.place (x=btn_column_1, y=btn_row_6, height=btn_h, width=btn_w)
bind(btn_bracket_right, 'both', '(', '(', '<(>')
btn_bracket_left = Button(frame, text=')', bg=btn_color, font=(btn_font), command=lambda: [animation(')'), math(')')])
btn_bracket_left.place (x=btn_column_2, y=btn_row_6, height=btn_h, width=btn_w)
bind(btn_bracket_left, 'both', ')', ')', '<)>')
btn_mode = Button(frame, text='mode', bg=btn_color, font=(btn_font), command=mode_switch)
btn_mode.place (x=btn_column_1, y=btn_row_5, height=btn_h, width=btn_w)
btn_mode.bind("<Enter>", lambda name: button_hover(name = btn_mode))
btn_mode.bind("<Leave>", lambda name: button_hover_leave(name = btn_mode))
root.bind('<Escape>', win_close)

terminal()

#making window stay opened
root.mainloop()

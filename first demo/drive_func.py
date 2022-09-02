import pygame
import pygame
import numpy as np
def car_control(keyboard_event, ser, run, save_flag, left_sig_text, right_sig_text, horn_text):
    for event in keyboard_event:
        # print(event)
        if event.type == pygame.QUIT:#----------------------------------------判斷視窗是否被關掉
            run = False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w:
                ser.write(b'w\n')
            if event.key==pygame.K_a:
                ser.write(b'a\n')
            if event.key==pygame.K_s:
                ser.write(b's\n')
            if event.key==pygame.K_d:
                ser.write(b'd\n')
            if event.key==pygame.K_UP:
                ser.write(b'h\n')
                horn_text = 'horn activated'
            if event.key==pygame.K_LSHIFT:
                ser.write(b'yy\n')
#------------------------------------------------------------------------------------------------方向燈都是按下來改變狀態
            if event.key==pygame.K_LEFT:
                if left_sig_text == '':
                    left_sig_text = 'left turn sig on'
                    ser.write(b'l\n')
                else:
                    left_sig_text = ''
                    ser.write(b'nl\n')
            if event.key==pygame.K_RIGHT:
                if right_sig_text == '':
                    right_sig_text = 'right turn sig on'
                    ser.write(b'r\n')#---------------------------改變方向燈狀態為“有”
                else:
                    right_sig_text = ''
                    ser.write(b'nr\n')#-------------------------改變方向燈狀態為“無”
#---------------------------------------------------------------------------------------------------方向燈都是按下來改變狀態
            if event.key==pygame.K_f:
                save_flag = True 

        elif event.type==pygame.KEYUP:
            if event.key==pygame.K_w:              
                ser.write(b'nw\n')
            if event.key==pygame.K_a:             
                ser.write(b'na\n')
            if event.key==pygame.K_s:           
                ser.write(b'ns\n')
            if event.key==pygame.K_d:            
                ser.write(b'nd\n')
            if event.key==pygame.K_UP: 
                ser.write(b'nh\n')
                horn_text = ''
            if event.key==pygame.K_LSHIFT:
                ser.write(b'xx\n')
    return run, save_flag, left_sig_text, right_sig_text, horn_text





def get_new_text(keys, save_flag):
    moving_direction_text = ''
    record_text = ''
   
    if keys[pygame.K_w] and keys[pygame.K_a] and keys[pygame.K_d]:#-----按下wad
        moving_direction_text = 'forward'
        # ser.write(b'w\n')
    elif keys[pygame.K_s] and keys[pygame.K_a] and keys[pygame.K_d]:#-----按下sad
        moving_direction_text = 'backward'
        # ser.write(b'b\n')
    elif keys[pygame.K_w] and keys[pygame.K_a]:#----------------------按下wa
        moving_direction_text = 'forward left'
        # ser.write(b'fl\n')
    elif keys[pygame.K_w] and keys[pygame.K_d]:#----------------------按下wd
        moving_direction_text = 'forward right'
        # ser.write(b'fr\n')
    elif keys[pygame.K_a] and keys[pygame.K_d]:#----------------------按下ad
         moving_direction_text = ''
    elif keys[pygame.K_s] and keys[pygame.K_a]:#----------------------按下sa
        moving_direction_text = 'backward left'
        # ser.write(b'bl\n')
    elif keys[pygame.K_s] and keys[pygame.K_d]:#----------------------按下sd
        moving_direction_text = 'backward right'
        # ser.write(b'br\n')
    elif keys[pygame.K_w]:
        moving_direction_text = 'forward'
        # ser.write(b'f\n')
    elif keys[pygame.K_a]:
        moving_direction_text = 'left'
        # ser.write(b'l\n')
    elif keys[pygame.K_s]:
        moving_direction_text = 'backward'
        # ser.write(b'b\n')
    elif keys[pygame.K_d]:
        moving_direction_text = 'right'
        # ser.write(b'r\n')
    if save_flag:
        record_text = 'recording'
    
    return moving_direction_text, record_text




def add_horn_turnsig(new_float_array, horn_text, left_sig_text, right_sig_text):
    if horn_text == 'horn activated':
        new_float_array = np.append(new_float_array, 1)#---------------------在陣列後加個喇叭狀態
    else:
        new_float_array = np.append(new_float_array, 0)
    if left_sig_text == 'left turn sig on':
        new_float_array = np.append(new_float_array, 1)
    else:
        new_float_array = np.append(new_float_array, 0)
    if right_sig_text == 'right turn sig on':
        new_float_array = np.append(new_float_array, 1)
    else:
        new_float_array = np.append(new_float_array, 0)
    return new_float_array
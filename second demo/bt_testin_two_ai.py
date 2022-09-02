import pygame
import serial
import cv2
from time import sleep
from time import time
import numpy as np
from drive_func2 import car_control
from drive_func2 import get_new_text
from drive_func2 import add_horn_turnsig
from video_func2 import record
from tensorflow import keras
from tensorflow.keras.models import load_model#import 要這樣打才可以跑   hello3
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def change_str_float_array(feedback):
    a = feedback.split(',')
    a.remove('\n')
    b = np.array(a)
    b = b.astype('float')
    return b
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
model_long = load_model('model97.h5')#--------------------------載入模型
model_short = load_model('model_short95.h5')#--------------------------載入模型
file_name = input("enter file name to write into:")
COM_number = input("enter com port number:")
cam_number = input("enter cam number:")
video_counter = int(input("enter the first video number:"))
COM_PORT = 'COM' + COM_number  # -------------------------------------------------------------序列埠名稱
BAUD_RATES = 38400
#---------------------------------------------------------------------- Screen width, height
S_W = 800
S_H = 500
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

left_sig_text = ''
right_sig_text = ''
moving_direction_text = ''
horn_text = ''
record_text = ''
file_type = '.txt'
pred_text_long = ''
pred_text_short = ''
prev_pred_text_short = ''
prev_pred_text_long = ''
preds_long = 0
run = True
save_flag = False #---------------------------------------------------------------是否開始存陣列
save_flag_short = False
array_hight = 10 #-------------------------------------------------------------------儲存的陣列高度（判斷蛇行用的長時序）
array_hight_short = 5#------------------------儲存的陣列高度（判斷左右轉用的短時序）
onetime = 0
onetime_short = 0
arr_save_counter = 0 #-----------------------------------------------------------儲存陣列用的計數器
arr_save_counter_short = 0 #-----------------------------------------------------------儲存陣列用的計數器
times_to_save = 20 #---------------------------------------------------------------一次要儲存幾個陣列
punish_countdown = 3

danger_flag = 0
danger_flag_time = 0
write_flag = 0  #判斷是否為寫入模式
out = 0
cap = cv2.VideoCapture(int(cam_number))
_CAMERA_WIDTH = 640  #攝影機擷取影像寬度
_CAMERA_HEIGH = 480  #攝影機擷取影像高度
cap.set(cv2.CAP_PROP_FRAME_WIDTH, _CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, _CAMERA_HEIGH)
# 設定擷取影像的尺寸大小


ser = serial.Serial(COM_PORT, BAUD_RATES, timeout = 0.01)
pygame.init()#---------------------------------------------------------------pygame初始化
winScreen = pygame.display.set_mode((S_W, S_H))
winScreen.fill([255,255,255])
pygame.display.set_caption("Keyboard Demo")
my_font = pygame.font.SysFont(None, 25)
clean_buffer = ser.readall().decode()#-------------------------------------------清空serial緩衝器裡面的值

while run:
    # time_start = time()
    pygame.time.Clock().tick(24)#--------------------------------------------設定每秒迴圈執行次數
    keyboard_event = pygame.event.get()
    run, save_flag, save_flag_short, left_sig_text, right_sig_text, horn_text = car_control(keyboard_event, ser, run, save_flag, save_flag_short, left_sig_text, right_sig_text, horn_text)#車子控制涵式
   
    video_counter, out, write_flag= record(video_counter, save_flag, cap, _CAMERA_WIDTH, _CAMERA_HEIGH, write_flag, out)
    
    keys = pygame.key.get_pressed()#----------------------------------------------偵測被按下的按鍵
    
    while ser.in_waiting:

        
        mcu_feedback = ser.readline().decode()  #------------------------------ 接收回應訊息並解碼
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    （以下）處理陣列部分
        # print(mcu_feedback)
        new_float_array = change_str_float_array(mcu_feedback)
        new_float_array = add_horn_turnsig(new_float_array, horn_text, left_sig_text, right_sig_text)


        if onetime == 0:
            float_array_2d = new_float_array
            onetime = onetime + 1
        float_array_2d = np.vstack((float_array_2d, new_float_array))#-----------新列加到舊列下
        float_array_2d_hight = float_array_2d.shape[0]
#---------------------------------------------------------------------------------------------------------------------------（以下為短矩陣部分）（以上為長矩陣部分）
        if onetime_short == 0:
            float_array_2d_short = new_float_array
            onetime_short = onetime_short + 1
        float_array_2d_short = np.vstack((float_array_2d_short, new_float_array))#-----------新列加到舊列下
        float_array_2d_short_hight = float_array_2d_short.shape[0]


#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////  （以下）   儲存資料部分
        if float_array_2d_hight == array_hight:
            if arr_save_counter == array_hight :#開始儲存時
                float_array_3d = float_array_2d
            if save_flag and (arr_save_counter > array_hight) and (arr_save_counter < (times_to_save + array_hight)):#等待（矩陣長度減一）之後才開始存才會存到0秒之後的矩陣
                float_array_3d = np.concatenate((float_array_3d, float_array_2d), axis = 0)
            # print(save_flag)
            # print(arr_save_counter)
            if save_flag:
                arr_save_counter = arr_save_counter + 1
            if arr_save_counter >= (times_to_save + array_hight):
                with open(file_name + file_type, 'a') as outfile:
                    np.savetxt(outfile, float_array_3d, delimiter=' ', newline='\n') #    dellimiter 每個元素間隔  ，newline 每列結束的字元
                    # outfile.write('\n')
                save_flag = False
                arr_save_counter = 0

            # print(float_array_2d)
            sample_long = float_array_2d.reshape(1, 10, 4)
            preds_long = model_long.predict_classes(sample_long)#判斷資料(lstm)
            if preds_long + 1 == 8:
                if keys[pygame.K_w]:
                    pred_text_long = 'forward no signal snaking'
                elif keys[pygame.K_s]:
                    pred_text_long = 'backward no signal snaking'              
            elif preds_long + 1 == 11:
                if keys[pygame.K_w]:
                    pred_text_long = 'forward left signal snaking'
                elif keys[pygame.K_s]:
                    pred_text_long = 'backward left signal snaking'
            elif preds_long + 1 == 12:
                if keys[pygame.K_w]:
                    pred_text_long = 'forward right signal snaking'
                elif keys[pygame.K_s]:
                    pred_text_long = 'backward right signal snaking'
            else :
                pred_text_long = ''
            float_array_2d = np.delete(float_array_2d, (0), axis = 0)#-----------刪除第一列
            # print('\n')
        #-----------------------------------------------------------------------------------------------------------------（以下為短矩陣儲存部分）（以上為長矩陣儲存部分）
        if float_array_2d_short_hight == array_hight_short:
            if arr_save_counter_short == array_hight_short :#開始儲存時
                float_array_3d_short = float_array_2d_short
            if save_flag_short and (arr_save_counter_short > array_hight_short) and (arr_save_counter_short < (times_to_save + array_hight_short)):#等待（矩陣長度減一）之後才開始存才會存到0秒之後的矩陣
                float_array_3d_short = np.concatenate((float_array_3d_short, float_array_2d_short), axis = 0)
            # print(save_flag_short)
            # print(arr_save_counter_short)
            if save_flag_short:
                arr_save_counter_short = arr_save_counter_short + 1
            if arr_save_counter_short >= (times_to_save + array_hight_short):
                with open(file_name + 'short' + file_type, 'a') as outfile:
                    np.savetxt(outfile, float_array_3d_short, delimiter=' ', newline='\n') #    dellimiter 每個元素間隔  ，newline 每列結束的字元
                    # outfile.write('\n')
                save_flag_short = False
                arr_save_counter_short = 0

            sample_short = float_array_2d_short.reshape(1, 5, 4)
            preds_short = model_short.predict_classes(sample_short)#判斷資料(lstm)
            if preds_short + 1 == 1:
                pred_text_short = 'normal'
                if keys[pygame.K_w]:
                    pred_text_short = 'forward ' + pred_text_short
                elif keys[pygame.K_s]:
                    pred_text_short = 'backward ' + pred_text_short      
            elif preds_short + 1 == 2:
                pred_text_short = 'no signal left'
                if keys[pygame.K_w]:
                    pred_text_short = 'forward ' + pred_text_short
                elif keys[pygame.K_s]:
                    pred_text_short = 'backward ' + pred_text_short       
            elif preds_short + 1 == 3:
                pred_text_short = 'no signal right'
                if keys[pygame.K_w]:
                    pred_text_short = 'forward ' + pred_text_short
                elif keys[pygame.K_s]:
                    pred_text_short = 'backward ' + pred_text_short    
            elif preds_short + 1 == 4:
                pred_text_short = 'left signal left'
                if keys[pygame.K_w]:
                    pred_text_short = 'forward ' + pred_text_short
                elif keys[pygame.K_s]:
                    pred_text_short = 'backward ' + pred_text_short    
            elif preds_short + 1 == 5:
                pred_text_short = 'right signal right'
                if keys[pygame.K_w]:
                    pred_text_short = 'forward ' + pred_text_short
                elif keys[pygame.K_s]:
                    pred_text_short = 'backward ' + pred_text_short    
            elif preds_short + 1 == 6:
                pred_text_short = 'left signal right'
                if keys[pygame.K_w]:
                    pred_text_short = 'forward ' + pred_text_short
                elif keys[pygame.K_s]:
                    pred_text_short = 'backward ' + pred_text_short    
            elif preds_short + 1 == 7:
                pred_text_short = 'right signal left'
                if keys[pygame.K_w]:
                    pred_text_short = 'forward ' + pred_text_short
                elif keys[pygame.K_s]:
                    pred_text_short = 'backward ' + pred_text_short    
            elif preds_short + 1 == 8:
                pred_text_short = 'right_signal'
                if keys[pygame.K_w]:
                    pred_text_short = 'forward ' + pred_text_short
                elif keys[pygame.K_s]:
                    pred_text_short = 'backward ' + pred_text_short    
            elif preds_short + 1 == 9:
                pred_text_short = 'left_signal'
                if keys[pygame.K_w]:
                    pred_text_short = 'forward ' + pred_text_short
                elif keys[pygame.K_s]:
                    pred_text_short = 'backward ' + pred_text_short   
            if (not(('normal' in pred_text_short)or('left signal left' in pred_text_short)or('right signal right' in pred_text_short)or('right_signal' in pred_text_short)or('left_signal' in pred_text_short))    or  (preds_long + 1 == 8)or(preds_long + 1 == 11)or(preds_long + 1 == 12)):
                if (danger_flag == 0) or(not(prev_pred_text_short == pred_text_short)):#三秒後 或 危險形態有變才扣分
                    punish_countdown = punish_countdown - 1
                    danger_flag = 1
                    danger_flag_time = pygame.time.get_ticks()#---------------------取得偵測到危險駕駛的時間
                if punish_countdown == 0:
                    print('punishingjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
                    ser.write(b'p\n')
                    rfid_text = 'car slowed'
                    punish_countdown = 3
                
                prev_pred_text_short = pred_text_short
                print(prev_pred_text_short)
            print(punish_countdown) 
    
            print(float_array_2d_short)
            float_array_2d_short = np.delete(float_array_2d_short, (0), axis = 0)#-----------刪除第一列
            print('\n')

    
    
    current_time = pygame.time.get_ticks()#---------------------------------------------取得現在時間
    if current_time - danger_flag_time > 1500:#---------------------------偵測到危險駕駛緩衝時間三秒
        danger_flag = 0
        


        
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            
    
    moving_direction_text, record_text = get_new_text(keys, save_flag)#更新要印出的文字    

    horn_text_surface = my_font.render(horn_text, True, blue)
    drive_text_surface = my_font.render(moving_direction_text, True, red)
    L_turn_text_surface = my_font.render(left_sig_text, True, blue)#---------------------------左方向燈狀態文字
    R_turn_text_surface = my_font.render(right_sig_text, True, blue)#---------------------------右方向燈狀態文字
    record_text_surface =  my_font.render(record_text, True, (0, 0, 0))
    prediction_text_surface_long = my_font.render(pred_text_long, True, (0, 0, 0))
    prediction_text_surface_short = my_font.render(pred_text_short, True, (0, 0, 0))

    move_text = my_font.render('moving direction(press w a s d):', True, red)
    signal_text = my_font.render('turn signal(press < >):', True, blue)
    horn_state_text = my_font.render('horn(press ^ ):', True, blue)
    record_state_text = my_font.render('record(press f ):', True, (0, 0, 0))
    pred_state_text = my_font.render('lstm predicton(long term)', True, (0, 0, 0))
    pred_state_text2 = my_font.render('lstm predicton(short term)', True, (0, 0, 0))

    winScreen.fill([255,255,255])
    winScreen.blit(drive_text_surface, (500, 10))#------------------------------------印出文字
    winScreen.blit(L_turn_text_surface, (500, 30))
    winScreen.blit(R_turn_text_surface, (500, 50))
    winScreen.blit(horn_text_surface, (500, 70))
    winScreen.blit(record_text_surface, (500, 90))
    winScreen.blit(prediction_text_surface_long, (500, 110))
    winScreen.blit(prediction_text_surface_short, (500, 130))
    winScreen.blit(move_text, (10, 10))
    winScreen.blit(signal_text, (10, 30))
    winScreen.blit(horn_state_text, (10, 70))
    winScreen.blit(record_state_text, (10, 90))
    winScreen.blit(pred_state_text, (10, 110))
    winScreen.blit(pred_state_text2, (10, 130))
    pygame.display.update()
    # time_end = time() 
    # print(time_end - time_start, 's')
ser.close()
print("再見")
cap.release()
if not (type(out) == 'int'):
    out.release()
cv2.destroyAllWindows()
pygame.quit()
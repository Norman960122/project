import cv2
import numpy as np

def record(video_counter, save_flag, cap, _CAMERA_WIDTH, _CAMERA_HEIGH, write_flag, out):
    
    
    video_name = 'video_' #儲存影片名稱
    file_type = '.avi' #儲存影片副檔名
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    FPS = 20  #擷取影片頻率
    


    ret, frame = cap.read()
    # if ret == True:
    if save_flag == 1 and write_flag == 0: # 寫入影格
        write_flag = 1
        save_name = video_name + str(video_counter) + file_type
        out = cv2.VideoWriter(save_name, fourcc, FPS, (_CAMERA_WIDTH, _CAMERA_HEIGH))
        # print('writing to ' + save_name)
    elif save_flag == 0 and write_flag == 1: #關閉影片
        write_flag = 0
        video_counter = video_counter + 1
        # print('finish')

    if (write_flag == 1):
        out.write(frame)
        # cv2.waitKey(1)
    cv2.imshow('frame',frame)
    
    return video_counter, out, write_flag


def show_video(file_name, start_frame, end_frame, frametime, window_name):
    frame_count = 1
    break_flag = False
    font = cv2.FONT_HERSHEY_SIMPLEX
    cap = cv2.VideoCapture(file_name)

    while(True):
        ret, frame = cap.read()

        if (not ret) or (frame_count > end_frame):
            break
        elif frame_count >= start_frame and frame_count <= end_frame:
            key = cv2.waitKey(frametime)
            if key == ord('q') or break_flag:
                break
            elif key == ord('p'):
                while(True):
                    # print("paused at frame ", frame_count)
                    frame_count_text = str(frame_count)
                    cv2.putText(frame, "paused at frame:" + frame_count_text ,(10,50), font, 1, (255,0,0), 2, cv2.LINE_AA)
                    cv2.imshow(window_name,frame)
                    resume_key = cv2.waitKey(0)
                    if resume_key == ord('p'):
                        break
                    elif resume_key == ord('q'):
                        break_flag = True
                        break
            
            cv2.imshow(window_name,frame)
        frame_count = frame_count + 1

    cap.release()


    print('video ended')


def show_img(_CAMERA_HEIGH, _CAMERA_WIDTH, start_frame, end_frame, arr_num):
    window_name = 'image'
    img = np.ones((_CAMERA_HEIGH, _CAMERA_WIDTH, 3), dtype="uint8")
    img[:] = (255, 255, 255)#--------------------------------畫布顏色
    start_frame_text = str(start_frame)
    end_frame_text = str(end_frame)
    arr_num_text = str(arr_num + 1)
    current_arr_text = 'frames from '+ start_frame_text + ' to '+ end_frame_text +' / matrix '+ arr_num_text
    # cv2.line(img,(0,0),(200,300),(255,255,255),50)#-----------------------------------------畫圖形(not needed)
    # cv2.rectangle(img,(500,250),(1000,500),(0,0,255),15)
    # cv2.circle(img,(447,63), 63, (0,255,0), -1)
    # pts = np.array([[100,50],[200,300],[700,200],[500,100]], np.int32)
    # pts = pts.reshape((-1,1,2))
    # cv2.polylines(img, [pts], True, (0,255,255), 3)#----------------------------------------畫圖形
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,'press p to play and pause',(10,50), font, 1, (0,0,0), 2, cv2.LINE_AA)
    cv2.putText(img,'press n to next clip',(10,100), font, 1, (0,0,0), 2, cv2.LINE_AA)
    cv2.putText(img,'press b to previous clip',(10,150), font, 1, (0,0,0), 2, cv2.LINE_AA)
    cv2.putText(img,'press q to quit playing clip',(10,200), font, 1, (0,0,0), 2, cv2.LINE_AA)
    cv2.putText(img,'press ESC to exit',(10,250), font, 1, (0,0,0), 2, cv2.LINE_AA)
    cv2.putText(img, current_arr_text,(10,300), font, 1, (0,0,255), 2, cv2.LINE_AA)
    cv2.imshow(window_name, img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return window_name
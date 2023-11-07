 '******** 2족 보행로봇 초기 영점 프로그램 ********

'-*- coding: utf-8 -*-'

DIM I AS BYTE
DIM J AS BYTE
DIM MODE AS BYTE
DIM A AS BYTE
DIM A_old AS BYTE
DIM B AS BYTE
DIM C AS BYTE
DIM 보행속도 AS BYTE
DIM 좌우속도 AS BYTE
DIM 좌우속도2 AS BYTE
DIM 보행순서 AS BYTE
DIM 현재전압 AS BYTE
DIM 반전체크 AS BYTE
DIM 모터ONOFF AS BYTE
DIM 자이로ONOFF AS BYTE
DIM 기울기앞뒤 AS INTEGER
DIM 기울기좌우 AS INTEGER

DIM 곡선방향 AS BYTE

DIM 넘어진확인 AS BYTE
DIM 기울기확인횟수 AS BYTE
DIM 보행횟수 AS BYTE
DIM angle_y AS BYTE   '로봇 상하 각도
DIM angle_x AS BYTE   '로봇 좌우 각도
DIM 보행COUNT AS BYTE

DIM 적외선거리값  AS BYTE

DIM S11  AS BYTE
DIM S16  AS BYTE
'************************************************
DIM NO_0 AS BYTE
DIM NO_1 AS BYTE
DIM NO_2 AS BYTE
DIM NO_3 AS BYTE
DIM NO_4 AS BYTE

DIM NUM AS BYTE

DIM BUTTON_NO AS INTEGER
DIM SOUND_BUSY AS BYTE
DIM TEMP_INTEGER AS INTEGER

'**** 기울기센서포트 설정 ****
CONST 앞뒤기울기AD포트 = 0
CONST 좌우기울기AD포트 = 1
CONST 기울기확인시간 = 20  'ms
CONST 적외선AD포트  = 4


CONST min = 61	'뒤로넘어졌을때
CONST max = 107	'앞으로넘어졌을때
CONST COUNT_MAX = 3


CONST 머리이동속도 = 10
'************************************************



PTP SETON 				'단위그룹별 점대점동작 설정
PTP ALLON				'전체모터 점대점 동작 설정

DIR G6A,1,0,0,1,0,0		'모터0~5번
DIR G6D,0,1,1,0,1,1		'모터18~23번
DIR G6B,1,1,1,1,1,1		'모터6~11번
DIR G6C,0,0,0,1,1,0		'모터12~17번

'************************************************

OUT 52,0	'머리 LED 켜기
'***** 초기선언 '************************************************

angle_y = 100  '머리 각도 상하
angle_x = 100  '머리 각도 좌우
보행순서 = 0
반전체크 = 0
기울기확인횟수 = 0
보행횟수 = 1
모터ONOFF = 0

'****초기위치 피드백*****************************


TEMPO 230
'MUSIC "cdefg"



SPEED 5
GOSUB MOTOR_ON

S11 = MOTORIN(11)
S16 = MOTORIN(16)

SERVO 11, 100
SERVO 16, S16

SERVO 16, 100


GOSUB 전원초기자세
GOSUB 기본자세


GOSUB 자이로INIT
GOSUB 자이로MID
GOSUB 자이로ON



PRINT "VOLUME 200 !"
'PRINT "SOUND 12 !" '안녕하세요

GOSUB All_motor_mode3


GOTO MAIN	'시리얼 수신 루틴으로 가기

'************************************************

'*********************************************
' Infrared_Distance = 60 ' About 20cm
' Infrared_Distance = 50 ' About 25cm
' Infrared_Distance = 30 ' About 45cm
' Infrared_Distance = 20 ' About 65cm
' Infrared_Distance = 10 ' About 95cm
'*********************************************
'************************************************
시작음:
    TEMPO 220
    MUSIC "O23EAB7EA>3#C"
    RETURN
    '************************************************
종료음:
    TEMPO 220
    MUSIC "O38GD<BGD<BG"
    RETURN
    '************************************************
에러음:
    TEMPO 250
    MUSIC "FFF"
    RETURN
    '************************************************
    '************************************************
MOTOR_ON: '전포트서보모터사용설정

    GOSUB MOTOR_GET

    MOTOR G6B
    DELAY 50
    MOTOR G6C
    DELAY 50
    MOTOR G6A
    DELAY 50
    MOTOR G6D

    모터ONOFF = 0
    GOSUB 시작음			
    RETURN

    '************************************************
    '전포트서보모터사용설정
MOTOR_OFF:

    MOTOROFF G6B
    MOTOROFF G6C
    MOTOROFF G6A
    MOTOROFF G6D
    모터ONOFF = 1	
    GOSUB MOTOR_GET	
    GOSUB 종료음	
    RETURN
    '************************************************
    '위치값피드백
MOTOR_GET:
    GETMOTORSET G6A,1,1,1,1,1,0
    GETMOTORSET G6B,1,1,1,0,0,1
    GETMOTORSET G6C,1,1,1,1,1,0
    GETMOTORSET G6D,1,1,1,1,1,0
    RETURN

    '************************************************
    '위치값피드백
MOTOR_SET:
    GETMOTORSET G6A,1,1,1,1,1,0
    GETMOTORSET G6B,1,1,1,0,0,1
    GETMOTORSET G6C,1,1,1,1,1,0
    GETMOTORSET G6D,1,1,1,1,1,0
    RETURN

    '************************************************
All_motor_Reset:

    MOTORMODE G6A,1,1,1,1,1,1
    MOTORMODE G6D,1,1,1,1,1,1
    MOTORMODE G6B,1,1,1,,,1
    MOTORMODE G6C,1,1,1,1,1

    RETURN
    '************************************************
All_motor_mode2:

    MOTORMODE G6A,2,2,2,2,2
    MOTORMODE G6D,2,2,2,2,2
    MOTORMODE G6B,2,2,2,,,2
    MOTORMODE G6C,2,2,2,2,2

    RETURN
    '************************************************
All_motor_mode3:

    MOTORMODE G6A,3,3,3,3,3
    MOTORMODE G6D,3,3,3,3,3
    MOTORMODE G6B,3,3,3,,,3
    MOTORMODE G6C,3,3,3,3,3

    RETURN
    '************************************************
Leg_motor_mode1:
    MOTORMODE G6A,1,1,1,1,1
    MOTORMODE G6D,1,1,1,1,1
    RETURN
    '************************************************
Leg_motor_mode2:
    MOTORMODE G6A,2,2,2,2,2
    MOTORMODE G6D,2,2,2,2,2
    RETURN

    '************************************************
Leg_motor_mode3:
    MOTORMODE G6A,3,3,3,3,3
    MOTORMODE G6D,3,3,3,3,3
    RETURN
    '************************************************
Leg_motor_mode4:
    MOTORMODE G6A,3,2,2,1,3
    MOTORMODE G6D,3,2,2,1,3
    RETURN
    '************************************************
Leg_motor_mode5:
    MOTORMODE G6A,3,2,2,1,2
    MOTORMODE G6D,3,2,2,1,2
    RETURN
    '************************************************
Arm_motor_mode1:
    MOTORMODE G6B,1,1,1,,,1
    MOTORMODE G6C,1,1,1,1,1
    RETURN
    '************************************************
Arm_motor_mode2:
    MOTORMODE G6B,2,2,2,,,2
    MOTORMODE G6C,2,2,2,2,2
    RETURN

    '************************************************
Arm_motor_mode3:
    MOTORMODE G6B,3,3,3,,,3
    MOTORMODE G6C,3,3,3,3,3
    RETURN
    '************************************************

전원초기자세:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,100,  35,  90, 190, 106 ' 106 = 정면 보는 값 
    WAIT
    mode = 0
    RETURN
    '************************************************
안정화자세:
    MOVE G6A,98,  76, 145,  93, 101, 100
    MOVE G6D,98,  76, 145,  93, 101, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,100,  35,  90, 190
    WAIT
    mode = 0

    RETURN
    '******************************************	


    '************************************************
고개중앙기본자세:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,100,  35,  90, 190, 106 ' 106 = 정면 보는 값 
    WAIT
    mode = 0
    RETURN    
    '******************************************	
기본자세:

    MOVE G6A,100,  76, 145,  93, 100, 100   '왼쪽 다리
    MOVE G6D,100,  76, 145,  93, 100, 100   '오른쪽 다리
    MOVE G6B,100,  30,  80,   '왼쪽 팔
    MOVE G6C,100,  30,  80, 190   '오른쪽 팔
    WAIT
    mode = 0

    RETURN
    '******************************************	
기본자세2:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  30,  80,
    MOVE G6C,100,  30,  80, 190
    WAIT
    mode = 0
    
    RETURN
    '******************************************	
차렷자세:
    MOVE G6A,100, 56, 182, 76, 100, 100
    MOVE G6D,100, 56, 182, 76, 100, 100
    MOVE G6B,100,  30,  80,
    MOVE G6C,100,  30,  80, 190
    WAIT
    mode = 2
    RETURN
    '******************************************
앉은자세:
    GOSUB 자이로OFF
    MOVE G6A,100, 145,  28, 145, 100, 100
    MOVE G6D,100, 145,  28, 145, 100, 100
    MOVE G6B,100,  30,  80,
    MOVE G6C,100,  30,  80, 190
    WAIT
    mode = 1

    RETURN
    '******************************************
    '***********************************************
    '***********************************************
    '**** 자이로감도 설정 ****
    
자이로INIT:

    GYRODIR G6A, 0, 0, 1, 0,0
    GYRODIR G6D, 1, 0, 1, 0,0

    GYROSENSE G6A,200,150,30,150,0
    GYROSENSE G6D,200,150,30,150,0

    RETURN
    '***********************************************
    '**** 자이로감도 설정 ****
자이로MAX:

    GYROSENSE G6A,250,180,30,180,0
    GYROSENSE G6D,250,180,30,180,0

    RETURN
    '***********************************************
자이로MID:

    GYROSENSE G6A,200,150,30,150,0
    GYROSENSE G6D,200,150,30,150,0

    RETURN
    '***********************************************
자이로MIN:

    GYROSENSE G6A,200,100,30,100,0
    GYROSENSE G6D,200,100,30,100,0
    RETURN
    '***********************************************
자이로ON:

    GYROSET G6A, 4, 3, 3, 3, 0
    GYROSET G6D, 4, 3, 3, 3, 0

    자이로ONOFF = 1

    RETURN
    '***********************************************
자이로OFF:

    GYROSET G6A, 0, 0, 0, 0, 0
    GYROSET G6D, 0, 0, 0, 0, 0


    자이로ONOFF = 0
    RETURN

    '************************************************

    '******************************************
    '**********************************************
    '**********************************************
RX_EXIT:

    ERX 4800, A, MAIN

    GOTO RX_EXIT
    '**********************************************
GOSUB_RX_EXIT:

    ERX 4800, A, GOSUB_RX_EXIT2

    GOTO GOSUB_RX_EXIT

GOSUB_RX_EXIT2:
    RETURN
    '**********************************************
    '**********************************************



' #############################################

 
공으로다가가기:
    GOSUB All_motor_mode3
    보행COUNT = 0
    SPEED 7
    HIGHSPEED SETON


    IF 보행순서 = 0 THEN
        보행순서 = 1
        MOVE G6A,95,  76, 147,  93, 101
        MOVE G6D,101,  76, 147,  93, 98
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        GOTO 공으로다가가기_1
    ELSE
        보행순서 = 0
        MOVE G6D,93,  76, 147,  93, 101
        MOVE G6A,104,  76, 147,  93, 98
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        GOTO 공으로다가가기_4
    ENDIF


    '**********************

공으로다가가기_1:
    MOVE G6A,95,  90, 125, 100, 104
    MOVE G6D,103,  76, 146,  93,  102
    MOVE G6B, 90
    MOVE G6C,115
    WAIT


공으로다가가기_2:

    MOVE G6A,107,   73, 140, 103,  100
    MOVE G6D, 90,  83, 146,  85, 102
    WAIT

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0

        GOTO RX_EXIT
    ENDIF

    보행COUNT = 보행COUNT + 1
    IF 보행COUNT > 보행횟수 THEN  GOTO 공으로다가가기_2_stop

    ERX 4800,A, 공으로다가가기_4
    IF A <> A_old THEN
    
공으로다가가기_2_stop:
        MOVE G6D,93,  90, 125, 95, 104
        MOVE G6A,107,  76, 145,  91,  102
        MOVE G6C, 100
        MOVE G6B,100
        WAIT
        HIGHSPEED SETOFF
        SPEED 15
        GOSUB 안정화자세
        SPEED 5
        GOSUB 기본자세2

        'DELAY 400
        GOTO RX_EXIT
    ENDIF

    '*********************************

공으로다가가기_4:
    MOVE G6D,95,  88, 125, 103, 104
    MOVE G6A,107,  76, 146,  93,  102
    MOVE G6C, 85
    MOVE G6B,110
    WAIT


공으로다가가기_5:
    MOVE G6D,102,    74, 140, 103,  100
    MOVE G6A, 97,  83, 146,  85, 102
    WAIT
    'DELAY 10

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO RX_EXIT
    ENDIF

    보행COUNT = 보행COUNT + 1
    IF 보행COUNT > 보행횟수 THEN  GOTO 공으로다가가기_5_stop

    ERX 4800,A, 공으로다가가기_1
    IF A <> A_old THEN
공으로다가가기_5_stop:
        MOVE G6A,95,  90, 125, 95, 104
        MOVE G6D,104,  76, 145,  91,  102
        MOVE G6B, 100
        MOVE G6C,100
        WAIT
        HIGHSPEED SETOFF
        SPEED 15
        GOSUB 안정화자세
        SPEED 5
        GOSUB 기본자세2

        'DELAY 400
        GOTO RX_EXIT
    ENDIF

    '*************************************

    '*********************************

    GOTO 공으로다가가기_1
	


' ##################################
' ##################################







    '****************************************


연속전진_골프:
    보행COUNT = 0
    보행속도 = 13
    좌우속도 = 4
    넘어진확인 = 0

    GOSUB Leg_motor_mode3

    IF 보행순서 = 0 THEN
        보행순서 = 1

        SPEED 4

        MOVE G6A, 88,  74, 144,  95, 110
        MOVE G6D,108,  76, 146,  93,  96
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        SPEED 10'

        MOVE G6A, 90, 90, 120, 105, 110,100
        MOVE G6D,110,  76, 147,  93,  96,100
        MOVE G6B,90
        MOVE G6C,110
        WAIT


        GOTO 연속전진_골프_1	
    ELSE
        보행순서 = 0

        SPEED 4

        MOVE G6D,  88,  74, 144,  95, 110
        MOVE G6A, 108,  76, 146,  93,  96
        MOVE G6C, 100
        MOVE G6B, 100
        WAIT

        SPEED 10

        MOVE G6D, 90, 90, 120, 105, 110,100
        MOVE G6A,110,  76, 147,  93,  96,100
        MOVE G6C,90
        MOVE G6B,110
        WAIT


        GOTO 연속전진_골프_2	

    ENDIF


    '*******************************


연속전진_골프_1:

    ETX 4800,11 '진행코드를 보냄
    SPEED 보행속도

    MOVE G6A, 86,  56, 145, 115, 110
    MOVE G6D,108,  76, 147,  93,  96
    WAIT


    SPEED 좌우속도
    GOSUB Leg_motor_mode3

    MOVE G6A,110,  76, 147, 93,  96
    MOVE G6D,86, 100, 145,  69, 110
    WAIT


    SPEED 보행속도

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO MAIN
    ENDIF

    ERX 4800,A, 연속전진_골프_2
    IF A = 11 THEN
        GOTO 연속전진_골프_2
    ELSE
        ' GOSUB Leg_motor_mode3

        MOVE G6A,112,  76, 146,  93, 96,100
        MOVE G6D,90, 100, 100, 115, 110,100
        MOVE G6B,110
        MOVE G6C,90
        WAIT
        HIGHSPEED SETOFF

        SPEED 8
        MOVE G6A, 106,  76, 146,  93,  96,100		
        MOVE G6D,  88,  71, 152,  91, 106,100
        MOVE G6B, 100
        MOVE G6C, 100
        WAIT	

        SPEED 2
        GOSUB 기본자세2

        GOTO RX_EXIT
    ENDIF
    '**********

연속전진_골프_2:

    MOVE G6A,110,  76, 147,  93, 96,100
    MOVE G6D,90, 90, 120, 105, 110,100
    MOVE G6B,110
    MOVE G6C,90
    WAIT

연속전진_골프_3:
    ETX 4800,11 '진행코드를 보냄

    SPEED 보행속도

    MOVE G6D, 86,  56, 145, 115, 110
    MOVE G6A,108,  76, 147,  93,  96
    WAIT

    SPEED 좌우속도
    MOVE G6D,110,  76, 147, 93,  96
    MOVE G6A,86, 100, 145,  69, 110
    WAIT

    SPEED 보행속도

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO MAIN
    ENDIF

    ERX 4800,A, 연속전진_골프_4
    IF A = 11 THEN
        GOTO 연속전진_골프_4
    ELSE

        MOVE G6A, 90, 100, 100, 115, 110,100
        MOVE G6D,112,  76, 146,  93,  96,100
        MOVE G6B,90
        MOVE G6C,110
        WAIT
        HIGHSPEED SETOFF
        SPEED 8

        MOVE G6D, 106,  76, 146,  93,  96,100		
        MOVE G6A,  88,  71, 152,  91, 106,100
        MOVE G6C, 100
        MOVE G6B, 100
        WAIT	
        SPEED 2
        GOSUB 기본자세2

        GOTO RX_EXIT
    ENDIF

연속전진_골프_4:
    '왼발들기10
    MOVE G6A,90, 90, 120, 105, 110,100
    MOVE G6D,110,  76, 146,  93,  96,100
    MOVE G6B, 90
    MOVE G6C,110
    WAIT

    GOTO 연속전진_골프_1
    '*******************************

    '************************************************
연속후진_골프:
    넘어진확인 = 0
    보행속도 = 12
    좌우속도 = 4
    GOSUB Leg_motor_mode3



    IF 보행순서 = 0 THEN
        보행순서 = 1

        SPEED 4
        MOVE G6A, 88,  71, 152,  91, 110
        MOVE G6D,108,  76, 145,  93,  96
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        SPEED 10
        MOVE G6A, 90, 100, 100, 115, 110
        MOVE G6D,110,  76, 145,  93,  96
        MOVE G6B,90
        MOVE G6C,110
        WAIT

        GOTO 연속후진_골프_1	
    ELSE
        보행순서 = 0

        SPEED 4
        MOVE G6D,  85,  71, 152,  91, 110
        MOVE G6A, 108,  76, 146,  93,  96
        MOVE G6C, 100
        MOVE G6B, 100
        WAIT

        SPEED 10
        MOVE G6D, 90, 100, 100, 115, 110
        MOVE G6A,112,  76, 146,  93,  96
        MOVE G6C,90
        MOVE G6B,110
        WAIT


        GOTO 연속후진_골프_2

    ENDIF

    '*************************************
연속후진_골프_1:
    ETX 4800,12 '진행코드를 보냄
    SPEED 보행속도

    MOVE G6D,110,  76, 146, 93,  96
    MOVE G6A,90, 98, 146,  69, 110
    WAIT

    SPEED 좌우속도
    MOVE G6D, 90,  60, 137, 120, 110
    MOVE G6A,107,  85, 137,  93,  96
    WAIT


    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO RX_EXIT
    ENDIF


    SPEED 11

    MOVE G6D,90, 90, 120, 105, 110
    MOVE G6A,112,  76, 146,  93, 96
    MOVE G6B,110
    MOVE G6C,90
    WAIT

    ERX 4800,A, 연속후진_골프_2
    IF A <> A_old THEN
연속후진_골프_1_EXIT:
        HIGHSPEED SETOFF
        SPEED 5

        MOVE G6A, 108,  76, 146,  93,  96		
        MOVE G6D,  85,  72, 148,  91, 106
        MOVE G6B, 100
        MOVE G6C, 100
        WAIT	

        SPEED 3
        GOSUB 기본자세2
        GOTO RX_EXIT
    ENDIF
    '**********

연속후진_골프_2:
    ETX 4800,12 '진행코드를 보냄
    SPEED 보행속도
    MOVE G6A,112,  76, 146, 93,  96
    MOVE G6D,90, 98, 146,  69, 110
    WAIT


    SPEED 좌우속도
    MOVE G6A, 90,  60, 137, 120, 110
    MOVE G6D,107  85, 137,  93,  96
    WAIT


    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO RX_EXIT
    ENDIF


    SPEED 11
    MOVE G6A,90, 90, 120, 105, 110
    MOVE G6D,110,  76, 146,  93,  96
    MOVE G6B, 90
    MOVE G6C,110
    WAIT


    ERX 4800,A, 연속후진_골프_1
    IF A <> A_old THEN
연속후진_골프_2_EXIT:
        HIGHSPEED SETOFF
        SPEED 5

        MOVE G6D, 106,  76, 146,  93,  96		
        MOVE G6A,  85,  72, 148,  91, 106
        MOVE G6B, 100
        MOVE G6C, 100
        WAIT	

        SPEED 3
        GOSUB 기본자세2
        GOTO RX_EXIT
    ENDIF  	

    GOTO 연속후진_골프_1
    '**********************************************




    '******************************************

    '******************************************
전진종종걸음_골프:
    GOSUB All_motor_mode3
    보행COUNT = 0
    SPEED 7
    HIGHSPEED SETON


    IF 보행순서 = 0 THEN
        보행순서 = 1
        MOVE G6A,95,  76, 147,  93, 101
        MOVE G6D,101,  76, 147,  93, 98
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        GOTO 전진종종걸음_골프_1
    ELSE
        보행순서 = 0
        MOVE G6D,93,  76, 147,  93, 101
        MOVE G6A,104,  76, 147,  93, 98
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        GOTO 전진종종걸음_골프_4
    ENDIF


    '**********************

전진종종걸음_골프_1:
    MOVE G6A,95,  90, 125, 100, 104
    MOVE G6D,103,  76, 146,  93,  102
    MOVE G6B, 90
    MOVE G6C,115
    WAIT


전진종종걸음_골프_2:

    MOVE G6A,107,   73, 140, 103,  100
    MOVE G6D, 90,  83, 146,  85, 102
    WAIT

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0

        GOTO RX_EXIT
    ENDIF

    보행COUNT = 보행COUNT + 1
    IF 보행COUNT > 보행횟수 THEN  GOTO 전진종종걸음_골프_2_stop

    ERX 4800,A, 전진종종걸음_골프_4
    IF A <> A_old THEN
전진종종걸음_골프_2_stop:
        MOVE G6D,93,  90, 125, 95, 104
        MOVE G6A,107,  76, 145,  91,  102
        MOVE G6C, 100
        MOVE G6B,100
        WAIT
        HIGHSPEED SETOFF
        SPEED 15
        GOSUB 안정화자세
        SPEED 5
        GOSUB 기본자세2

        'DELAY 400
        GOTO RX_EXIT
    ENDIF

    '*********************************

전진종종걸음_골프_4:
    MOVE G6D,95,  88, 125, 103, 104
    MOVE G6A,107,  76, 146,  93,  102
    MOVE G6C, 85
    MOVE G6B,110
    WAIT


전진종종걸음_골프_5:
    MOVE G6D,102,    74, 140, 103,  100
    MOVE G6A, 97,  83, 146,  85, 102
    WAIT
    'DELAY 10

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO RX_EXIT
    ENDIF

    ' 보행COUNT = 보행COUNT + 1
    ' IF 보행COUNT > 보행횟수 THEN  GOTO 전진종종걸음_골프_5_stop

    ERX 4800,A, 전진종종걸음_골프_1
    IF A <> A_old THEN
전진종종걸음_골프_5_stop:
        MOVE G6A,95,  90, 125, 95, 104
        MOVE G6D,104,  76, 145,  91,  102
        MOVE G6B, 100
        MOVE G6C,100
        WAIT
        HIGHSPEED SETOFF
        SPEED 15
        GOSUB 안정화자세
        SPEED 5
        GOSUB 기본자세2

        'DELAY 400
        GOTO RX_EXIT
    ENDIF

    '*************************************

    '*********************************

    GOTO 전진종종걸음_골프_1

    '******************************************
    '******************************************
    '******************************************
후진종종걸음_골프:
    GOSUB All_motor_mode3
    넘어진확인 = 0
    보행COUNT = 0
    SPEED 7
    HIGHSPEED SETON


    IF 보행순서 = 0 THEN
        보행순서 = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  76, 145,  93, 98
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        GOTO 후진종종걸음_골프_1
    ELSE
        보행순서 = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  76, 145,  93, 98
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        GOTO 후진종종걸음_골프_4
    ENDIF


    '**********************

후진종종걸음_골프_1:
    MOVE G6D,104,  76, 147,  93,  102
    MOVE G6A,95,  95, 120, 95, 104
    MOVE G6B,115
    MOVE G6C,85
    WAIT



후진종종걸음_골프_3:
    MOVE G6A, 103,  79, 147,  89, 100
    MOVE G6D,95,   65, 147, 103,  102
    WAIT

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO RX_EXIT
    ENDIF
    ' 보행COUNT = 보행COUNT + 1
    ' IF 보행COUNT > 보행횟수 THEN  GOTO 후진종종걸음_골프_3_stop

    ERX 4800,A, 후진종종걸음_골프_4
    IF A <> A_old THEN
후진종종걸음_골프_3_stop:
        MOVE G6D,95,  85, 130, 100, 104
        MOVE G6A,104,  77, 146,  93,  102
        MOVE G6C, 100
        MOVE G6B,100
        WAIT

        'SPEED 15
        GOSUB 안정화자세
        HIGHSPEED SETOFF
        SPEED 5
        GOSUB 기본자세2

        'DELAY 400
        GOTO RX_EXIT
    ENDIF
    '*********************************

후진종종걸음_골프_4:
    MOVE G6A,104,  76, 147,  93,  102
    MOVE G6D,95,  95, 120, 95, 104
    MOVE G6C,115
    MOVE G6B,85
    WAIT


후진종종걸음_골프_6:
    MOVE G6D, 103,  79, 147,  89, 100
    MOVE G6A,95,   65, 147, 103,  102
    WAIT
    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO RX_EXIT
    ENDIF

    ' 보행COUNT = 보행COUNT + 1
    'IF 보행COUNT > 보행횟수 THEN  GOTO 후진종종걸음_골프_6_stop

    ERX 4800,A, 후진종종걸음_골프_1
    IF A <> A_old THEN  'GOTO 후진종종걸음_멈춤
후진종종걸음_골프_6_stop:
        MOVE G6A,95,  85, 130, 100, 104
        MOVE G6D,104,  77, 146,  93,  102
        MOVE G6B, 100
        MOVE G6C,100
        WAIT

        'SPEED 15
        GOSUB 안정화자세
        HIGHSPEED SETOFF
        SPEED 5
        GOSUB 기본자세2

        'DELAY 400
        GOTO RX_EXIT
    ENDIF

    GOTO 후진종종걸음_골프_1




    '******************************************



    '************************************************
오른쪽옆으로20_골프: '****
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 12
    MOVE G6D, 95,  90, 125, 100, 107, 100
    MOVE G6A,107,  77, 147,  93, 107 , 100
    WAIT

    SPEED 12
    MOVE G6D, 102,  77, 147, 93, 100, 100
    MOVE G6A,90,  80, 140,  95, 107, 100
    WAIT

    SPEED 12
    MOVE G6D,95,  76, 147,  93, 98, 100
    MOVE G6A,95,  76, 147,  93, 98, 100
    WAIT

    SPEED 3
    GOSUB 기본자세2

    GOTO RX_EXIT
    
    '************************************************

왼쪽옆으로20_골프: '****
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 12
    MOVE G6A, 95,  90, 125, 100, 104, 100
    MOVE G6D,105,  76, 146,  93, 104, 100
    WAIT

    SPEED 12
    MOVE G6A, 102,  76, 146, 93, 100, 100
    MOVE G6D,90,  80, 140,  95, 107, 100
    WAIT

    SPEED 12
    MOVE G6A,95,  76, 146,  93, 98, 100
    MOVE G6D,95,  76, 146,  93, 98, 100
    WAIT

    SPEED 3
    GOSUB 기본자세2

    GOTO RX_EXIT

    '**********************************************
    '******************************************
오른쪽옆으로70연속_골프:
    MOTORMODE G6A,3,3,2,3,2
    MOTORMODE G6D,3,3,2,3,2

오른쪽옆으로70연속_골프_loop:
    DELAY  10

    SPEED 10
    MOVE G6D, 90,  90, 120, 105, 110, 100
    MOVE G6A,103,  77, 147,  93, 107, 100
    WAIT

    SPEED 13
    MOVE G6D, 102,  77, 147, 93, 100, 100
    MOVE G6A,83,  77, 140,  96, 115, 100
    WAIT

    SPEED 13
    MOVE G6D,98,  77, 147,  93, 100, 100
    MOVE G6A,98,  77, 147,  93, 100, 100
    WAIT

    SPEED 12
    MOVE G6A,100,  77, 145,  93, 100, 100
    MOVE G6D,100,  77, 145,  93, 100, 100
    WAIT


    SPEED 3
    GOSUB 기본자세2

    GOTO RX_EXIT
    '**********************************************

왼쪽옆으로70연속_골프:
    MOTORMODE G6A,3,3,2,3,2
    MOTORMODE G6D,3,3,2,3,2
왼쪽옆으로70연속_골프_loop:
    DELAY  10

    SPEED 10
    MOVE G6A, 90,  90, 120, 95, 110, 100	
    MOVE G6D,100,  76, 146,  93, 107, 100	
    WAIT

    SPEED 13
    MOVE G6A, 102,  76, 146, 93, 100, 100
    MOVE G6D,83,  79, 140,  99, 115, 100
    WAIT

    SPEED 13
    MOVE G6A,98,  76, 146,  93, 100, 100
    MOVE G6D,98,  76, 146,  93, 100, 100
    WAIT

    SPEED 12
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6A,100,  76, 145,  93, 100, 100
    WAIT


    SPEED 3
    GOSUB 기본자세2

    GOTO RX_EXIT

    '**********************************************
    '************************************************
    '*********************************************

왼쪽턴3:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
왼쪽턴3_LOOP:

    IF 보행순서 = 0 THEN
        보행순서 = 1
        SPEED 15
        MOVE G6D,100,  73, 145,  93, 100, 100
        MOVE G6A,100,  79, 145,  93, 100, 100
        WAIT

        SPEED 6
        MOVE G6D,100,  84, 145,  78, 100, 100
        MOVE G6A,100,  68, 145,  108, 100, 100
        WAIT

        SPEED 9
        MOVE G6D,90,  90, 145,  78, 102, 100
        MOVE G6A,104,  71, 145,  105, 100, 100
        WAIT
        SPEED 7
        MOVE G6D,90,  80, 130, 102, 104
        MOVE G6A,105,  76, 146,  93,  100
        WAIT



    ELSE
        보행순서 = 0
        SPEED 15
        MOVE G6D,100,  73, 145,  93, 100, 100
        MOVE G6A,100,  79, 145,  93, 100, 100
        WAIT


        SPEED 6
        MOVE G6D,100,  88, 145,  78, 100, 100
        MOVE G6A,100,  65, 145,  108, 100, 100
        WAIT

        SPEED 9
        MOVE G6D,104,  86, 146,  80, 100, 100
        MOVE G6A,90,  58, 145,  110, 100, 100
        WAIT

        SPEED 7
        MOVE G6A,90,  85, 130, 98, 104
        MOVE G6D,105,  77, 146,  93,  100
        WAIT



    ENDIF

    SPEED 12
    GOSUB 기본자세2


    GOTO RX_EXIT

    '**********************************************
오른쪽턴3:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

오른쪽턴3_LOOP:

    IF 보행순서 = 0 THEN
        보행순서 = 1
        SPEED 15
        MOVE G6A,100,  73, 145,  93, 100, 100
        MOVE G6D,100,  79, 145,  93, 100, 100
        WAIT


        SPEED 6
        MOVE G6A,100,  84, 145,  78, 100, 100
        MOVE G6D,100,  68, 145,  108, 100, 100
        WAIT

        SPEED 9
        MOVE G6A,90,  90, 145,  78, 102, 100
        MOVE G6D,104,  71, 145,  105, 100, 100
        WAIT
        SPEED 7
        MOVE G6A,90,  80, 130, 102, 104
        MOVE G6D,105,  76, 146,  93,  100
        WAIT



    ELSE
        보행순서 = 0
        SPEED 15
        MOVE G6A,100,  73, 145,  93, 100, 100
        MOVE G6D,100,  79, 145,  93, 100, 100
        WAIT


        SPEED 6
        MOVE G6A,100,  88, 145,  78, 100, 100
        MOVE G6D,100,  65, 145,  108, 100, 100
        WAIT

        SPEED 9
        MOVE G6A,104,  86, 146,  80, 100, 100
        MOVE G6D,90,  58, 145,  110, 100, 100
        WAIT

        SPEED 7
        MOVE G6D,90,  85, 130, 98, 104
        MOVE G6A,105,  77, 146,  93,  100
        WAIT

    ENDIF
    SPEED 12
    GOSUB 기본자세2

    GOTO RX_EXIT

    '******************************************************
    '**********************************************
왼쪽턴5_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 5
    MOVE G6A,100,  81, 145,  88, 106, 100
    MOVE G6D,94,  71, 145, 98, 100, 100
    WAIT

    SPEED 12
    MOVE G6A,97,  81, 145,  88, 104, 100
    MOVE G6D,91,  71, 145, 98, 96, 100
    WAIT

    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2
    GOTO RX_EXIT
    '**********************************************
오른쪽턴5_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 5
    MOVE G6A,97,  71, 145,  98, 103, 100
    MOVE G6D,97,  81, 145,  88, 103, 100
    WAIT

    SPEED 12
    MOVE G6A,94,  71, 145,  98, 101, 100
    MOVE G6D,94,  81, 145,  88, 101, 100
    WAIT
    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2

    GOTO RX_EXIT
    '**********************************************

    '**********************************************
왼쪽턴10_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 5
    MOVE G6A,100,  86, 145,  83, 106, 100
    MOVE G6D,94,  66, 145, 103, 100, 100
    WAIT

    SPEED 12
    MOVE G6A,97,  86, 145,  83, 104, 100
    MOVE G6D,91,  66, 145, 103, 96, 100
    WAIT

    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2
    GOTO RX_EXIT
    '**********************************************
오른쪽턴10_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 5
    MOVE G6A,97,  66, 145,  103, 103, 100
    MOVE G6D,97,  86, 145,  83, 103, 100
    WAIT

    SPEED 12
    MOVE G6A,94,  66, 145,  103, 101, 100
    MOVE G6D,94,  86, 145,  83, 101, 100
    WAIT
    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2

    GOTO RX_EXIT
    '**********************************************
    '**********************************************
왼쪽턴20_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 8
    MOVE G6A,95,  96, 145,  73, 108, 100
    MOVE G6D,91,  56, 145,  113, 102, 100
    WAIT

    SPEED 12
    MOVE G6A,91,  96, 145,  73, 108, 100
    MOVE G6D,88,  56, 145,  113, 102, 100
    WAIT
    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2

    GOTO RX_EXIT
    '**********************************************
오른쪽턴20_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 8
    MOVE G6A,95,  56, 145,  113, 105, 100
    MOVE G6D,95,  96, 145,  73, 105, 100
    WAIT

    SPEED 12
    MOVE G6A,93,  56, 145,  113, 105, 100
    MOVE G6D,93,  96, 145,  73, 105, 100
    WAIT

    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100

    WAIT

    GOSUB 기본자세2

    GOTO RX_EXIT
    '**********************************************

    '**********************************************	


    '**********************************************
왼쪽턴45_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2


    SPEED 10
    MOVE G6A,95,  106, 145,  63, 108, 100
    MOVE G6D,91,  46, 145,  123, 102, 100
    WAIT

    SPEED 12
    MOVE G6A,91,  106, 145,  63, 108, 100
    MOVE G6D,88,  46, 145,  123, 102, 100
    WAIT

    SPEED 8
    GOSUB 기본자세2

    '
    GOTO RX_EXIT

    '**********************************************
오른쪽턴45_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2


    SPEED 10
    MOVE G6A,95,  46, 145,  123, 105, 100
    MOVE G6D,95,  106, 145,  63, 105, 100
    WAIT

    SPEED 12
    MOVE G6A,93,  46, 145,  123, 105, 100
    MOVE G6D,93,  106, 145,  63, 105, 100
    WAIT

    SPEED 8
    GOSUB 기본자세2

    GOTO RX_EXIT
    '**********************************************
왼쪽턴60_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2


    SPEED 15
    MOVE G6A,95,  116, 145,  53, 108, 100
    MOVE G6D,91,  36, 145,  133, 102, 100
    WAIT

    SPEED 15
    MOVE G6A,91,  116, 145,  53, 108, 100
    MOVE G6D,88,  36, 145,  133, 102, 100
    WAIT

    SPEED 10
    GOSUB 기본자세2

    GOTO RX_EXIT

    '**********************************************
오른쪽턴60_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2


    SPEED 15
    MOVE G6A,95,  36, 145,  133, 105, 100
    MOVE G6D,95,  116, 145,  53, 105, 100
    WAIT

    SPEED 15
    MOVE G6A,90,  36, 145,  133, 105, 100
    MOVE G6D,90,  116, 145,  53, 105, 100
    WAIT

    SPEED 10
    GOSUB 기본자세2

    GOTO RX_EXIT
    '****************************************
    '************************************************
    '**********************************************


    '************************************************

    ''************************************************
    '************************************************
    '************************************************
뒤로일어나기:

    HIGHSPEED SETOFF
    PTP SETON 				
    PTP ALLON		

    GOSUB 자이로OFF

    GOSUB All_motor_Reset

    SPEED 15
    GOSUB 기본자세

    MOVE G6A,90, 130, 120,  80, 110, 100
    MOVE G6D,90, 130, 120,  80, 110, 100
    MOVE G6B,150, 160,  10, 100, 100, 100
    MOVE G6C,150, 160,  10, 190, 100, 100
    WAIT

    MOVE G6B,185, 160,  10, 100, 100, 100
    MOVE G6C,185, 160,  10, 190, 100, 100
    WAIT

    SPEED 12
    MOVE G6B,185,  50, 10,  100, 100, 100
    MOVE G6C,185,  50, 10,  190, 100, 100
    WAIT



    SPEED 10
    MOVE G6A, 80, 155,  80, 150, 150, 100
    MOVE G6D, 80, 155,  80, 150, 150, 100
    MOVE G6B,185,  20, 50,  100, 100, 100
    MOVE G6C,185,  20, 50,  190, 100, 100
    WAIT

    MOVE G6A, 75, 162,  55, 162, 155, 100
    MOVE G6D, 75, 162,  55, 162, 155, 100
    MOVE G6B,188,  10, 100, 100, 100, 100
    MOVE G6C,188,  10, 100, 190, 100, 100
    WAIT

    SPEED 10
    MOVE G6A, 60, 162,  30, 162, 145, 100
    MOVE G6D, 60, 162,  30, 162, 145, 100
    MOVE G6B,170,  10, 100, 100, 100, 100
    MOVE G6C,170,  10, 100, 190, 100, 100
    WAIT

    DELAY 200


    GOSUB Leg_motor_mode3	
    MOVE G6A, 60, 150,  28, 155, 140, 100
    MOVE G6D, 60, 150,  28, 155, 140, 100
    MOVE G6B,150,  60,  90, 100, 100, 100
    MOVE G6C,150,  60,  90, 190, 100, 100
    WAIT

    MOVE G6A,100, 150,  28, 140, 100, 100
    MOVE G6D,100, 150,  28, 140, 100, 100
    MOVE G6B,130,  50,  85, 100, 100, 100
    MOVE G6C,130,  50,  85, 190, 100, 100
    WAIT
    DELAY 100

    MOVE G6A,100, 150,  33, 140, 100, 100
    MOVE G6D,100, 150,  33, 140, 100, 100
    WAIT
    SPEED 10
    GOSUB 기본자세

    넘어진확인 = 1

    DELAY 200
    GOSUB 자이로ON

    RETURN


    '**********************************************
앞으로일어나기:


    HIGHSPEED SETOFF
    PTP SETON 				
    PTP ALLON

    GOSUB 자이로OFF

    HIGHSPEED SETOFF

    GOSUB All_motor_Reset

    SPEED 15
    MOVE G6A,100, 35,  70, 130, 100,
    MOVE G6D,100, 35,  70, 130, 100,
    MOVE G6B,15,  140,  15
    MOVE G6C,15,  140,  15
    WAIT

    SPEED 12
    MOVE G6B,15,  100,  10
    MOVE G6C,15,  100,  10
    WAIT

    SPEED 12
    MOVE G6A,100, 136,  35, 80, 100,
    MOVE G6D,100, 136,  35, 80, 100,
    MOVE G6B,15,  15,  75
    MOVE G6C,15,  15,  75
    WAIT

    SPEED 10
    MOVE G6A,100, 165,  75, 20, 100,
    MOVE G6D,100, 165,  75, 20, 100,
    MOVE G6B,15,  20,  95
    MOVE G6C,15,  20,  95
    WAIT

    DELAY 200

    GOSUB Leg_motor_mode3

    SPEED 8
    MOVE G6A,100, 165,  85, 20, 100,
    MOVE G6D,100, 165,  85, 20, 100,
    MOVE G6B,130,  50,  60
    MOVE G6C,130,  50,  60
    WAIT

    SPEED 8
    MOVE G6A,100, 165,  85, 30, 100,
    MOVE G6D,100, 165,  85, 30, 100,
    WAIT

    SPEED 8
    MOVE G6A,100, 155,  45, 110, 100,
    MOVE G6D,100, 155,  45, 110, 100,
    MOVE G6B,130,  50,  60
    MOVE G6C,130,  50,  60
    WAIT

    SPEED 6
    MOVE G6A,100, 145,  45, 130, 100,
    MOVE G6D,100, 145,  45, 130, 100,
    WAIT


    SPEED 8
    GOSUB All_motor_mode2
    GOSUB 기본자세
    넘어진확인 = 1

    '******************************
    DELAY 200
    GOSUB 자이로ON
    RETURN

    '******************************************
    '******************************************
    '******************************************
    '**************************************************

    '******************************************
    '******************************************	
    '**********************************************

머리왼쪽1도:
	SPEED 머리이동속도
	SERVO 11, 99
	GOTO RX_EXIT
머리왼쪽2도:
	SPEED 머리이동속도
 	SERVO 11, 98
	GOTO RX_EXIT
머리왼쪽3도:
	SPEED 머리이동속도
	SERVO 11, 97
	GOTO RX_EXIT
머리왼쪽4도:
	SPEED 머리이동속도
	SERVO 11, 96
	GOTO RX_EXIT
머리왼쪽5도:
	SPEED 머리이동속도
	SERVO 11, 95
	GOTO RX_EXIT
머리왼쪽6도:
 	SPEED 머리이동속도
	SERVO 11, 94
 	GOTO RX_EXIT
머리왼쪽7도:
 	SPEED 머리이동속도
 	SERVO 11, 93
 	GOTO RX_EXIT
머리왼쪽8도:
 	SPEED 머리이동속도
 	SERVO 11, 92
 	GOTO RX_EXIT
머리왼쪽9도:
 	SPEED 머리이동속도
 	SERVO 11, 91
 	GOTO RX_EXIT
머리왼쪽10도:
 	SPEED 머리이동속도
 	SERVO 11, 90
 	GOTO RX_EXIT
머리왼쪽11도:
 	SPEED 머리이동속도
 	SERVO 11, 89
 	GOTO RX_EXIT
머리왼쪽12도:
 	SPEED 머리이동속도
 	SERVO 11, 88
 	GOTO RX_EXIT
머리왼쪽13도:
 	SPEED 머리이동속도
 	SERVO 11, 87
 	GOTO RX_EXIT
머리왼쪽14도:
 	SPEED 머리이동속도
 	SERVO 11, 86
 	GOTO RX_EXIT
머리왼쪽15도:
 	SPEED 머리이동속도
 	SERVO 11, 85
 	GOTO RX_EXIT
머리왼쪽16도:
 	SPEED 머리이동속도
 	SERVO 11, 84
 	GOTO RX_EXIT
머리왼쪽17도:
 	SPEED 머리이동속도
 	SERVO 11, 83
 	GOTO RX_EXIT
머리왼쪽18도:
 	SPEED 머리이동속도
 	SERVO 11, 82
 	GOTO RX_EXIT
머리왼쪽19도:
 	SPEED 머리이동속도
 	SERVO 11, 81
 	GOTO RX_EXIT
머리왼쪽20도:
 	SPEED 머리이동속도
 	SERVO 11, 80
 	GOTO RX_EXIT
머리왼쪽21도:
 	SPEED 머리이동속도
 	SERVO 11, 79
 	GOTO RX_EXIT
머리왼쪽22도:
 	SPEED 머리이동속도
 	SERVO 11, 78
 	GOTO RX_EXIT
머리왼쪽23도:
 	SPEED 머리이동속도
 	SERVO 11, 77
 	GOTO RX_EXIT
머리왼쪽24도:
 	SPEED 머리이동속도
 	SERVO 11, 76
 	GOTO RX_EXIT
머리왼쪽25도:
 	SPEED 머리이동속도
 	SERVO 11, 75
 	GOTO RX_EXIT
머리왼쪽26도:
 	SPEED 머리이동속도
 	SERVO 11, 74
 	GOTO RX_EXIT
머리왼쪽27도:
 	SPEED 머리이동속도
 	SERVO 11, 73
 	GOTO RX_EXIT
머리왼쪽28도:
 	SPEED 머리이동속도
 	SERVO 11, 72
 	GOTO RX_EXIT
머리왼쪽29도:
 	SPEED 머리이동속도
 	SERVO 11, 71
 	GOTO RX_EXIT
머리왼쪽30도:
 	SPEED 머리이동속도
 	SERVO 11, 70
 	GOTO RX_EXIT
머리왼쪽31도:
 	SPEED 머리이동속도
 	SERVO 11, 69
 	GOTO RX_EXIT
머리왼쪽32도:
 	SPEED 머리이동속도
 	SERVO 11, 68
 	GOTO RX_EXIT
머리왼쪽33도:
 	SPEED 머리이동속도
 	SERVO 11, 67
 	GOTO RX_EXIT
머리왼쪽34도:
 	SPEED 머리이동속도
 	SERVO 11, 66
 	GOTO RX_EXIT
머리왼쪽35도:
 	SPEED 머리이동속도
 	SERVO 11, 65
 	GOTO RX_EXIT
머리왼쪽36도:
 	SPEED 머리이동속도
 	SERVO 11, 64
 	GOTO RX_EXIT
머리왼쪽37도:
 	SPEED 머리이동속도
 	SERVO 11, 63
 	GOTO RX_EXIT
머리왼쪽38도:
 	SPEED 머리이동속도
 	SERVO 11, 62
 	GOTO RX_EXIT
머리왼쪽39도:
 	SPEED 머리이동속도
 	SERVO 11, 61
 	GOTO RX_EXIT
머리왼쪽40도:
 	SPEED 머리이동속도
 	SERVO 11, 60
 	GOTO RX_EXIT
머리왼쪽41도:
 	SPEED 머리이동속도
 	SERVO 11, 59
 	GOTO RX_EXIT
머리왼쪽42도:
 	SPEED 머리이동속도
 	SERVO 11, 58
 	GOTO RX_EXIT
머리왼쪽43도:
 	SPEED 머리이동속도
 	SERVO 11, 57
 	GOTO RX_EXIT
머리왼쪽44도:
 	SPEED 머리이동속도
 	SERVO 11, 56
 	GOTO RX_EXIT
머리왼쪽45도:
 	SPEED 머리이동속도
 	SERVO 11, 55
 	GOTO RX_EXIT
머리왼쪽46도:
 	SPEED 머리이동속도
 	SERVO 11, 54
 	GOTO RX_EXIT
머리왼쪽47도:
 	SPEED 머리이동속도
 	SERVO 11, 53
 	GOTO RX_EXIT
머리왼쪽48도:
 	SPEED 머리이동속도
 	SERVO 11, 52
 	GOTO RX_EXIT
머리왼쪽49도:
 	SPEED 머리이동속도
 	SERVO 11, 51
 	GOTO RX_EXIT
머리왼쪽50도:
 	SPEED 머리이동속도
 	SERVO 11, 50
 	GOTO RX_EXIT
머리왼쪽51도:
 	SPEED 머리이동속도
 	SERVO 11, 49
 	GOTO RX_EXIT
머리왼쪽52도:
 	SPEED 머리이동속도
 	SERVO 11, 48
 	GOTO RX_EXIT
머리왼쪽53도:
 	SPEED 머리이동속도
 	SERVO 11, 47
 	GOTO RX_EXIT
머리왼쪽54도:
 	SPEED 머리이동속도
 	SERVO 11, 46
 	GOTO RX_EXIT
머리왼쪽55도:
 	SPEED 머리이동속도
 	SERVO 11, 45
 	GOTO RX_EXIT
머리왼쪽56도:
 	SPEED 머리이동속도
 	SERVO 11, 44
 	GOTO RX_EXIT
머리왼쪽57도:
 	SPEED 머리이동속도
 	SERVO 11, 43
 	GOTO RX_EXIT
머리왼쪽58도:
 	SPEED 머리이동속도
 	SERVO 11, 42
 	GOTO RX_EXIT
머리왼쪽59도:
 	SPEED 머리이동속도
 	SERVO 11, 41
 	GOTO RX_EXIT
머리왼쪽60도:
 	SPEED 머리이동속도
 	SERVO 11, 40
 	GOTO RX_EXIT
머리왼쪽61도:
 	SPEED 머리이동속도
 	SERVO 11, 39
 	GOTO RX_EXIT
머리왼쪽62도:
 	SPEED 머리이동속도
 	SERVO 11, 38
 	GOTO RX_EXIT
머리왼쪽63도:
 	SPEED 머리이동속도
 	SERVO 11, 37
 	GOTO RX_EXIT
머리왼쪽64도:
 	SPEED 머리이동속도
 	SERVO 11, 36
 	GOTO RX_EXIT
머리왼쪽65도:
 	SPEED 머리이동속도
 	SERVO 11, 35
 	GOTO RX_EXIT
머리왼쪽66도:
 	SPEED 머리이동속도
 	SERVO 11, 34
 	GOTO RX_EXIT
머리왼쪽67도:
 	SPEED 머리이동속도
 	SERVO 11, 33
 	GOTO RX_EXIT
머리왼쪽68도:
 	SPEED 머리이동속도
 	SERVO 11, 32
 	GOTO RX_EXIT
머리왼쪽69도:
 	SPEED 머리이동속도
 	SERVO 11, 31
 	GOTO RX_EXIT
머리왼쪽70도:
 	SPEED 머리이동속도
 	SERVO 11, 30
 	GOTO RX_EXIT
머리왼쪽71도:
 	SPEED 머리이동속도
 	SERVO 11, 29
 	GOTO RX_EXIT
머리왼쪽72도:
 	SPEED 머리이동속도
 	SERVO 11, 28
 	GOTO RX_EXIT
머리왼쪽73도:
 	SPEED 머리이동속도
 	SERVO 11, 27
 	GOTO RX_EXIT
머리왼쪽74도:
 	SPEED 머리이동속도
 	SERVO 11, 26
 	GOTO RX_EXIT
머리왼쪽75도:
 	SPEED 머리이동속도
 	SERVO 11, 25
 	GOTO RX_EXIT
머리왼쪽76도:
 	SPEED 머리이동속도
 	SERVO 11, 24
 	GOTO RX_EXIT
머리왼쪽77도:
 	SPEED 머리이동속도
 	SERVO 11, 23
 	GOTO RX_EXIT
머리왼쪽78도:
 	SPEED 머리이동속도
 	SERVO 11, 22
 	GOTO RX_EXIT
머리왼쪽79도:
 	SPEED 머리이동속도
 	SERVO 11, 21
 	GOTO RX_EXIT
머리왼쪽80도:
 	SPEED 머리이동속도
 	SERVO 11, 20
 	GOTO RX_EXIT
머리왼쪽81도:
 	SPEED 머리이동속도
 	SERVO 11, 19
 	GOTO RX_EXIT
머리왼쪽82도:
 	SPEED 머리이동속도
 	SERVO 11, 18
 	GOTO RX_EXIT
머리왼쪽83도:
 	SPEED 머리이동속도
 	SERVO 11, 17
 	GOTO RX_EXIT
머리왼쪽84도:
 	SPEED 머리이동속도
 	SERVO 11, 16
 	GOTO RX_EXIT
머리왼쪽85도:
 	SPEED 머리이동속도
 	SERVO 11, 15
 	GOTO RX_EXIT
머리왼쪽86도:
 	SPEED 머리이동속도
 	SERVO 11, 14
 	GOTO RX_EXIT
머리왼쪽87도:
 	SPEED 머리이동속도
 	SERVO 11, 13
 	GOTO RX_EXIT
머리왼쪽88도:
 	SPEED 머리이동속도
 	SERVO 11, 12
 	GOTO RX_EXIT
머리왼쪽89도:
 	SPEED 머리이동속도
 	SERVO 11, 11
 	GOTO RX_EXIT
머리왼쪽90도:
 	SPEED 머리이동속도
 	SERVO 11, 10
 	GOTO RX_EXIT
	'******************************************
머리오른쪽1도:
	SPEED 머리이동속도
	SERVO 11, 101
	GOTO RX_EXIT
머리오른쪽2도:
	SPEED 머리이동속도
	SERVO 11, 102
	GOTO RX_EXIT
머리오른쪽3도:
	SPEED 머리이동속도
	SERVO 11, 103
	GOTO RX_EXIT
머리오른쪽4도:
	SPEED 머리이동속도
	SERVO 11, 104
	GOTO RX_EXIT
머리오른쪽5도:
	SPEED 머리이동속도
	SERVO 11, 105
	GOTO RX_EXIT
머리오른쪽6도:
	SPEED 머리이동속도
	SERVO 11, 106
	GOTO RX_EXIT
머리오른쪽7도:
	SPEED 머리이동속도
	SERVO 11, 107
	GOTO RX_EXIT
머리오른쪽8도:
	SPEED 머리이동속도
	SERVO 11, 108
	GOTO RX_EXIT
머리오른쪽9도:
	SPEED 머리이동속도
	SERVO 11, 109
	GOTO RX_EXIT
머리오른쪽10도:
	SPEED 머리이동속도
	SERVO 11, 110
	GOTO RX_EXIT
머리오른쪽11도:
	SPEED 머리이동속도
	SERVO 11, 111
	GOTO RX_EXIT
머리오른쪽12도:
	SPEED 머리이동속도
	SERVO 11, 112
	GOTO RX_EXIT
머리오른쪽13도:
	SPEED 머리이동속도
	SERVO 11, 113
	GOTO RX_EXIT
머리오른쪽14도:
	SPEED 머리이동속도	
	SERVO 11, 114
	GOTO RX_EXIT	
머리오른쪽15도:
	SPEED 머리이동속도
	SERVO 11, 115
	GOTO RX_EXIT
머리오른쪽16도:
	SPEED 머리이동속도
	SERVO 11, 116
	GOTO RX_EXIT
머리오른쪽17도:
	SPEED 머리이동속도
	SERVO 11, 117
	GOTO RX_EXIT
머리오른쪽18도:	
	SPEED 머리이동속도
	SERVO 11, 118
	GOTO RX_EXIT
머리오른쪽19도:
	SPEED 머리이동속도
	SERVO 11, 119
	GOTO RX_EXIT
머리오른쪽20도:
	SPEED 머리이동속도
	SERVO 11, 120
	GOTO RX_EXIT
머리오른쪽21도:
	SPEED 머리이동속도
	SERVO 11, 121
	GOTO RX_EXIT	
머리오른쪽22도:
	SPEED 머리이동속도
	SERVO 11, 122
	GOTO RX_EXIT
머리오른쪽23도:
	SPEED 머리이동속도
	SERVO 11, 123
	GOTO RX_EXIT
머리오른쪽24도:
	SPEED 머리이동속도
	SERVO 11, 124
	GOTO RX_EXIT
머리오른쪽25도:
	SPEED 머리이동속도
	SERVO 11, 125
	GOTO RX_EXIT
머리오른쪽26도:
	SPEED 머리이동속도
	SERVO 11, 126
	GOTO RX_EXIT
머리오른쪽27도:
	SPEED 머리이동속도
	SERVO 11, 127
	GOTO RX_EXIT
머리오른쪽28도:
	SPEED 머리이동속도
	SERVO 11, 128
	GOTO RX_EXIT
머리오른쪽29도:
	SPEED 머리이동속도
	SERVO 11, 129
	GOTO RX_EXIT
머리오른쪽30도:
	SPEED 머리이동속도
	SERVO 11, 130
	GOTO RX_EXIT
머리오른쪽31도:
	SPEED 머리이동속도
	SERVO 11, 131
	GOTO RX_EXIT
머리오른쪽32도:
	SPEED 머리이동속도
	SERVO 11, 132
	GOTO RX_EXIT
머리오른쪽33도:
	SPEED 머리이동속도
	SERVO 11, 133
	GOTO RX_EXIT
머리오른쪽34도:
	SPEED 머리이동속도
	SERVO 11, 134
	GOTO RX_EXIT
머리오른쪽35도:	
	SPEED 머리이동속도
	SERVO 11, 135
	GOTO RX_EXIT
머리오른쪽36도:
	SPEED 머리이동속도
	SERVO 11, 136
	GOTO RX_EXIT
머리오른쪽37도:
	SPEED 머리이동속도
	SERVO 11, 137
	GOTO RX_EXIT
머리오른쪽38도:
	SPEED 머리이동속도
	SERVO 11, 138
	GOTO RX_EXIT	
머리오른쪽39도:
	SPEED 머리이동속도
	SERVO 11, 139
	GOTO RX_EXIT
머리오른쪽40도:
	SPEED 머리이동속도
	SERVO 11, 140
	GOTO RX_EXIT
머리오른쪽41도:
	SPEED 머리이동속도
	SERVO 11, 141
	GOTO RX_EXIT
머리오른쪽42도:
	SPEED 머리이동속도
	SERVO 11, 142
	GOTO RX_EXIT
머리오른쪽43도:
	SPEED 머리이동속도
	SERVO 11, 143
	GOTO RX_EXIT
머리오른쪽44도:
	SPEED 머리이동속도
	SERVO 11, 144
	GOTO RX_EXIT
머리오른쪽45도:
	SPEED 머리이동속도
	SERVO 11, 145
	GOTO RX_EXIT
머리오른쪽46도:
	SPEED 머리이동속도
	SERVO 11, 146
	GOTO RX_EXIT
머리오른쪽47도:
	SPEED 머리이동속도
	SERVO 11, 147
	GOTO RX_EXIT
머리오른쪽48도:
	SPEED 머리이동속도
	SERVO 11, 148
	GOTO RX_EXIT
머리오른쪽49도:
	SPEED 머리이동속도
	SERVO 11, 149
	GOTO RX_EXIT
머리오른쪽50도:
	SPEED 머리이동속도
	SERVO 11, 150
	GOTO RX_EXIT
머리오른쪽51도:
	SPEED 머리이동속도
	SERVO 11, 151
	GOTO RX_EXIT
머리오른쪽52도:
	SPEED 머리이동속도
	SERVO 11, 152
	GOTO RX_EXIT
머리오른쪽53도:
	SPEED 머리이동속도
	SERVO 11, 153
	GOTO RX_EXIT
머리오른쪽54도:
	SPEED 머리이동속도
	SERVO 11, 154
	GOTO RX_EXIT
머리오른쪽55도:
	SPEED 머리이동속도
	SERVO 11, 155
	GOTO RX_EXIT
머리오른쪽56도:
	SPEED 머리이동속도
	SERVO 11, 156
	GOTO RX_EXIT
머리오른쪽57도:
	SPEED 머리이동속도
	SERVO 11, 157
	GOTO RX_EXIT
머리오른쪽58도:
	SPEED 머리이동속도
	SERVO 11, 158
	GOTO RX_EXIT
머리오른쪽59도:
	SPEED 머리이동속도
	SERVO 11, 159
	GOTO RX_EXIT
머리오른쪽60도:
	SPEED 머리이동속도
	SERVO 11, 160
	GOTO RX_EXIT
머리오른쪽61도:
	SPEED 머리이동속도
	SERVO 11, 161
	GOTO RX_EXIT
머리오른쪽62도:
	SPEED 머리이동속도
	SERVO 11, 162
	GOTO RX_EXIT
머리오른쪽63도:
	SPEED 머리이동속도
	SERVO 11, 163
	GOTO RX_EXIT
머리오른쪽64도:
	SPEED 머리이동속도
	SERVO 11, 164
	GOTO RX_EXIT
머리오른쪽65도:
	SPEED 머리이동속도
	SERVO 11, 165
	GOTO RX_EXIT
머리오른쪽66도:
	SPEED 머리이동속도
	SERVO 11, 166
	GOTO RX_EXIT
머리오른쪽67도:
	SPEED 머리이동속도
	SERVO 11, 167
	GOTO RX_EXIT
머리오른쪽68도:
	SPEED 머리이동속도
	SERVO 11, 168
	GOTO RX_EXIT
머리오른쪽69도:
	SPEED 머리이동속도
	SERVO 11, 169
	GOTO RX_EXIT
머리오른쪽70도:
	SPEED 머리이동속도
	SERVO 11, 170
	GOTO RX_EXIT
머리오른쪽71도:
	SPEED 머리이동속도
	SERVO 11, 171
	GOTO RX_EXIT
머리오른쪽72도:
	SPEED 머리이동속도
	SERVO 11, 172
	GOTO RX_EXIT
머리오른쪽73도:
	SPEED 머리이동속도
	SERVO 11, 173
	GOTO RX_EXIT
머리오른쪽74도:
	SPEED 머리이동속도
	SERVO 11, 174
	GOTO RX_EXIT
머리오른쪽75도:
	SPEED 머리이동속도
	SERVO 11, 175
	GOTO RX_EXIT
머리오른쪽76도:
	SPEED 머리이동속도
	SERVO 11, 176
	GOTO RX_EXIT
머리오른쪽77도:
	SPEED 머리이동속도
	SERVO 11, 177
	GOTO RX_EXIT
머리오른쪽78도:
	SPEED 머리이동속도
	SERVO 11, 178
	GOTO RX_EXIT
머리오른쪽79도:
	SPEED 머리이동속도
	SERVO 11, 179
	GOTO RX_EXIT
머리오른쪽80도:
	SPEED 머리이동속도
	SERVO 11, 180
	GOTO RX_EXIT
머리오른쪽81도:
	SPEED 머리이동속도
	SERVO 11, 181
	GOTO RX_EXIT
머리오른쪽82도:
	SPEED 머리이동속도
	SERVO 11, 182
	GOTO RX_EXIT
머리오른쪽83도:
	SPEED 머리이동속도
	SERVO 11, 183
	GOTO RX_EXIT
머리오른쪽84도:
	SPEED 머리이동속도
	SERVO 11, 184
	GOTO RX_EXIT
머리오른쪽85도:
	SPEED 머리이동속도
	SERVO 11, 185
	GOTO RX_EXIT
머리오른쪽86도:
	SPEED 머리이동속도
	SERVO 11, 186
	GOTO RX_EXIT
머리오른쪽87도:
	SPEED 머리이동속도
	SERVO 11, 187
	GOTO RX_EXIT
머리오른쪽88도:
	SPEED 머리이동속도
	SERVO 11, 188
	GOTO RX_EXIT
머리오른쪽89도:
	SPEED 머리이동속도
	SERVO 11, 189
	GOTO RX_EXIT
머리오른쪽90도:
	SPEED 머리이동속도
	SERVO 11, 190
	GOTO RX_EXIT
	'******************************************
머리좌우중앙:
    SPEED 머리이동속도
    SERVO 11,100
    GOTO RX_EXITs
머리상하정면:
    SPEED 머리이동속도
    SERVO 11,100	
    SPEED 5
    GOSUB 기본자세
    GOTO RX_EXIT
    '******************************************
상하정면10도:
	SPEED 머리이동속도
	SERVO 16, 10
	GOTO RX_EXIT
상하정면11도:
	SPEED 머리이동속도
	SERVO 16, 11
	GOTO RX_EXIT
상하정면12도:
	SPEED 머리이동속도
	SERVO 16, 12
	GOTO RX_EXIT
상하정면13도:
	SPEED 머리이동속도
	SERVO 16, 13
	GOTO RX_EXIT
상하정면14도:
	SPEED 머리이동속도
	SERVO 16, 14
	GOTO RX_EXIT
상하정면15도:
	SPEED 머리이동속도
	SERVO 16, 15
	GOTO RX_EXIT
상하정면16도:
	SPEED 머리이동속도
	SERVO 16, 16
	GOTO RX_EXIT
상하정면17도:
	SPEED 머리이동속도
	SERVO 16, 17
	GOTO RX_EXIT
상하정면18도:
	SPEED 머리이동속도
	SERVO 16, 18
	GOTO RX_EXIT
상하정면19도:
	SPEED 머리이동속도
	SERVO 16, 19
	GOTO RX_EXIT
상하정면20도:
	SPEED 머리이동속도
	SERVO 16, 20
	GOTO RX_EXIT
상하정면21도:
	SPEED 머리이동속도
	SERVO 16, 21
	GOTO RX_EXIT
상하정면22도:
	SPEED 머리이동속도
	SERVO 16, 22
	GOTO RX_EXIT
상하정면23도:
	SPEED 머리이동속도
	SERVO 16, 23
	GOTO RX_EXIT
상하정면24도:
	SPEED 머리이동속도
	SERVO 16, 24
	GOTO RX_EXIT
상하정면25도:
	SPEED 머리이동속도
	SERVO 16, 25
	GOTO RX_EXIT
상하정면26도:
	SPEED 머리이동속도
	SERVO 16, 26
	GOTO RX_EXIT
상하정면27도:
	SPEED 머리이동속도
	SERVO 16, 27
	GOTO RX_EXIT
상하정면28도:
	SPEED 머리이동속도
	SERVO 16, 28
	GOTO RX_EXIT
상하정면29도:
	SPEED 머리이동속도
	SERVO 16, 29
	GOTO RX_EXIT
상하정면30도:
	SPEED 머리이동속도
	SERVO 16, 30
	GOTO RX_EXIT
상하정면31도:
	SPEED 머리이동속도
	SERVO 16, 31
	GOTO RX_EXIT
상하정면32도:
	SPEED 머리이동속도
	SERVO 16, 32
	GOTO RX_EXIT
상하정면33도:
	SPEED 머리이동속도
	SERVO 16, 33
	GOTO RX_EXIT
상하정면34도:
	SPEED 머리이동속도
	SERVO 16, 34
	GOTO RX_EXIT
상하정면35도:
	SPEED 머리이동속도
	SERVO 16, 35
	GOTO RX_EXIT
상하정면36도:
	SPEED 머리이동속도
	SERVO 16, 36
	GOTO RX_EXIT
상하정면37도:
	SPEED 머리이동속도
	SERVO 16, 37
	GOTO RX_EXIT
상하정면38도:
	SPEED 머리이동속도
	SERVO 16, 38
	GOTO RX_EXIT
상하정면39도:
	SPEED 머리이동속도
	SERVO 16, 39
	GOTO RX_EXIT
상하정면40도:
	SPEED 머리이동속도
	SERVO 16, 40
	GOTO RX_EXIT
상하정면41도:
	SPEED 머리이동속도
	SERVO 16, 41
	GOTO RX_EXIT
상하정면42도:
	SPEED 머리이동속도
	SERVO 16, 42
	GOTO RX_EXIT
상하정면43도:
	SPEED 머리이동속도	
	SERVO 16, 43
	GOTO RX_EXIT
상하정면44도:
	SPEED 머리이동속도
	SERVO 16, 44
	GOTO RX_EXIT
상하정면45도:
	SPEED 머리이동속도
	SERVO 16, 45
	GOTO RX_EXIT
상하정면46도:
	SPEED 머리이동속도
	SERVO 16, 46
	GOTO RX_EXIT
상하정면47도:
	SPEED 머리이동속도
	SERVO 16, 47
	GOTO RX_EXIT
상하정면48도:
	SPEED 머리이동속도
	SERVO 16, 48
	GOTO RX_EXIT
상하정면49도:
	SPEED 머리이동속도
	SERVO 16, 49
	GOTO RX_EXIT
상하정면50도:
	SPEED 머리이동속도
	SERVO 16, 50
	GOTO RX_EXIT
상하정면51도:
	SPEED 머리이동속도
	SERVO 16, 51
	GOTO RX_EXIT
상하정면52도:
	SPEED 머리이동속도
	SERVO 16, 52
	GOTO RX_EXIT
상하정면53도:
	SPEED 머리이동속도
	SERVO 16, 53
	GOTO RX_EXIT
상하정면54도:
	SPEED 머리이동속도
	SERVO 16, 54
	GOTO RX_EXIT
상하정면55도:
	SPEED 머리이동속도
	SERVO 16, 55
	GOTO RX_EXIT
상하정면56도:
	SPEED 머리이동속도
	SERVO 16, 56
	GOTO RX_EXIT
상하정면57도:
	SPEED 머리이동속도
	SERVO 16, 57
	GOTO RX_EXIT
상하정면58도:
	SPEED 머리이동속도
	SERVO 16, 58
	GOTO RX_EXIT
상하정면59도:
	SPEED 머리이동속도
	SERVO 16, 59
	GOTO RX_EXIT
상하정면60도:
	SPEED 머리이동속도
	SERVO 16, 60
	GOTO RX_EXIT
상하정면61도:
	SPEED 머리이동속도
	SERVO 16, 61
	GOTO RX_EXIT
상하정면62도:
	SPEED 머리이동속도
	SERVO 16, 62
	GOTO RX_EXIT
상하정면63도:
	SPEED 머리이동속도
	SERVO 16, 63
	GOTO RX_EXIT
상하정면64도:
	SPEED 머리이동속도
	SERVO 16, 64
	GOTO RX_EXIT
상하정면65도:
	SPEED 머리이동속도
	SERVO 16, 65
	GOTO RX_EXIT
상하정면66도:
	SPEED 머리이동속도
	SERVO 16, 66
	GOTO RX_EXIT
상하정면67도:
	SPEED 머리이동속도
	SERVO 16, 67
	GOTO RX_EXIT
상하정면68도:
	SPEED 머리이동속도
	SERVO 16, 68
	GOTO RX_EXIT
상하정면69도:
	SPEED 머리이동속도
	SERVO 16, 69
	GOTO RX_EXIT
상하정면70도:
	SPEED 머리이동속도
	SERVO 16, 70
	GOTO RX_EXIT
상하정면71도:
	SPEED 머리이동속도
	SERVO 16, 71
	GOTO RX_EXIT
상하정면72도:
	SPEED 머리이동속도
	SERVO 16, 72
	GOTO RX_EXIT
상하정면73도:
	SPEED 머리이동속도
	SERVO 16, 73
	GOTO RX_EXIT
상하정면74도:
	SPEED 머리이동속도
	SERVO 16, 74
	GOTO RX_EXIT
상하정면75도:
	SPEED 머리이동속도
	SERVO 16, 75
	GOTO RX_EXIT
상하정면76도:
	SPEED 머리이동속도
	SERVO 16, 76
	GOTO RX_EXIT
상하정면77도:
	SPEED 머리이동속도
	SERVO 16, 77
	GOTO RX_EXIT
상하정면78도:
	SPEED 머리이동속도
	SERVO 16, 78
	GOTO RX_EXIT
상하정면79도:
	SPEED 머리이동속도
	SERVO 16, 79
	GOTO RX_EXIT
상하정면80도:
	SPEED 머리이동속도
	SERVO 16, 80
	GOTO RX_EXIT
상하정면81도:
	SPEED 머리이동속도
	SERVO 16, 81
	GOTO RX_EXIT
상하정면82도:
	SPEED 머리이동속도
	SERVO 16, 82
	GOTO RX_EXIT
상하정면83도:
	SPEED 머리이동속도
	SERVO 16, 83
	GOTO RX_EXIT
상하정면84도:
	SPEED 머리이동속도
	SERVO 16, 84
	GOTO RX_EXIT
상하정면85도:
	SPEED 머리이동속도
	SERVO 16, 85
	GOTO RX_EXIT
상하정면86도:
	SPEED 머리이동속도
	SERVO 16, 86
	GOTO RX_EXIT
상하정면87도:
	SPEED 머리이동속도
	SERVO 16, 87
	GOTO RX_EXIT
상하정면88도:
	SPEED 머리이동속도
	SERVO 16, 88
	GOTO RX_EXIT
상하정면89도:
	SPEED 머리이동속도
	SERVO 16, 89
	GOTO RX_EXIT
상하정면90도:
	SPEED 머리이동속도
	SERVO 16, 90
	GOTO RX_EXIT
상하정면91도:
	SPEED 머리이동속도
	SERVO 16, 91
	GOTO RX_EXIT
상하정면92도:
	SPEED 머리이동속도
	SERVO 16, 92
	GOTO RX_EXIT
상하정면93도:
	SPEED 머리이동속도
	SERVO 16, 93
	GOTO RX_EXIT
상하정면94도:
	SPEED 머리이동속도
	SERVO 16, 94
	GOTO RX_EXIT
상하정면95도:
	SPEED 머리이동속도
	SERVO 16, 95
	GOTO RX_EXIT
상하정면96도:
	SPEED 머리이동속도
	SERVO 16, 96
	GOTO RX_EXIT
상하정면97도:
	SPEED 머리이동속도
	SERVO 16, 97
	GOTO RX_EXIT
상하정면98도:
	SPEED 머리이동속도
	SERVO 16, 98
	GOTO RX_EXIT
상하정면99도:
	SPEED 머리이동속도
	SERVO 16, 99
	GOTO RX_EXIT
상하정면100도:
	SPEED 머리이동속도
	SERVO 16, 100
	GOTO RX_EXIT
상하정면101도:
	SPEED 머리이동속도
	SERVO 16, 101
	GOTO RX_EXIT
상하정면102도:
	SPEED 머리이동속도
	SERVO 16, 102
	GOTO RX_EXIT
상하정면103도:
	SPEED 머리이동속도
	SERVO 16, 103
	GOTO RX_EXIT
상하정면104도:
	SPEED 머리이동속도
	SERVO 16, 104
	GOTO RX_EXIT
상하정면105도:
	SPEED 머리이동속도
	SERVO 16, 105
	GOTO RX_EXIT
상하정면106도:
	SPEED 머리이동속도
	SERVO 16, 106	
	GOTO RX_EXIT
상하정면107도:
	SPEED 머리이동속도
	SERVO 16, 107
	GOTO RX_EXIT
상하정면108도:
	SPEED 머리이동속도
	SERVO 16, 108
	GOTO RX_EXIT
상하정면109도:
	SPEED 머리이동속도
	SERVO 16, 109
	GOTO RX_EXIT
상하정면110도:
	SPEED 머리이동속도
	SERVO 16, 110
	GOTO RX_EXIT    
    '******************************************
    
	'******************************************
전방하향110도:
    SPEED 머리이동속도
    SERVO 16, 110

    GOTO RX_EXIT
    '******************************************
전방하향105도:
    SPEED 머리이동속도
    SERVO 16, 105
    SERVO 11, 100

    GOTO RX_EXIT
    '******************************************
전방하향100도:
    SPEED 머리이동속도
    SERVO 16, 100
    SERVO 11, 100

    GOTO RX_EXIT
    '******************************************
전방하향97도:
    SPEED 머리이동속도
    SERVO 16, 97
    SERVO 11, 100

    GOTO RX_EXIT
    '******************************************
전방하향95도:
    SPEED 머리이동속도
    SERVO 16, 95
	SERVO 11, 100
    GOTO RX_EXIT
    '******************************************
전방하향90도:
    SPEED 머리이동속도
    SERVO 16, 92
    SERVO 11, 100

    GOTO RX_EXIT
    '******************************************
전방하향85도:
    SPEED 머리이동속도
    SERVO 16, 85
    SERVO 11, 100

    GOTO RX_EXIT
    '******************************************
전방하향80도:
    SPEED 머리이동속도
    SERVO 16, 80
    SERVO 11, 100

    GOTO RX_EXIT
    '******************************************
전방하향75도:
    SPEED 머리이동속도
    SERVO 16, 76
    SERVO 11, 100

    GOTO RX_EXIT
    '******************************************
전방하향70도:
    SPEED 머리이동속도
    SERVO 16, 73
    SERVO 11, 100

    GOTO RX_EXIT
    '******************************************
전방하향65도:
    SPEED 머리이동속도
    SERVO 16, 69
    SERVO 11, 100

    GOTO RX_EXIT
    '******************************************
전방하향60도:
    SPEED 머리이동속도
    SERVO 16, 65
    SERVO 11, 100
    
    MOVE G6B, , , , , 
    ETX  4800,125
    GOTO RX_EXIT
    '******************************************
전방하향55도:
    SPEED 머리이동속도
    SERVO 16, 59

    GOTO RX_EXIT
    '******************************************
전방하향50도:
    SPEED 머리이동속도
    SERVO 16, 54

    GOTO RX_EXIT
    '******************************************

전방하향45도:
    SPEED 머리이동속도
    SERVO 16, 50

    GOTO RX_EXIT
    '******************************************
전방하향40도:
    SPEED 머리이동속도
    SERVO 16, 45

    GOTO RX_EXIT
    '******************************************
전방하향35도:
    SPEED 머리이동속도
    SERVO 16, 40
    
    GOTO RX_EXIT
    '******************************************
전방하향30도:
    SPEED 머리이동속도
    SERVO 16, 36

    GOTO RX_EXIT
    '******************************************
전방하향25도:
    SPEED 머리이동속도
    SERVO 16, 30

    GOTO RX_EXIT
    '******************************************
전방하향20도:
    SPEED 머리이동속도
    SERVO 16, 26

    GOTO RX_EXIT
    '******************************************
전방하향18도:

    SPEED 머리이동속도
    SERVO 16, 22

    GOTO RX_EXIT
    '******************************************
전방하향10도:

    SPEED 머리이동속도
    SERVO 16, 10

    GOTO RX_EXIT
    '******************************************
전방하향:
	SPEED 머리이동속도
	angle_y = angle_y - 5
	IF angle_y < 10 THEN
		MUSIC "C"
		angle_y = 10
		SERVO 16, angle_y
		SERVO 11, angle_x
	ELSE
		SERVO 16, angle_y
		SERVO 11, angle_x
		
	ENDIF
	GOTO RX_EXIT
	'******************************************
전방상향:
	SPEED 머리이동속도
	angle_y = angle_y + 5
	IF angle_y > 110 THEN
		MUSIC "C"
		angle_y = 110
		SERVO 16, angle_y
		SERVO 11, angle_x
		
	ELSE
		SERVO 16, angle_y
		SERVO 11, angle_x
		
	ENDIF
	GOTO RX_EXIT
	'******************************************
우향:
	SPEED 머리이동속도
	angle_x = angle_x + 5
	IF angle_x > 190 THEN
		MUSIC "C"	
		angle_x = 190
		SERVO 16, angle_y
		SERVO 11, angle_x
	ELSE
		SERVO 16, angle_y
		SERVO 11, angle_x
		
	ENDIF
	GOTO RX_EXIT
	'******************************************	
좌향:
	SPEED 머리이동속도
	angle_x = angle_x - 5
	IF angle_x < 10 THEN
		MUSIC "C"
		angle_x = 10
		SERVO 16, angle_y
		SERVO 11, angle_x
	
	ELSE
		SERVO 16, angle_y
		SERVO 11, angle_x
	
	ENDIF
	GOTO RX_EXIT












    '******************************************
    '******************************************
앞뒤기울기측정:
    FOR i = 0 TO COUNT_MAX
        A = AD(앞뒤기울기AD포트)	'기울기 앞뒤
        IF A > 250 OR A < 5 THEN RETURN
        IF A > MIN AND A < MAX THEN RETURN
        DELAY 기울기확인시간
    NEXT i

    IF A < MIN THEN
        GOSUB 기울기앞
    ELSEIF A > MAX THEN
        GOSUB 기울기뒤
    ENDIF

    RETURN
    '**************************************************
기울기앞:
    A = AD(앞뒤기울기AD포트)
    'IF A < MIN THEN GOSUB 앞으로일어나기
    IF A < MIN THEN
        ETX  4800,16
        GOSUB 뒤로일어나기

    ENDIF
    RETURN

기울기뒤:
    A = AD(앞뒤기울기AD포트)
    'IF A > MAX THEN GOSUB 뒤로일어나기
    IF A > MAX THEN
        ETX  4800,15
        GOSUB 앞으로일어나기
    ENDIF
    RETURN
    '**************************************************
좌우기울기측정:
    FOR i = 0 TO COUNT_MAX
        B = AD(좌우기울기AD포트)	'기울기 좌우
        IF B > 250 OR B < 5 THEN RETURN
        IF B > MIN AND B < MAX THEN RETURN
        DELAY 기울기확인시간
    NEXT i

    IF B < MIN OR B > MAX THEN
        SPEED 8
        MOVE G6B,140,  40,  80
        MOVE G6C,140,  40,  80
        WAIT
        GOSUB 기본자세	
    ENDIF
    RETURN
    '******************************************
    '************************************************
SOUND_PLAY_CHK:
    DELAY 60
    SOUND_BUSY = IN(46)
    IF SOUND_BUSY = 1 THEN GOTO SOUND_PLAY_CHK
    DELAY 50

    RETURN
    '************************************************

    '************************************************
NUM_1_9:
    IF NUM = 1 THEN
        PRINT "1"
    ELSEIF NUM = 2 THEN
        PRINT "2"
    ELSEIF NUM = 3 THEN
        PRINT "3"
    ELSEIF NUM = 4 THEN
        PRINT "4"
    ELSEIF NUM = 5 THEN
        PRINT "5"
    ELSEIF NUM = 6 THEN
        PRINT "6"
    ELSEIF NUM = 7 THEN
        PRINT "7"
    ELSEIF NUM = 8 THEN
        PRINT "8"
    ELSEIF NUM = 9 THEN
        PRINT "9"
    ELSEIF NUM = 0 THEN
        PRINT "0"
    ENDIF

    RETURN
    '************************************************
    '************************************************
NUM_TO_ARR:

    NO_4 =  BUTTON_NO / 10000
    TEMP_INTEGER = BUTTON_NO MOD 10000

    NO_3 =  TEMP_INTEGER / 1000
    TEMP_INTEGER = BUTTON_NO MOD 1000

    NO_2 =  TEMP_INTEGER / 100
    TEMP_INTEGER = BUTTON_NO MOD 100

    NO_1 =  TEMP_INTEGER / 10
    TEMP_INTEGER = BUTTON_NO MOD 10

    NO_0 =  TEMP_INTEGER

    RETURN
    '************************************************
Number_Play: '  BUTTON_NO = 숫자대입


    GOSUB NUM_TO_ARR

    PRINT "NPL "
    '*************

    NUM = NO_4
    GOSUB NUM_1_9

    '*************
    NUM = NO_3
    GOSUB NUM_1_9

    '*************
    NUM = NO_2
    GOSUB NUM_1_9
    '*************
    NUM = NO_1
    GOSUB NUM_1_9
    '*************
    NUM = NO_0
    GOSUB NUM_1_9
    PRINT " !"

    ' GOSUB SOUND_PLAY_CHK
    '    PRINT "SND 16 !"
    '    GOSUB SOUND_PLAY_CHK
    RETURN
    '************************************************

    RETURN


    '******************************************

    ' ************************************************
적외선거리센서확인:

    적외선거리값 = AD(적외선AD포트)

    IF 적외선거리값 > 50 THEN '50 = 적외선거리값 = 25cm
        'MUSIC "C"
        DELAY 200
    ENDIF


    RETURN

    '******************************************
변수값_음성값출력:

    J = AD(적외선AD포트)	'적외선거리값 읽기
    BUTTON_NO = J
    GOSUB Number_Play
    GOSUB SOUND_PLAY_CHK
    GOSUB GOSUB_RX_EXIT


    RETURN

    '************************************************
골프_왼쪽으로_샷1:

    CONST 골프채높이 = 135

    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,150,  100,  10, 10
    WAIT

    MOVE G6C,135,  20,  90, 10
    WAIT

    DELAY 400


    MOVE G6C,135,  40,  90, 10
    WAIT

    '**** 골프 _왼쪽으로_샷 스피드 *******
    'HIGHSPEED SETON
    SPEED 8
    MOVE G6C,135,  10,  70, 10
    WAIT
    DELAY 1000
    ' HIGHSPEED SETOFF

    '************

    SPEED 8
    MOVE G6C,135,  100,  10, 10
    WAIT

    MOVE G6C,135,  50,  60, 190
    WAIT

    GOSUB 기본자세

    RETURN
    '******************************************

골프_왼쪽으로_어드레스1:
    GOSUB All_motor_mode3

    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,150,  100,  10, 10
    WAIT


    MOVE G6C,135,  20,  90, 10
    WAIT

    RETURN
    '******************************************

    '************************************************
골프_오른쪽으로_샷1:

    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,100,  130,  10, 10
    WAIT

    MOVE G6C,145,  130,  10, 10
    WAIT

    MOVE G6C,145,  60,  10, 10
    WAIT

    MOVE G6C,135,  40,  30, 10
    WAIT


    MOVE G6C,140,  10,  80, 10
    WAIT

    DELAY 400

    MOVE G6B,100,  35,  90,
    MOVE G6C,140,  10,  70, 10
    WAIT


    '**** 골프 _오른쪽으로_샷 스피드 *******
    'HIGHSPEED SETON
    SPEED 3

    MOVE G6C,140,  30,  100, 10
    WAIT
    DELAY 1000
    ' HIGHSPEED SETOFF

    '************

    SPEED 8
    MOVE G6C,135,  50,  60, 190
    WAIT

    GOSUB 기본자세

    RETURN
    '******************************************


골프_오른쪽으로_어드레스1:
    GOSUB All_motor_mode3

    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,150,  100,  10, 10
    WAIT


    MOVE G6C,135,  40,  40, 10
    WAIT

    MOVE G6C,135,  10,  80, 10
    WAIT


    RETURN
    '******************************************
    '******************************************	
MAIN: '라벨설정

    ETX 4800, 38 ' 동작 멈춤 확인 송신 값

MAIN_2:

    GOSUB 앞뒤기울기측정
    GOSUB 좌우기울기측정
    GOSUB 적외선거리센서확인


    ERX 4800,A,MAIN_2	

    A_old = A

    '**** 입력된 A값이 0 이면 MAIN 라벨로 가고
    '**** 1이면 KEY1 라벨, 2이면 key2로... 가는문
    ON A GOTO MAIN,KEY1,KEY2,KEY3,KEY4,KEY5,KEY6,KEY7,KEY8,KEY9,KEY10,KEY11,KEY12,KEY13,KEY14,KEY15,KEY16,KEY17,KEY18,KEY19,KEY20,KEY21,KEY22,KEY23,KEY24,KEY25,KEY26,KEY27,KEY28,KEY29,KEY30,KEY31,KEY32,KEY33,KEY34,KEY35,KEY36,KEY37,KEY38,KEY39,KEY40,KEY41,KEY42,KEY43,KEY44,KEY45,KEY46,KEY47,KEY48,KEY49,KEY50,KEY51,KEY52,KEY53,KEY54,KEY55,KEY56,KEY57,KEY58,KEY59,KEY60,KEY61,KEY62,KEY63,KEY64,KEY65,KEY66,KEY67,KEY68,KEY69,KEY70,KEY71,KEY72,KEY73,KEY74,KEY75,KEY76,KEY77,KEY78,KEY79,KEY80,KEY81,KEY82,KEY83,KEY84,KEY85,KEY86,KEY87,KEY88,KEY89,KEY90,KEY91,KEY92,KEY93,KEY94,KEY95,KEY96,KEY97,KEY98,KEY99,KEY100,KEY101,KEY102,KEY103,KEY104,KEY105,KEY106,KEY107,KEY108,KEY109,KEY110,KEY111,KEY112,KEY113,KEY114,KEY115,KEY116,KEY117,KEY118,KEY119,KEY120,KEY121,KEY122,KEY123,KEY124,KEY125,KEY126,KEY127,KEY128,KEY129,KEY130,KEY131,KEY132,KEY133,KEY134,KEY135,KEY136,KEY137,KEY138,KEY139,KEY140,KEY141,KEY142,KEY143,KEY144,KEY145,KEY146,KEY147,KEY148,KEY149,KEY150,KEY151,KEY152,KEY153,KEY154,KEY155,KEY156,KEY157,KEY158,KEY159,KEY160,KEY161,KEY162,KEY163,KEY164,KEY165,KEY166,KEY167,KEY168,KEY169,KEY170,KEY171,KEY172,KEY173,KEY174,KEY175,KEY176,KEY177,KEY178,KEY179,KEY180,KEY181,KEY182,KEY183,KEY184,KEY185,KEY186,KEY187,KEY188,KEY189,KEY190,KEY191,KEY192,KEY193,KEY194,KEY195,KEY196,KEY197,KEY198,KEY199,KEY200,KEY201,KEY202,KEY203,KEY204,KEY205,KEY206,KEY207,KEY208,KEY209,KEY210,KEY211,KEY212,KEY213,KEY214,KEY215,KEY216,KEY217,KEY218,KEY219,KEY220,KEY221,KEY222,KEY223,KEY224,KEY225,KEY226,KEY227,KEY228,KEY229,KEY230,KEY231,KEY232,KEY233,KEY234,KEY235,KEY236,KEY237,KEY238,KEY239,KEY240,KEY241,KEY242,KEY243,KEY244,KEY245,KEY246,KEY247,KEY248,KEY249,KEY250,KEY251,KEY252,KEY253,KEY254,KEY255,KEY256,KEY257,KEY258,KEY259,KEY260,KEY261,KEY262,KEY263,KEY264,KEY265,KEY266,KEY267,KEY268,KEY269,KEY270,KEY271,KEY272,KEY273,KEY274,KEY275,KEY276,KEY277,KEY278,KEY279,KEY280,KEY281,KEY282,KEY283,KEY284,KEY285,KEY286,KEY287,KEY288,KEY289,KEY290,KEY291,KEY292,KEY293,KEY294,KEY295,KEY296,KEY297,KEY298,KEY299,KEY300,KEY301,KEY302,KEY303,KEY304,KEY305,KEY306,KEY307,KEY308,KEY309,KEY310,KEY311,KEY312,KEY313,KEY314,KEY315,KEY316,KEY317,KEY318,KEY319,KEY320,KEY321,KEY322,KEY323,KEY324,KEY325,KEY326,KEY327,KEY328,KEY329,KEY330,KEY331,KEY332,KEY333,KEY334,KEY335,KEY336,KEY337,KEY338,KEY339,KEY340,KEY341,KEY342,KEY343,KEY344,KEY345,KEY346,KEY347,KEY348,KEY349,KEY350,KEY351,KEY352,KEY353,KEY354,KEY355,KEY356,KEY357,KEY358,KEY359,KEY360,KEY361,KEY362,KEY363,KEY364,KEY365,KEY366,KEY367,KEY368,KEY369,KEY370,KEY371,KEY372,KEY373,KEY374,KEY375,KEY376,KEY377,KEY378,KEY379,KEY380,KEY381,KEY382,KEY383,KEY384,KEY385,KEY386,KEY387,KEY388,KEY389,KEY390,KEY391,KEY392,KEY393,KEY394,KEY395,KEY396,KEY397,KEY398,KEY399,KEY400,KEY401,KEY402,KEY403,KEY404,KEY405,KEY406,KEY407,KEY408,KEY409,KEY410,KEY411,KEY412,KEY413,KEY414,KEY415,KEY416,KEY417,KEY418,KEY419,KEY420,KEY421,KEY422,KEY423,KEY424,KEY425,KEY426,KEY427,KEY428,KEY429,KEY430,KEY431,KEY432,KEY433,KEY434,KEY435,KEY436,KEY437,KEY438,KEY439,KEY440,KEY441,KEY442,KEY443,KEY444,KEY445,KEY446,KEY447,KEY448,KEY449,KEY450,KEY451,KEY452


  '  IF A > 100 AND A < 110 THEN
'        BUTTON_NO = A - 100
'        GOSUB Number_Play
'        GOSUB SOUND_PLAY_CHK
'        GOSUB GOSUB_RX_EXIT
'
'
'    ELSE
    IF A = 250 THEN
        GOSUB All_motor_mode3
        SPEED 4
        MOVE G6A,100,  76, 145,  93, 100, 100
        MOVE G6D,100,  76, 145,  93, 100, 100
        MOVE G6B,100,  40,  90,
        MOVE G6C,100,  40,  90,
        WAIT
        DELAY 500
        SPEED 6
        GOSUB 기본자세

    ENDIF


    GOTO MAIN	
    '*******************************************
    '		MAIN 라벨로 가기
    '*******************************************

KEY1:
    ETX  4800,1
    GOTO 왼쪽턴5_골프


    GOTO RX_EXIT
    '***************	
KEY2:
    ETX  4800,2


    GOSUB 골프_왼쪽으로_샷1


    GOTO RX_EXIT
    '***************
KEY3:
    ETX  4800,3

    GOTO 오른쪽턴5_골프

    GOTO RX_EXIT
    '***************
KEY4:
    ETX  4800,4

    GOTO 왼쪽턴10_골프

    GOTO RX_EXIT
    '***************
KEY5:
    ETX  4800,5

    GOSUB 골프_오른쪽으로_샷1



    GOTO RX_EXIT
    '***************
KEY6:
    ETX  4800,6

    GOTO 오른쪽턴10_골프


    GOTO RX_EXIT
    '***************
KEY7:
    ETX  4800,7
    GOTO 왼쪽턴20_골프

    GOTO RX_EXIT
    '***************
KEY8:
    ETX  4800,8


    GOTO RX_EXIT
    '***************
KEY9:
    ETX  4800,9
    GOTO 오른쪽턴20_골프


    GOTO RX_EXIT
    '***************
'KEY10: '0
    'ETX  4800,10 
    '보행횟수=1 
    'GOTO 전진종종걸음_골프
    'GOTO RX_EXIT 
    '***************
KEY10:
	ETX  4800,10
	보행횟수= 1
	GOTO 공으로다가가기
	GOTO RX_EXIT
	'***************'***************'***************    
    
KEY11: ' ▲
    ETX  4800,11
    GOTO 연속전진_골프
    GOTO RX_EXIT
    '***************
KEY12: ' ▼
    ETX  4800,12
    GOTO 연속후진_골프

    GOTO RX_EXIT
    '***************
KEY13: '▶
    ETX  4800,13
    GOTO 오른쪽옆으로70연속_골프


    GOTO RX_EXIT
    '***************
KEY14: ' ◀
    ETX  4800,14
    GOTO 왼쪽옆으로70연속_골프


    GOTO RX_EXIT
    '***************
KEY15: ' A
    ETX  4800,15
    GOTO 왼쪽옆으로20_골프


    GOTO RX_EXIT
    '***************
KEY16: ' POWER
    ETX  4800,16

    GOSUB Leg_motor_mode3
    IF MODE = 0 THEN
        SPEED 10
        MOVE G6A,100, 140,  37, 145, 100, 100
        MOVE G6D,100, 140,  37, 145, 100, 100
        WAIT
    ENDIF
    SPEED 4
    GOSUB 앉은자세	
    GOSUB 종료음

    GOSUB MOTOR_GET
    GOSUB MOTOR_OFF


    GOSUB GOSUB_RX_EXIT
KEY16_1:

    IF 모터ONOFF = 1  THEN
        OUT 52,1
        DELAY 200
        OUT 52,0
        DELAY 200
    ENDIF
    ERX 4800,A,KEY16_1
    ETX  4800,A

    '**** RX DATA Number Sound ********
    BUTTON_NO = A
    GOSUB Number_Play
    GOSUB SOUND_PLAY_CHK


    IF  A = 16 THEN 	'다시 파워버튼을 눌러야만 복귀
        GOSUB MOTOR_ON
        SPEED 10
        MOVE G6A,100, 140,  37, 145, 100, 100
        MOVE G6D,100, 140,  37, 145, 100, 100
        WAIT

        GOSUB 기본자세2
        GOSUB 자이로ON
        GOSUB All_motor_mode3
        GOTO RX_EXIT
    ENDIF

    GOSUB GOSUB_RX_EXIT
    GOTO KEY16_1



    GOTO RX_EXIT
    '***************
KEY17: ' C
    ETX  4800,17
    GOTO 머리왼쪽90도


    GOTO RX_EXIT
    '***************
KEY18: ' E
    ETX  4800,18	


    GOSUB 자이로OFF
    GOSUB 에러음
KEY18_wait:

    ERX 4800,A,KEY18_wait	

    IF  A = 26 THEN
        GOSUB 시작음
        GOSUB 자이로ON
        GOTO RX_EXIT
    ENDIF

    GOTO KEY18_wait


    GOTO RX_EXIT
    '***************
KEY19: ' P2
    ETX  4800,19
    GOTO 오른쪽턴60_골프

    GOTO RX_EXIT
    '***************
KEY20: ' B	
    ETX  4800,20
    GOTO 오른쪽옆으로20_골프


    GOTO RX_EXIT
    '***************
KEY21: ' △
    ETX  4800,21
    GOTO 전방상향

    GOTO RX_EXIT
    '***************
KEY22: ' *	
    ETX  4800,22
    GOTO 왼쪽턴45_골프

    GOTO RX_EXIT
    '***************
KEY23: ' G
    ETX  4800,23




    GOTO RX_EXIT
    '***************
KEY24: ' #
    ETX  4800,24
    GOTO 오른쪽턴45_골프

    GOTO RX_EXIT
    '***************
KEY25: ' P1
    ETX  4800,25
    GOTO 왼쪽턴60_골프

    GOTO RX_EXIT
    '***************
KEY26: ' ■
    ETX  4800,26

    SPEED 5
    GOSUB 기본자세2	
    TEMPO 220
    MUSIC "ff"
    GOSUB 기본자세
    GOTO RX_EXIT
    '***************
KEY27: ' D
    ETX  4800,27
    GOTO 머리오른쪽90도


    GOTO RX_EXIT
    '***************
KEY28: ' ◁
    ETX  4800,28
    GOTO 좌향
    GOTO RX_EXIT
    '***************
KEY29: ' □
    ETX  4800,29

    GOTO 전원초기자세

    GOTO RX_EXIT
    '***************
KEY30: ' ▷
    ETX  4800,30
    GOTO 우향
    GOTO RX_EXIT
    '***************
KEY31: ' ▽
    ETX  4800,31
    GOTO 전방하향

    GOTO RX_EXIT
    '***************

KEY32: ' F
    ETX  4800,32
    GOTO 후진종종걸음_골프
    GOTO RX_EXIT
    '***************

KEY33:
	ETX  4800, 33
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY34:
	ETX  4800, 34
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY35:
	ETX  4800, 35
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY36:
	ETX  4800, 36
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY37:
	ETX  4800, 37
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY38:
	ETX  4800, 38
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY39:
	ETX 4800, 39
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY40:
	ETX 4800, 40
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY41:
	ETX 4800, 41
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY42:
	ETX 4800, 42
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY43:
	ETX 4800, 43
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY44:
	ETX 4800, 44
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY45:
	ETX 4800, 45
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY46:
	ETX 4800, 46
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY47:
	ETX 4800, 47
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY48:
	ETX 4800, 48
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY49:
	ETX 4800, 49
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY50:
	ETX 4800, 50
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY51:
	ETX 4800, 51
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY52:
	ETX 4800, 52
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY53:
	ETX 4800, 53
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY54:
	ETX 4800, 54
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY55:
	ETX 4800, 55
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY56:
	ETX 4800, 56
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY57:
	ETX 4800, 57
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY58:
	ETX 4800, 58
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY59:
	ETX 4800, 59
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY60:
	ETX 4800, 60
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY61:
	ETX 4800, 61
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY62:
	ETX 4800, 62
	GOTO 고개중앙기본자세
	GOTO RX_EXIT

KEY63:
	ETX 4800, 63
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY64:
	ETX 4800, 64
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY65:
	ETX 4800, 65
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY66:
	ETX 4800, 66
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY67:
	ETX 4800, 67
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY68:
	ETX 4800, 68
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY69:
	ETX 4800, 69
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY70:
	ETX 4800, 70
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY71:
	ETX 4800, 71
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY72:
	ETX 4800, 72
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY73:
	ETX 4800, 73
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY74:
	ETX 4800, 74
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY75:
	ETX 4800, 75
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY76:
	ETX 4800, 76
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY77:
	ETX 4800, 77
	GOTO 고개중앙기본자세
	GOTO RX_EXIT	

KEY78:
	ETX 4800, 78
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY79:
	ETX 4800, 79
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY80:
	ETX 4800, 80
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY81:
	ETX 4800, 81
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY82:
	ETX 4800, 82
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY83:
	ETX 4800, 83
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY84:
	ETX 4800, 84
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY85:
	ETX 4800, 85
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY86:
	ETX 4800, 86
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY87:
	ETX 4800, 87
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY88:
	ETX 4800, 88
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY89:
	ETX 4800, 89
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY90:
	ETX 4800, 90
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY91:
	ETX 4800, 91
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY92:
	ETX 4800, 92
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY93:
	ETX 4800, 93
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY94:
	ETX 4800, 94
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY95:
	ETX 4800, 95
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY96:
	ETX 4800, 96
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY97:
	ETX 4800, 97
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY98:
	ETX 4800, 98
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY99:
	ETX 4800, 99
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
	
'KEY33 ~ KEY99 까지 처음 시작할 때 어떤 자세로 할지 똑같이 넣어주기
	
	'************************************** 여기부터 모션 코드 시작 *******************************
	
KEY100:
	ETX 4800, 100
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
	
	'******** walk - FORWARD ********
KEY101:
	ETX 4800, 101
	보행횟수 = 1
	GOTO 공으로다가가기'횟수_전진종종걸음으로 바꾸면 좋을듯
	GOTO RX_EXIT
KEY102:
	ETX 4800, 102
	보행횟수 = 1
	'GOTO           
	GOTO RX_EXIT
KEY103:
	ETX 4800,103
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
	'******************
KEY104:
	ETX 4800,104
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY105:
	ETX 4800,105
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY106:
	ETX 4800,106
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY107:
	ETX 4800,107
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY108:
	ETX 4800,108
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY109:
	ETX 4800,109
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY110:
	ETX 4800,110
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
	'******** walk - BACKWARD ********
KEY111:
	ETX 4800, 101
	보행횟수 = 1
	GOTO 공으로다가가기'횟수_전진종종걸음으로 바꾸면 좋을듯
	GOTO RX_EXIT
KEY112:
	ETX 4800, 102
	보행횟수 = 1
	'GOTO           
	GOTO RX_EXIT
KEY113:
	ETX 4800,103
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
	'******************
KEY114:
	ETX 4800,114
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY115:
	ETX 4800,115
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY116:
	ETX 4800,116
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY117:
	ETX 4800,117
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY118:
	ETX 4800,118
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY119:
	ETX 4800,119
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
KEY120:
	ETX 4800,120
	GOTO 고개중앙기본자세
	GOTO RX_EXIT
	'****************** set_head ******************
KEY121:
    ETX  4800,121
    GOTO 전방하향20도
    GOTO RX_EXIT
KEY122:
    ETX  4800,122
    GOTO 전방하향30도
    GOTO RX_EXIT
KEY123:
    ETX  4800,123
    GOTO 전방하향40도
    GOTO RX_EXIT
KEY124:
    ETX  4800,124
    GOTO 전방하향45도
    GOTO RX_EXIT
KEY125:
    ETX  4800,125
    GOTO 전방하향60도
    GOTO RX_EXIT
KEY126:
    ETX  4800,126
    GOTO 전방하향70도
    GOTO RX_EXIT
KEY127:
    ETX  4800,127
    GOTO 전방하향80도
    GOTO RX_EXIT
KEY128:
    ETX  4800,128
    GOTO 전방하향90도
    GOTO RX_EXIT
KEY129:
    ETX  4800,129
    GOTO 전방하향100도
    GOTO RX_EXIT
KEY130:
    ETX  4800,130
    GOTO 전방하향110도
    GOTO RX_EXIT
	'******************
KEY131:
    ETX 4800, 131
    GOTO 머리왼쪽90도
    GOTO RX_EXIT
KEY132:
    ETX 4800, 132
    GOTO 머리왼쪽60도
    GOTO RX_EXIT
KEY133:
    ETX 4800, 133
    GOTO 머리왼쪽45도
    GOTO RX_EXIT
KEY134:
    ETX 4800, 134
    GOTO 머리왼쪽30도
    GOTO RX_EXIT
KEY135:
    ETX 4800, 135
    GOTO 머리좌우중앙
    GOTO RX_EXIT
KEY136:
    ETX 4800, 136
    GOTO 머리오른쪽30도
    GOTO RX_EXIT
KEY137:
    ETX 4800, 137
    GOTO 머리오른쪽45도
    GOTO RX_EXIT
KEY138:
    ETX 4800, 138
    GOTO 머리오른쪽60도
    GOTO RX_EXIT
KEY139:
    ETX 4800, 139
    GOTO 머리오른쪽90도
    GOTO RX_EXIT
KEY140:
    ETX 4800, 140
    GOTO 머리상하정면
    GOTO RX_EXIT
    '****************** turn ******************
KEY141:
    ETX 4800, 141
    GOTO 왼쪽턴10_골프
    GOTO RX_EXIT
KEY142:
    ETX 4800, 142
    GOTO 왼쪽턴20_골프
    GOTO RX_EXIT
KEY143:
    ETX 4800, 143
    GOTO 왼쪽턴45_골프
    GOTO RX_EXIT
KEY144:
    ETX 4800, 144
    GOTO 왼쪽턴60_골프
    GOTO RX_EXIT
KEY145:
    ETX 4800, 145
    GOTO 오른쪽턴10_골프
    GOTO RX_EXIT
KEY146:
    ETX 4800, 146
    GOTO 오른쪽턴20_골프
    GOTO RX_EXIT
KEY147:
    ETX 4800, 147
    GOTO 오른쪽턴45_골프
    GOTO RX_EXIT
KEY148:
    ETX 4800, 148
    GOTO 오른쪽턴60_골프
    GOTO RX_EXIT
KEY149:
    ETX 4800, 149
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY150:
    ETX 4800, 150
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY151:
    ETX 4800, 151
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY152:
    ETX 4800, 152
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY153:
    ETX 4800, 153
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY154:
    ETX 4800, 154
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY155:
    ETX 4800, 155
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY156:
    ETX 4800, 156
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY157:
    ETX 4800, 157
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY158:
    ETX 4800, 158
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY159:
    ETX 4800, 159
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY160:
    ETX 4800, 160
    GOTO 고개중앙기본자세
    GOTO RX_EXIT

    '**************** walk_side ********************
KEY161:
    ETX 4800, 161
    GOTO 왼쪽옆으로20_골프
    GOTO RX_EXIT
KEY162:
    ETX 4800, 162
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY163:
    ETX 4800, 163
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY164:
    ETX 4800, 164
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY165:
    ETX 4800, 165
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY166:
    ETX 4800, 166
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY167:
    ETX 4800, 167
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY168:
    ETX 4800, 168
    GOTO 고개중앙기본자세
    GOTO RX_EXIT
KEY169:
    ETX 4800, 169
    GOTO 오른쪽옆으로20_골프
    GOTO RX_EXIT
    '*************** Putting  ***************
KEY170:
    ETX 4800, 170
    GOSUB 골프_오른쪽으로_샷1
    GOTO RX_EXIT
KEY171:
	ETX 4800, 171
	GOSUB 골프_왼쪽으로_샷1
    GOTO RX_EXIT
    '*************** head_set more 상하정면 ***************
KEY172:
	ETX 4800 172
	GOTO 상하정면10도
	GOTO RX_EXIT
KEY173:
	ETX 4800 173
	GOTO 상하정면11도
	GOTO RX_EXIT
KEY174:
	ETX 4800 174
	GOTO 상하정면12도
	GOTO RX_EXIT
KEY175:
	ETX 4800 175
	GOTO 상하정면13도
	GOTO RX_EXIT
KEY176:
	ETX 4800 176
	GOTO 상하정면14도
	GOTO RX_EXIT
KEY177:
	ETX 4800 177
	GOTO 상하정면15도
	GOTO RX_EXIT
KEY178:
	ETX 4800 178
	GOTO 상하정면16도
	GOTO RX_EXIT
KEY179:
	ETX 4800 179
	GOTO 상하정면17도
	GOTO RX_EXIT
KEY180:
	ETX 4800 180
	GOTO 상하정면18도
	GOTO RX_EXIT
KEY181:
	ETX 4800 181
	GOTO 상하정면19도
	GOTO RX_EXIT
KEY182:
	ETX 4800 182
	GOTO 상하정면20도
	GOTO RX_EXIT
KEY183:
	ETX 4800 183
	GOTO 상하정면21도
	GOTO RX_EXIT
KEY184:
	ETX 4800 184
	GOTO 상하정면22도
	GOTO RX_EXIT
KEY185:
	ETX 4800 185
	GOTO 상하정면23도
	GOTO RX_EXIT
KEY186:
	ETX 4800 186
	GOTO 상하정면24도
	GOTO RX_EXIT
KEY187:
	ETX 4800 187
	GOTO 상하정면25도
	GOTO RX_EXIT
KEY188:
	ETX 4800 188
	GOTO 상하정면26도
	GOTO RX_EXIT
KEY189:
	ETX 4800 189
	GOTO 상하정면27도
	GOTO RX_EXIT
KEY190:
	ETX 4800 190
	GOTO 상하정면28도
	GOTO RX_EXIT
KEY191:
	ETX 4800 191
	GOTO 상하정면29도
	GOTO RX_EXIT
KEY192:
	ETX 4800 192
	GOTO 상하정면30도
	GOTO RX_EXIT
KEY193:
	ETX 4800 193
	GOTO 상하정면31도
	GOTO RX_EXIT
KEY194:
	ETX 4800 194
	GOTO 상하정면32도
	GOTO RX_EXIT
KEY195:
	ETX 4800 195
	GOTO 상하정면33도
	GOTO RX_EXIT
KEY196:
	ETX 4800 196
	GOTO 상하정면34도
	GOTO RX_EXIT
KEY197:
	ETX 4800 197
	GOTO 상하정면35도
	GOTO RX_EXIT
KEY198:
	ETX 4800 198
	GOTO 상하정면36도
	GOTO RX_EXIT
KEY199:
	ETX 4800 199
	GOTO 상하정면37도
	GOTO RX_EXIT
KEY200:
	ETX 4800 200
	GOTO 상하정면38도
	GOTO RX_EXIT
KEY201:
	ETX 4800 201
	GOTO 상하정면39도
	GOTO RX_EXIT
KEY202:
	ETX 4800 202
	GOTO 상하정면40도
	GOTO RX_EXIT
KEY203:
	ETX 4800 203
	GOTO 상하정면41도
	GOTO RX_EXIT
KEY204:
	ETX 4800 204
	GOTO 상하정면42도
	GOTO RX_EXIT
KEY205:
	ETX 4800 205
	GOTO 상하정면43도
	GOTO RX_EXIT
KEY206:
	ETX 4800 206
	GOTO 상하정면44도
	GOTO RX_EXIT
KEY207:
	ETX 4800 207
	GOTO 상하정면45도
	GOTO RX_EXIT
KEY208:
	ETX 4800 208
	GOTO 상하정면46도
	GOTO RX_EXIT
KEY209:
	ETX 4800 209
	GOTO 상하정면47도
	GOTO RX_EXIT
KEY210:
	ETX 4800 210
	GOTO 상하정면48도
	GOTO RX_EXIT
KEY211:
	ETX 4800 211
	GOTO 상하정면49도
	GOTO RX_EXIT
KEY212:
	ETX 4800 212
	GOTO 상하정면50도
	GOTO RX_EXIT
KEY213:
	ETX 4800 213
	GOTO 상하정면51도
	GOTO RX_EXIT
KEY214:
	ETX 4800 214
	GOTO 상하정면52도
	GOTO RX_EXIT
KEY215:
	ETX 4800 215
	GOTO 상하정면53도
	GOTO RX_EXIT
KEY216:
	ETX 4800 216
	GOTO 상하정면54도
	GOTO RX_EXIT
KEY217:
	ETX 4800 217
	GOTO 상하정면55도
	GOTO RX_EXIT
KEY218:
	ETX 4800 218
	GOTO 상하정면56도
	GOTO RX_EXIT
KEY219:
	ETX 4800 219
	GOTO 상하정면57도
	GOTO RX_EXIT
KEY220:
	ETX 4800 220
	GOTO 상하정면58도
	GOTO RX_EXIT
KEY221:
	ETX 4800 221
	GOTO 상하정면59도
	GOTO RX_EXIT
KEY222:
	ETX 4800 222
	GOTO 상하정면60도
	GOTO RX_EXIT
KEY223:
	ETX 4800 223
	GOTO 상하정면61도
	GOTO RX_EXIT
KEY224:
	ETX 4800 224
	GOTO 상하정면62도
	GOTO RX_EXIT
KEY225:
	ETX 4800 225
	GOTO 상하정면63도
	GOTO RX_EXIT
KEY226:
	ETX 4800 226
	GOTO 상하정면64도
	GOTO RX_EXIT
KEY227:
	ETX 4800 227
	GOTO 상하정면65도
	GOTO RX_EXIT
KEY228:
	ETX 4800 228
	GOTO 상하정면66도
	GOTO RX_EXIT
KEY229:
	ETX 4800 229
	GOTO 상하정면67도
	GOTO RX_EXIT
KEY230:
	ETX 4800 230
	GOTO 상하정면68도
	GOTO RX_EXIT
KEY231:
	ETX 4800 231
	GOTO 상하정면69도
	GOTO RX_EXIT
KEY232:
	ETX 4800 232 
	GOTO 상하정면70도
	GOTO RX_EXIT
KEY233:
	ETX 4800 233
	GOTO 상하정면71도
	GOTO RX_EXIT
KEY234:
	ETX 4800 234
	GOTO 상하정면72도
	GOTO RX_EXIT
KEY235:
	ETX 4800 235
	GOTO 상하정면73도
	GOTO RX_EXIT
KEY236:
	ETX 4800 236
	GOTO 상하정면74도
	GOTO RX_EXIT
KEY237:
	ETX 4800 237
	GOTO 상하정면75도
	GOTO RX_EXIT
KEY238:
	ETX 4800 238
	GOTO 상하정면76도
	GOTO RX_EXIT
KEY239:
	ETX 4800 239
	GOTO 상하정면77도
	GOTO RX_EXIT
KEY240:
	ETX 4800 240
	GOTO 상하정면78도
	GOTO RX_EXIT
KEY241:
	ETX 4800 241
	GOTO 상하정면79도
	GOTO RX_EXIT
KEY242:
	ETX 4800 242
	GOTO 상하정면80도
	GOTO RX_EXIT
KEY243:
	ETX 4800 243
	GOTO 상하정면81도
	GOTO RX_EXIT
KEY244:
	ETX 4800 244
	GOTO 상하정면82도
	GOTO RX_EXIT
KEY245:
	ETX 4800 245
	GOTO 상하정면83도
	GOTO RX_EXIT
KEY246:
	ETX 4800 246
	GOTO 상하정면84도
	GOTO RX_EXIT
KEY247:
	ETX 4800 247
	GOTO 상하정면85도
	GOTO RX_EXIT
KEY248:
	ETX 4800 248
	GOTO 상하정면86도
	GOTO RX_EXIT
KEY249:
	ETX 4800 249
	GOTO 상하정면87도
	GOTO RX_EXIT
KEY250:
	ETX 4800 250
	GOTO 상하정면88도
	GOTO RX_EXIT
KEY251:
	ETX 4800 251
	GOTO 상하정면89도
	GOTO RX_EXIT
KEY252:
	ETX 4800 252
	GOTO 상하정면90도
	GOTO RX_EXIT
KEY253:
	ETX 4800 253
	GOTO 상하정면91도
	GOTO RX_EXIT
KEY254:
	ETX 4800 254
	GOTO 상하정면92도
	GOTO RX_EXIT
KEY255:
	ETX 4800 255
	GOTO 상하정면93도
	GOTO RX_EXIT
KEY256:
	ETX 4800 256
	GOTO 상하정면94도
	GOTO RX_EXIT
KEY257:
	ETX 4800 257
	GOTO 상하정면95도
	GOTO RX_EXIT
KEY258:
	ETX 4800 258
	GOTO 상하정면96도
	GOTO RX_EXIT
KEY259:
	ETX 4800 259
	GOTO 상하정면97도
	GOTO RX_EXIT
KEY260:
	ETX 4800 260
	GOTO 상하정면98도
	GOTO RX_EXIT
KEY261:
	ETX 4800 261
	GOTO 상하정면99도
	GOTO RX_EXIT
KEY262:
	ETX 4800 262
	GOTO 상하정면100도
	GOTO RX_EXIT
KEY263:
	ETX 4800 263
	GOTO 상하정면101도
	GOTO RX_EXIT
KEY264:
	ETX 4800 264
	GOTO 상하정면102도
	GOTO RX_EXIT
KEY265:
	ETX 4800 265
	GOTO 상하정면103도
	GOTO RX_EXIT
KEY266:
	ETX 4800 266
	GOTO 상하정면104도
	GOTO RX_EXIT
KEY267:
	ETX 4800 267
	GOTO 상하정면105도
	GOTO RX_EXIT
KEY268:
	ETX 4800 268
	GOTO 상하정면106도
	GOTO RX_EXIT
KEY269:
	ETX 4800 269
	GOTO 상하정면107도
	GOTO RX_EXIT
KEY270:
	ETX 4800 270
	GOTO 상하정면108도
	GOTO RX_EXIT
KEY271:
	ETX 4800 271
	GOTO 상하정면109도
	GOTO RX_EXIT
KEY272:
	ETX 4800 272
	GOTO 상하정면110도
	GOTO RX_EXIT
    '*************** head_set more 우 ***************
KEY273:
	ETX 4800 273
	GOTO 머리오른쪽90도
	GOTO RX_EXIT
KEY274:
	ETX 4800 274
	GOTO 머리오른쪽89도
	GOTO RX_EXIT
KEY275:
	ETX 4800 275
	GOTO 머리오른쪽88도
	GOTO RX_EXIT
KEY276:
	ETX 4800 276
	GOTO 머리오른쪽87도
	GOTO RX_EXIT
KEY277:
	ETX 4800 277
	GOTO 머리오른쪽86도
	GOTO RX_EXIT
KEY278:
	ETX 4800 278
	GOTO 머리오른쪽85도
	GOTO RX_EXIT
KEY279:
	ETX 4800 279
	GOTO 머리오른쪽84도
	GOTO RX_EXIT
KEY280:
	ETX 4800 280
	GOTO 머리오른쪽83도
	GOTO RX_EXIT
KEY281:
	ETX 4800 281
	GOTO 머리오른쪽82도
	GOTO RX_EXIT
KEY282:
	ETX 4800 282
	GOTO 머리오른쪽81도
	GOTO RX_EXIT
KEY283:
	ETX 4800 283
	GOTO 머리오른쪽80도
	GOTO RX_EXIT
KEY284:
	ETX 4800 284
	GOTO 머리오른쪽79도
	GOTO RX_EXIT
KEY285:
	ETX 4800 285
	GOTO 머리오른쪽78도
	GOTO RX_EXIT
KEY286:
	ETX 4800 286
	GOTO 머리오른쪽77도
	GOTO RX_EXIT
KEY287:
	ETX 4800 287
	GOTO 머리오른쪽76도
	GOTO RX_EXIT
KEY288:
	ETX 4800 288
	GOTO 머리오른쪽75도
	GOTO RX_EXIT
KEY289:
	ETX 4800 289
	GOTO 머리오른쪽74도
	GOTO RX_EXIT
KEY290:
	ETX 4800 290
	GOTO 머리오른쪽73도
	GOTO RX_EXIT
KEY291:
	ETX 4800 291
	GOTO 머리오른쪽72도
	GOTO RX_EXIT
KEY292:
	ETX 4800 292
	GOTO 머리오른쪽71도
	GOTO RX_EXIT
KEY293:
	ETX 4800 293
	GOTO 머리오른쪽70도
	GOTO RX_EXIT
KEY294:
	ETX 4800 294
	GOTO 머리오른쪽69도
	GOTO RX_EXIT
KEY295:
	ETX 4800 295
	GOTO 머리오른쪽68도
	GOTO RX_EXIT
KEY296:
	ETX 4800 296
	GOTO 머리오른쪽67도
	GOTO RX_EXIT
KEY297:
	ETX 4800 297
	GOTO 머리오른쪽66도
	GOTO RX_EXIT
KEY298:
	ETX 4800 298
	GOTO 머리오른쪽65도
	GOTO RX_EXIT
KEY299:
	ETX 4800 299
	GOTO 머리오른쪽64도
	GOTO RX_EXIT
KEY300:
	ETX 4800 300
	GOTO 머리오른쪽63도
	GOTO RX_EXIT
KEY301:
	ETX 4800 301
	GOTO 머리오른쪽62도
	GOTO RX_EXIT
KEY302:
	ETX 4800 302
	GOTO 머리오른쪽61도
	GOTO RX_EXIT
KEY303:
	ETX 4800 303
	GOTO 머리오른쪽60도
	GOTO RX_EXIT
KEY304:
	ETX 4800 304
	GOTO 머리오른쪽59도
	GOTO RX_EXIT
KEY305:
	ETX 4800 305
	GOTO 머리오른쪽58도
	GOTO RX_EXIT
KEY306:
	ETX 4800 306
	GOTO 머리오른쪽57도
	GOTO RX_EXIT
KEY307:
	ETX 4800 307
	GOTO 머리오른쪽56도
	GOTO RX_EXIT
KEY308:
	ETX 4800 308
	GOTO 머리오른쪽55도
	GOTO RX_EXIT
KEY309:
	ETX 4800 309
	GOTO 머리오른쪽54도
	GOTO RX_EXIT
KEY310:
	ETX 4800 310
	GOTO 머리오른쪽53도
	GOTO RX_EXIT
KEY311:
	ETX 4800 311
	GOTO 머리오른쪽52도
	GOTO RX_EXIT
KEY312:
	ETX 4800 312
	GOTO 머리오른쪽51도
	GOTO RX_EXIT
KEY313:
	ETX 4800 313
	GOTO 머리오른쪽50도
	GOTO RX_EXIT
KEY314:
	ETX 4800 314
	GOTO 머리오른쪽49도
	GOTO RX_EXIT
KEY315:
	ETX 4800 315
	GOTO 머리오른쪽48도
	GOTO RX_EXIT
KEY316:
	ETX 4800 316
	GOTO 머리오른쪽47도
	GOTO RX_EXIT
KEY317:
	ETX 4800 317
	GOTO 머리오른쪽46도
	GOTO RX_EXIT
KEY318:
	ETX 4800 318
	GOTO 머리오른쪽45도
	GOTO RX_EXIT
KEY319:
	ETX 4800 319
	GOTO 머리오른쪽44도
	GOTO RX_EXIT
KEY320:
	ETX 4800 320
	GOTO 머리오른쪽43도
	GOTO RX_EXIT
KEY321:
	ETX 4800 321
	GOTO 머리오른쪽42도
	GOTO RX_EXIT
KEY322:
	ETX 4800 322
	GOTO 머리오른쪽41도
	GOTO RX_EXIT
KEY323:
	ETX 4800 323
	GOTO 머리오른쪽40도
	GOTO RX_EXIT
KEY324:
	ETX 4800 324
	GOTO 머리오른쪽39도
	GOTO RX_EXIT
KEY325:
	ETX 4800 325
	GOTO 머리오른쪽38도
	GOTO RX_EXIT
KEY326:
	ETX 4800 326
	GOTO 머리오른쪽37도
	GOTO RX_EXIT
KEY327:
	ETX 4800 327
	GOTO 머리오른쪽36도
	GOTO RX_EXIT
KEY328:
	ETX 4800 328
	GOTO 머리오른쪽35도
	GOTO RX_EXIT
KEY329:
	ETX 4800 329
	GOTO 머리오른쪽34도
	GOTO RX_EXIT
KEY330:
	ETX 4800 330
	GOTO 머리오른쪽33도
	GOTO RX_EXIT
KEY331:
	ETX 4800 331
	GOTO 머리오른쪽32도
	GOTO RX_EXIT
KEY332:
	ETX 4800 332
	GOTO 머리오른쪽31도
	GOTO RX_EXIT
KEY333:
	ETX 4800 333
	GOTO 머리오른쪽30도
	GOTO RX_EXIT
KEY334:
	ETX 4800 334
	GOTO 머리오른쪽29도
	GOTO RX_EXIT
KEY335:
	ETX 4800 335
	GOTO 머리오른쪽28도
	GOTO RX_EXIT
KEY336:
	ETX 4800 336
	GOTO 머리오른쪽27도
	GOTO RX_EXIT
KEY337:
	ETX 4800 337
	GOTO 머리오른쪽26도
	GOTO RX_EXIT
KEY338:
	ETX 4800 338
	GOTO 머리오른쪽25도
	GOTO RX_EXIT
KEY339:
	ETX 4800 339
	GOTO 머리오른쪽24도
	GOTO RX_EXIT
KEY340:
	ETX 4800 340
	GOTO 머리오른쪽23도
	GOTO RX_EXIT
KEY341:
	ETX 4800 341
	GOTO 머리오른쪽22도
	GOTO RX_EXIT
KEY342:
	ETX 4800 342
	GOTO 머리오른쪽21도
	GOTO RX_EXIT
KEY343:
	ETX 4800 343
	GOTO 머리오른쪽20도
	GOTO RX_EXIT
KEY344:
	ETX 4800 344
	GOTO 머리오른쪽19도
	GOTO RX_EXIT
KEY345:
	ETX 4800 345
	GOTO 머리오른쪽18도
	GOTO RX_EXIT
KEY346:
	ETX 4800 346
	GOTO 머리오른쪽17도
	GOTO RX_EXIT
KEY347:
	ETX 4800 347
	GOTO 머리오른쪽16도
	GOTO RX_EXIT
KEY348:
	ETX 4800 348
	GOTO 머리오른쪽15도
	GOTO RX_EXIT
KEY349:
	ETX 4800 349
	GOTO 머리오른쪽14도
	GOTO RX_EXIT
KEY350:
	ETX 4800 350
	GOTO 머리오른쪽13도
	GOTO RX_EXIT
KEY351:
	ETX 4800 351
	GOTO 머리오른쪽12도
	GOTO RX_EXIT
KEY352:
	ETX 4800 352
	GOTO 머리오른쪽11도
	GOTO RX_EXIT
KEY353:
	ETX 4800 353
	GOTO 머리오른쪽10도
	GOTO RX_EXIT
KEY354:
	ETX 4800 354
	GOTO 머리오른쪽9도
	GOTO RX_EXIT
KEY355:
	ETX 4800 355
	GOTO 머리오른쪽8도
	GOTO RX_EXIT
KEY356:
	ETX 4800 356
	GOTO 머리오른쪽7도
	GOTO RX_EXIT
KEY357:
	ETX 4800 357
	GOTO 머리오른쪽6도
	GOTO RX_EXIT
KEY358:
	ETX 4800 358
	GOTO 머리오른쪽5도
	GOTO RX_EXIT
KEY359:
	ETX 4800 359
	GOTO 머리오른쪽4도
	GOTO RX_EXIT
KEY360:
	ETX 4800 360
	GOTO 머리오른쪽3도
	GOTO RX_EXIT
KEY361:
	ETX 4800 361
	GOTO 머리오른쪽2도
	GOTO RX_EXIT
KEY362:
	ETX 4800 362
	GOTO 머리오른쪽1도
	GOTO RX_EXIT
KEY363:
	ETX 4800 363
	GOTO 머리왼쪽 1도
	GOTO RX_EXIT
KEY364:
	ETX 4800 364
	GOTO 머리왼쪽 2도
	GOTO RX_EXIT
KEY365:
	ETX 4800 365
	GOTO 머리왼쪽 3도
	GOTO RX_EXIT
KEY366:
	ETX 4800 366
	GOTO 머리왼쪽 4도
	GOTO RX_EXIT
KEY367:
	ETX 4800 367
	GOTO 머리왼쪽 5도
	GOTO RX_EXIT
KEY368:
	ETX 4800 368
	GOTO 머리왼쪽 6도
	GOTO RX_EXIT
KEY369:
	ETX 4800 369
	GOTO 머리왼쪽 7도
	GOTO RX_EXIT
KEY370:
	ETX 4800 370
	GOTO 머리왼쪽 8도
	GOTO RX_EXIT
KEY371:
	ETX 4800 371
	GOTO 머리왼쪽 9도
	GOTO RX_EXIT
KEY372:
	ETX 4800 372
	GOTO 머리왼쪽 10도
	GOTO RX_EXIT
KEY373:
	ETX 4800 373
	GOTO 머리왼쪽 11도
	GOTO RX_EXIT
KEY374:
	ETX 4800 374
	GOTO 머리왼쪽 12도
	GOTO RX_EXIT
KEY375:
	ETX 4800 375
	GOTO 머리왼쪽 13도
	GOTO RX_EXIT
KEY376:
	ETX 4800 376
	GOTO 머리왼쪽 14도
	GOTO RX_EXIT
KEY377:
	ETX 4800 377
	GOTO 머리왼쪽 15도
	GOTO RX_EXIT
KEY378:
	ETX 4800 378
	GOTO 머리왼쪽 16도
	GOTO RX_EXIT
KEY379:
	ETX 4800 379
	GOTO 머리왼쪽 17도
	GOTO RX_EXIT
KEY380:
	ETX 4800 380
	GOTO 머리왼쪽 18도
	GOTO RX_EXIT
KEY381:
	ETX 4800 381
	GOTO 머리왼쪽 19도
	GOTO RX_EXIT
KEY382:
	ETX 4800 382
	GOTO 머리왼쪽 20도
	GOTO RX_EXIT
KEY383:
	ETX 4800 383
	GOTO 머리왼쪽 21도
	GOTO RX_EXIT
KEY384:
	ETX 4800 384
	GOTO 머리왼쪽 22도
	GOTO RX_EXIT
KEY385:
	ETX 4800 385
	GOTO 머리왼쪽 23도
	GOTO RX_EXIT
KEY386:
	ETX 4800 386
	GOTO 머리왼쪽 24도
	GOTO RX_EXIT
KEY387:
	ETX 4800 387
	GOTO 머리왼쪽 25도
	GOTO RX_EXIT
KEY388:
	ETX 4800 388
	GOTO 머리왼쪽 26도
	GOTO RX_EXIT
KEY389:
	ETX 4800 389
	GOTO 머리왼쪽 27도
	GOTO RX_EXIT
KEY390:
	ETX 4800 390
	GOTO 머리왼쪽 28도
	GOTO RX_EXIT
KEY391:
	ETX 4800 391
	GOTO 머리왼쪽 29도
	GOTO RX_EXIT
KEY392:
	ETX 4800 392
	GOTO 머리왼쪽 30도
	GOTO RX_EXIT
KEY393:
	ETX 4800 393
	GOTO 머리왼쪽 31도
	GOTO RX_EXIT
KEY394:
	ETX 4800 394
	GOTO 머리왼쪽 32도
	GOTO RX_EXIT
KEY395:
	ETX 4800 395
	GOTO 머리왼쪽 33도
	GOTO RX_EXIT
KEY396:
	ETX 4800 396
	GOTO 머리왼쪽 34도
	GOTO RX_EXIT
KEY397:
	ETX 4800 397
	GOTO 머리왼쪽 35도
	GOTO RX_EXIT
KEY398:
	ETX 4800 398
	GOTO 머리왼쪽 36도
	GOTO RX_EXIT
KEY399:
	ETX 4800 399
	GOTO 머리왼쪽 37도
	GOTO RX_EXIT
KEY400:
	ETX 4800 400
	GOTO 머리왼쪽 38도
	GOTO RX_EXIT
KEY401:
	ETX 4800 401
	GOTO 머리왼쪽 39도
	GOTO RX_EXIT
KEY402:
	ETX 4800 402
	GOTO 머리왼쪽 40도
	GOTO RX_EXIT
KEY403:
	ETX 4800 403
	GOTO 머리왼쪽 41도
	GOTO RX_EXIT
KEY404:
	ETX 4800 404
	GOTO 머리왼쪽 42도
	GOTO RX_EXIT
KEY405:
	ETX 4800 405
	GOTO 머리왼쪽 43도
	GOTO RX_EXIT
KEY406:
	ETX 4800 406
	GOTO 머리왼쪽 44도
	GOTO RX_EXIT
KEY407:
	ETX 4800 407
	GOTO 머리왼쪽 45도
	GOTO RX_EXIT
KEY408:
	ETX 4800 408
	GOTO 머리왼쪽 46도
	GOTO RX_EXIT
KEY409:
	ETX 4800 409
	GOTO 머리왼쪽 47도
	GOTO RX_EXIT
KEY410:
	ETX 4800 410
	GOTO 머리왼쪽 48도
	GOTO RX_EXIT
KEY411:
	ETX 4800 411
	GOTO 머리왼쪽 49도
	GOTO RX_EXIT
KEY412:
	ETX 4800 412
	GOTO 머리왼쪽 50도
	GOTO RX_EXIT
KEY413:
	ETX 4800 413
	GOTO 머리왼쪽 51도
	GOTO RX_EXIT
KEY414:
	ETX 4800 414
	GOTO 머리왼쪽 52도
	GOTO RX_EXIT
KEY415:
	ETX 4800 415
	GOTO 머리왼쪽 53도
	GOTO RX_EXIT
KEY416:
	ETX 4800 416
	GOTO 머리왼쪽 54도
	GOTO RX_EXIT
KEY417:
	ETX 4800 417
	GOTO 머리왼쪽 55도
	GOTO RX_EXIT
KEY418:
	ETX 4800 418
	GOTO 머리왼쪽 56도
	GOTO RX_EXIT
KEY419:
	ETX 4800 419
	GOTO 머리왼쪽 57도
	GOTO RX_EXIT
KEY420:
	ETX 4800 420
	GOTO 머리왼쪽 58도
	GOTO RX_EXIT
KEY421:
	ETX 4800 421
	GOTO 머리왼쪽 59도
	GOTO RX_EXIT
KEY422:
	ETX 4800 422
	GOTO 머리왼쪽 60도
	GOTO RX_EXIT
KEY423:
	ETX 4800 423
	GOTO 머리왼쪽 61도
	GOTO RX_EXIT
KEY424:
	ETX 4800 424
	GOTO 머리왼쪽 62도
	GOTO RX_EXIT
KEY425:
	ETX 4800 425
	GOTO 머리왼쪽 63도
	GOTO RX_EXIT
KEY426:
	ETX 4800 426
	GOTO 머리왼쪽 64도
	GOTO RX_EXIT
KEY427:
	ETX 4800 427
	GOTO 머리왼쪽 65도
	GOTO RX_EXIT
KEY428:
	ETX 4800 428
	GOTO 머리왼쪽 66도
	GOTO RX_EXIT
KEY429:
	ETX 4800 429
	GOTO 머리왼쪽 67도
	GOTO RX_EXIT
KEY430:
	ETX 4800 430
	GOTO 머리왼쪽 68도
	GOTO RX_EXIT
KEY431:
	ETX 4800 431
	GOTO 머리왼쪽 69도
	GOTO RX_EXIT
KEY432:
	ETX 4800 432
	GOTO 머리왼쪽 70도
	GOTO RX_EXIT
KEY433:
	ETX 4800 433
	GOTO 머리왼쪽 71도
	GOTO RX_EXIT
KEY434:
	ETX 4800 434
	GOTO 머리왼쪽 72도
	GOTO RX_EXIT
KEY435:
	ETX 4800 435
	GOTO 머리왼쪽 73도
	GOTO RX_EXIT
KEY436:
	ETX 4800 436
	GOTO 머리왼쪽 74도
	GOTO RX_EXIT
KEY437:
	ETX 4800 437
	GOTO 머리왼쪽 75도
	GOTO RX_EXIT
KEY438:
	ETX 4800 438
	GOTO 머리왼쪽 76도
	GOTO RX_EXIT
KEY439:
	ETX 4800 439
	GOTO 머리왼쪽 77도
	GOTO RX_EXIT
KEY440:
	ETX 4800 440
	GOTO 머리왼쪽 78도
	GOTO RX_EXIT
KEY441:
	ETX 4800 441
	GOTO 머리왼쪽 79도
	GOTO RX_EXIT
KEY442:
	ETX 4800 442
	GOTO 머리왼쪽 80도
	GOTO RX_EXIT
KEY443:
	ETX 4800 443
	GOTO 머리왼쪽 81도
	GOTO RX_EXIT
KEY444:
	ETX 4800 444
	GOTO 머리왼쪽 82도
	GOTO RX_EXIT
KEY445:
	ETX 4800 445
	GOTO 머리왼쪽 83도
	GOTO RX_EXIT
KEY446:
	ETX 4800 446
	GOTO 머리왼쪽 84도
	GOTO RX_EXIT
KEY447:
	ETX 4800 447
	GOTO 머리왼쪽 85도
	GOTO RX_EXIT
KEY448:
	ETX 4800 448
	GOTO 머리왼쪽 86도
	GOTO RX_EXIT
KEY449:
	ETX 4800 449
	GOTO 머리왼쪽 87도
	GOTO RX_EXIT
KEY450:
	ETX 4800 450
	GOTO 머리왼쪽 88도
	GOTO RX_EXIT
KEY451:
	ETX 4800 451
	GOTO 머리왼쪽 89도
	GOTO RX_EXIT
KEY452:
	ETX 4800 452
	GOTO 머리왼쪽 90도
	GOTO RX_EXIT
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#現在のソースは検出した色（赤）の場所をシリアルで送信します
#コメント文になっている部分は色検出でLEDを光らす名残りである
#
#GPIOからシリアルの値を出力している
#
#最終編集日 2016/1/18


import cv
import RPi.GPIO as GPIO
import serial


ser = serial.Serial('/dev/ttyAMA0', 9600)



GPIO.setmode(GPIO.BOARD)

color_tracker_window="Color Tracker"

LED = 40

GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

#クラスを作成
#色を追跡するクラス
class ColorTracker:

	#インスタンス
	def __init__(self):
		#表示される画面の定義
		cv.NamedWindow( color_tracker_window,1)
		#カメラからのデータを持っておく
		self.capture = cv.CaptureFromCAM(0)
		
	def run(self):
		while True:
			#カメラからイメージを入手
			img = cv.QueryFrame(self.capture)
			
			#カラーのノイズを減らす範囲
			cv.Smooth(img,img,cv.CV_BLUR,3);
			
			
			hsv_img = cv.CreateImage(cv.GetSize(img),8,3)
			cv.CvtColor(img, hsv_img,cv.CV_BGR2HSV)
			
			thresholded_img = cv.CreateImage(cv.GetSize(hsv_img),8,1)
			cv.InRangeS(hsv_img,(0,150,150),(25,255,255),thresholded_img)
			#ここで赤色を識別しています

			moments = cv.Moments(cv.GetMat(thresholded_img,1),0)
			area = cv.GetCentralMoment(moments,0,0)
			
			if(area > 100000):
					
				
				x = cv.GetSpatialMoment(moments,1,0)/area
				y = cv.GetSpatialMoment(moments,0,1)/area

				int(x)
				print int(x)
				#シリアルスタートビット
				ser.write(b':')
				#本体データ
				ser.write (bytes(x))
				#エンドデータ
				ser.write(b'#')
				
				if y > 200 :
					GPIO.output(LED, GPIO.HIGH)
				else:
					GPIO.output(LED, GPIO.LOW)		

				overlay = cv.CreateImage(cv.GetSize(img),8,3)
				
				cv.Circle(img,(int(x),int(y)),2,(255,255,255),20)
				cv.Add(img,overlay,img)
				
				cv.Merge(thresholded_img,None,None,None,img)
				
		#		GPIO.output(LED, GPIO.HIGH)

		#	else:
		#		GPIO.output(LED, GPIO.LOW)

			cv.ShowImage(color_tracker_window,img)
			
		
			#これがくるまでループ
			if cv.WaitKey(10) == 27:
				ser.close()
				break
				
if __name__=="__main__":
	color_tracker = ColorTracker()
	color_tracker.run()
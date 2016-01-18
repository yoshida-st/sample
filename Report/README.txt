機能
サーボモーターで赤色の方向を見ます

使い方
raspberry piとarduinoを連携させて使用します
raspberry piのOpenCVを使用し色認識（赤色）を読み出します
赤色のあるX座標を取り出しシリアルで送信します

PI側のGPIOシリアルピン(TX)を有効にしarduinoのシリアルピン（RX）に接続します
この際電圧の違いがありますのでraspbery piの送信側（TX)のみ使用します

arduinoではシリアルデータを1パケット分受信しサーボモーターを制御します
サーボモーターの制御ピンは９番ピンを使用しています

参考にしたサイト
http://www.davidhampgonsalves.com/opencv-python-color-tracking
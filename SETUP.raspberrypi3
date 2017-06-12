# Raspberry Pi3 でBluetooth＋Serial通信を始めるための初期設定

## OSのダウンロード
Raspberry Pi公式サイト
https://www.raspberrypi.org/

  RASPBIAN JESSIE WITH PIXEL
  Image with PIXEL desktop based on Debian Jessie
  Version:April 2017
  Release date:2017-04-10
  Kernel version:4.4
  
このバージョン（正確には2017年2月以降）の良いところは、raspi-config（コンソール版）でSerial Terminal設定をOFFの状態でSerialポート(UART)を有効にできるようになっているところ。
（GUI版はTerminal設定が強制される）

## モジュールを最新にアップデート
  aptitude update
  aptitude upgrade
  ===> shutdown -r now でリブート
## Serial(UART)を有効化
  raspi-config でserialを有効化（Terminalを有効にするかの質問にはNOと答える）
  ===> shutdown -r now でリブート

## Bluez関連はLEを使用しなければ、特にインストール不要な様子（あとで追記）

## （参考サイト）
セットアップはこちらのサイトさんのを参考にすると良かった。
http://www.neko.ne.jp/~freewing/raspberry_pi/



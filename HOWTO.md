
## Raspberry PiでBluetooth RFCOMMを起動時に実行する。

    パスを確認
    pi@raspberrypi:~$ which sudo
    /usr/bin/sudo
    pi@raspberrypi:~$ which rfcomm
    /usr/bin/rfcomm
    pi@raspberrypi:~$ which hciconfig
    /bin/hciconfig
    pi@raspberrypi:~$ which sdptool
    /usr/bin/sdptool
    pi@raspberrypi:~$ 

## rc.localを編集
sudo vi /etc/rc.local

    # Turn on bluetooth RFCOMM profile
    sleep 10
    /usr/bin/sudo /bin/hciconfig hci0 piscan
    /usr/bin/sudo /usr/bin/sdptool add sp
    #/usr/bin/sudo /bin/hciconfig hci0 sspmode 0       #必要に応じて

sleepが案外大事。

## 再起動して　sudo sdptool browse local　コマンドで、RFCOMMが登録されていることを確認。

    Service Name: Serial Port
    Service Description: COM Port
    Service Provider: BlueZ
    Service RecHandle: 0x10005
    Service Class ID List:
      "Serial Port" (0x1101)
    Protocol Descriptor List:
      "L2CAP" (0x0100)
      "RFCOMM" (0x0003)
        Channel: 1
    Language Base Attr List:
      code_ISO639: 0x656e
      encoding:    0x6a
      base_offset: 0x100
    Profile Descriptor List:
      "Serial Port" (0x1101)
        Version: 0x0100

## hciconfigでISCANが表示される事を確認。
    pi@raspberrypi:~$ sudo hciconfig show
    hci0:   Type: BR/EDR  Bus: UART
            BD Address: B8:27:EB:98:66:00  ACL MTU: 1021:8  SCO MTU: 64:1
            UP RUNNING PSCAN ISCAN 
            RX bytes:1286 acl:4 sco:0 events:69 errors:0
            TX bytes:2677 acl:4 sco:0 commands:57 errors:0

## 以下のコマンドで接続テスト。
    sudo rfcomm listen F8:A9:D0:A4:09:22 &
AndroidからBlueterm等で接続すると、/dev/rfcomm0 が作成される。

BlueTerm　（PlayStoreにある類似品がたくさんあるので注意）
https://github.com/johnhowe/BlueTerm

## 参考にするのはこのあたり。
https://raspberrypi.stackexchange.com/questions/47200/automatically-accepting-bluetooth-connections-on-a-pi-3

## UART経由でPLC MELSEQ-Qにデータを送れるが、受信できない場合
以下のチップだけだとフロー制御が動かないために、ピンのブリッジが必要。4（DTR)-6（DSR)　7（RTS)-8（CTS)をブリッジするとよい。
http://akizukidenshi.com/catalog/g/gK-06464/

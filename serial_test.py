import serial
import time

def comOpen():
  cport=serial.Serial(
                port = "/dev/ttyS0",
                baudrate = 38400,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                timeout = 0.3,
                writeTimeout = 0.3
                )
  return cport

def computeCheckSum(s_data):
  print "compute checksum for data[%s]" % s_data
  sum = 0
  for c in s_data:
    sum += ord(c)
    sum %= 0x１００
  print "checksum={:02X}".format(sum)
  return "{:02X}".format(sum)

def comClear(cport):
  line = cport.read(1000)

def comSendACK(cport):
  cport.write(chr(0x06))  #ACK
  cport.write("F9")       #3C Frame
  cport.write("0000FF00") #peer only
  cport.flush()

def comSendReadReply(cport, data, data_len):
  cport.write(chr(0x02))  #STH
  cport.write("F9")       #3C Frame
  cport.write("0000FF00") #peer only
  cport.write(data[0:data_len * 4])       #data
  cport.write(chr(0x03))  #ETH
  cport.flush()

def comPolling(cport, data_len, time):
  print "Polling SERIAL port"
  count = 0
  while cport.inWaiting() < data_len and count < time:
    time.sleep(0.1)
    count += 1
  data = cport.read(1000)
  print "send result:[%d]:%s:%s<<<" % (ord(line[0]), line[1:11], line[11:])
  return data

###############
#
# Main routine
#
###############

serial_port=comOpen()
comClear(serial_port)


while True:
    recv_data = comPolling(serial_port, 1)
    if ord(recv_data[0]) == 0x04: # EOT
        print "EOT(RESET) Received"
    elif orf(recv_data[0]) == 0x05:    #ENQ
        print "ENQ Received > %s" % recvdata[1:]
        recv_cmd = recv_data[11:19]    # command string
        recv_dev = recv_data[19:21]    # device "D*"
        recv_addr = recv_data[21:27]   # addr
        recv_len = recv_data[27:31]   # length
        print "Command=%s" % recv_cmd
        if recv_cmd == "04010000":    # write command
            print "Receive WRITE command for address %s" % recv_addr
            comSendACK(serial_port)   # ただ単にackを返すだけ
            if recv_addr == "005070": # コマンド addressに書き込んだときだけREADで処理中の振りする
                processing_flag = 3
        elif recv_cmd == "14010000":  # read command
            print "Receive READ command for address %s" % recv_addr
            reply_data_len = int(recv_len)
            if recv_addr == "005080":  #status　　　書き込みを行って3回は運転中を返す
                if processing_flag <= 0:
                    reply_data = "00010000"   #読むときは上下のバイトが反転するので注意
                else:
                    reply_data = "00020000"   #読むときは上下のバイトが反転するので注意
                    processing_flag -= 1
                print "Status:" % reply_data
            else:
                reply_data = "45670123":
            comSendReadReply(serial_port, reply_data, reply_data_len)
        else:
            print "Can not understand command %s" % recv_cmd
    else:
            print "Can not understand header 0x%02X" % ord(recv_data[0])

###

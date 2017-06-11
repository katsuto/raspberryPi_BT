import serial
import bluetooth
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
    sum %= 0xFF
  print "checksum={:02X}".format(sum)
  return "{:02X}".format(sum)

def comClear(cport):
  line = cport.read(1000)

def comPLCReset(cport):
  cport.write(chr(0x04))  #EOT
  cport.write(chr(0x0C))  #CL
  cport.flush()
  time.sleep(0.3)
  line = cport.read(1000)
        
def comPLCWrite(cport, addr, s_len, data):
  line = cport.read(1000) #flush the read port
  print "SEND write command to SERIAL"
  cport.write(chr(0x05))    #ENQ
  cport.write("F9")         #3C Frame
  cport.write("0000FF00")   #peer only
  cport.write("04010000")   #WRITE CMD
  cport.write("D*")         #Device
  addrstr = "000000" + addr
  cport.write(addrstr[-6:]) #"000000" 6chars
  lenstr = "0000" + s_len
  cport.write(lenstr[-4:])  #"0000" 4chars
  cport.write(data)         #"XXXX" x len chars
  cport.write(computeCheckSum("F90000FF0004010000D*" + addrstr[-6:] + lenstr[-4:] + data))
  cport.flush()
  count = 0
  while cport.inWaiting() < 10 and count < 10:
    time.sleep(0.5)
    count += 1
  line = cport.read(1000)
  if len(line) == 0:
    line = chr(0)
  print "send result:[%d]:%s<<<" % (ord(line[0]), line[1:])
  if ord(line[0]) == 0x06:     #ACK
    print "send successful"
    return True
  else:
    print "send error"
    return False

def comPLCRead(cport, addr, s_len):
  line = cport.read(1000) #flush the read port
  print "SEND READ COMMAND TO SERIAL"
  cport.write(chr(0x05))  #ENQ
  cport.write("F9")       #3C Frame
  cport.write("0000FF00") #peer only
  cport.write("14010000") #READ CMD
  cport.write("D*")
  addrstr = "000000" + addr
  cport.write(addrstr[-6:]) #"000000" 6chars
  lenstr = "0000" + s_len
  cport.write(lenstr[-4:])  #"0000" 4chars
  cport.write(computeCheckSum("F90000FF0014010000D*" + addrstr[-6:] + lenstr[-4:]))
  cport.flush()
  print "SEND READ COMMAND FINISHED"
  count = 0
  datalen = 11 + int(s_len) * 4    # word(2bytes=4chars)
  while cport.inWaiting() < datalen and count < 10:
    time.sleep(0.5)
    count += 1
  line = cport.read(1000)
  if len(line) == 0:
    line = "DUMMYSTRINGNONE"
  print "send result:[%d]:%s:%s<<<" % (ord(line[0]), line[1:11], line[11:])
  data = line[11:datalen]
  return data

###############
#
# Main routine
#
###############

serial_port=comOpen()
comClear(serial_port)
comPLCReset(serial_port)

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
bt_port = 1

server_sock.bind(("", bt_port))
server_sock.listen(1)
print "Listening on port %d" % bt_port

uuid = "00001101-0000-1000-8000-00805f9b34fb"
bluetooth.advertise_service(server_sock, "COM Bridge Service", uuid)
print "Advertise start"

while True:
  client_sock,address = server_sock.accept()
  print "Accepted connection from ", address
  try:
    while True:
      data = ""
      line_end = False
      while not line_end:
        recv_data = client_sock.recv(1024)
        for c in recv_data:
          if ord(c) != 0x0D:    #CR
            print "BT RECV (%d) [%s]" % (ord(c), c)
            data += c.upper()
          else:
            print "BT RECV (%d) [CR]" % ord(c)
            line_end = True          
            
      print "BT received [%s]" % data
      try:
        if data[0] == 'S':
          s_addr = data[1:7]
          s_len = data[7:11]
          s_data = data[11:]
          print "SEND COMMAND:ADDR[%s] LEN[%s] DATA[%s]" % (s_addr, s_len, s_data)
          if int(s_len) * 4 == len(s_data):
            ret = comPLCWrite(serial_port, s_addr, s_len, s_data)
          else:
            ret = False
          
          if ret == False:
            ret = "NACK"
          else:
            ret = "ACK "
        elif data[0] == 'R':
          s_addr = data[1:7]
          s_len = data[7:12]
          print "RECV COMMAND:ADDR[%s] LEN[%s]" % (s_addr, s_len)
          ret = comPLCRead(serial_port, s_addr, s_len)
        else:
          ret = "CERR"
        print "SERIAL result [%s]" % ret
        client_sock.send(ret)
#      except IOError:
      except:
        print "Serial Port Error, Reset the port."
        serial_port.close()
        time.sleep(0.5)
        serial_port = comOpen()
        client_sock.close()
  except IOError:
    client_sock.close()

  print "BT connection closed"

server_sock.close()


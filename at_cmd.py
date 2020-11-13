# coding: utf-8
import serial
import time
import threading


class AT_Command(object):
    """
    This class Define a AT comand set of Beidou RDSS module.
    Call the serial to communicate with module.
    """

    def __init__(self):
        """
        init the serial.
        """
        SERIAL_DEV = "/dev/ttyUSB0"
        SERIAL_TIMEOUT_SEC = 0.5
        SERIAL_BAUDRATE = 9600

        self.CMD = {
            "at_mode":      b"AT+ENAT",
            "get_id":       b"AT+SRCAD?",
            "get_csq":      b"AT+CSQ?",
            "get_dst_addr": b"AT+DSTAD?",
            "set_dst_addr": b"AT+DSTAD=",
            "get_loc":      b"AT+LOCINF?",
        }

        self.tx_count = 0
        self.rx_count = 0
        self.err = None
        try:
            self.serial = serial.Serial(SERIAL_DEV, SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT_SEC)
            self.receiveProcess = threading.Thread(target=self.thread_read)
            self.receiveProcess.setDaemon(True)
            self.receiveProcess.start()
        except Exception as e:
            self.serial = None
            self.err = e
            print(e)

    def is_serial_ok(self):
        # check the serial is open normal
        return self.serial is not None

    def send_cmd(self, cmd):
        if (self.serial is not None):
            if self.serial.isOpen():
                try:
                    result = self.serial.write(cmd)
                    self.tx_count += result
                    print("[TX] ", cmd.decode('utf-8'))
                    #  data = ' '
                    #  datas = []
                    #  data = self.serial.readline()
                    #  print(data)
                    #  datas.append(data.decode("utf-8"))
                    #  data = self.serial.readline()
                    #  print(data)
                    #  datas.append(data.decode("utf-8"))
                    #  while True:
                    #      data = self.serial.readline()
                    #      print(data)
                    #      self.rx_count += len(data)
                    #      if len(data) == 0:
                    #          break
                    #      datas.append(data.decode("utf-8"))
                    #  print(datas)
                    time.sleep(0.8)
                    #  return datas
                except Exception as e:
                    print(e)
                    self.err = e
                    return ['Error:', ]

    def thread_read(self):
        self.recv_stop = False
        msg_line = ''
        while not self.recv_stop:
            try:
                readlenth = max(1, min(2048, self.serial.in_waiting))
                bytes = self.serial.read(readlenth)
                if bytes is not None:
                    self.rx_count += len(bytes)
                    if(len(bytes) != 0):
                        if bytes.find(b'\n') == -1:
                            msg_line += bytes.decode('utf-8')
                        else:
                            print('[RX] ', msg_line, end='')
                            msg_line = ''
            except Exception as e:
                print(e)
                break


#  class ThreadSerial(object):
#      """
#      Serial with thread.
#      """
#      def __init__(self, comport, baudrate, timeout):
#          self.serial = serial.Serial(comport, baudrate, timeout=timeout)
#
#      def send(self, b_string):
#          result = self.serial.write(b_string)
#          return result
#


if __name__ == "__main__":
    """
    test class
    """
    ser = AT_Command()
    ser.set_at_mode()

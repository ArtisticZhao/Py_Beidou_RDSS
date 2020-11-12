# coding: utf-8
import serial

CMD = {
    "at_mode":      b"AT+ENAT",
    "get_id":       b"AT+SRCAD",
    "get_csq":      b"AT+CSQ?",
    "get_dst_addr": b"AT+DSTAD?",
    "set_dst_addr": b"AT+DSTAD=",
    "get_loc":      b"AT+LOCINF?",
}


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
        SERIAL_TIMEOUT_SEC = 0.1
        SERIAL_BAUDRATE = 9600
        try:
            self.serial = serial.Serial(SERIAL_DEV, SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT_SEC)
            self.tx_count = 0
            self.rx_count = 0
        except Exception as e:
            self.serial = None
            print(e)

    def send_cmd(self, cmd):
        if (self.serial is not None):
            print(self.serial)
            if self.serial.isOpen():
                try:
                    result = self.serial.write(cmd)
                    self.tx_count += result
                    data = ' '
                    datas = []
                    while True:
                        data = self.serial.readline()
                        self.rx_count += len(data)
                        if len(data) == 0:
                            break
                        datas.append(data)
                    return datas

                except Exception as e:
                    print(e)
                    return ['Error:', e]


if __name__ == "__main__":
    """
    test class
    """
    ser = AT_Command()
    ser.set_at_mode()

# A Host software of RDSS Beidou module.
This is a software of RDSS Beidou module. Developped by PyQt5.

## Dependencies
PyQt5  
pyserial

## Install
- clone this repo
```
git clone https://github.com/ArtisticZhao/Py_Beidou_RDSS.git
```

- install dependencies
```
pip3 install PyQt5 --user
pip3 install pyserial --user
```

## Usage
- Open serial without sudo
```shell
sudo usermod -a -G dialout $USER
```

- Run program
```
python3 main.py
```

## Inspired
[Neutree/COMTool](https://github.com/Neutree/COMTool) about the thread read of serial

## LICENSE
MIT

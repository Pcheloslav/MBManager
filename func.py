# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from operator import __getitem__

from pymodbus import bit_write_message
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.compat import iteritems
from pymodbus.constants import Endian
from pymodbus.exceptions import *
import time
from PyQt5.QtWidgets import QMessageBox



global state
state = 0


def establish_connection():
    state = 1
    USB_PORT = 'COM6'
    PARITY = 'N'  # 'N'
    BAUD_RATE = 9600
    TIMEOUT = 1
    global client
    client = ModbusClient(method='rtu',
                          port=USB_PORT,
                          stopbits=1,
                          bytesize=8,
                          parity=PARITY,
                          baudrate=BAUD_RATE,
                          timeout=TIMEOUT, )

    for i in range(1, 2):
        connection = client.connect()
        print(f"COM Details {client.socket}")
        print(f"Connection status is: {connection} \nClient State: {client.state} \nTimeout: {client.timeout}")
        try:
            holding_values = client.read_holding_registers(0x0000, 10, unit=0x01)  #  ДИМА ! вот это говно считывает нужную нам инфу и ее нужно фигачить в бд
            print(holding_values.registers)  # а еще нужно обновлять значения каждые 5 мин

            # client.write_register(0x081A, 0x00, unit=0x01)  # хуйня
            value = client.read_holding_registers(0x081a, 1)
            """if value.registers[0] != 2:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Не в удаленном режиме")
                msg.setWindowTitle("Error")
                msg.exec_()
                return"""

        except ConnectionException as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("НЕ подключено к усб")
            msg.setWindowTitle("Error")
            msg.exec_()
            print(f"USB Disconnected {e}")
    return state


# Включить лампочку
def on():
    value = client.read_holding_registers(0x081a, 1)
    if value.registers[0] != 2:
        return "not2"
    client.write_coil(address=0x00, value=0xff00, unit=0x01)


# Выключить лампочку
def off():
    value = client.read_holding_registers(0x081a, 1)
    if value.registers[0] != 2:  # __getitem__(1)
        return "not2"
    client.write_coil(address=0x00, value=0x0000, unit=0x01)


# Переключить в режим remote
def switchtoremote():
    if state == 1:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Не подключено. Нажмите подключиться")
        msg.setWindowTitle("Error")
        msg.exec_()
    value = client.read_holding_registers(0x081a, 1)
    if value.registers[0] != 2:  # __getitem__(1)
        client.write_register(0x081A, 0x02, unit=0x01)
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Уже в удаленном режиме")
        msg.setWindowTitle("Error")
        msg.exec_()


def switchtooff():
    if state == 0:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Не подключено. Нажмите подключиться")
        msg.setWindowTitle("Error")
        msg.exec_()
        return
    value = client.read_holding_registers(0x081a, 1)
    if value.registers[0] != 0:  # __getitem__(1)
        client.write_register(0x081A, 0x00, unit=0x01)
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Уже выключено")
        msg.setWindowTitle("Error")
        msg.exec_()


def switchtoalarm():
    if state == 0:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Не подключено. Нажмите подключиться")
        msg.setWindowTitle("Error")
        msg.exec_()
        return
    value = client.read_holding_registers(0x081a, 1)
    if value.registers[0] != 1:  # __getitem__(1)
        client.write_register(0x081A, 0x01, unit=0x01)
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Уже в сигнале")
        msg.setWindowTitle("Error")
        msg.exec_()


if __name__ == '__func__':

    USB_PORT = 'COM6'
    PARITY = 'N'  # 'N'
    BAUD_RATE = 9600
    TIMEOUT = 1

    client = ModbusClient(method='rtu',
                          port=USB_PORT,
                          stopbits=1,
                          bytesize=8,
                          parity=PARITY,
                          baudrate=BAUD_RATE,
                          timeout=TIMEOUT, )

    for i in range(1, 2):
        connection = client.connect()
        print(f"COM Details {client.socket}")
        print(f"Connection status is: {connection} \nClient State: {client.state} \nTimeout: {client.timeout}")
        try:

            holding_values = client.read_holding_registers(0x0000, 10, unit=0x01)
            print(holding_values.registers)

            while True:
                state = str(input("State"))
                # Включить лампочку ввести ff00
                if state == "ff00":
                    """client.write_register(0x081A, 0x01, unit=0x01)
                    holding_values = client.read_holding_registers(0x081a, 10)
                    print(holding_values.registers)"""
                    client.write_coil(address=0x00, value=0xff00, unit=0x01)
                # Выключить лампочку ввести 0000
                elif state == "0000":
                    """client.write_register(0x081A, 0x00, unit=0x01)
                    holding_values = client.read_holding_registers(0x081a, 1)
                    print(holding_values.registers)"""
                    client.write_coil(address=0x00, value=0x0000, unit=0x01)
                # Перевести в режим remote ввести 2
                elif state == "2":
                    client.write_register(0x081A, 0x02, unit=0x01)
                    holding_values = client.read_holding_registers(0x081a, 10)
                    print(holding_values.registers)
                # Выход
                elif state == "exit":
                    exit(0)

        except ConnectionException as e:
            print(f"USB Disconnected {e}")

        time.sleep(1)
        client.close()

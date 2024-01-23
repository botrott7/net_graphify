import ipaddress
import threading
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout

from scapy.layers.inet import IP, ICMP, Ether
from scapy.sendrecv import srp


class DeviceAvailability(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Проверка доступности сетевых устройств')
        self.setStyleSheet(open('styles/style_port_scanner.css').read())
        self.setGeometry(300, 300, 480, 400)
        layout = QVBoxLayout()

        self.label_start = QLabel('Введите начальный IP-адрес:', self)
        layout.addWidget(self.label_start)
        self.input_start = QLineEdit(self)
        layout.addWidget(self.input_start)
        self.label_end = QLabel('Введите префикс подсети:', self)
        layout.addWidget(self.label_end)
        self.input_end = QLineEdit(self)
        layout.addWidget(self.input_end)
        self.result_label = QLabel('Результаты сканирования:', self)
        layout.addWidget(self.result_label)
        self.result_text = QTextEdit(self)
        layout.addWidget(self.result_text)
        self.result_text.setReadOnly(True)

        self.btn_check_availability = QPushButton('Проверить доступность устройств', self)
        layout.addWidget(self.btn_check_availability)
        self.setLayout(layout)

        # Подключаем событие нажатия кнопки
        self.btn_check_availability.clicked.connect(self.check_device_availability)

    def check_device_availability(self):
        start_ip = self.input_start.text()
        prefix = self.input_end.text()

        network = f"{start_ip}/{prefix}"

        network_ip = ipaddress.IPv4Network(network)
        available_devices = []
        threads = []
        for ip in network_ip:
            thread = threading.Thread(target=self.check_device_availability_helper, args=(str(ip), available_devices))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Очищаем поле вывода результатов
        self.result_text.clear()

        for device in available_devices:
            ip_address, mac_address = device
            self.result_text.append(f"Устройство {ip_address} доступно. MAC-адрес: {mac_address}")

    def check_device_availability_helper(self, ip_address, available_devices):
        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / IP(dst=ip_address) / ICMP()
        try:
            response, _ = srp(packet, timeout=2, verbose=False)
            if response:
                mac_address = response[0][1].src
                available_devices.append((ip_address, mac_address))
        except Exception as e:
            pass

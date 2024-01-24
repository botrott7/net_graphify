import nmap
import traceback
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QProgressBar, QHBoxLayout, QSizePolicy)
from threading import Thread
from tqdm import tqdm


class PortScanner(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Порт-сканер")
        # self.setStyleSheet(open('styles/style_port_scanner.css').read())
        self.layout = QHBoxLayout()

        self.target_label = QLabel("IP:")
        self.target_input = QLineEdit()
        self.target_input.setFixedWidth(100)
        self.layout.addWidget(self.target_label)
        self.layout.addWidget(self.target_input)

        self.start_label = QLabel("Начальный Порт:")
        self.start_input = QLineEdit()
        self.layout.addWidget(self.start_label)
        self.layout.addWidget(self.start_input)

        self.end_label = QLabel("Конечный Порт:")
        self.end_input = QLineEdit()
        self.layout.addWidget(self.end_label)
        self.layout.addWidget(self.end_input)

        self.scan_button = QPushButton("Сканирование")
        self.scan_button.clicked.connect(self.start_scan_thread)
        self.layout.addWidget(self.scan_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding,
                                        QSizePolicy.Preferred)
        self.progress_bar.setFixedHeight(25)
        self.progress_bar.setFixedWidth(200)
        self.layout.addWidget(self.progress_bar)

        self.result_label = QLabel()
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)
        self.setGeometry(750, 400, 400, 250)

    def closeEvent(self, event):
        self.main_app.show()

    def start_scan_thread(self):
        if getattr(self, 'scan_thread', None) and self.scan_thread.is_alive():
            return
        self.scan_button.setVisible(False)
        self.scan_thread = Thread(target=self.scan_ports)
        self.scan_thread.start()

    def scan_ports(self):
        try:
            ip_address = self.target_input.text()
            start_port = int(self.start_input.text())
            end_port = int(self.end_input.text())
            nmap_path = [r'C:\Program Files (x86)\Nmap\nmap.exe', ]
            nm = nmap.PortScanner(nmap_search_path=nmap_path)
            total_ports = end_port - start_port + 1
            open_ports = []
            with tqdm(range(total_ports), unit='port') as pbar:
                self.progress_bar.setMaximum(total_ports)
                for port in pbar:
                    result = nm.scan(ip_address, str(start_port + port))
                    tcp_scan_data = result.get('scan', {}).get(ip_address, {}).get('tcp')
                    if tcp_scan_data:
                        state = tcp_scan_data.get(start_port + port, {}).get('state')
                        if state == 'open':
                            open_ports.append(start_port + port)

                    self.progress_bar.setValue(port + 1)
            self.update_result_label(open_ports)
            self.scan_button.setVisible(True)
        except Exception as err:
            print("Ошибка сканирования: ", err)
            traceback.print_exc()

    def update_result_label(self, open_ports):
        if open_ports:
            result = "Открытые порты: " + ', '.join(str(port) for port in open_ports)
        else:
            result = "Нет открытых портов."

        self.result_label.setText(result)

    def clear_input_fields(self):
        self.start_input.clear()
        self.end_input.clear()

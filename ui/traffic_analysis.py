from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal
from scapy.all import sniff


class TrafficThread(QThread):
    packet_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.is_running = False

    def run(self):
        self.is_running = True

        def packet_handler(packet):
            if self.is_running:
                self.packet_received.emit(packet.summary())

        sniff(iface='Ethernet', prn=packet_handler)

    def stop(self):
        self.is_running = False


class TrafficAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(open('styles/style_port_scanner.css').read())
        self.setWindowTitle("Анализ трафика")
        self.layout = QVBoxLayout()

        self.result_label = QLabel("Результат:")
        self.layout.addWidget(self.result_label)

        self.result_browser = QTextBrowser()
        self.layout.addWidget(self.result_browser)

        self.start_button = QPushButton("Старт")
        self.start_button.clicked.connect(self.start_traffic_analysis)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Стоп")
        self.stop_button.clicked.connect(self.stop_traffic_analysis)
        self.layout.addWidget(self.stop_button)

        self.setLayout(self.layout)

    def start_traffic_analysis(self):
        self.result_browser.clear()
        self.traffic_thread = TrafficThread()
        self.traffic_thread.packet_received.connect(self.update_results)
        self.traffic_thread.start()

    def stop_traffic_analysis(self):
        self.traffic_thread.stop()

    def update_results(self, packet_summary):
        self.result_browser.append(packet_summary)

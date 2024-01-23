import sys
from PyQt5.QtGui import QFontDatabase

from ui.topology import show_topology
from ui.traffic_analysis import TrafficAnalyzer
from ui.interface_data import show_interface_data
from ui.device_availability import DeviceAvailability
from ui.port_scanner import PortScanner
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Net_Graphify')

        self.setStyleSheet(open('styles/style.css').read())

        btn_topology = QPushButton('Отображение топологии сети', self)
        btn_topology.setGeometry(50, 50, 400, 50)
        btn_topology.clicked.connect(show_topology)
        btn_topology.setStyleSheet("text-align: center;")

        btn_traffic_analysis = QPushButton('Анализ сетевого трафика', self)
        btn_traffic_analysis.setGeometry(50, 100, 400, 50)
        btn_traffic_analysis.clicked.connect(self.show_traffic_analysis)
        btn_traffic_analysis.setStyleSheet("text-align: center;")

        btn_device_availability = QPushButton('Проверка доступности сетевых\n устройств', self)
        btn_device_availability.setGeometry(50, 150, 400, 80)
        btn_device_availability.clicked.connect(self.show_device_availability)
        btn_device_availability.setStyleSheet("text-align: center;")

        btn_port_scanner = QPushButton('Порт-сканер', self)
        btn_port_scanner.setGeometry(50, 230, 400, 50)
        btn_port_scanner.clicked.connect(self.show_port_scanner)
        btn_port_scanner.setStyleSheet("text-align: center;")

        self.setGeometry(700, 300, 480, 370)
        # self.setFixedSize(480, 400)
        self.show()

    def show_traffic_analysis(self):
        self.hide()
        self.device_availability_window = TrafficAnalyzer()
        self.device_availability_window.show()

    def show_device_availability(self):
        self.hide()
        self.device_availability_window = DeviceAvailability()
        self.device_availability_window.show()

    def show_port_scanner(self):
        self.hide()
        self.port_scanner_window = PortScanner(self)
        self.port_scanner_window.show()

    def closeEvent(self, event):
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("fonts/Montserrat-Regular.ttf")
    ex = MyApp()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print("Unhandled exception:", e)

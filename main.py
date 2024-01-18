import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QFontDatabase

from ui.topology import show_topology
from ui.traffic_analysis import show_traffic_analysis
from ui.interface_data import show_interface_data
from ui.device_availability import show_device_availability
from ui.port_scanner import show_port_scanner


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
        btn_traffic_analysis.clicked.connect(show_traffic_analysis)
        btn_traffic_analysis.setStyleSheet("text-align: center;")

        btn_interface_data = QPushButton('Опрос и обработка данных\n о сетевых интерфейсах', self)
        btn_interface_data.setGeometry(50, 150, 400, 80)
        btn_interface_data.clicked.connect(show_interface_data)
        btn_interface_data.setStyleSheet("text-align: center;")

        btn_device_availability = QPushButton('Проверка доступности сетевых\n устройств', self)
        btn_device_availability.setGeometry(50, 210, 400, 80)
        btn_device_availability.clicked.connect(show_device_availability)
        btn_device_availability.setStyleSheet("text-align: center;")

        btn_port_scanner = QPushButton('Порт-сканер', self)
        btn_port_scanner.setGeometry(50, 280, 400, 50)
        btn_port_scanner.clicked.connect(show_port_scanner)
        btn_port_scanner.setStyleSheet("text-align: center;")

        self.setGeometry(300, 300, 480, 400)
        self.setFixedSize(480, 400)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("fonts/Montserrat-Regular.ttf")
    ex = MyApp()
    sys.exit(app.exec_())

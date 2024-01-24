import netifaces
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser, QPushButton
from threading import Thread


class Topology(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.initUI()

    def initUI(self):
        # self.setStyleSheet(open('styles/style_port_scanner.css').read())
        self.setWindowTitle('Топологии сети')
        self.layout = QVBoxLayout()

        self.result_name = QLabel('Результат')
        self.layout.addWidget(self.result_name)
        self.result_topology = QTextBrowser()
        self.layout.addWidget(self.result_topology)

        self.start_btn = QPushButton('Старт')
        self.start_btn.clicked.connect(self.start_topology)
        self.layout.addWidget(self.start_btn)

        self.setGeometry(750, 400, 400, 250)
        self.setLayout(self.layout)

    def closeEvent(self, event):
        self.main_app.show()

    def get_network_interfaces(self):
        interfaces = netifaces.interfaces()
        interface_info = []

        for iface in interfaces:
            iface_addresses = netifaces.ifaddresses(iface)
            addresses = iface_addresses.get(netifaces.AF_INET)
            ip_addresses = [addr['addr'] for addr in addresses] if addresses else []
            mac_addresses = iface_addresses.get(netifaces.AF_LINK)
            mac_address = mac_addresses[0]['addr'] if mac_addresses else None

            flags = netifaces.AF_INET6 in iface_addresses
            interface_enabled = True if flags else False

            interface_type = 'Unknown'
            if netifaces.AF_LINK in iface_addresses:
                interface_type = 'Ethernet'
            elif netifaces.AF_INET in iface_addresses:
                interface_type = 'IPv4'
            elif netifaces.AF_INET6 in iface_addresses:
                interface_type = 'IPv6'

            interface_data = {
                'interface': iface,
                'ip_addresses': ip_addresses,
                'mac_address': mac_address,
                'enabled': interface_enabled,
                'type': interface_type
            }

            interface_info.append(interface_data)
        return interface_info

    def start_topology(self):
        self.result_topology.clear()
        Thread(target=self.update_result_topology, args=(self.get_network_interfaces(),)).start()

    def update_result_topology(self, network_interfaces):
        for interface in network_interfaces:
            output = f"Интерфейс: {interface['interface']}\n"
            output += f"Тип интерфейса: {interface['type']}\n"
            output += f"IP-адреса: {', '.join(interface['ip_addresses'])}\n"
            output += f"MAC-адрес: {interface['mac_address']}\n"
            output += f"Состояние интерфейса: {'Включен' if interface['enabled'] else 'Выключен'}\n\n"
            self.result_topology.append(output)

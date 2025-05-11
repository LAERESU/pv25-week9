import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QWidget, QVBoxLayout,
    QTabWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QFontDialog, QHBoxLayout
)
from PyQt5.QtCore import Qt


class TabInputNama(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label_nama = QLabel("Nama:")
        self.label_hasil = QLabel("")  # Akan menampilkan nama di sebelah "Nama:"

        # Layout horizontal untuk "Nama: [hasil input]"
        self.nama_layout = QHBoxLayout()
        self.nama_layout.addWidget(self.label_nama)

        self.input_nama = QLineEdit()
        self.tombol = QPushButton("Input Nama")

        self.layout.addWidget(self.tombol)
        self.layout.addWidget(self.input_nama)
        self.layout.addLayout(self.nama_layout)  # Gunakan layout horizontal di sini
        self.setLayout(self.layout)

        self.tombol.clicked.connect(self.kirim_nama)
        self.on_nama_input = None

    def kirim_nama(self):
        nama = self.input_nama.text()
        self.label_nama.setText(f"Nama: {nama}")
        if self.on_nama_input:
            self.on_nama_input(nama)

    def get_nama(self):
        return self.input_nama.text()



class TabPilihFont(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("")
        self.tombol = QPushButton("Pilih Font")

        self.tombol.clicked.connect(self.pilih_font)

        self.layout.addWidget(self.tombol)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def pilih_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.label.setFont(font)

    def set_nama(self, nama):
        self.label.setText(f"Nama: {nama}")


class TabBukaFile(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("")
        self.tombol = QPushButton("Buka File")
        self.teks_file = QLineEdit()
        self.teks_file.setReadOnly(True)
        self.teks_file.setFixedHeight(200)


        self.tombol.clicked.connect(self.buka_file)

        self.layout.addWidget(self.tombol)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.teks_file)
        self.setLayout(self.layout)

    def buka_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Buka File", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.teks_file.setText(content)
            except Exception as e:
                self.teks_file.setText(f"Error: {e}")



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Week 9")
        self.setGeometry(100, 100, 600, 300)

        self.tabs = QTabWidget()
        self.tab1 = TabInputNama()
        self.tab2 = TabPilihFont()
        self.tab3 = TabBukaFile()

        self.tabs.addTab(self.tab1, "Input Nama")
        self.tabs.addTab(self.tab2, "Pilih Font")
        self.tabs.addTab(self.tab3, "Buka File")

        self.tabs.tabBar().setStyleSheet("""
            QTabBar::tab:selected { background: lightgreen; color: white; }
            QTabBar::tab:!selected { background: white; color: black; }
        """)
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.tabs)
        central_layout.setAlignment(Qt.AlignCenter)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        self.tab1.on_nama_input = self.tab2.set_nama

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        fitur_menu = menu_bar.addMenu("Fitur")

        keluar_action = QAction("Keluar", self)
        keluar_action.triggered.connect(self.close)
        file_menu.addAction(keluar_action)

        fitur_menu.addAction("Input Nama", lambda: self.tabs.setCurrentIndex(0))
        fitur_menu.addAction("Pilih Font", self.buka_tab_font)
        fitur_menu.addAction("Buka File", lambda: self.tabs.setCurrentIndex(2))

        self.tabs.currentChanged.connect(self.perbarui_tab)

    def buka_tab_font(self):
        nama = self.tab1.get_nama()
        self.tab2.set_nama(nama)
        self.tabs.setCurrentIndex(1)

    def perbarui_tab(self, index):
        if index == 1:
            nama = self.tab1.get_nama()
            self.tab2.set_nama(nama)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

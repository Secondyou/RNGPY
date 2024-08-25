import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, 
    QPushButton, QFileDialog, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor  # Add QColor import
from settings import SettingsWindow, SettingsManager

RARITY_COLORS = {
    "Common": QColor(0, 0, 0),             # Black
    "Uncommon": QColor(30, 144, 255),      # DodgerBlue
    "Rare": QColor(75, 0, 130),            # Indigo
    "Epic": QColor(148, 0, 211),           # DarkViolet
    "Legendary": QColor(255, 165, 0)       # Orange
}

class RNGSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_manager = SettingsManager()
        self.items = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("RNG System")
        self.setGeometry(100, 100, 600, 400)

        generate_button = QPushButton("Generate", self)
        generate_button.clicked.connect(self.generate)

        settings_button = QPushButton("Settings", self)
        settings_button.clicked.connect(self.open_settings)

        self.result_label = QLabel("", self)
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setAlignment(Qt.AlignCenter)

        # Position buttons in a horizontal layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(generate_button, alignment=Qt.AlignLeft)
        button_layout.addWidget(settings_button, alignment=Qt.AlignRight)

        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_settings(self):
        """Open the settings window."""
        self.settings_window = SettingsWindow(self, self.settings_manager)
        self.settings_window.show()

    def generate(self):
        if not self.items:
            self.items = self.settings_manager.config.get("items", [])
            if not self.items:
                QMessageBox.warning(self, "No Items", "No items available to generate.")
                return

        total_chance = sum(item['chance'] for item in self.items)
        random_number = random.randint(1, total_chance)
        cumulative_chance = 0

        result_item = None
        for item in self.items:
            cumulative_chance += item['chance']
            if random_number <= cumulative_chance:
                result_item = item
                break

        if result_item:
            self.display_results(result_item)

    def display_results(self, item):
        self.result_label.setText("Rolling...")
        QApplication.processEvents()

        final_result = f"{item['name']} ({item['rarity']})"
        QTimer.singleShot(1000, lambda: self.result_label.setText(f"Result: {final_result}"))

        rarity = item.get('rarity', 'Common')
        sound_file = self.settings_manager.config.get('sounds', {}).get(rarity)
        if sound_file:
            self.play_sound(sound_file)

    def play_sound(self, file_path):
        """Play sound based on rarity using PyQt5's QSound or another audio library."""
        pass  # Implement sound playback logic here

if __name__ == "__main__":
    app = QApplication(sys.argv)
    rng_system = RNGSystem()
    rng_system.show()
    sys.exit(app.exec_())

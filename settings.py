import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QCheckBox, QPushButton, QLineEdit, QLabel, QFileDialog,  QSpinBox
)
from PyQt5.QtCore import Qt
from item_config import ItemConfigWindow  # Import the new configuration window
class SettingsManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = {
            "items": [],
            "rarity_chances": {},
            "sounds": {},
            "sound_enabled": True,
            "multi_roll_chance": 0,
            "multi_roll_count": 1,
            "roll_sound": ""  # Default value for roll sound
        }
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, "r") as f:
                self.config = json.load(f)
            if "sounds" not in self.config:
                self.config["sounds"] = {}
        except FileNotFoundError:
            self.save_config()

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    def set_sound_enabled(self, enabled):
        self.config["sound_enabled"] = enabled
        self.save_config()

    def set_sound_file(self, rarity, file_path):
        self.config["sounds"][rarity] = file_path
        self.save_config()

    def set_multi_roll_chance(self, chance):
        self.config["multi_roll_chance"] = chance
        self.save_config()

    def set_multi_roll_count(self, count):
        self.config["multi_roll_count"] = count
        self.save_config()

    def set_roll_sound(self, file_path):
        self.config["roll_sound"] = file_path
        self.save_config()

    def get_roll_sound(self):
        return self.config.get("roll_sound", "")
        
class SettingsWindow(QDialog):
    def __init__(self, parent=None, settings_manager=None):
        super().__init__(parent)
        self.settings_manager = settings_manager

        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 400, 500)  # Adjust height for new fields

        layout = QVBoxLayout()

        # Sound Enable Checkbox
        self.sound_checkbox = QCheckBox("Enable Sound", self)
        self.sound_checkbox.setChecked(self.settings_manager.config.get("sound_enabled", True))
        self.sound_checkbox.stateChanged.connect(self.toggle_sound)
        layout.addWidget(self.sound_checkbox)

        # Sound Files for Each Rarity
        self.sound_inputs = {}
        for rarity in ["Common", "Uncommon", "Rare", "Epic", "Legendary"]:
            label = QLabel(f"{rarity} Sound:", self)
            layout.addWidget(label)

            sound_input = QLineEdit(self)
            sound_input.setText(self.settings_manager.config["sounds"].get(rarity, ""))
            layout.addWidget(sound_input)

            browse_button = QPushButton("...", self)
            browse_button.clicked.connect(lambda checked, rarity=rarity: self.select_file(rarity))
            layout.addWidget(browse_button)

            self.sound_inputs[rarity] = sound_input

        # Multi-Roll Chance Setting
        self.multi_roll_chance_label = QLabel("Multi-Roll Chance (%):", self)
        layout.addWidget(self.multi_roll_chance_label)

        self.multi_roll_chance_input = QLineEdit(self)
        self.multi_roll_chance_input.setText(str(self.settings_manager.config.get("multi_roll_chance", 0)))
        layout.addWidget(self.multi_roll_chance_input)

        # Multi-Roll Count Setting
        self.multi_roll_count_label = QLabel("Multi-Roll Count:", self)
        layout.addWidget(self.multi_roll_count_label)

        self.multi_roll_count_input = QSpinBox(self)
        self.multi_roll_count_input.setMinimum(1)
        self.multi_roll_count_input.setValue(self.settings_manager.config.get("multi_roll_count", 1))
        layout.addWidget(self.multi_roll_count_input)

        # Roll Sound Setting
        self.roll_sound_label = QLabel("Roll Sound:", self)
        layout.addWidget(self.roll_sound_label)

        self.roll_sound_input = QLineEdit(self)
        self.roll_sound_input.setText(self.settings_manager.get_roll_sound())
        layout.addWidget(self.roll_sound_input)

        roll_sound_browse_button = QPushButton("...", self)
        roll_sound_browse_button.clicked.connect(self.select_roll_sound_file)
        layout.addWidget(roll_sound_browse_button)

        # Button to open ItemConfigWindow
        item_config_button = QPushButton("Configure Items and Rules", self)
        item_config_button.clicked.connect(self.open_item_config)
        layout.addWidget(item_config_button)

        # Save Button
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def toggle_sound(self, state):
        self.settings_manager.set_sound_enabled(state == Qt.Checked)

    def select_file(self, rarity):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Sound File")
        if file_path:
            self.sound_inputs[rarity].setText(file_path)
            self.settings_manager.set_sound_file(rarity, file_path)

    def select_roll_sound_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Roll Sound File")
        if file_path:
            self.roll_sound_input.setText(file_path)
            self.settings_manager.set_roll_sound(file_path)

    def open_item_config(self):
        item_config_window = ItemConfigWindow(self, self.settings_manager)
        item_config_window.exec_()

    def save_settings(self):
        # Save sound settings
        for rarity, sound_input in self.sound_inputs.items():
            self.settings_manager.set_sound_file(rarity, sound_input.text())

        # Save multi-roll chance and count
        multi_roll_chance = int(self.multi_roll_chance_input.text())
        self.settings_manager.set_multi_roll_chance(multi_roll_chance)

        multi_roll_count = self.multi_roll_count_input.value()
        self.settings_manager.set_multi_roll_count(multi_roll_count)

        # Save roll sound setting
        self.settings_manager.set_roll_sound(self.roll_sound_input.text())

        self.close()

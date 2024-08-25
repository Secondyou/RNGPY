# item_edit.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox, QSpinBox
)

class ItemEditWindow(QDialog):
    def __init__(self, parent=None, item=None):
        super().__init__(parent)
        self.item = item if item else {}

        self.setWindowTitle("Edit Item")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        # Item Name
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter Item Name")
        self.name_input.setText(self.item.get("name", ""))
        layout.addWidget(QLabel("Item Name:"))
        layout.addWidget(self.name_input)

        # Rarity Selection
        self.rarity_combo = QComboBox(self)
        self.rarity_combo.addItems(["Common", "Uncommon", "Rare", "Epic", "Legendary"])
        self.rarity_combo.setCurrentText(self.item.get("rarity", "Common"))
        layout.addWidget(QLabel("Item Rarity:"))
        layout.addWidget(self.rarity_combo)

        # Chance Input
        self.chance_input = QSpinBox(self)
        self.chance_input.setRange(1, 100)
        self.chance_input.setValue(self.item.get("chance", 1))
        layout.addWidget(QLabel("Chance (%):"))
        layout.addWidget(self.chance_input)

        # Save and Cancel Buttons
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_item)
        layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.close)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def save_item(self):
        """Save the item details."""
        self.item["name"] = self.name_input.text()
        self.item["rarity"] = self.rarity_combo.currentText()
        self.item["chance"] = self.chance_input.value()
        self.accept()  # Closes the dialog and returns QDialog.Accepted

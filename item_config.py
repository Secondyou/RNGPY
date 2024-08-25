# item_config.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QListWidget, 
    QHBoxLayout, QLabel, QMenu, QAction, QInputDialog, QComboBox, QSpinBox
)
from PyQt5.QtCore import Qt, QPoint
from item_edit import ItemEditWindow  # Import the new ItemEditWindow

class ItemConfigWindow(QDialog):
    def __init__(self, parent=None, settings_manager=None):
        super().__init__(parent)
        self.settings_manager = settings_manager

        self.setWindowTitle("Configure Items and Custom Rules")
        self.setGeometry(150, 150, 500, 400)

        layout = QVBoxLayout()

        # Item List
        self.item_list = QListWidget(self)
        self.item_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.item_list.customContextMenuRequested.connect(self.open_context_menu)  # Connect to context menu
        self.load_items()
        layout.addWidget(self.item_list)

        # Add Item Section
        add_layout = QHBoxLayout()
        self.item_name_input = QLineEdit(self)
        self.item_name_input.setPlaceholderText("Enter Item Name")
        add_layout.addWidget(self.item_name_input)

        add_button = QPushButton("Add Item", self)
        add_button.clicked.connect(self.add_item)
        add_layout.addWidget(add_button)

        layout.addLayout(add_layout)

        # Save and Close Buttons
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def load_items(self):
        self.item_list.clear()
        for item in self.settings_manager.config.get("items", []):
            if isinstance(item, dict):
                item_name = item.get("name", "Unnamed Item")
            else:
                item_name = str(item)
            self.item_list.addItem(item_name)

    def add_item(self):
        item_name = self.item_name_input.text()
        if item_name:
            item_dict = {"name": item_name, "rarity": "Common", "chance": 1}  # Create a dictionary to store item details
            self.settings_manager.config["items"].append(item_dict)
            self.item_list.addItem(item_name)
            self.item_name_input.clear()

    def save_settings(self):
        self.settings_manager.save_config()
        self.close()

    def open_context_menu(self, position: QPoint):
        """Open context menu when right-clicking on an item."""
        menu = QMenu(self)
        edit_action = QAction("Edit", self)
        delete_action = QAction("Delete", self)

        edit_action.triggered.connect(self.edit_item)
        delete_action.triggered.connect(self.delete_item)

        menu.addAction(edit_action)
        menu.addAction(delete_action)

        menu.exec_(self.item_list.mapToGlobal(position))

    def edit_item(self):
        """Edit the selected item."""
        selected_items = self.item_list.selectedItems()
        if not selected_items:
            return
        item = selected_items[0]
        item_index = self.item_list.row(item)

        # Open ItemEditWindow to edit the item
        item_data = self.settings_manager.config["items"][item_index]
        edit_window = ItemEditWindow(self, item_data)
        if edit_window.exec_() == QDialog.Accepted:
            # Update the item in the list and settings manager
            self.settings_manager.config["items"][item_index] = edit_window.item
            self.item_list.item(item_index).setText(edit_window.item["name"])

    def delete_item(self):
        """Delete the selected item."""
        selected_items = self.item_list.selectedItems()
        if not selected_items:
            return
        item = selected_items[0]
        item_index = self.item_list.row(item)

        # Remove item from the list widget and settings manager
        self.item_list.takeItem(item_index)
        del self.settings_manager.config["items"][item_index]

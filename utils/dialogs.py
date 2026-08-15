from PySide6.QtWidgets import QFileDialog


def select_folder(parent=None):
    folder = QFileDialog.getExistingDirectory(
        parent,
        "Select Output Folder"
    )

    return folder
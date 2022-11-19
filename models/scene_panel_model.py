from PySide6.QtWidgets import QTreeWidgetItem


class ScenePanelModel:
    def __init__(self):
        self._item_map: dict[int, QTreeWidgetItem] = {}

    @property
    def item_map(self):
        return self._item_map

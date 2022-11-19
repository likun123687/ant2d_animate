from _weakref import ReferenceType
from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon, QPalette, QColor
from PySide6.QtWidgets import QMainWindow, QToolBar, QComboBox, QDoubleSpinBox

from common.signal_bus import SIGNAL_BUS
from views.property import PropertyType


class ToolBar:
    def __init__(self, main_window: ReferenceType[QMainWindow]):
        self._main_window: ReferenceType[QMainWindow] = main_window
        self._pos_x_spin_box: Optional[QDoubleSpinBox] = None
        self._pos_y_spin_box: Optional[QDoubleSpinBox] = None
        self._angle_spin_box: Optional[QDoubleSpinBox] = None

        self.create_tool_bar1()
        self.create_tool_bar2()
        self.create_tool_bar3()

    def create_tool_bar1(self):
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(True)
        self._main_window().addToolBar(toolbar)

        button_action = QAction(QIcon("bug.png"), "Armature", self._main_window())
        button_action.setStatusTip("Armature")
        button_action.setToolTip("Armature")
        button_action.setCheckable(True)
        toolbar.addAction(button_action)
        toolbar.addSeparator()

        button_action1 = QAction(QIcon("bug.png"), "Animation", self._main_window())
        button_action1.setStatusTip("Animation")
        button_action1.setToolTip("Animation")
        button_action1.setCheckable(True)
        toolbar.addAction(button_action1)

    def create_tool_bar2(self):
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self._main_window().addToolBar(toolbar)
        button_action = QAction(QIcon("bug.png"), "Select", self._main_window())
        button_action.setStatusTip("Select")
        button_action.setToolTip("Select")
        button_action.setCheckable(True)
        toolbar.addAction(button_action)
        toolbar.addSeparator()

        button_action1 = QAction(QIcon("bug.png"), "Pose", self._main_window())
        button_action1.setStatusTip("Pose")
        button_action1.setToolTip("Pose")
        button_action1.setCheckable(True)
        toolbar.addAction(button_action1)
        toolbar.addSeparator()

        button_action2 = QAction(QIcon("bug.png"), "Create Bone", self._main_window())
        button_action2.setStatusTip("Create Bone")
        button_action2.setToolTip("Create Bone")
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)
        toolbar.addSeparator()

        button_action3 = QAction(QIcon("bug.png"), "Create Bone", self._main_window())
        button_action3.setStatusTip("Create Bone")
        button_action3.setToolTip("Create Bone")
        button_action3.setCheckable(True)
        toolbar.addAction(button_action2)
        toolbar.addSeparator()

        scale_list = QComboBox()
        scale_list.addItems(["One", "Two", "Three"])
        scale_list.setEditable(True)
        scale_list.setInsertPolicy(QComboBox.NoInsert)
        toolbar.addWidget(scale_list)

    def create_tool_bar3(self):
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self._main_window().addToolBar(toolbar)
        # add move tool
        button_action = QAction(QIcon("test.png"), "Move", self._main_window())
        button_action.setStatusTip("Move")
        button_action.setToolTip("Move")
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        widget = QDoubleSpinBox()
        widget.setRange(-999999.00, 999999.00)
        toolbar.addWidget(widget)
        self._pos_x_spin_box = widget
        self._pos_x_spin_box.valueChanged.connect(self.slot_pos_x_changed)

        widget = QDoubleSpinBox()
        widget.setRange(-999999.00, 999999.00)
        toolbar.addWidget(widget)
        self._pos_y_spin_box = widget
        self._pos_y_spin_box.valueChanged.connect(self.slot_pos_y_changed)

        icon = QIcon("test.png")
        button_action = QAction(icon, "Move", self._main_window())
        button_action.setStatusTip("Move")
        button_action.setToolTip("Move")
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        # add rotate tool
        button_action = QAction(QIcon("rotate.png"), "Rotate", self._main_window())
        button_action.setStatusTip("Rotate")
        button_action.setToolTip("Rotate")
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        widget = QDoubleSpinBox()
        widget.setRange(-179.00, 180.00)
        self._angle_spin_box = widget
        self._angle_spin_box.valueChanged.connect(self.slot_angle_changed)

        toolbar.addWidget(widget)

        button_action = QAction(QIcon("rotate.png"), "Rotate", self._main_window())
        button_action.setStatusTip("Rotate")
        button_action.setToolTip("Rotate")
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        # add scale tool
        button_action = QAction(QIcon("bug.png"), "Select", self._main_window())
        button_action.setStatusTip("Select")
        button_action.setToolTip("Select")
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        widget = QDoubleSpinBox()
        toolbar.addWidget(widget)

        widget = QDoubleSpinBox()
        toolbar.addWidget(widget)

        widget = QDoubleSpinBox()
        toolbar.addWidget(widget)

        widget = QDoubleSpinBox()
        toolbar.addWidget(widget)

        button_action = QAction(QIcon("bug.png"), "Select", self._main_window())
        button_action.setStatusTip("Select")
        button_action.setToolTip("Select")
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        button_action = QAction(QIcon("bug.png"), "Select", self._main_window())
        button_action.setStatusTip("Select")
        button_action.setToolTip("Select")
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

    @property
    def pos_x_spin_box(self):
        return self._pos_x_spin_box

    @property
    def pos_y_spin_box(self):
        return self._pos_y_spin_box

    @property
    def angle_spin_box(self):
        return self._angle_spin_box

    def slot_pos_x_changed(self, d):
        SIGNAL_BUS.signal_item_property_changed.emit(d, PropertyType.POS_X, "from_toolbar")

    def slot_pos_y_changed(self, d):
        SIGNAL_BUS.signal_item_property_changed.emit(d, PropertyType.POS_Y, "from_toolbar")

    def slot_angle_changed(self, d):
        SIGNAL_BUS.signal_item_property_changed.emit(d, PropertyType.ANGLE, "from_toolbar")

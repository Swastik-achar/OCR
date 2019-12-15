from PyQt5.QtWidgets import QGraphicsPolygonItem
from PyQt5.QtWidgets import QGraphicsSceneHoverEvent
from PyQt5.QtGui import QBrush, QColor,QFont


class WordPolygon(QGraphicsPolygonItem):
    """Subclass of QGraphicsPolygonItem designed to display a translated word and its frame
    """

    def __init__(self, polygon=None, text=None) -> None:
        super().__init__(polygon)
        font = QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(50)
        self.text = text
        #self.text.setFont(font)
        #self.text.setTextWidth(1000)
        #self.text.boundingRect()
        #self.text.adjustSize()
        #self.text.setAlignment(QtCore.Qt.AlignCenter)
        #self.text.defaultTextColor(QColor(255, 0, 0, 75))
        
        self.setAcceptHoverEvents(True)
        self.setBrush(QBrush(QColor(51, 171, 249, 75)))

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Shows word/makes fraframe opaque when mouse hovers over frame.

        :param event: hover enter event to handle
        """

        self.setBrush(QBrush(QColor(51, 171, 249, 255)))
        self.text.setOpacity(1)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Hides translated word/makes frame semi-transparent when mouse stops hovering over frame.
        """

        self.setBrush(QBrush(QColor(51, 171, 249, 75)))
        self.text.setOpacity(0)

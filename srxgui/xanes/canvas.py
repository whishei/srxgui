from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.figure as cf

class Canvas(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = cf.Figure()
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from task_manager import TaskManager  # task_manager.py からインポート

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("TODOアプリ")
    self.setGeometry(100, 100, 400, 600)

    # TaskManager クラスのインスタンスを作成して設定
    task_manager = TaskManager()
    self.setCentralWidget(task_manager)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  app.exec()

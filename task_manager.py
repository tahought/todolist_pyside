import os
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, \
    QInputDialog, QCalendarWidget, QCheckBox

TASKS_FILE = "tasks.txt"

class TaskManager(QWidget):
  def __init__(self):
    super().__init__()

    self.task_list = QListWidget(self)
    self.task_input = QLineEdit(self)

    # 期限の有無を選ぶチェックボックスを追加
    self.due_date_checkbox = QCheckBox("期限を設定", self)
    self.due_date_checkbox.toggled.connect(self.toggle_due_date)

    # カレンダーウィジェットを追加
    self.calendar = QCalendarWidget(self)
    self.calendar.setGridVisible(True)  # グリッドを表示
    self.calendar.clicked.connect(self.update_due_date)

    # 期限入力フィールドをカレンダーウィジェットに変更
    self.due_date_input = self.calendar
    self.due_date_input.setVisible(False)  # 初期状態では非表示

    add_button = QPushButton("タスク追加", self)
    add_button.clicked.connect(self.add_task)

    delete_button = QPushButton("タスク削除", self)
    delete_button.clicked.connect(self.delete_task)

    edit_button = QPushButton("タスク編集", self)
    edit_button.clicked.connect(self.edit_task)

    layout = QVBoxLayout()
    input_layout = QHBoxLayout()
    input_layout.addWidget(self.task_input)
    layout.addLayout(input_layout)
    layout.addWidget(self.task_list)
    layout.addWidget(add_button)
    layout.addWidget(delete_button)
    layout.addWidget(edit_button)

    # 期限選択のチェックボックスとカレンダーをレイアウトに追加
    layout.addWidget(self.due_date_checkbox)
    layout.addWidget(self.due_date_input)

    self.setLayout(layout)

    self.load_tasks()

  def toggle_due_date(self):
    """期限設定の有無に応じてカレンダーの表示/非表示を切り替える"""
    if self.due_date_checkbox.isChecked():
      self.due_date_input.setVisible(True)  # 期限設定を有効にする
    else:
      self.due_date_input.setVisible(False)  # 期限設定を無効にする

  def add_task(self):
    task_text = self.task_input.text().strip()
    due_date = None

    if self.due_date_checkbox.isChecked():
      due_date = self.due_date_input.selectedDate().toString("yyyy-MM-dd")  # カレンダーから期限を取得

    if task_text:
      item = QListWidgetItem(task_text)
      item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
      item.setCheckState(Qt.CheckState.Unchecked)

      # 期限をタスクに保存
      item.setData(Qt.UserRole, due_date)
      self.task_list.addItem(item)
      self.task_input.clear()
      self.due_date_checkbox.setChecked(False)  # 期限を設定した後、チェックボックスをリセット
      self.due_date_input.setVisible(False)  # 期限の表示をリセット
      self.save_tasks()

  def delete_task(self):
    selected_item = self.task_list.currentItem()
    if selected_item:
      row = self.task_list.row(selected_item)
      self.task_list.takeItem(row)
      self.save_tasks()

  def edit_task(self):
    selected_item = self.task_list.currentItem()
    if selected_item:
      current_text = selected_item.text()
      new_text, ok = QInputDialog.getText(
          self, "タスクの編集", "新しいタスク名:", text=current_text)

      if ok and new_text.strip():
        selected_item.setText(new_text.strip())
        self.save_tasks()

  def update_due_date(self):
    """カレンダーから選択した日付をタスクの期限として設定"""
    selected_date = self.due_date_input.selectedDate().toString("yyyy-MM-dd")
    print(f"選択された期限: {selected_date}")

  def update_task_style(self, item):
    """タスクの完了状態を視覚的に反映"""
    font = QFont("Arial", 12)

    # 期限を取得
    due_date = item.data(Qt.UserRole)
    current_date = QDate.currentDate().toString("yyyy-MM-dd")

    if due_date and due_date < current_date:
      item.setBackground(QColor("lightcoral"))  # 期限切れのタスクは赤色の背景

    if item.checkState() == Qt.CheckState.Checked:
      item.setForeground(QColor("gray"))
      font.setItalic(True)
      item.setFont(font)
      item.setText(f"✔ {item.text().replace('✔ ', '')}")
    else:
      item.setForeground(QColor("black"))
      font.setItalic(False)
      item.setFont(font)
      item.setText(item.text().replace("✔ ", ""))

    self.save_tasks()

  def save_tasks(self):
    with open(TASKS_FILE, 'w', encoding='utf-8') as file:
      for i in range(self.task_list.count()):
        item = self.task_list.item(i)
        task_text = item.text().replace("✔ ", "")
        task_state = "checked" if item.checkState() == Qt.CheckState.Checked else "unchecked"
        due_date = item.data(Qt.UserRole)  # 期限も一緒に保存

        # タスクと期限を保存
        file.write(
            f"{task_text}|{task_state}|{due_date if due_date else ''}\n")

  def load_tasks(self):
    if os.path.exists(TASKS_FILE):
      with open(TASKS_FILE, 'r', encoding='utf-8') as file:
        for line in file:
          task_data = line.strip().split('|')
          if len(task_data) >= 2:
            task_text, task_state = task_data[0], task_data[1]
            due_date = task_data[2] if len(task_data) > 2 else None
            item = QListWidgetItem(task_text)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Checked if task_state == "checked" else Qt.CheckState.Unchecked)
            item.setData(Qt.UserRole, due_date)  # 期限をセット
            self.task_list.addItem(item)
            self.update_task_style(item)  # スタイルを適用

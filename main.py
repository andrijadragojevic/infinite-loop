import sqlite3

from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox, QListWidget, QVBoxLayout
from PyQt5.uic import loadUi
import sys
from qtconsole.qt import QtCore


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("main.ui", self)
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
        self.deleteButton.clicked.connect(self.deleteTask)
        self.addButton.clicked.connect(self.addNewTask)
        self.tasksListWidget.itemSelectionChanged.connect(self.selectionChanged)
        

    def calendarDateChanged(self):
        print("The calendar date was changed.")
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        print("Date selected:", dateSelected)
        self.updateTaskList(dateSelected)

# Prikazivanje Taskova
    def updateTaskList(self, date):
        self.tasksListWidget.clear()

        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date,)
        results = cursor.execute(query, row).fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if result[1] == "YES":
                item.setCheckState(QtCore.Qt.Checked)
            elif result[1] == "NO":
                item.setCheckState(QtCore.Qt.Unchecked)
            self.tasksListWidget.addItem(item)
            
            
# Vaca selectoviani item
    def selectionChanged(self):        
        item = self.tasksListWidget.selectedItems()
        item = item[0]
        selected_task = item.text()
        print("SELECTED TASK: " + selected_task)
        return selected_task
        
    def deleteTask(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = str(self.calendarWidget.selectedDate().toPyDate())
        task = self.selectionChanged()
        print("DATE IS:" + date)
        
        query = "DELETE FROM tasks WHERE task = ? AND date = ?" 
        row = (task, date,)
        cursor.execute(query, row)
        db.commit()
        self.updateTaskList(date)
        
# Cuvanje promjena nad listom
    def saveChanges(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()

        for i in range(self.tasksListWidget.count()):
            item = self.tasksListWidget.item(i)
            task = item.text()
            print(item.text)
            if item.checkState() == QtCore.Qt.Checked:
                query = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND date = ?"
            else:
                query = "UPDATE tasks SET completed = 'NO' WHERE task = ? AND date = ?"
            row = (task, date,)
            cursor.execute(query, row)
        db.commit()


    def addNewTask(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        
        time = self.timeBox.text()
        
        if (len(str(self.taskLineEdit.text())) > 0):
            newTask = "  " + str(self.taskLineEdit.text()) + "\n   " + time
            date = self.calendarWidget.selectedDate().toPyDate()
            
            query = "INSERT INTO tasks(task, completed, date) VALUES (?,?,?)"
            row = (newTask, "NO", date,)
    
            cursor.execute(query, row)
            db.commit()
            self.updateTaskList(date)
            self.taskLineEdit.clear()
            self.saveChanges()        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
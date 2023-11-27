import sys
from PyQt5.uic import loadUi
import io
from PyQt5.QtWidgets import QLabel, QTableWidget, QPushButton, QApplication, QMainWindow, QProgressBar, QLineEdit, \
    QStatusBar, QTableWidgetItem, QComboBox, QWidget, QMenu, QAction, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QColor, QIcon
import csv
from xlsxwriter.workbook import Workbook

form = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>645</width>
    <height>447</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Таблицы истинности</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QGridLayout" name="gridLayout">
    <item row="0" column="0">
     <layout class="QGridLayout" name="gridLayout_2">
      <item row="0" column="1">
       <widget class="QComboBox" name="log_oper">
        <item>
         <property name="text">
          <string>не выбрано</string>
         </property>
        </item>
        <item>
         <property name="text">
          <string>не</string>
         </property>
        </item>
        <item>
         <property name="text">
          <string>или(+)</string>
         </property>
        </item>
        <item>
         <property name="text">
          <string>и(*)</string>
         </property>
        </item>
        <item>
         <property name="text">
          <string>импликация(-&gt;)</string>
         </property>
        </item>
        <item>
         <property name="text">
          <string>экьюваленция(&lt;-&gt;)</string>
         </property>
        </item>
        <item>
         <property name="text">
          <string>строгая дизьюнкция(⊕)</string>
         </property>
        </item>
       </widget>
      </item>
      <item row="0" column="4">
       <widget class="QPushButton" name="clear_btn">
        <property name="text">
         <string>Очистить</string>
        </property>
       </widget>
      </item>
      <item row="0" column="2">
       <widget class="QPushButton" name="pushButton">
        <property name="text">
         <string>создать лог. переменную</string>
        </property>
       </widget>
      </item>
      <item row="0" column="3">
       <widget class="QPushButton" name="create_t">
        <property name="text">
         <string>Выполнить</string>
        </property>
       </widget>
      </item>
      <item row="0" column="0">
       <widget class="QLabel" name="label">
        <property name="text">
         <string>Логическое действие</string>
        </property>
       </widget>
      </item>
     </layout>
    </item>
    <item row="1" column="0">
     <widget class="QTableWidget" name="table"/>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>645</width>
     <height>21</height>
    </rect>
   </property>
   <widget class="QMenu" name="menu">
    <property name="title">
     <string>файл</string>
    </property>
    <addaction name="action_3"/>
    <addaction name="action_4"/>
    <addaction name="action_xlsx"/>
    <addaction name="action_5"/>
   </widget>
   <widget class="QMenu" name="menu_2">
    <property name="title">
     <string>инструкция</string>
    </property>
   </widget>
   <addaction name="menu"/>
   <addaction name="menu_2"/>
  </widget>
  <widget class="QToolBar" name="toolBar">
   <property name="windowTitle">
    <string>toolBar</string>
   </property>
   <attribute name="toolBarArea">
    <enum>TopToolBarArea</enum>
   </attribute>
   <attribute name="toolBarBreak">
    <bool>false</bool>
   </attribute>
  </widget>
  <action name="action_3">
   <property name="text">
    <string>сохранить</string>
   </property>
  </action>
  <action name="action_4">
   <property name="text">
    <string>сохранить как</string>
   </property>
  </action>
  <action name="action_xlsx">
   <property name="text">
    <string>экспорт в xlsx</string>
   </property>
  </action>
  <action name="action_5">
   <property name="text">
    <string>открыть</string>
   </property>
  </action>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

alplabet = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y',
            'Z']
text = '''\t\tИнструкция
1. Создайте все логические переменные, которые
 вам понадобятся(кнопка 'создать лог. переменную')
2. Выберите действие.
3. Выберите необходимые переменные нажав
 на название столбца.
4. Нажмите кнопку выполнить.
\tПорядок выполнения логических операций.
1. Инверсия(не) 
2. Коньюнкция(*)
3. Дизъюнкция(+), строгая дизюнкция(⊕) 
4. Импликация(->)
5. Экюваленция (=)
\npowered by Arsenii Mineev'''


class Instyk(QWidget):
    def __init__(self):
        super().__init__()
        self.laout1 = QHBoxLayout(self)
        self.label = QLabel(self)
        self.laout1.addWidget(self.label)
        self.label.setText(text)
        self.setGeometry(300, 300, 290, 200)
        self.setWindowTitle("Инструкция")


class Premen:
    def __init__(self, mas, name):
        self.znaz = [int(i) for i in mas]
        self.name = name

    def __neg__(self):
        new = []
        for i in self.znaz:
            if i == 0:
                new.append(1)
            else:
                new.append(0)
        return Premen(new, f"-{self.name}")

    def __mul__(self, other):
        new = []
        for i in range(len(self.znaz)):
            if self.znaz[i] and other.znaz[i]:
                new.append(1)
            else:
                new.append(0)
        return Premen(new, f"({self.name} * {other.name})")

    def __add__(self, other):
        new = []
        for i in range(len(self.znaz)):
            if self.znaz[i] or other.znaz[i]:
                new.append(1)
            else:
                new.append(0)
        return Premen(new, f"({self.name} + {other.name})")

    def __eq__(self, other):
        new = []
        for i in range(len(self.znaz)):
            try:
                if self.znaz[i] == other.znaz[i]:
                    new.append(1)
                else:
                    new.append(0)
            except AttributeError:
                return False
        try:
            return Premen(new, f"({self.name}={other.name})")
        except AttributeError:
            return False

    def get_znak(self):
        return self.znaz

    def implik(self, other):
        new = []
        for i in range(len(self.znaz)):
            if self.znaz[i] == other.znaz[i] or (self.znaz[i] == 0 and other.znaz[i] == 1):
                new.append(1)
            else:
                new.append(0)
        return Premen(new, f"({self.name}->{other.name})")

    def st_dis(self, other):
        new = []
        for i in range(len(self.znaz)):
            if self.znaz[i] == other.znaz[i]:
                new.append(0)
            else:
                new.append(1)
        return Premen(new, f"({self.name}⊕{other.name})")

    def is_mas(self, s_mas):
        if self.znaz == s_mas:
            return True
        else:
            return False


class Logic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.peremen = []
        self.first_v = ''
        self.two_v = ''
        self.labels = []
        self.loadUI()
        self.fail = None
        self.instryk = Instyk()
        self.instryk.hide()

    def loadUI(self):
        f_menu = io.StringIO(form)
        loadUi(f_menu, self)
        self.setWindowIcon(QIcon("icon.jpg"))
        self.setCentralWidget(self.centralwidget)
        self.table: QTableWidget
        self.pushButton: QPushButton
        self.pushButton.clicked.connect(self.create_log)
        self.table.itemSelectionChanged.connect(self.vabor)
        self.create_t.clicked.connect(self.varage)
        self.action_4: QAction
        self.action_3: QAction
        self.action_xlsx: QAction
        self.action_xlsx.triggered.connect(self.export)
        self.action_3.triggered.connect(self.save_table)
        self.menu_2: QMenu
        self.action_4.triggered.connect(self.save_as_table)
        self.menu_2.aboutToShow.connect(self.show_ins)
        self.clear_btn: QPushButton
        self.clear_btn.clicked.connect(self.clear_tabe)
        self.action_5: QAction
        self.action_5.triggered.connect(self.open_table)

    def show_ins(self):
        self.instryk.show()

    def export(self):
        if self.fail is None:
            self.fail, ok = QFileDialog.getSaveFileName(self, 'сохранить', "*.xlsx")
            if not ok:
                return None
            else:
                if len(self.fail) > 5:
                    self.fail = self.fail[:-5] + ".csv"
                else:
                    self.fail = self.fail + ".csv"
                self.save_table()
        csvfile = self.fail
        if csvfile != "":
            workbook = Workbook(csvfile[:-4] + '.xlsx')
            worksheet = workbook.add_worksheet()
            with open(csvfile, 'rt', encoding='utf8') as f:
                reader = csv.reader(f, delimiter=';')
                for r, row in enumerate(reader):
                    for c, col in enumerate(row):
                        worksheet.write(r, c, col)
            workbook.close()

    def save_as_table(self):
        fail, ok = QFileDialog.getSaveFileName(self, 'сохранить', "*.csv")
        if fail != "" and ok:
            with open(fail, 'w', newline='') as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"',
                    quoting=csv.QUOTE_MINIMAL)
                # Получение списка заголовков
                writer.writerow(
                    [self.table.horizontalHeaderItem(i).text()
                     for i in range(self.table.columnCount())])
                for i in range(self.table.rowCount()):
                    row = []
                    for j in range(self.table.columnCount()):
                        item = self.table.item(i, j)
                        if item is not None:
                            item: QTableWidgetItem
                            try:
                                row.append(int(item.text()))
                            except BaseException:
                                row.append(item.text())
                                print(str)
                    writer.writerow(row)

    def save_table(self):
        ok = True
        if self.fail is None:
            self.fail, ok = QFileDialog.getSaveFileName(self, 'сохранить', "*.csv")
        if self.fail != "" and ok:
            with open(self.fail, 'w', newline='') as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"',
                    quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [self.table.horizontalHeaderItem(i).text()
                     for i in range(self.table.columnCount())])
                for i in range(self.table.rowCount()):
                    row = []
                    for j in range(self.table.columnCount()):
                        item = self.table.item(i, j)
                        if item is not None:
                            row.append(int(item.text()))
                    writer.writerow(row)

    def clear_tabe(self):
        self.labels.clear()
        self.peremen.clear()
        self.table: QTableWidget
        self.table.clear()
        self.two_v = ''
        self.first_v = ''
        self.table.setColumnCount(0)
        self.pushButton: QPushButton
        self.pushButton.setEnabled(True)
        self.fail = None
        self.table.setRowCount(0)

    def create_log(self):
        self.table: QTableWidget
        len_per = len(self.peremen) + 1
        if len(alplabet) < len_per:
            return None
        try:
            self.labels.append(alplabet[len_per - 1])
        except IndexError:
            self.labels.append(alplabet[- 1] + f"{len_per - len(alplabet)}")
        self.table.setColumnCount(len_per)
        splog = []
        for i in range(2 ** len_per):
            if len(bin(i)[2:]) < len_per:
                splog.append(("0" * (len_per - len(bin(i)[2:]))) + bin(i)[2:])
            else:
                splog.append(bin(i)[2:])
        self.table.setRowCount(2 ** len_per)
        self.peremen.clear()
        for i in range(len_per):
            mas = []
            for j in range(len(splog)):
                self.table.setItem(j, i, QTableWidgetItem(splog[j][i]))
                mas.append(splog[j][i])
            self.peremen.append(Premen(mas, alplabet[i]))
        self.table.setHorizontalHeaderLabels(alplabet)
        self.table.resizeColumnsToContents()

    def varage(self):
        self.table: QTableWidget
        self.log_oper: QComboBox
        if self.log_oper == "не выбрано" or self.first_v == '':
            return None
        self.first_v: Premen
        if self.log_oper.currentText() == "не":
            self.first_v: Premen
            d = -self.first_v
        elif self.two_v == "":
            return None
        elif self.log_oper.currentText() == "или(+)":
            self.two_v: Premen
            d = self.two_v + self.first_v
        elif self.log_oper.currentText() == "и(*)":
            d = self.two_v * self.first_v
        elif self.log_oper.currentText() == "экьюваленция(<->)":
            self.two_v: Premen
            self.first_v: Premen
            d = self.two_v == self.first_v
        elif self.log_oper.currentText() == "импликация(->)":
            self.first_v: Premen
            d = self.first_v.implik(self.two_v)
        else:
            self.two_v: Premen
            self.first_v: Premen
            d = self.first_v.st_dis(self.two_v)
        data = d.get_znak()
        self.table.setColumnCount(self.table.columnCount() + 1)
        for i in range(len(data)):
            self.table.setItem(i, self.table.columnCount() - 1, QTableWidgetItem(str(data[i])))
        d: Premen
        self.peremen.append(d)
        self.pushButton: QPushButton
        self.pushButton.setEnabled(False)
        self.first_v = ''
        self.two_v = ''
        self.labels.append(d.name)
        for i in range(self.table.columnCount()):
            for j in range(self.table.rowCount()):
                self.table.item(j, i).setBackground(QColor(255, 255, 255))
        self.table.setHorizontalHeaderLabels(self.labels)
        self.table.resizeColumnsToContents()

    def open_table(self):
        self.fail, ok = QFileDialog.getOpenFileName(self, 'открыть', "*.csv")
        if ok:
            self.table: QTableWidget
            self.table.clear()
            file_input = open(self.fail, encoding="utf-8")
            reader = csv.reader(file_input, delimiter=';', quotechar='"')
            reader = list(reader)
            self.table.setRowCount(len(reader) - 1)
            self.table.setColumnCount(len(reader[0]))
            self.table.setHorizontalHeaderLabels(reader[0])
            for index, row in enumerate(reader):
                if index == 0:
                    continue
                for i in range(len(row)):
                    self.table.setItem(index, i, QTableWidgetItem(str(reader[index][i])))
            self.table.resizeColumnsToContents()
            file_input.close()
            if len(reader) - 1 != 2 ** len(reader[0]):
                self.pushButton.setEnabled(False)
            mas = []
            for i in range(len(reader[0])):
                new = []
                for j in range(1, len(reader)):
                    new.append(reader[j][i])
                mas.append(new)
            for i in range(len(mas)):
                self.peremen.append(Premen(mas[i], reader[0][i]))
                self.labels.append(reader[0][i])

    def vabor(self):
        self.table: QTableWidget
        mas = []
        for i in self.table.selectedItems():
            mas.append(int(i.text()))
            i.setBackground(QColor(172, 174, 255))
        index = 0
        if mas == list():
            self.first_v = ""
            self.two_v = ''
            return None
        for i in range(len(self.peremen)):
            if self.peremen[i].znaz == mas:
                index = i
                break
        if self.first_v == "":
            self.first_v = Premen(mas, self.peremen[index].name)
        else:
            self.two_v = Premen(mas, self.peremen[index].name)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Logic()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

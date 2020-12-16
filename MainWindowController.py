from views.MainWindow import Ui_MainForm
from PyQt5 import QtWidgets
from Serializer import Serializer
from TableModel import TableModel
from Executor import Executor
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from TipBoxController import TipBoxController
import math
import os
import string
import numpy
import PyQt5
import random as rand
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


class MainWindowController(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindowController, self).__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)

        self.ui.addSaleButton.clicked.connect(self.add_sale_action)
        self.ui.removeSaleButton.clicked.connect(self.remove_sale_action)

        self.ui.resultTableView.setModel(TableModel([], [], []))

        self.ui.saveButton.clicked.connect(self.save_to_file)
        self.ui.loadButton.clicked.connect(self.load_from_file)
        self.ui.tipButton.clicked.connect(self.show_tip)

        self.ui.calcButton.clicked.connect(self.make_calculation)
        self.ui.saleTableWidget.cellChanged.connect(self.cell_changed)

    def add_sale_action(self):
        row_count = self.ui.saleTableWidget.rowCount()
        self.ui.saleTableWidget.insertRow(row_count)

    def remove_sale_action(self):
        selected_row = self.ui.saleTableWidget.currentRow()
        if selected_row >= 0:
            self.ui.saleTableWidget.removeRow(selected_row)
        else:
            self.ui.saleTableWidget.removeRow(self.ui.saleTableWidget.rowCount() - 1)

    def save_to_file(self):
        try:
            sfd_res = QtWidgets.QFileDialog.getSaveFileName(self, 'Load file...')
            if len(sfd_res) == 0:
                QtWidgets.QMessageBox.critical(self, 'Error', 'Файлы не выбраны')
                return
            else:
                path = sfd_res[0]
                sales_data = []
                for i in range(self.ui.saleTableWidget.rowCount()):
                    sales_row = []
                    for j in range(self.ui.saleTableWidget.columnCount()):
                        cell_text = ''
                        if self.ui.saleTableWidget.item(i, j):
                            cell_text = self.ui.saleTableWidget.item(i, j).text()
                        sales_row.append(cell_text)
                    sales_data.append(sales_row)
                data = [
                    self.ui.WSpinBox.value(),
                    self.ui.TSpinBox.value(),
                    self.ui.CpSpinBox.value(),
                    self.ui.CxSpinBox.value(),
                    self.ui.CdSpinBox.value(),
                    self.ui.CySpinBox.value(),
                    self.ui.DtSpinBox.value(),
                    sales_data
                    ]
                Serializer.serialize(path, data)
        except Exception:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Ошибка сохранения')

    def load_from_file(self):
        try:
            ofd_res = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file...')
            if len(ofd_res) == 0:
                QtWidgets.QMessageBox.critical(self, 'Error', 'Файлы не выбраны')
                return
            else:
                w_value, t_value, cp_value, cx_value, cd_value, cy_value, dt_value, sales_data = \
                    Serializer.deserialize(ofd_res[0])
                self.ui.WSpinBox.setValue(float(w_value))
                self.ui.TSpinBox.setValue(float(t_value))
                self.ui.CpSpinBox.setValue(float(cp_value))
                self.ui.CxSpinBox.setValue(float(cx_value))
                self.ui.CdSpinBox.setValue(float(cd_value))
                self.ui.CySpinBox.setValue(float(cy_value))
                self.ui.DtSpinBox.setValue(float(dt_value))
                self.ui.saleTableWidget.clear()
                self.ui.saleTableWidget.setRowCount(0)
                for row in sales_data:
                    self.ui.saleTableWidget.setRowCount(self.ui.saleTableWidget.rowCount() + 1)
                    self.ui.saleTableWidget.setColumnCount(len(row))
                    for i in range(len(row)):
                        cell = self.ui.saleTableWidget.item(self.ui.saleTableWidget.rowCount() - 1, i)
                        if not cell:
                            new_cell = QtWidgets.QTableWidgetItem()
                            new_cell.setText(row[i])
                            self.ui.saleTableWidget.setItem(self.ui.saleTableWidget.rowCount() - 1, i, new_cell)

        except Exception:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Ошибка сохранения')

    def cell_changed(self, row, column):
        value = self.ui.saleTableWidget.item(row, column).text()
        if value == '':
            return
        if not str.isnumeric(value) or float(value) < 0:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Неверно введенное значение. Пример значения: 3.14')
        if (column == 0 and self.ui.saleTableWidget.item(row, 1) and str.isnumeric(self.ui.saleTableWidget.item(row, 1).text())
            and float(self.ui.saleTableWidget.item(row, 1).text()) < float(value)) or \
            (column == 1 and self.ui.saleTableWidget.item(row, 0) and str.isnumeric(self.ui.saleTableWidget.item(row, 0).text())
             and float(self.ui.saleTableWidget.item(row, 0).text()) > float(value)):
            QtWidgets.QMessageBox.critical(self, 'Error', 'Начальное значение должно быть меньше конечного')
            self.ui.saleTableWidget.item(row, column).setText('')
        if column == 2 and float(value) > 100:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Достигнут верхний предел значения')
            self.ui.saleTableWidget.item(row, column).setText(str(100))

    def show_tip(self):
        tip = TipBoxController()
        tip.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        tip.exec_()

    def make_calculation(self):
        try:
            W_val = self.ui.WSpinBox.value()
            T_val = self.ui.TSpinBox.value()
            Cp_val = self.ui.CpSpinBox.value()
            Cx_val = self.ui.CxSpinBox.value()
            Cd_val = self.ui.CdSpinBox.value()
            Cy_val = self.ui.CySpinBox.value()
            Dt_val = self.ui.DtSpinBox.value()

            sales_values = []
            for i in range(self.ui.saleTableWidget.rowCount()):
                lower = self.ui.saleTableWidget.item(i, 0)
                if not lower or not lower.text() or not str.isnumeric(lower.text()):
                    if i == 0:
                        lower = 0
                    else:
                        QtWidgets.QMessageBox.critical(self, 'Error', 'Неверно задан нижний предел скидки')
                        return
                else:
                    lower = lower.text()
                higher = self.ui.saleTableWidget.item(i, 1)
                if not higher or not higher.text() or not str.isnumeric(higher.text()):
                    if i == self.ui.saleTableWidget.rowCount() - 1:
                        higher = math.inf
                    else:
                        QtWidgets.QMessageBox.critical(self, 'Error', 'Неверно задан верхний предел скидки')
                        return
                else:
                    higher = higher.text()
                coeff = self.ui.saleTableWidget.item(i, 2)
                if not coeff or not coeff.text() or not str.isnumeric(coeff.text()):
                    QtWidgets.QMessageBox.critical(self, 'Error', 'Неверно задан коэффициент скидки')
                    return
                sales_values.append({
                    'lo': float(lower),
                    'hi': float(higher),
                    'cf':  float(coeff.text()) / 100
                })
        except Exception:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Ошибка при чтении данных')
            return

        try:
            solver = Executor(W_val, T_val, Cp_val, Cx_val, Cd_val, Cy_val, Dt_val)

            solution_parameters = []
            solution_parameters.append(solver.calculate_parameters())
            for sale_value in sales_values:
                solution_parameters.append(solver.calculate_parameters(sale_value['lo'], sale_value['hi'], sale_value['cf']))

            best_parameter = sorted(solution_parameters, key=lambda x: x['s_sum'], reverse=False)[0]
            best_index = solution_parameters.index(best_parameter)

        except Exception:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Ошибка при проведении расчетов')
            return

        try:
            self.print_result(solution_parameters, best_index)
            file_path = self.draw_plot(best_parameter)
            pixmap = QPixmap(file_path)
            self.ui.graphLabel.setEnabled(True)
            self.ui.graphLabel.setPixmap(pixmap)
            self.ui.graphLabel.resize(pixmap.width(), pixmap.height())
        except Exception:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Ошибка при выводе данных')
            return

    def print_result(self, solution_parameters, index_best):
        self.ui.resultTableView.model().clear()
        self.ui.resultTableView.model().add_columns(11, None, ['n', 'K', 'Q\'', 'M\'', 't\'', 'P', 'Sx', 'Sд', 'Sп', 'Sу', 'S'])
        row_num = 0

        for row in solution_parameters:
            self.ui.resultTableView.model().add_row([
                round(row['orders'], 4),
                round(row['k'], 4),
                round(row['q_opt'], 4),
                round(row['m_opt'], 4),
                round(row['t_opt'], 4),
                round(row['ord_opt'], 4),
                round(row['s_x'], 4),
                round(row['s_d'], 4),
                round(row['s_p'], 4),
                round(row['s_y'], 4),
                round(row['s_sum'], 4)
            ], [row_num + 1])
            row_num += 1
        self.ui.resultTableView.resizeColumnsToContents()
        self.ui.resultTableView.model().primary_row = index_best

    def draw_plot(self, plot_data):
        fig, pl = plt.subplots(figsize=(6.5, 3.5))

        m_value = plot_data['m_opt']
        q_value = plot_data['q_opt']
        t_value = plot_data['t_opt']
        orders_quantity = plot_data['orders']
        order_level = plot_data['ord_opt']

        pl.set_xlim(0, orders_quantity * t_value)
        pl.set_ylim(m_value - q_value - 1, m_value + 1)

        x_coords = []
        y_coords = []
        for i in range(orders_quantity):
            y_coords.append(m_value)
            x_coords.append(i * t_value)
            y_coords.append(m_value - q_value)
            x_coords.append((i + 1) * t_value)
        pl.plot(x_coords, y_coords)

        pl.set_xlabel('t')
        pl.set_ylabel('I(t)')
        pl.set_title('График поставок')
        pl.axhline(y=order_level, color='red', linestyle='dashed')
        pl.axhline(y=0, color='black', linestyle='-')

        filename = './plots/' + ''.join([rand.choice(string.ascii_lowercase) for i in range(10)]) + '.png'
        if not os.path.exists(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))
        plt.savefig(filename)
        return filename



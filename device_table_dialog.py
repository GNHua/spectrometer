import sys
from seabreeze.spectrometers import list_devices
from PyQt4 import QtCore, QtGui, uic

class DevTableModel(QtCore.QAbstractTableModel):
    def __init__(self, dev=[]):
        super().__init__()
        self._headers = ['Serial Number', 'Model']
        self._dev = dev
        
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
    def rowCount(self, parent): return len(self._dev)
    def columnCount(self, parent): return 2
    
    def data(self, index, role):
        if not index.isValid(): return None
        if role == QtCore.Qt.DisplayRole:
            return self._dev[index.row()][index.column()]
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        else:
            return None
            
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._headers[section]
            else:
                return section+1

Ui_Dialog, QDialog = loadUiType('device_table_dialog.ui')
class DevTableDialog(QDialog, Ui_Dialog):
    '''
    A dialog window to select device.
    '''
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.model = DevTableModel()
        self.tableViewDev.setModel(self.model)

        self.pushButtonRefresh.clicked.connect(self.refresh)
        self.buttonBox.accepted.connect(self.openDev)
        self.selected_dev = None

        self.refresh()

    def refresh(self):
        del self.model._dev[:]

        for d in sb.list_devices():
            self.model._dev.append([d.serial, d.model])

    def openDev(self):
        selected = self.tableViewDev.selectedIndexes()
        if len(selected) > 0:
            # make sure the spectrometer is powered by +5V power supply.
            QtGui.QMessageBox.warning(self, 'Message',
                                      'Make sure power supply is connected!',
                                      QtGui.QMessageBox.Ok)
            # get the serial number of the selected device
            self.selected_dev = self.model._dev[selected[0].row()][0]

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = DevTableDialog()
    main.show()
    sys.exit(app.exec_())

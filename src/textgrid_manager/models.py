import json
from pathlib import Path
from importlib import resources

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
    QDate,
)
from PySide6.QtGui import (
    QPixmap,
    QIcon,
    QColor
)
from textgrid_manager import utils

icons_dir = resources.files('textgrid_manager.resources') / 'fuge-icons'

class TGTableModel(QAbstractTableModel):

    def __init__(self, data=None):
        super().__init__()
        if data is None:
            # Temporal
            self._data = []
        self._headers = ['Text', 'Tier', 'start', 'end', 'file']
        self._data = utils.scan_library(r'D:\Users\FN\Documents\projects\textgrid-manager\tests\data')
        self.update_data(self._data)

    def update_data(self, data):
        list_ = []
        for tg in data:
            for tier in tg:
                for item in tier:
                    if item.text == '':
                        continue
                    list_.append(item)
        self._data = list_

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return

        if orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return section+1

    def data(self, index=QModelIndex(), role=Qt.ItemDataRole.DisplayRole):
        row, column = index.row(), index.column()
        item = self._data[row]
        print(item.xmin)

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            if column == 0: # ID
                return item.text

            elif column == 1: # tier
                return item.parent.name

            elif column == 2: # Time
                return str(round(item.xmin, 2))

            elif column == 3: # Time
                return str(round(item.xmax, 2))
    
            #elif column == 4:
                #return item.parent.parent.path.name

            # elif column in (2, 3, 4): # Documento
                # last_doc = dict_['documents'][-1]
                # if column == 2:
                    # return last_doc[0] # Título del documento
                # if column == 3:
                    # return QDate.fromString(last_doc[1], 'yyyy-MM-dd') # Fecha de documento
                # if column == 4:
                    # return last_doc[2] # Expediente

            # elif column == 5: # Estado
                # return dict_['status']

            # elif column == 6: # Dependencia
                # return dict_['office']

        # elif role == Qt.ItemDataRole.DecorationRole:
            # if column == 0:
                # status = dict_['status']
                # if status == 0:
                    # return QIcon(str(icons_dir / 'disc-blue-new.png'))
                # elif status == 1:
                    # return QIcon(str(icons_dir / 'disc-burn.png'))
                # elif status == 2:
                    # return QIcon(str(icons_dir / 'eye.png'))
                # elif status == 3:
                    # return QIcon(str(icons_dir / 'tick-button.png'))
                # elif status == -1:
                    # return QIcon(str(icons_dir / 'exclamation.png'))

            # elif column == 3:
                # date = index.data()
                # status = dict_['status']

                # if date == '':
                    # return QColor(255,255,255)

                # if status == 3:
                    # return QColor(255,255,255)

                # diff = date.daysTo(QDate.currentDate())
                # if diff > 30:
                    # return QColor(255,0,0) # red
                # elif diff > 20:
                    # return QColor(255,255,51) # yellow
                # else:
                    # return QColor(173,255,47) # green
            # return

        # elif role == Qt.ItemDataRole.UserRole:
            # return dict_['_file_path'].parent

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        # if role != Qt.ItemDataRole.EditRole:
            # return

        # column, row = index.column(), index.row()
        #   'ID', 'Responsable', 'Documento', 'Fecha', 'Expediente'
        # if column == 1: # Authors
            # self._data[row]['authors'] = value.split(';')
            # self.save(row)
            # return True

        # if column == 2: # Doc title
            # self._data[row]['documents'][-1][0] = value
            # self.save(row)
            # return True

        # if column == 3: #Date
            # self._data[row]['documents'][-1][1] = value.toString('yyyy-MM-dd')
            # self.save(row)
            # return True

        # if column == 4: # Doc id
            # self._data[row]['documents'][-1][2] = value
            # self.save(row)
            # return True

        # elif column == 5:
            # self._data[row]['status'] = int(value)
            # self.save(row)
            # return True

        # elif column == 6:
            # self._data[row]['office'] = value
            # self.save(row)
            # return True
        # return False
        pass

    def append_data(self, dict_):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(dict_)
        row = len(self._data) - 1
        self.save(row)
        self.endInsertRows()

    def flags(self, index=QModelIndex()):
        myflags = Qt.ItemFlag.ItemIsSelectable|Qt.ItemFlag.ItemIsEnabled 
        if index.column():
            return myflags|Qt.ItemFlag.ItemIsEditable
        return myflags

    def refresh_library(self):
        if self.location is None:
            return
        self.beginResetModel()
        data = self.scan_library()
        self.endResetModel()

    def data_collection(self):
        return self._data

    def save(self, row):
        # dict_ = self._data[row]
        # file_path = dict_['_file_path']
        # newdict = {k:v for k, v in dict_.items() if not k.startswith('_')}

        # with open(file_path, 'w', encoding='utf-8') as f:
            # json.dump(newdict, f, ensure_ascii=False, indent=4)
        pass


from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QStyleFactory, QDialog, QFileDialog, QGroupBox, QHBoxLayout,\
    QPushButton, QVBoxLayout, QLabel, QLineEdit, QRadioButton, QMessageBox,\
    QGridLayout, QCheckBox
from PyQt6.QtCore import Qt

import configparser
import class_exception
import database.class_data as class_data
import config as cfg
import os
import database.class_convert_BDGD as class_convert_BDGD
import fiona


class C_ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "Insira uma Base de Dados Geográfica da Distribuidora (BDGD)"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.setMinimumSize(640,100)

        self.databaseInfo = {}

        self.dadosBDGD = class_data.dadosBDGD()

        self.InitUI()

    def InitUI(self):

        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface
        self.adjustSize()


        self.Dialog_Layout = QVBoxLayout() #Layout da Dialog

        #### Grupo do BDGD
        self.GroupBox_BDGD = QGroupBox("Conexão Local")
        self.GroupBox_BDGD_Layout = QHBoxLayout()

        self.GroupBox_BDGD_Label = QLabel("Diretório:")
        self.GroupBox_BDGD_Layout.addWidget(self.GroupBox_BDGD_Label)
        self.GroupBox_BDGD_Edit = QLineEdit()
        self.GroupBox_BDGD_Edit.setMinimumWidth(300)
        self.GroupBox_BDGD_Edit.setEnabled(False)
        self.GroupBox_BDGD_Layout.addWidget(self.GroupBox_BDGD_Edit)

        self.GroupBox_BDGD_Btn = QPushButton()
        self.GroupBox_BDGD_Btn.setIcon(QIcon('img/icon_opendatabase.png'))
        self.GroupBox_BDGD_Btn.setFixedWidth(30)
        self.GroupBox_BDGD_Btn.clicked.connect(self.OpenDataBase)
        self.GroupBox_BDGD_Layout.addWidget(self.GroupBox_BDGD_Btn)

        self.GroupBox_BDGD.setLayout(self.GroupBox_BDGD_Layout)
        self.Dialog_Layout.addWidget(self.GroupBox_BDGD)


        ###### Botões
        self.Dilalog_Btns_Layout = QHBoxLayout()
        self.Dilalog_Btns_Layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.Dilalog_Btns_Save_Btn = QPushButton("Salvar Parâmetros")
        self.Dilalog_Btns_Save_Btn.setIcon(QIcon('img/icon_save.png'))
        self.Dilalog_Btns_Save_Btn.setFixedWidth(170)
        self.Dilalog_Btns_Save_Btn.clicked.connect(self.saveDefaultParameters)
        self.Dilalog_Btns_Layout.addWidget(self.Dilalog_Btns_Save_Btn)

        self.Dilalog_Btns_Cancel_Btn = QPushButton("Cancelar")
        self.Dilalog_Btns_Cancel_Btn.setIcon(QIcon('img/icon_cancel.png'))
        self.Dilalog_Btns_Cancel_Btn.setFixedWidth(100)
        self.Dilalog_Btns_Cancel_Btn.clicked.connect(self.reject)
        self.Dilalog_Btns_Layout.addWidget(self.Dilalog_Btns_Cancel_Btn)

        self.Dilalog_Btns_Ok_Btn = QPushButton("OK")
        self.Dilalog_Btns_Ok_Btn.setIcon(QIcon('img/icon_ok.png'))
        self.Dilalog_Btns_Ok_Btn.setFixedWidth(100)
        self.Dilalog_Btns_Ok_Btn.clicked.connect(self.Accept)
        self.Dilalog_Btns_Layout.addWidget(self.Dilalog_Btns_Ok_Btn)

        self.Dialog_Layout.addLayout(self.Dilalog_Btns_Layout, 0)
        self.setLayout(self.Dialog_Layout)

        ####
        self.loadDefaultParameters()

    def Accept(self):
        Conversor: class_convert_BDGD.ConnectorInterfaceConversor
        self.loadParameters()
        if self.databaseInfo["Sqlite_DirDataBase"]:
            self.close()

        else:
            self.CONVERSOR = class_convert_BDGD.ConnectorInterfaceConversor(self)
            self.CONVERSOR.DataBaseInfo = self.databaseInfo
            self.CONVERSOR.initUI()

    def loadParameters(self):
        directory_database: str = self.GroupBox_BDGD_Edit.text()

        ## Geral
        if directory_database:
            self.databaseInfo["Modelo"] = self.modelo_database(directory_database)
            self.databaseInfo['versao'] = self.get_versao_database(self.databaseInfo["Modelo"])
            if self.checkDirDataBase(directory_database):
                self.get_directories(directory_database)


    def get_directories(self, directory_database: str) -> None:
        match self.tipo_database(directory_database):
            case '.gdb':
                self.databaseInfo["Geodb_DirDataBase"] = directory_database
                self.databaseInfo["Sqlite_DirDataBase"] = ''
            case '.gdb.sqlite':
                path_sqlite_convertido = os.path.join(directory_database,
                                                      "SIPLA_" + os.path.basename(directory_database) + '.sqlite')

                self.databaseInfo["Geodb_DirDataBase"] = ''
                self.databaseInfo["Sqlite_DirDataBase"] = path_sqlite_convertido
            case '.sqlite':
                self.databaseInfo["Geodb_DirDataBase"] = ''
                self.databaseInfo["Sqlite_DirDataBase"] = directory_database

    def get_versao_database(self, Modelo: str) -> str:
        match Modelo:
            case "Modelo Versao 1.0":
                return "2021"
            case "Modelo Novo":
                return "2017"
            case "Modelo Antigo":
                return "2016"

    def loadDefaultParameters(self):  # Só carrega quando abre a janela pela primeira vez
        try:
            config = configparser.ConfigParser()
            config.read('siplaconfigdatabase.ini')
            print(config['Sqlite']['dir'])
            if os.path.isdir(config['Sqlite']['dir']):
                print("1")
                if self.checkDirDataBase(config['Sqlite']['dir']):
                    self.GroupBox_BDGD_Edit.setText(config['Sqlite']['dir'])
            elif os.path.isdir(config['Geodb']['dir']):
                print("2")
                if self.checkDirDataBase(config['Geodb']['dir']):
                    self.GroupBox_BDGD_Edit.setText(config['Geodb']['dir'])
            else:
                print("3")
                self.GroupBox_BDGD_Edit.clear()

            ##### Carregando parâmetros
            self.loadParameters()
        except:
            raise class_exception.FileDataBaseError("Configuração do Banco de Dados",
                                                    "Erro ao carregar os parâmetros do Banco de Dados!")

    def saveDefaultParameters(self):
        try:
            self.loadParameters()

            if not self.databaseInfo["Sqlite_DirDataBase"]:
                QMessageBox(QMessageBox.Icon.Information, "DataBase Configuration",
                            "Não foi possível salvar o diretório do BDGD: \n"
                            + "Primeiro, é necessário converter o BDGD para o formato apropriado.\n"
                            + "Pressione OK na tela de inserção do BDGD para iniciar a conversão!",
                            QMessageBox.StandardButton.Ok).exec()
                return

            config = configparser.ConfigParser()

            ## Load Flow
            config['BDGD']= { }
            config['BDGD']['Modelo'] = self.databaseInfo["Modelo"]
            config['BDGD']['versao'] = self.databaseInfo["versao"]

            config['Sqlite'] = {}
            config['Sqlite']['dir'] = self.databaseInfo["Sqlite_DirDataBase"]

            config['Geodb'] = {}
            config['Geodb']['dir'] = self.databaseInfo['Geodb_DirDataBase']


            with open('siplaconfigdatabase.ini', 'w') as configfile:
                config.write(configfile)

            QMessageBox(QMessageBox.Icon.Information, "DataBase Configuration", "Configurações Salvas com Sucesso!",
                        QMessageBox.StandardButton.Ok).exec()

        except:
            raise class_exception.FileDataBaseError("Configuração do Banco de Dados", "Erro ao salvar os parâmetros\
                                                    do Banco de Dados!")

    def OpenDataBase(self):
        nameDirDataBase = str(
            QFileDialog.getExistingDirectory(None, "Selecione o Diretório com o Danco de Dados", "Banco/",
                                             QFileDialog.Option.ShowDirsOnly))

        self.GroupBox_BDGD_Edit.setText(nameDirDataBase)

        if self.checkDirDataBase(nameDirDataBase):
            self.GroupBox_BDGD_Edit.setText(nameDirDataBase)
        else:
            self.GroupBox_BDGD_Edit.setText("")

    def checkDirDataBase(self, directory_database:str) -> bool:
        """
        Verifica e lista se todas
        as layers necessárias estão presentes no diretório de acordo com a respectiva versão.
        :param directory_database:
        :return True or False:
        """
        modelo_database = self.modelo_database(directory_database)
        if modelo_database == 'Modelo nao identificado':
            QMessageBox(QMessageBox.Icon.Warning, "DataBase Configuration",
                        "Não foi possível identificar o modelo do BDGD pela falta de uma das seguintes layers: \n"
                        + "    -> UNTRMT\n    -> UNTRD\n    -> UN_TR_D",
                        QMessageBox.StandardButton.Ok).exec()
            return False

        layers_necessarias = self.dadosBDGD.get_layers_uteis_BDGD(modelo_database)
        layers_ausentes = []


        match self.tipo_database(directory_database):
            case '.gdb':
                layers_presentes_geodb = fiona.listlayers(directory_database)

                for layer in layers_necessarias:
                    if layer not in layers_presentes_geodb:
                        layers_ausentes.append(layer)

            case '.gdb.sqlite':
                path_sqlite_convertido = os.path.join(directory_database, "SIPLA_" +
                                                      os.path.basename(directory_database) + '.sqlite')

                for layer in layers_necessarias:
                    if layer.endswith("_tab"):
                        layer = layer[:-4]
                    if not os.path.isfile(path_sqlite_convertido + "//" + layer + ".sqlite"):
                        layers_ausentes.append(layer)

            case '.sqlite':
                for layer in layers_necessarias:
                    if layer.endswith("_tab"):
                        layer = layer[:-4]
                    if not os.path.isfile(directory_database + "//" + layer + ".sqlite"):
                        layers_ausentes.append(layer)

        if layers_ausentes:
            QMessageBox(QMessageBox.Icon.Warning, "DataBase Configuration",
                        "O banco de dados não possui os seguintes layers : \n" + str(layers_ausentes),
                        QMessageBox.StandardButton.Ok).exec()
            return False
        else:
            return True

    def modelo_database(self, directory_database):
        match self.tipo_database(directory_database):
            case '.gdb':
                layers_presentes_geodb = fiona.listlayers(directory_database)
                print('ok1')
                if "UNTRMT" in layers_presentes_geodb:
                    return "Modelo Versao 1.0"
                elif "UNTRD" in layers_presentes_geodb:
                    return "Modelo Novo"
                elif "UN_TR_D" in layers_presentes_geodb:
                    return "Modelo Antigo"
            case '.gdb.sqlite':
                path_sqlite_convertido = os.path.join(directory_database, "SIPLA_" +
                                                      os.path.basename(directory_database) + '.sqlite')
                print('ok2')

                if os.path.isfile(os.path.join(path_sqlite_convertido, "UNTRMT" + ".sqlite")):
                    return "Modelo Versao 1.0"
                elif os.path.isfile(os.path.join(path_sqlite_convertido, "UNTRD" + ".sqlite")):
                    return "Modelo Novo"
                elif os.path.isfile(os.path.join(path_sqlite_convertido, "UN_TR_D" + ".sqlite")):
                    return "Modelo Antigo"
            case '.sqlite':
                print('ok3')

                if os.path.isfile(os.path.join(directory_database, "UNTRMT" + ".sqlite")):
                    return "Modelo Versao 1.0"
                elif os.path.isfile(os.path.join(directory_database, "UNTRD" + ".sqlite")):
                    return "Modelo Novo"
                elif os.path.isfile(os.path.join(directory_database, "UN_TR_D" + ".sqlite")):
                    return "Modelo Antigo"

        return 'Modelo nao identificado'

    def tipo_database(self, directory_database: str) -> str:
        # Instância de uma possível db em sqlite, resultado de uma conversão de um Geo Package
        path_sqlite_convertido = os.path.join(directory_database, "SIPLA_" +
                                              os.path.basename(directory_database) + '.sqlite')
        # Identifica se o diretório é uma BDGD em formato nativo Geo Package (Padrão Aneel) ou Pasta sqlite
        if directory_database.endswith('.gdb'):

            if os.path.isdir(path_sqlite_convertido):
                return '.gdb.sqlite'
            else:
                return '.gdb'

        else:
            return '.sqlite'

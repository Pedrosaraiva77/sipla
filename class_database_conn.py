from PyQt5.QtWidgets import QFileDialog
from class_exception import FileDataBaseError

from os import path
import platform
import sqlite3

class C_ConnDBase(): #Classe de banco de dados

    def __init__(self):
        super(C_ConnDBase, self).__init__()
        #Variáveis das Classes
        #Nome do Diretório
        self.dirDataBase = ""
        self.nameDataBase = ""
        #Todos dos Banco de Dados que serão necessários
        self.DBPRODIST = ["CTAT", "EQTRM", "SSDMT", "UNREMT", "UNTRS", "CTMT", "EQTRS", "UCBT", "UNSEAT", "EQSE", "RAMLIG", "UCMT", "UNSEMT", "EQTRD", "SEGCON", "UNCRMT", "UNCRBT", "UNTRD"]

    def setDirDataBase(self):

        if not self.dirDataBase:
            nameDirDataBase = str(QFileDialog.getExistingDirectory(None, "Selecione o Diretório com o Danco de Dados","Banco/", QFileDialog.ShowDirsOnly))
            nameDirDataBase += "/"
            if not self.setDefDirDataBase(nameDirDataBase):
                return False
            else:
                return True
        else:
            return True

    def getDirDataBase(self):
        return self.dirDataBase


    def setDefDirDataBase(self, nameDirDataBase):

        if not self.dirDataBase:

            if platform.system() == "Windows":
                nameDirDataBase = nameDirDataBase.replace('/', '\\')

            self.dirDataBase = nameDirDataBase

            if not self.checkDataBaseDados():
                self.dirDataBase = ""
                return False
            else:
                return True
        else:
            return True


    def getDirDataBase(self):
        return self.dirDataBase

    def checkDataBaseDados(self): #Verifica se todos os arquivos estão no Diretório selecionado

        try:
            for ctd in self.DBPRODIST:
                if not path.isfile(self.dirDataBase + ctd + ".sqlite"):
                    raise FileDataBaseError("BDGB não encontrado na pasta selecionada!","Arquivo " + ctd + ".sqlite ausente!")
                    return False
            return True

        except FileDataBaseError:
            pass


    def getSQLDB(self,nomeBancoDados,strSQL):

        #print('file:' + self.dirDataBase + nomeBancoDados + '.sqlite?mode=ro')

        try:
            #Conectando em apenas leitura!
            connDB =  sqlite3.connect('file:' + self.dirDataBase + nomeBancoDados + '.sqlite?mode=ro', uri=True)

            cbanco = connDB.execute(strSQL)

            # connDB.close()

            return cbanco

        except AttributeError:
            raise ConnDataBaseError("Erro de conexão no Banco de Dados:" + nomeBancoDados)

                
                

            
            

        
        
        
            
                

    

import os
import platform
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget
import cmath

import class_opendss_conn
import class_database_conn
import class_opendss_data
import class_exception


class C_OpenDSS(): # classe OpenDSSDirect

    def __init__(self):

        self.dataOpenDSS = class_opendss_data.C_OpenDSS_Data() #Acesso ao Banco de Dados

        self._DataBaseConn = class_database_conn.C_DBaseConn()  # Criando a instância do Banco de Dados

        self._nCircuitoAT_MT = ''
        self._nSE_MT_Selecionada = ''
        self._nFieldsMT = ''

        self._OpenDSSConn = ''

        self.tableVoltageResults = QTableWidget() # Tabela de Resultados

    @property
    def OpenDSSConn(self):
        return self._OpenDSSConn

    @OpenDSSConn.setter
    def OpenDSSConn(self, value):
        self._OpenDSSConn = value

    @property
    def DataBaseConn(self):
        return self._DataBaseConn

    @DataBaseConn.setter
    def DataBaseConn(self, value):
        self._DataBaseConn = value

    @property
    def nCircuitoAT_MT(self):
        return self._nCircuitoAT_MT

    @nCircuitoAT_MT.setter
    def nCircuitoAT_MT(self, value):
        self._nCircuitoAT_MT = value

    @property
    def nSE_MT_Selecionada(self):
        return self._nSE_MT_Selecionada

    @nSE_MT_Selecionada.setter
    def nSE_MT_Selecionada(self, value):
        self._nSE_MT_Selecionada = value

    @property
    def nFieldsMT(self):
        return self._nFieldsMT

    @nFieldsMT.setter
    def nFieldsMT(self, value):
        self._nFieldsMT = value


    def loadData(self):

        ### Passando as variáveis
        self.dataOpenDSS.DataBaseConn = self.DataBaseConn

        self.dataOpenDSS.nFieldsMT = self.nFieldsMT
        self.dataOpenDSS.nCircuitoAT_MT = self.nCircuitoAT_MT
        self.dataOpenDSS.nSE_MT_Selecionada = self.nSE_MT_Selecionada

        ######## Define o Engine do OpenDSS
        try:
            if self.OpenDSSConn == "OpenDSSDirect":
                self.OpenDSSEngine = class_opendss_conn.C_OpenDSSDirect_Conn()
            elif self.OpenDSSConn == "COM":
                self.OpenDSSEngine = class_opendss_conn.C_OpenDSSCOM_Conn()
            else:
                raise class_exception.ExecOpenDSS("Erro ao definir o Engine do OpenDSS!")
        except:
            pass



    ##########
       # self.OpenDSS_Progress_Dialog = C_OpenDSS_ExecDialog()


        ##### Executa os Arquitvos que serão executados e inseridos

        self.execOpenDSSFunc = {"header": ["Cabeçalho ...", self.dataOpenDSS.exec_HeaderFile],
                      "EqThAT": ["Equivalente de Thevenin ...", self.dataOpenDSS.exec_EQUIVALENTE_DE_THEVENIN],
                      # "EqThMT":["Equivalente de Thevenin MT...",self.dataOpenDSS.exec_EQUIVALENTE_DE_THEVENIN_MEDIA],
                      "SecEqThAT_SecAT": ["Chaves entre o Equivalente e a SecAT ...", self.dataOpenDSS.exec_SEC_EQTHAT_SECAT],
                      "TrafoATMT": ["Trafo AT - MT...", self.dataOpenDSS.exec_TRANSFORMADORES_DE_ALTA_PARA_MEDIA],
                      "CondMT": ["Condutores MT...", self.dataOpenDSS.exec_CONDUTORES_DE_MEDIA_TENSAO],
                      # "CondBT":["Condutores de BT...",self.dataOpenDSS.exec_CONDUTORES_DE_BAIXA_TENSAO],
                      #"CondRamais": ["Condutores de Ramais ...", self.dataOpenDSS.exec_CONDUTORES_DE_RAMAL],
                      "SecAT": ["Seccionadoras de AT...", self.dataOpenDSS.exec_SEC_DE_ALTA_TENSAO],
                      "SecATControl": ["Controle Seccionadoras de AT...",self.dataOpenDSS.exec_CONTROLE_SEC_DE_ALTA_TENSAO],
                      "SecOleoMT": ["Chave a óleo de MT ...", self.dataOpenDSS.exec_SEC_CHAVE_A_OLEO_DE_MEDIA_TENSAO],
                      "SecOleoMTControl": ["Controle Chave a óleo de MT...",self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_A_OLEO_DE_MEDIA_TENSAO],
                      "SecFacaMT": ["Chave Faca de MT ...", self.dataOpenDSS.exec_SEC_CHAVE_FACA_DE_MEDIA_TENSAO],
                      "SecFacaMTControl": ["Controle Chave Faca de MT ...",self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_FACA_DE_MEDIA_TENSAO],
                      "SecTripolarMT": ["Chave Faca Tripolar de MT ...",self.dataOpenDSS.exec_SEC_CHAVE_FACA_TRIPOLAR_DE_MEDIA_TENSAO],
                      "SecTripolarMTControl": ["Controle Chave Faca Tripolar de MT ...",self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_FACA_TRIPOLAR_DE_MEDIA_TENSAO],
                      "ChFusMT": ["Chave Fusível de MT ...", self.dataOpenDSS.exec_SEC_CHAVE_FUSIVEL_DE_MEDIA_TENSAO],
                      "ChFusMTControl": ["Controle Chave Fusível de MT ...",self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_FUSIVEL_DE_MEDIA_TENSAO],
                      "DJMT": ["DJ de MT ...", self.dataOpenDSS.exec_SEC_CHAVE_DJ_RELE_DE_MEDIA_TENSAO],
                      "DJMTControl": ["Controle DJ de MT ...", self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_DJ_RELE_DE_MEDIA_TENSAO],
                      "ReligMT": ["Religador de MT ...", self.dataOpenDSS.exec_SEC_CHAVE_RELIGADOR_DE_MEDIA_TENSAO],
                      "ReligMTControl": ["Controle do Religador de MT ...",self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_RELIGADOR_DE_MEDIA_TENSAO],
                      "ChTripolarSEMT": ["Chave Tripolar da SE MT ...",self.dataOpenDSS.exec_SEC_CHAVE_TRIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO],
                      "ChTripolarSEMTControl": ["Controle Chave Tripolar da SE MT ...",self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_TRIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO],
                      "ChUnipolarSEMT": ["Chave Unipolar da SE MT ...",self.dataOpenDSS.exec_SEC_CHAVE_UNIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO],
                      "ChUnipolarSEMTControl": ["Controle da Chave Unipolar da SE MT ...",self.dataOpenDSS.exec_CONTROLE_SEC_CHAVE_UNIPOLAR_SUBESTACAO_DE_MEDIA_TENSAO],
                      # ObsSandy1             #"Reg":["Regulador MT ...",self.dataOpenDSS.exec_REGULADORES_DE_MEDIA_TENSAO],
                      "SegMT": ["Segmentos de Linhas MT ...", self.dataOpenDSS.exec_SEG_LINHAS_DE_MEDIA_TENSAO],
                      "UConMT": ["Unidades Consumidoras MT ...", self.dataOpenDSS.exec_UNID_CONSUMIDORAS_MT],
                      # ObsSandy2            #"TrafoDist":["Trafos de Distribuição ...",self.dataOpenDSS.exec_TRANSFORMADORES_DE_DISTRIBUICAO],
                      # "SegBT":["Segmentos de Linhas BT ...",self.dataOpenDSS.exec_SEG_LINHAS_DE_BAIXA_TENSAO],
                      # "UConBT":["Unidades Consumidoras BT ...",self.dataOpenDSS.exec_UNID_CONSUMIDORAS_BT],
                      # "RamLig":["Ramais de Ligação  ...",self.dataOpenDSS.exec_RAMAL_DE_LIGACAO,self.dataOpenDSS.memoFileRamaisLigBT],
                      "CompMT": ["Unidades Compensadoras de MT ...",self.dataOpenDSS.exec_UNID_COMPENSADORAS_DE_REATIVO_DE_MEDIA_TENSAO],
                      # "CompBT":["Unidades Compensadoras de BT ...",self.dataOpenDSS.exec_UNID_COMPENSADORAS_DE_REATIVO_DE_BAIXA_TENSAO],
                      "footer": ["Rodapé ...", self.dataOpenDSS.exec_FooterFile],
                      }


       # self.OpenDSS_Progress_Dialog.progBar.setMaximum(len(self.execFunc))

        #self.OpenDSS_Progress_Dialog.show()

        #ctdN = 0
        for ctd in self.execOpenDSSFunc:
            msg = self.execOpenDSSFunc[ctd][-2]
            #Executando a função
            self.execOpenDSSFunc[ctd][-1]()

        #   ctdN += 1
        #    self.OpenDSS_Progress_Dialog.Info_GroupBox_MsgLabel.setText(msg)
       #     self.OpenDSS_Progress_Dialog.progBar.setValue(ctdN)
       #     print(self.OpenDSS_Progress_Dialog.progBar.value())
            #self.OpenDSS_Progress_Dialog.close()


        self.OpenDSSDataResult = {"header": self.dataOpenDSS.memoFileHeader,
                      "EqThAT": self.dataOpenDSS.memoFileEqTh,
                      # "EqThMT":self.dataOpenDSS.memoFileEqThMT,
                      "SecEqThAT_SecAT": self.dataOpenDSS.memoFileSecAT_EqThAT,
                      "TrafoATMT": self.dataOpenDSS.memoFileTrafoATMT,
                      "CondMT": self.dataOpenDSS.memoFileCondMT,
                      # "CondBT": self.dataOpenDSS.memoFileCondBT,
                      "CondRamais": self.dataOpenDSS.memoFileCondRamal,
                      "SecAT": self.dataOpenDSS.memoFileSecAT ,
                      "SecATControl":  self.dataOpenDSS.memoFileSecAT_Control,
                      "SecOleoMT": self.dataOpenDSS.memoFileSecOleoMT,
                      "SecOleoMTControl": self.dataOpenDSS.memoFileSecOleoMT_Control,
                      "SecFacaMT": self.dataOpenDSS.memoFileSecFacaMT,
                      "SecFacaMTControl": self.dataOpenDSS.memoFileSecFacaMT_Control,
                      "SecTripolarMT": self.dataOpenDSS.memoFileSecFacaTripolarMT,
                      "SecTripolarMTControl": self.dataOpenDSS.memoFileSecFacaTripolarMT_Control,
                      "ChFusMT":self.dataOpenDSS.memoFileSecFusivelMT,
                      "ChFusMTControl": self.dataOpenDSS.memoFileSecFusivelMT_Control,
                      "DJMT":self.dataOpenDSS.memoFileSecDJReleMT,
                      "DJMTControl": self.dataOpenDSS.memoFileSecDJReleMT_Control,
                      "ReligMT": self.dataOpenDSS.memoFileSecReligadorMT,
                      "ReligMTControl": self.dataOpenDSS.memoFileSecReligadorMT_Control,
                      "ChTripolarSEMT":self.dataOpenDSS.memoFileSecTripolarSEMT,
                      "ChTripolarSEMTControl": self.dataOpenDSS.memoFileSecTripolarSEMT_Control,
                      "ChUnipolarSEMT":self.dataOpenDSS.memoFileSecUnipolarSEMT,
                      "ChUnipolarSEMTControl": self.dataOpenDSS.memoFileSecUnipolarSEMT_Control ,
                      # ObsSandy1             #"Reg":self.dataOpenDSS.memoFileReguladorMT,
                      "SegMT":self.dataOpenDSS.memoFileSegLinhasMT,
                      "UConMT":self.dataOpenDSS.memoFileUniConsumidoraMT,
                      # ObsSandy2            #"TrafoDist":self.dataOpenDSS.memoFileTrafoDist,
                      # "SegBT":self.dataOpenDSS.memoFileSegLinhasBT,
                      # "UConBT":self.dataOpenDSS.memoFileUniConsumidoraBT,
                      # "RamLig":self.dataOpenDSS.memoFileRamaisLigBT,self.memoFileRamaisLigBT,
                      "CompMT": self.dataOpenDSS.memoFileUndCompReatMT,
                      # "CompBT":self.dataOpenDSS.memoFileUndCompReatBT,
                      "footer":self.memoFileFooter,
                      }


    def exec_SaveFileDialogDSS(self):

        arquivoSalvo = QFileDialog.getSaveFileName(None, "Save OpenDSS File", "Results/",
                                                            "DSS Files (*.dss)")[0]

        nome_do_arquivo_criado = os.path.basename(str(arquivoSalvo))

        diretorio = os.path.dirname(str(arquivoSalvo)) +  "/"

        if platform.system() == "Windows":
            diretorio = diretorio.replace('/', '\\')

        self.saveFileDSS(diretorio, nome_do_arquivo_criado, self.createMainFileDSS())


        for ctd in self.OpenDSSDataResult:
            redirectFile = ''
            if (ctd != "header") and (ctd != "EqThAT") and (ctd != "footer"):  # Cabeçalho do arquivo
                data = self.OpenDSSDataResult[ctd]
                for cont in data:
                    redirectFile += str(cont) + '\n'

            self.saveFileDSS(diretorio, ctd, redirectFile )


    def saveFileDSS(self, dirSave, nameMemo, dataMemo ): #Salvar em Arquivo
        arquivo = open(dirSave +  nameMemo + ".dss", 'w', encoding='utf-8')
        arquivo.writelines( dataMemo )
        arquivo.close()

    def createMainFileDSS(self): # Para salvar em arquivo

        mainFile = ''

        for ctd in self.execOpenDSSFunc:
            if (ctd == "header") or (ctd == "EqThAT") or (ctd == "footer"): # Cabeçalho do arquivo
                data = self.OpenDSSDataResult[ctd]
                for cont in data:
                    mainFile += str(cont) + '\n'
            else:
                mainFile += "! " + self.execOpenDSSFunc[ctd][-2] + "\n"
                mainFile += "Redirect " + ctd + ".dss "+'\n'

        #Falta o final do arquivo

        return mainFile

    def definedSettings(self, config):

        self.OpenDSSConn = config.openDSSConn

        self.memoFileFooter = self.dataOpenDSS.memoFileFooter
        self.memoFileFooter.append("set voltagebases = [" +  config.VoltageBase +  "]")
        self.memoFileFooter.append("calcv")
        self.memoFileFooter.append("set mode = direct")
        #self.memoFileFooter.append("set mode = " + config.VoltageBase + " stepsize = " +  config.StepSize + " number = " + config.Number)

        #Maxiterations: int
        #Maxcontroliter: int


    def exec_OpenDSS(self):

        for ctd in self.OpenDSSDataResult:

            command = self.OpenDSSDataResult[ctd]

            for com in command:
                self.OpenDSSEngine.run(com)

            self.OpenDSSEngine.run("Solve")

#            self.OpenDSSEngine.run("Show Voltage LN Nodes")
            self.getVoltageResults() ## Mostrando o resultado das tensões
        self.OpenDSSEngine.run("New energymeter.m1")
        self.OpenDSSEngine.run("Solve")
        self.OpenDSSEngine.run("Show Voltage LN Nodes")
        self.OpenDSSEngine.run("Show Meters")



    def getVoltageResults(self):

        busNames = self.OpenDSSEngine.Circuit_AllBusNames() ## Lista com nomes de todos os nós
        VoltagePhaseAPU = self.OpenDSSEngine.Circuit_AllNodeVmagPUByPhase(1) ## Lista com todas as tensões de LN da fase A em PU
        VoltagePhaseBPU = self.OpenDSSEngine.Circuit_AllNodeVmagPUByPhase(2) ## Lista com todas as tensões de LN da fase B em PU
        VoltagePhaseCPU = self.OpenDSSEngine.Circuit_AllNodeVmagPUByPhase(3) ## Lista com todas as tensões de LN da fase C em PU
        busVoltagesALL = self.OpenDSSEngine.Circuit_AllBusVolts() ## Lista com todas as tensões de LN da fase ABN complexa  em PU

        self.tableVoltageResults.setRowCount(len(busNames))

        for ctdBus in range(0, len(busNames)):
            ## Nome da Barra
            self.tableVoltageResults.setItem(ctdBus, 0, QTableWidgetItem( busNames[ctdBus] ))
        for ctdVoltage1 in range(0, len(VoltagePhaseAPU)):
            ##Tensão nodal fase A em pu
            self.tableVoltageResults.setItem(ctdVoltage1, 7, QTableWidgetItem(str(round(VoltagePhaseAPU[ctdVoltage1] , 5 ))))
        for ctdVoltage2 in range(0, len(VoltagePhaseBPU)):
            ##Tensão nodal fase B em pu
            self.tableVoltageResults.setItem(ctdVoltage2, 9, QTableWidgetItem(str(round(VoltagePhaseBPU[ctdVoltage2] , 5 ))))
        for ctdVoltage3 in range(0, len(VoltagePhaseCPU)):
            ##Tensão nodal fase C em pu
            self.tableVoltageResults.setItem(ctdVoltage3, 11, QTableWidgetItem(str(round(VoltagePhaseCPU[ctdVoltage3] , 5 ))))

        for ctdVoltageA in range(0, len(busVoltagesALL)):
            ## Tensões nodais fase A em V
            try:
                Va = complex(busVoltagesALL[ctdVoltageA], busVoltagesALL[ctdVoltageA+1])
                self.tableVoltageResults.setItem(ctdVoltageA, 1, QTableWidgetItem(str(round(abs(Va)/1000, 5))))
                self.tableVoltageResults.setItem(ctdVoltageA, 2, QTableWidgetItem(str(round((cmath.phase(Va) * 180 / cmath.pi) ,3 ))))
                self.tableVoltageResults.setItem(ctdVoltageA, 8, QTableWidgetItem(str(round((cmath.phase(Va) * 180 / cmath.pi), 3))))
            except:
                pass
        for ctdVoltageB in range(0, len(busVoltagesALL)):
            ## Tensões nodais fase B em V
            try:
                Vb = complex(busVoltagesALL[ctdVoltageB+2], busVoltagesALL[ctdVoltageB+3])
                self.tableVoltageResults.setItem(ctdVoltageB, 3, QTableWidgetItem(str(round(abs(Vb)/1000 , 5))))
                self.tableVoltageResults.setItem(ctdVoltageB, 4, QTableWidgetItem(str(round( cmath.phase(Vb) * 180 / cmath.pi , 3))))
                self.tableVoltageResults.setItem(ctdVoltageB, 10, QTableWidgetItem(str(round( cmath.phase(Vb) * 180 / cmath.pi, 3))))
            except:
                pass
        for ctdVoltageC in range(0, len(busVoltagesALL)):
            ## Tensões nodais fase C em V
            try:
                Vc = complex(busVoltagesALL[ctdVoltageC+4], busVoltagesALL[ctdVoltageC+5])
                self.tableVoltageResults.setItem(ctdVoltageC, 5, QTableWidgetItem(str(round(abs(Vc)/1000 , 5))))
                self.tableVoltageResults.setItem(ctdVoltageC, 6, QTableWidgetItem(str(round((cmath.phase(Vc) * 180 / cmath.pi),3))))
                self.tableVoltageResults.setItem(ctdVoltageC, 12, QTableWidgetItem(str(round((cmath.phase(Vc) * 180 / cmath.pi), 3))))
            except:
                pass


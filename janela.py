from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtGui import QClipboard
import sys
import traceback
from api import api

class janelaMain(QMainWindow):
    def __init__(self):
        super(janelaMain, self).__init__()
        self.loader = QUiLoader()
        self.ui = self.loader.load('janela.ui')
        self.ui.show()

        # Alterando nome da janela
        self.ui.setWindowTitle('OS externas - KMD')

        # Fixando tamanho da janela
        self.ui.setFixedSize(460, 617)

        # ligando os widgets de entrada
        self.botaoIncluir = self.ui.botaoInclusao
        self.numeroNFS = self.ui.numeroNFS
        self.placaNFS = self.ui.placaNFS
        self.serieNFS = self.ui.serieNFS
        self.funcionarioNFS = self.ui.funcionarioNFS
        self.cnpjNFS = self.ui.cnpjNFS
        self.dataNFS = self.ui.dataNFS
        self.valorTotalNFS = self.ui.valorTotalNFS
        self.procedimento0 = self.ui.procedimento0
        self.valorProc0 = self.ui.valorProc0
        self.quantidade0 = self.ui.quantidade0
        self.conjunto = self.ui.dataOS
        self.obsProcedimento0 = self.ui.obsProcedimento0
        self.obsProcedimento1 = self.ui.obsProcedimento1
        self.obsProcedimento2 = self.ui.obsProcedimento2
        self.procedimento1 = self.ui.procedimento1
        self.procedimento2 = self.ui.procedimento2
        self.valorProc1 = self.ui.valorProc1
        self.valorProc2 = self.ui.valorProc2
        self.quantidade1 = self.ui.quantidade1
        self.quantidade2 = self.ui.quantidade2

        # Criar widget para exibir erro
        self.erro = QTextEdit(self)
        self.erro.setGeometry(10, 520, 440, 80)
        self.erro.setReadOnly(True)

        # Desativar o botão incluir inicialmente
        self.botaoIncluir.setEnabled(False)

        # Conectar os campos ao método que ativa/desativa o botão (campos que precisam estar preenchidos)
        self.numeroNFS.textChanged.connect(self.verificar_campos)
        self.placaNFS.textChanged.connect(self.verificar_campos)
        self.serieNFS.textChanged.connect(self.verificar_campos)
        self.funcionarioNFS.textChanged.connect(self.verificar_campos)
        self.cnpjNFS.textChanged.connect(self.verificar_campos)
        self.dataNFS.textChanged.connect(self.verificar_campos)
        self.valorTotalNFS.textChanged.connect(self.verificar_campos)
        self.procedimento0.textChanged.connect(self.verificar_campos)
        self.obsProcedimento0.textChanged.connect(self.verificar_campos)
        self.valorProc0.textChanged.connect(self.verificar_campos)
        self.quantidade0.textChanged.connect(self.verificar_campos)
        self.conjunto.textChanged.connect(self.verificar_campos)
        self.obsProcedimento1.textChanged.connect(self.verificar_campos)
        self.obsProcedimento2.textChanged.connect(self.verificar_campos)
        self.procedimento1.textChanged.connect(self.verificar_campos)
        self.procedimento2.textChanged.connect(self.verificar_campos)
        self.valorProc1.textChanged.connect(self.verificar_campos)
        self.valorProc2.textChanged.connect(self.verificar_campos)
        self.quantidade1.textChanged.connect(self.verificar_campos)
        self.quantidade2.textChanged.connect(self.verificar_campos)

        # Modificando o estilo do botão incluir
        self.botaoIncluir.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #000000;
                border-radius: 12px;
                padding: 0px;
                font-size: 12px;
                width: 200px;
                height: 200px;
            }
            QPushButton:hover {
                background-color: #00BFFF;
            }
        """)

        # Conectando o botão à função de incluir
        self.botaoIncluir.clicked.connect(self.incluir)

    def verificar_campos(self):
        # Verifica se todos os campos obrigatórios estão preenchidos
        if (
            self.numeroNFS.text() and 
            self.placaNFS.text() and 
            self.serieNFS.text() and 
            self.funcionarioNFS.text() and 
            self.cnpjNFS.text() and 
            self.dataNFS.text() and 
            self.valorTotalNFS.text() and 
            self.procedimento0.text() and 
            self.valorProc0.text() and
            self.quantidade0.text() and
            self.conjunto.text()
        ):
            # Ativar botão se todos os campos estiverem preenchidos
            self.botaoIncluir.setEnabled(True)
        else:
            # Desativar botão se algum campo estiver vazio
            self.botaoIncluir.setEnabled(False)


    def incluir(self):
        try:
            print("Iniciando a inclusão...")

            # Guardar os dados em variáveis
            numero_NFS = self.ui.numeroNFS.text()
            placa = self.ui.placaNFS.text().upper()
            serie = self.ui.serieNFS.text()
            funcionario = self.ui.funcionarioNFS.text()
            cnpj = self.ui.cnpjNFS.text()
            dataNFS = self.ui.dataNFS.text()
            valorTotal = self.ui.valorTotalNFS.text().replace(',', '.')
            procedimento0 = self.ui.procedimento0.text().upper()
            valorprocedimento0 = self.ui.valorProc0.text()
            obsProcedimento0 = self.ui.obsProcedimento0.toPlainText()
            quantidade0 = self.ui.quantidade0.text()
            conjunto = self.ui.dataOS.text()
            obsProcedimento1 = self.ui.obsProcedimento1.toPlainText().upper() 
            obsProcedimento2 = self.ui.obsProcedimento2.toPlainText().upper() 
            procedimento1 = self.ui.procedimento1.text().upper()
            procedimento2 = self.ui.procedimento2.text().upper()
            valorprocedimento1 = self.ui.valorProc1.text()
            valorprocedimento2 = self.ui.valorProc2.text()
            quantidade1 = self.ui.quantidade1.text()
            quantidade2 = self.ui.quantidade2.text()

            funcionarioCopy = f"SELECT NOMFUN FROM OSEFUN WHERE CODFUN = {funcionario}"
            funcionarioCopy = api('GET', funcionarioCopy)
            funcionarioCopy = funcionarioCopy[0]['NOMFUN']

            ordemDeServico = f"SELECT MAX(CODORD) + 1 FROM OSEORD WHERE CODFIL = 1"
            ordemDeServico = api('GET', ordemDeServico)
            ordemDeServico = ordemDeServico[0]['']

            # Se chegar até aqui, a inclusão deu certo, agora vamos copiar os dados pro clipboard
            dados = f"""
            OS: {ordemDeServico}(1)
            Placa: {placa}
            Autorizado por: {funcionarioCopy}
            """

            # Acessa o clipboard e copia os dados
            clipboard = QApplication.clipboard()
            clipboard.setText(dados)

            dataNFS = dataNFS.split('/')
            dataNFS = f"{dataNFS[2]}-{dataNFS[1]}-{dataNFS[0]}"

            # Formatação do CNPJ
            cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
            print(f"CNPJ formatado: {cnpj}")
            if len(cnpj) == 14:
                cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
            else:
                self.erro.setText("Erro: CNPJ inválido.")
                return

            print(f"CNPJ formatado: {cnpj_formatado}")

            # Consulta do fornecedor usando o CNPJ formatado
            consulta = f"SELECT CODCLIFOR FROM RODCLI WHERE CODCGC = '{cnpj_formatado}'"
            print(f"Consulta SQL: {consulta}")
            try:
                resultado = api('GET', consulta)
                print(f"Resultado da consulta: {resultado}")
            except Exception as e:
                print(f"Erro ao consultar API: {e}")
                self.erro.setText(f"Erro ao consultar API: {e}")
                return

            if len(resultado) == 0:
                self.erro.setText("Erro: Nenhum fornecedor encontrado.")
                return
            codforn = resultado[0]['CODCLIFOR']
            print(f"CODCLIFOR: {codforn}")

            # Try para capturar erros na hora de executar as procs
            try:
                # Inserção da Ordem de Serviço
                query_OS = f"""
                    EXEC SP_InsertOS 
                    @CODCLIFOR = {codforn}, 
                    @SERIE = '{serie}', 
                    @NUMDOC = '{numero_NFS}', 
                    @VLRDOC = {valorTotal}, 
                    @CODFUN = {funcionario}, 
                    @VALORTOTAL = {valorTotal}, 
                    @PLACA = '{placa}', 
                    @PROCE = '{procedimento0}', 
                    @QUANTI = {quantidade0}, 
                    @VLRUNI = {valorprocedimento0},
                    @DATA = '{dataNFS}',
                    @DATANFS = '{dataNFS}',
                    @CODCON = {conjunto}
                """
                print(f"Query OS: {query_OS}")
                api('POST', query_OS)
                # Verifica se o procedimento0 é um procedimento existente
                # Se for, não cria um novo procedimento,  e sim insere o procedimento na Ordem de Serviço
                if procedimento0 == ['SERVICOS GERAIS', 'SERVICOS DE GUINCHO', 'SERVIÇO DE SOLDA', 'SERVIÇO DE HIGIENIZAÇÃO', 'SERVIÇO ELÉTRICO', 'RECARGA DE GÁS', 'TROCA DE ÓLEO', 'RECARGA DE GÁS COM ÓLEO']:
                    query_ProceOS = f"""
                    EXEC SP_InsertProceOS
                    @VLRUNI = {valorprocedimento0},
                    @QUANTI = {quantidade0},
                    @PROCE = '{procedimento0}',
                    @OBSERV = '{obsProcedimento0}'
                    """
                    print(f"Query ProceOS: {query_ProceOS}")
                    api('POST', query_ProceOS)
                else:
                    # Cria o procedimento caso não exista
                    print("Iniciando inserção do procedimento principal...")
                    query_Proce = f"""
                    EXEC SP_InsertProce
                    @PROCE = '{procedimento0}',
                    @VLRUNI = {valorprocedimento0}
                    """
                    print(f"Query Proce: {query_Proce}")
                    api('POST', query_Proce)

                    # Coloca o procedimento na ordem de serviço
                    query_ProceOS = f"""
                    EXEC SP_InsertProceOS
                    @VLRUNI = {valorprocedimento0},
                    @QUANTI = {quantidade0},
                    @PROCE = '{procedimento0}',
                    @OBSERV = '{obsProcedimento0}'
                    """
                    print(f"Query ProceOS: {query_ProceOS}")
                    api('POST', query_ProceOS)

                # Procedimento1 e Procedimento2 (se preenchidos)
                if procedimento1 and valorprocedimento1 and quantidade1:
                    if procedimento1 in ['SERVICOS GERAIS', 'SERVICOS DE GUINCHO', 'SERVIÇO DE SOLDA', 'SERVIÇO DE HIGIENIZAÇÃO', 'SERVIÇO ELÉTRICO', 'RECARGA DE GÁS', 'TROCA DE ÓLEO', 'RECARGA DE GÁS COM ÓLEO']:
                        # Após verificar se o procedimento existe, insere o procedimento na Ordem de Serviço
                        query_ProceOS1_exist = f"""
                        EXEC SP_InsertProceOS
                        @VLRUNI = {valorprocedimento1},
                        @QUANTI = {quantidade1},
                        @PROCE = '{procedimento1}',
                        @OBSERV = '{obsProcedimento1}'
                        """
                        print(f"Query ProceOS: {query_ProceOS1_exist}")
                        api('POST', query_ProceOS1_exist)
                        print("Iniciando inserção do procedimento 1...")
                    else:
                        # Cria o procedimento caso não exista
                        query_Proce1 = f"""
                        EXEC SP_InsertProce
                        @PROCE = '{procedimento1}',
                        @VLRUNI = {valorprocedimento1}
                        """
                        print(f"Query Proce 1: {query_Proce1}")
                        api('POST', query_Proce1)

                        # Coloca o procedimento na ordem de serviço
                        query_ProceOS1 = f"""
                        EXEC SP_InsertProceOS
                        @VLRUNI = {valorprocedimento1},
                        @QUANTI = {quantidade1},
                        @PROCE = '{procedimento1}',
                        @OBSERV = '{obsProcedimento1}'
                        """
                        print(f"Query ProceOS 1: {query_ProceOS1}")
                        api('POST', query_ProceOS1)

                    if procedimento2 and valorprocedimento2 and quantidade2:
                        if procedimento2 in ['SERVICOS GERAIS', 'SERVICOS DE GUINCHO', 'SERVIÇO DE SOLDA', 'SERVIÇO DE HIGIENIZAÇÃO', 'SERVIÇO ELÉTRICO', 'RECARGA DE GÁS', 'TROCA DE ÓLEO', 'RECARGA DE GÁS COM ÓLEO']:
                          # Após verificar se o procedimento existe, insere o procedimento na Ordem de Serviço
                            query_ProceOS2_exist = f"""
                            EXEC SP_InsertProceOS
                            @VLRUNI = {valorprocedimento2},
                            @QUANTI = {quantidade2},
                            @PROCE = '{procedimento2}',
                            @OBSERV = '{obsProcedimento2}'
                            """
                            print(f"Query ProceOS: {query_ProceOS2_exist}")
                            api('POST', query_ProceOS2_exist)
                            print("Iniciando inserção do procedimento 1...")
                        else:
                            # Cria o procedimento caso não exista
                            print("Iniciando inserção do procedimento 2...")
                            query_Proce2 = f"""
                            EXEC SP_InsertProce
                            @PROCE = '{procedimento2}',
                            @VLRUNI = {valorprocedimento2}
                            """
                            print(f"Query Proce 2: {query_Proce2}")
                            api('POST', query_Proce2)

                            # Coloca o procedimento na ordem de serviço
                            query_ProceOS2 = f"""
                            EXEC SP_InsertProceOS
                            @VLRUNI = {valorprocedimento2},
                            @QUANTI = {quantidade2},
                            @PROCE = '{procedimento2}',
                            @OBSERV = '{obsProcedimento2}'
                            """
                            print(f"Query ProceOS 2: {query_ProceOS2}")
                            api('POST', query_ProceOS2)

            # Tratamento de exceções
            except Exception as e:
                error_message = f"Erro ao incluir o procedimento ou OS: {str(e)}\n{traceback.format_exc()}"
                print(error_message)
                self.erro.setText(error_message)
                return
        # Tratamento de exceções
        except Exception as e:
            error_message = f"Erro geral: {str(e)}\n{traceback.format_exc()}"
            print(error_message)
            self.erro.setText(error_message)

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    janela = janelaMain()
    sys.exit(app.exec())

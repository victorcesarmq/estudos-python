from ocorrencia import Ocorrencia
import pandas as pd
from pathlib import Path
from datetime import datetime
import json

class Registro():
    def __init__(self):
        self.arquivo = Path(__file__).parent / "dadosx" / "ocorrencias.json"
        self.ocorrencias = []

        if self.arquivo.exists() and self.arquivo.stat().st_size > 0:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                data_ocorrencias = json.load(f)

                for dados in data_ocorrencias:
                    oc = Ocorrencia()
                    oc.id = dados["Id"]
                    oc.tipo = dados["tipo"]
                    oc.local = dados["local"]
                    oc.status = dados["status"]
                    oc.descricao = dados["descricao"]
                    oc.data = datetime.strptime(dados["data"],"%d/%m/%Y %H:%M:%S")
                    self.ocorrencias.append(oc)

# ---------------------REGISTRA OCORRENCIA---------------------
    """
    Adiciona uma ocorrência ao registro e gera um ID automaticamente.
    A ocorrência recebida deve ter seus atributos preenchidos.
    """
    def adicionar(self, ocorrencia):
        ocorrencia.id = len(self.ocorrencias) + 1
        self.ocorrencias.append(ocorrencia)

# ---------------------LISTAR OCORRENCIAS---------------------
    """
    Retorna as ocorrências em formato DataFrame para geração de relatórios.
    """
    def listar(self):
        if not self.ocorrencias:
            print("Nenhuma ocorrência cadastrada.")
            return

        dados = []

        for oc in self.ocorrencias:
            dados.append({
                "Id": oc.id,
                "Tipo": oc.tipo,
                "Local": oc.local,
                "Descrição": oc.descricao,
                "Data": oc.data.strftime("%d/%m/%Y %H:%M:%S"),
                "Status": oc.status
            })
        df = pd.DataFrame(dados)
        return df

# ---------------------SALVAR OCORRENCIA---------------------
    """
    Salva todas as ocorrências no arquivo JSON.
    Deve ser chamada após adicionar() para persistir os dadosx.
    """
    def salvar(self):
        dados = []

        for oc in self.ocorrencias:
            dados.append({
                "Id": oc.id,
                "tipo": oc.tipo,
                "local": oc.local,
                "descricao": oc.descricao,
                "data": oc.data.strftime("%d/%m/%Y %H:%M:%S"),
                "status": oc.status
            })

        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
# ---------------------ENCERRAR OCORRENCIA---------------------
    def encerrar(self):
        while True:
            encerrar_id = int(input("ID da ocorrencia que deseja encerrar: "))
            encontrado = False
            for oc in self.ocorrencias:
                if oc.id == encerrar_id:
                    if oc.status == "Em andamento":
                        oc.status = "Concluído"
                        encontrado = True
                        self.salvar()
                        print("Ocorrencia Finalizada com sucesso!")
                        break
                    elif oc.status == "Concluído":
                        print("Ocorrencia ja concluida")
                        encontrado = True
            if not encontrado:
                print("Nenhuma ocorrência com esse ID")
            else: break
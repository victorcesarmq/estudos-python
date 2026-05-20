from ocorrencia import *
from datetime import datetime
import pandas as pd
import json
from pathlib import Path


class Registro():
    def __init__(self):
        self.arquivo = Path(__file__).parent / "dados" / "ocorrencias.json"
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
                    oc.data = datetime.strptime(
                        dados["data"],
                        "%d/%m/%Y %H:%M:%S"
                    )

                    self.ocorrencias.append(oc)

# ---------------------REGISTRA OCORRENCIA---------------------

    def adicionar(self, ocorrencia):
        ocorrencia.id = len(self.ocorrencias) + 1
        self.ocorrencias.append(ocorrencia)

# ---------------------LISTAR OCORRENCIAS---------------------

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
        print(df.to_string(index=False))

# ---------------------SALVAR OCORRENCIA---------------------

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
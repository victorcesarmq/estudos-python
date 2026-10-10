import os
import shutil

# Caminho da pasta original
pasta_origem = r"C:\Users\victo\AppData\Local\Potassium\workspace\Modules GB"
# Caminho da pasta onde os txts vão ficar organizados separadamente
pasta_destino = r"C:\Users\victo\AppData\Local\Potassium\workspace\Modules_TXT_Exportados"

contador = 0
for root, dirs, files in os.walk(pasta_origem):
    # Evita ler a própria pasta de destino se ela estiver dentro do mesmo diretório
    if pasta_destino in root:
        continue

    for file in files:
        if file.lower().endswith(".lua"):
            caminho_lua = os.path.join(root, file)

            # Descobre a estrutura relativa da pasta para replicar no destino
            rel_path = os.path.relpath(root, pasta_origem)
            target_dir = os.path.join(pasta_destino, rel_path)

            # Cria a pasta de destino se não existir
            os.makedirs(target_dir, exist_ok=True)

            # Define o caminho do novo arquivo .txt
            nome_txt = os.path.splitext(file)[0] + ".txt"
            caminho_txt = os.path.join(target_dir, nome_txt)

            # Copia o conteúdo do .lua para o novo .txt
            shutil.copy2(caminho_lua, caminho_txt)
            contador += 1

print(f"Sucesso! {contador} arquivos foram convertidos e salvos em: {pasta_destino}")
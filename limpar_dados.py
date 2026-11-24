"""
Limpeza e tratamento de dados com Python.

Lê um cadastro de clientes "bagunçado" (clientes_brutos.csv), corrige os
problemas mais comuns e gera:
  - clientes_limpos.csv   -> base pronta para análise
  - relatorio_qualidade.md -> o que estava errado e o que foi corrigido

Rodar:  python limpar_dados.py
"""
import csv
import re
import sys
from collections import Counter
from datetime import datetime

ENTRADA = "clientes_brutos.csv"
SAIDA = "clientes_limpos.csv"
RELATORIO = "relatorio_qualidade.md"

FORMATOS_DATA = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%Y", "%d/%m/%y", "%Y/%m/%d"]
UFS = {
    "SP": "SP", "SAO PAULO": "SP", "SÃO PAULO": "SP",
    "RJ": "RJ", "RIO DE JANEIRO": "RJ",
    "MG": "MG", "MINAS GERAIS": "MG", "MINAS": "MG",
    "PR": "PR", "PARANA": "PR", "PARANÁ": "PR",
}

problemas = Counter()  # conta cada tipo de correção feita


def limpar_nome(nome):
    nome = " ".join(nome.split())  # tira espaços extras
    if not nome:
        problemas["nome vazio"] += 1
        return None
    novo = nome.title()
    for palavra in (" De ", " Da ", " Do ", " Dos ", " Das ", " E "):
        novo = novo.replace(palavra, palavra.lower())
    if novo != nome:
        problemas["nome com maiúsculas/espaços errados"] += 1
    return novo


def limpar_email(email):
    email = email.strip().lower()
    if not email:
        problemas["e-mail vazio"] += 1
        return None
    if ".." in email or not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.]+", email):
        problemas["e-mail inválido"] += 1
        return None
    return email


def limpar_telefone(tel):
    digitos = re.sub(r"\D", "", tel)  # mantém só números
    if digitos.startswith("55") and len(digitos) in (12, 13):
        digitos = digitos[2:]  # remove o código do país
    if len(digitos) == 11:
        return f"({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}"
    if len(digitos) == 10:
        return f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
    problemas["telefone inválido ou vazio"] += 1
    return None


def limpar_data(texto):
    texto = texto.strip()
    for formato in FORMATOS_DATA:
        try:
            data = datetime.strptime(texto, formato).date()
            if formato != "%Y-%m-%d":
                problemas["data fora do padrão (convertida)"] += 1
            return data.isoformat()
        except ValueError:
            continue
    problemas["data inválida ou vazia"] += 1
    return None


def limpar_estado(uf):
    chave = uf.strip().upper()
    if chave in UFS:
        if chave != UFS[chave]:
            problemas["estado escrito por extenso (padronizado)"] += 1
        return UFS[chave]
    problemas["estado inválido ou vazio"] += 1
    return None


def limpar_valor(texto):
    """Converte 'R$ 1.234,56', '1234.56', '1,234' etc. em número."""
    t = texto.strip().replace("R$", "").replace(" ", "")
    if not t:
        problemas["valor vazio"] += 1
        return None
    if "," in t:  # formato brasileiro: 1.234,56
        t = t.replace(".", "").replace(",", ".")
    try:
        return round(float(t), 2)
    except ValueError:
        problemas["valor inválido"] += 1
        return None


def main():
    sys.stdout.reconfigure(encoding="utf-8")

    with open(ENTRADA, encoding="utf-8") as f:
        brutos = list(csv.DictReader(f))

    limpos, vistos = [], set()
    for linha in brutos:
        # Sem nome e sem e-mail não dá para identificar o cliente: descarta
        if not linha["nome"].strip() and not linha["email"].strip():
            problemas["linha descartada (sem nome e e-mail)"] += 1
            continue
        cliente = {
            "nome": limpar_nome(linha["nome"]),
            "email": limpar_email(linha["email"]),
            "telefone": limpar_telefone(linha["telefone"]),
            "data_cadastro": limpar_data(linha["data_cadastro"]),
            "estado": limpar_estado(linha["estado"]),
            "valor_gasto": limpar_valor(linha["valor_gasto"]),
        }
        # Remove duplicados pelo e-mail (ou pelo nome, se não tiver e-mail)
        chave = cliente["email"] or cliente["nome"]
        if chave in vistos:
            problemas["registro duplicado (removido)"] += 1
            continue
        vistos.add(chave)
        limpos.append(cliente)

    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(limpos[0].keys()))
        escritor.writeheader()
        escritor.writerows(limpos)

    # Relatório de qualidade
    completos = sum(all(v is not None for v in c.values()) for c in limpos)
    linhas = [
        "# Relatório de Qualidade dos Dados\n",
        f"- Registros recebidos: **{len(brutos)}**",
        f"- Registros após a limpeza: **{len(limpos)}**",
        f"- Registros 100% completos: **{completos}** "
        f"({100 * completos / len(limpos):.0f}%)\n",
        "## Problemas encontrados e tratados\n",
        "| Problema | Ocorrências |",
        "| --- | --- |",
        *[f"| {p} | {q} |" for p, q in problemas.most_common()],
    ]
    with open(RELATORIO, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")

    print(f"{len(brutos)} registros lidos -> {len(limpos)} registros limpos.")
    print("Problemas tratados:")
    for p, q in problemas.most_common():
        print(f"  - {p}: {q}")
    print(f"\nArquivos gerados: {SAIDA} e {RELATORIO}")


if __name__ == "__main__":
    main()

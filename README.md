# Limpeza e Tratamento de Dados com Python

Na vida real, os dados quase nunca chegam prontos. Este projeto pega um cadastro de clientes **bagunçado** (nomes com maiúsculas erradas, e-mails inválidos, telefones em vários formatos, datas misturadas, registros duplicados, valores em "R$ 1.250,00") e transforma em uma base **limpa e padronizada**, pronta para análise.

> Os dados são **fictícios**, criados para praticar.

## O que o script trata

| Problema | Tratamento |
| --- | --- |
| Nomes com espaços extras e maiúsculas erradas | Padroniza (`ana paula  SOUZA` → `Ana Paula Souza`) |
| E-mails com letras maiúsculas ou inválidos | Coloca em minúsculas e valida com expressão regular |
| Telefones em formatos diferentes | Padroniza para `(11) 98765-4321` e remove o +55 |
| Datas em 5 formatos diferentes | Converte tudo para `AAAA-MM-DD` e descarta datas impossíveis (31/02) |
| Estados por extenso (`são paulo`, `Minas Gerais`) | Converte para a sigla (`SP`, `MG`) |
| Valores como `R$ 1.250,00` ou `890.50` | Converte para número |
| Linhas vazias e registros duplicados | Remove |

No final, gera um **relatório de qualidade** com quantos problemas de cada tipo foram encontrados.

## Tecnologias

- **Python 3**, só a biblioteca padrão: `csv`, `re` (expressões regulares), `datetime`, `collections.Counter`

## Como rodar

```bash
python limpar_dados.py
```

Arquivos gerados:
- `clientes_limpos.csv`: a base tratada
- `relatorio_qualidade.md`: o resumo dos problemas encontrados

## O que aprendi

- Identificar problemas de qualidade de dados (dados faltantes, duplicados, formatos inconsistentes)
- Usar expressões regulares para validar e-mails e extrair números
- Tratar datas em vários formatos
- Documentar as decisões de limpeza (o que descartar e o que corrigir)

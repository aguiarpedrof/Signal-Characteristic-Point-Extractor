# Signal Characteristic Point Extractor

> **Desafio Técnico** — Processo Seletivo para Iniciação Científica · FAPEMIG  
> Desenvolvido por **Pedro** | Prof. Giovani Bernardes

---

## Sobre o Projeto

Este projeto foi desenvolvido como parte do processo seletivo para bolsa de **Iniciação Científica (FAPEMIG)**. O desafio consiste em criar um algoritmo capaz de processar formas de onda temporais e extrair automaticamente **6 pontos característicos** de cada sinal — sem qualquer marcação manual.

A motivação vai além do processo seletivo: sinaleis temporais estão no centro de aplicações em eletrônica de potência, bioengenharia e sistemas embarcados. Saber extrair e analisar automaticamente pontos-chave de uma forma de onda é uma habilidade fundamental em engenharia.

---

## O que o algoritmo faz

```
CSV → Suavização (Savitzky-Golay) → Detecção dos 6 pontos → Gráficos + Estatística
```

| Feature | Ponto | Como é detectado |
|---------|-------|-----------------|
| **F1** | Início da subida | Primeira cruzamento do limiar da derivada positiva |
| **F2** | Pico intermediário | `find_peaks` com filtro de proeminência na região de subida |
| **F3** | Vale intermediário | `find_peaks` invertido entre F2 e F4 |
| **F4** | Pico máximo (regime) | `argmax` global do sinal suavizado |
| **F5** | Último ponto antes da descida | Maior variação negativa da derivada após F4 |
| **F6** | Retorno ao nível basal | Primeiro cruzamento do percentil 10 após F4 |

---

## Estrutura do Repositório

```
📦 DesafioIC/
 ├── SignalProcessor.py          # Algoritmo principal
 ├── dados/                      # Arquivos CSV de entrada
 ├── graficos/
 │   ├── sinais_individuais/     # Gráfico de cada sinal com os 6 pontos
 │   └── dispersao/              # Dispersão geral de todos os pontos
 ├── tabela_estatistica.txt      # Média e desvio padrão por feature
 ├── requirements.txt
 └── README.md
```

> Os arquivos CSV devem estar em `dados/` (ou ajustar `PASTA_DADOS` no código).  
> Cada CSV: coluna 1 = Tempo (ms), coluna 2 = Valor do sinal.

---

## Como Executar

**1. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**2. Execute:**
```bash
python SignalProcessor.py
```

Os gráficos e a tabela são gerados automaticamente.

---

## Dependências

```
numpy
pandas
matplotlib
scipy
```

---

## Saídas Geradas

- **10 gráficos individuais** — sinal original + 6 pontos destacados  
- **1 gráfico de dispersão** — todos os pontos característicos das 10 formas de onda  
- **Tabela estatística** — média e desvio padrão de tempo e amplitude para cada feature

---

## Habilidades Demonstradas

- Processamento digital de sinais (filtragem, derivada, detecção de picos)  
- Análise estatística (média, desvio padrão por grupo)  
- Python científico: `numpy`, `scipy`, `pandas`, `matplotlib`  
- Estruturação e documentação de projeto

---

*Desenvolvido em Python 3 · Março 2026*

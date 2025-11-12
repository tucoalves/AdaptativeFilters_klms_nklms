

# 🎧 Adaptive Filters: LMS, NLMS, KLMS e NKLMS

Este repositório contém a implementação prática do trabalho de conclusão de curso:

> **"Análise de Funções Kernel Aplicadas em Filtros Adaptativos para Cancelamento de Ruído"**  
> *Arthur Pereira Alves — Universidade do Vale do Itajaí (UNIVALI), 2025.*

O projeto investiga o desempenho de filtros adaptativos **lineares (LMS, NLMS)** e **não lineares (KLMS, NKLMS)**, aplicados à **filtragem de ruído e reverberação em sinais de voz**.  
As implementações foram realizadas em **Python**, com simulação de adição de ruído e por simulação acústica em sala fechada, e calculado métricas de desempenho (SNR, SDR e PESQ) para os resultados dos filtros.



## 🧩 Estrutura do Projeto
```
AdaptativeFilters_klms_nklms/
├── data/
│   ├── audio_limpo.wav           # Áudio de referência (voz limpa)
│   ├── ruidos/                   # Conjunto de ruídos (white e babble)
│   ├── corrupted_dataset/        # Áudios corrompidos gerados pelo script ruidos.py
│   ├── result_lms/               # Resultados do filtro LMS
│   ├── result_nlms/              # Resultados do filtro NLMS
│   ├── result_klms/              # Resultados do filtro KLMS
│   └── result_nklms/             # Resultados do filtro NKLMS
│
├── filtros.py                    # Implementação dos filtros LMS, NLMS, KLMS e NKLMS
├── filtro_poly.py                # Implementação KLMS/NKLMS com kernel polinomial para execução dos múltiplos parâmetros
├── ruidos.py                     # Geração de sinais corrompidos com ruído e reverberação
├── README.md
└── requirements.txt
```



## ⚙️ Funcionalidades

### 🧠 Filtros Adaptativos Implementados
| Filtro | Tipo | Descrição |
|--------|------|-----------|
| **LMS (Least Mean Squares)** | Linear | Método simples de atualização de pesos via erro instantâneo. |
| **NLMS (Normalized LMS)** | Linear | Versão normalizada do LMS — melhora estabilidade e convergência. |
| **KLMS (Kernel LMS)** | Não Linear | Mapeia o sinal para o espaço de Hilbert (RKHS) via truque de kernel. |
| **NKLMS (Normalized Kernel LMS)** | Não Linear | Combina normalização do NLMS com o espaço RKHS para melhor desempenho. |

## ▶️ Como Executar
### Instale as dependências
```bash
pip install -r requirements.txt
````

## 🧪 Geração dos Dados Corrompidos

O script `ruidos.py` gera versões corrompidas do áudio limpo adicionando **ruídos (white/babble)** e **reverberação** simulada via biblioteca **[Pyroomacoustics](https://pyroomacoustics.readthedocs.io)**.

**Exemplo de uso:**
```bash
python ruidos.py
````

Este script:

1. Carrega `data/audio_limpo.wav`;
2. Adiciona ruído com SNRs de 0, 5 e 10 dB;
3. Gera sinal sem reverberação, apenas soma do sinal limpo + ruído
4. Gera sinal com reverberação em salas de dimensões aleatórias;
5. Salva os resultados em `data/corrupted_dataset/`.

---

## 🎛️ Execução dos Filtros

Os filtros podem ser executados diretamente com Python:

### 1️⃣ Filtros LMS, NLMS, KLMS e NKLMS (Gaussian/Laplacian/Polinomial)

```bash
python filtros.py
```

### 2️⃣ Para execução de vários parametros para o kernel polinomial, usar "filtro_poly.py"

```bash
python filtro_poly.py
```

Durante a execução, o script:

* Processa cada arquivo corrompido em `data/corrupted_dataset/`;
* Aplica os filtros definidos;
* Calcula as métricas SNR, SDR e PESQ;
* Armazena os resultados em planilhas `.xlsx`.

---

## 📊 Métricas de Avaliação

| Métrica                                            | Descrição                                              |
| -------------------------------------------------- | ------------------------------------------------------ |
| **SNR (Signal-to-Noise Ratio)**                    | Mede a relação entre o sinal limpo e o ruído residual. |
| **SDR (Signal-to-Distortion Ratio)**               | Quantifica distorções introduzidas pelo filtro.        |
| **PESQ (Perceptual Evaluation of Speech Quality)** | Mede a qualidade perceptual da fala (ITU-T P.862).     |

Os resultados são armazenados em `resultados_final.xlsx`.

---


## 📚 Referências Principais

* **Liu, W., Pokharel, P. P., & Principe, J. C. (2010).** *Kernel Adaptive Filtering.* John Wiley & Sons.
* **Haykin, S. (2002).** *Adaptive Filter Theory.* Prentice Hall.
* **Dos Santos, L. (2022).** *Improving Speaker Recognition in Environmental Noise with Adaptive Filter.*
* **Scheibler, R. et al. (2017).** *Pyroomacoustics: A Python Package for Audio Room Simulation.*

---

## 🧑‍💻 Autor

**Arthur Pereira Alves**
Graduando em Engenharia da Computação – UNIVALI
🔗 [GitHub: tucoalves](https://github.com/tucoalves)

---

## 🪪 Licença

Este projeto é distribuído sob a licença **MIT**.
Sinta-se livre para usar, modificar e compartilhar com atribuição ao autor original.

---

```

---

Quer que eu adicione uma **seção com resultados resumidos (tabelas de desempenho por filtro e kernel)** extraída do relatório PDF? Isso deixaria o `README` ainda mais informativo.
```

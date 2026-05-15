# 💰 Simulador de Poder de Compra Real

Este projeto é uma ferramenta interativa desenvolvida em **Python** que permite visualizar a desvalorização monetária e o impacto da inflação (IPCA) sobre o Real e o Salário Mínimo desde o início do Plano Real (1995).

### 🚀 [Acesse o App aqui](https://simulador-do-poder-de-compra-mhvx3bwhnszaoasbkkh4zs.streamlit.app/)

---

## 🛠️ Tecnologias e Conceitos
Este projeto foi construído focando em boas práticas de engenharia de dados e arquitetura de software:

* **Extração de Dados (ETL):** Consumo em tempo real das APIs do Sistema Gerenciador de Séries (SGS) do **Banco Central do Brasil**.
* **Processamento Vetorizado:** Utilização da biblioteca **Pandas** para manipulação de DataFrames, garantindo alta performance no tratamento de séries temporais.
* **Matemática Financeira:** Implementação de **Índice Encadeado** (Produto Acumulado) para cálculo de juros compostos da inflação via método `.prod()`.
* **Otimização:** Uso de **Caching** (`@st.cache_data`) para reduzir a latência e o volume de requisições às APIs governamentais.
* **Interface Reativa:** UI desenvolvida com **Streamlit** e gráficos dinâmicos com **Plotly Express**.

---

## 🧠 Arquitetura do Projeto
O software segue o princípio de responsabilidade única (SRP), dividindo a lógica em:

* `app.py`: Camada de Interface (Frontend) e gerenciamento de estado da UI.
* `main.py`: Camada de Lógica de Negócio (Backend), contendo os algoritmos de cálculo e tratamento de dados.
* `requirements.txt`: Gestão de dependências e ambiente virtual.

---

## 📊 Como a Inflação é Calculada?
Diferente da soma aritmética simples, a inflação acumulada é o produto dos fatores mensais. O algoritmo realiza a seguinte operação:

$$Fator_{final} = \prod_{i=1}^{n} (1 + \frac{taxa_i}{100})$$

Isso garante que o simulador reflita o impacto real de "juros sobre juros" nos preços da economia.

---

## 💻 Como Rodar Localmente

1. Clone o repositório:
   ```bash
   git clone [https://github.com/Lucas224-dev/Simulador-do-Poder-de-Compra.git](https://github.com/Lucas224-dev/Simulador-do-Poder-de-Compra.git)

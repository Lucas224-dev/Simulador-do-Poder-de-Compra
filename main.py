import pandas as pd 
import streamlit as st

ipca = 16122 
sm = 1619 
@st.cache_data # Cache para evitar requisições repetitivas
def carregar_ipca():
    try: # Try: para tratamento de erros                                                                                     
        url_ipca = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{ipca}/dados?formato=json" # Extração: Consome os dados brutos em formato JSON via API do BC
        df_ipca = pd.read_json(url_ipca)                                                      
        #print(df_ipca.tail())
        
        df_ipca['data'] = pd.to_datetime(df_ipca['data'], dayfirst=True) # Transformação (Data Cleaning & Wrangling):                 
        df_ipca['valor'] = pd.to_numeric(df_ipca['valor'])     
                                       
        df_ipca = df_ipca[df_ipca['data'] >= '1995-01-01'] # Filtro histórico: Mantém apenas dados estáveis pós-Plano Real             
                              
        df_ipca['valor_formatado'] = df_ipca['valor'].map("{:.2f}%".format) # Feature Engineering: Cria coluna formatada para exibição visual      
                   
        return df_ipca # Retorna o DataFrame pronto para análise      
                                                                     
    except Exception as e:                                                                    
        st.error(f"Erro ao conectar com o Banco Central: {e}") # Tratamento de exceção para falhas de conexão ou mudanças na estrutura da API
        return pd.DataFrame()                                                                 
                                                                                                            
@st.cache_data # Cache para evitar requisições repetitivas
def carregar_sm():
    try:
        url_sm = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{sm}/dados?formato=json" # Extração: Consome os dados brutos em formato JSON via API do BC
        df_sm = pd.read_json(url_sm)
        #print(df_sm.tail())
        
        df_sm['data'] = pd.to_datetime(df_sm['data'], dayfirst=True) # Transformação (Data Cleaning & Wrangling): 
        df_sm['valor'] = pd.to_numeric(df_sm['valor'])
        
        df_sm = df_sm[df_sm['data'] >= '1995-01-01'] # Filtro histórico: Mantém apenas dados estáveis pós-Plano Real   
        
        return df_sm # Retorna o DataFrame pronto para análise    
    
    except Exception as e:
        st.error(f"Erro ao conectar com o Banco Central: {e}") # Tratamento de exceção para falhas de conexão ou mudanças na estrutura da API
        return pd.DataFrame()

def calcular_poder_de_compra(ano_inicio : int, ano_fim : int, df_ipca : pd.DataFrame): 
    mask = (df_ipca['data'].dt.year >= ano_inicio) & (df_ipca['data'].dt.year <= ano_fim)  # Filtra os anos usando a coluna de data convertida para ano
    df_filtrado = df_ipca.loc[mask]
    
    if df_filtrado.empty:
        return 0.0, 0.0
    
    fatores = (df_filtrado['valor'] / 100) + 1  # Cálculo da inflação acumulada
    fator_acumulado = fatores.prod()
    
    inflacao_total_perc = (fator_acumulado - 1) * 100 # Definição das variáveis de retorno
    valor_corrigido = 100 * fator_acumulado # Simulação baseada em R$ 100,00
    
    return round(valor_corrigido, 2), round(inflacao_total_perc, 2)

def calcular_salario_ipca(salario_antigo, ano_inicio, ano_fim, df_ipca):
    data_inicio_limite = f"{int(ano_inicio)}-01-01"  # Lógica de datas para pegar o ano cheio
    data_fim_limite = f"{int(ano_fim)}-12-31"
    
    filtro_periodo = (df_ipca['data'] >= data_inicio_limite) & (df_ipca['data'] <= data_fim_limite)
    df_filtrado = df_ipca[filtro_periodo]
    
    if df_filtrado.empty:
        return salario_antigo
        
    fatores = (df_filtrado['valor'] / 100) + 1
    fator_acumulado = fatores.prod()
    
    return round(salario_antigo * fator_acumulado, 2)

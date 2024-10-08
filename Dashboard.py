import streamlit as st
import pandas as pd

class dashboard:
    def __init__(self):
        self.df_historico = pd.read_excel("Planilha Ágora.xlsx", sheet_name="Historico")
        self.df_fundamentalista = pd.read_excel("Planilha Ágora.xlsx", sheet_name="Indicadorfundamentalista")
    
    
    def Historico_negociação(self):
        lista = self.df_historico['Ano'].unique().tolist()
        indicador = st.selectbox("Selecione o indicador", lista)
        historico = self.df_historico[self.df_historico["Ano"].str.contains(int(indicador), case=False, na=False)]
        st.dataframe(historico)
    
     
    def Fundamentalista(self):        
        lista_indicador = self.df_fundamentalista['Indicador'].unique().tolist()
        
        indicador = st.selectbox("Selecione o indicador", lista_indicador)
        df_indicador = self.df_fundamentalista[self.df_fundamentalista["Indicador"].str.contains(f"{indicador}", case=False, na=False)]

        Empresas = self.df_fundamentalista[self.df_fundamentalista["Indicador"].str.contains("Market Cap", case=False, na=False)].iloc[:,:3]
        df_indicador_Market_cap = self.df_fundamentalista[self.df_fundamentalista["Indicador"].str.contains("Market Cap", case=False, na=False)].iloc[:, 3:]
        df_indicador_Book_to_Market = self.df_fundamentalista[self.df_fundamentalista["Indicador"].str.contains("Book-to-Market", case=False, na=False)].iloc[:, 3:]
        df_indicador_Pl = self.df_fundamentalista[self.df_fundamentalista["Indicador"].str.contains("Preço/Lucro", case=False, na=False)].iloc[:, 3:]
        # Resetando índices
        
        st.title("Valor mercado")
        st.dataframe(self.df_fundamentalista[self.df_fundamentalista["Indicador"].str.contains("Market Cap", case=False, na=False)])
        
        st.title("Book to market")
        st.dataframe(self.df_fundamentalista[self.df_fundamentalista["Indicador"].str.contains("Book-to-Market", case=False, na=False)])
        
        st.title("P/L")
        st.dataframe(self.df_fundamentalista[self.df_fundamentalista["Indicador"].str.contains("Preço/Lucro", case=False, na=False)])
        
        
        df_indicador.reset_index(drop=True, inplace=True)
        df_indicador_Book_to_Market.reset_index(drop=True, inplace=True)
        df_indicador_Pl.reset_index(drop=True, inplace=True)


        df_valor_contabil = df_indicador_Market_cap * df_indicador_Book_to_Market
        df_valor_contabil_final = pd.concat([Empresas, df_valor_contabil], axis=1)
        st.title("Valor contabil da empresa (BI)")
        st.dataframe(df_valor_contabil_final)
        
        
        
        df_lucro_liquido = df_indicador_Market_cap / df_indicador_Pl
        df_lucro_liquido_final = pd.concat([Empresas, df_lucro_liquido], axis=1)
        st.title("Lucro liquido (BI)")
        st.dataframe(df_lucro_liquido_final)
        
        
        df_crescimento_receita = df_lucro_liquido.T.pct_change().fillna(0)
        df_crescimento_receita = df_crescimento_receita.applymap(lambda x: f"{x * 1:.2f}%")
        df_crescimento_receita_final = pd.concat([Empresas, df_crescimento_receita.T], axis=1)
        st.title("Crescimento de receita (%)")
        st.dataframe(df_crescimento_receita_final)
        
        
        df_Roe = df_lucro_liquido/df_valor_contabil
        df_Roe = df_Roe.applymap(lambda x: f"{x * 1:.2f}%")
        df_Roe_final = pd.concat([Empresas, df_Roe], axis=1)
        st.title("Roe (%)")
        st.dataframe(df_Roe_final)

                
    def main(self):
        lista_navegação = []
        

        lista_navegação.append(st.Page(self.Fundamentalista, title= "🏢 Fundamentalista"))
        lista_navegação.append(st.Page(self.Historico_negociação, title="📝 Historico_negociação"))
        
        pg = st.navigation({"Opções de analise":lista_navegação}, position="sidebar")
        pg.run()

    
if __name__ == "__main__":
    dash = dashboard()  # Instanciar a classe
    dash.main()        # Chamar o método
import json
import math
from pandas import DataFrame
import connection
import db_ctrl_estoque

class EstoqueService:
    def __init__(self):
        self.produtos_tpa = connection.getProdutosControleEstoque()
        self.p_controle = db_ctrl_estoque.getEstoqueCompleto()
        self.semiacabados_tpa = connection.getControleSemiAcabados()
        self.sa_controle = db_ctrl_estoque.getEstoqueSA()
        
        self.ctrl_acabados = None        
        self.ctrl_semiacabados = None
        
        
    
    def formatarProdutosControle(self):
        for x in self.sa_controle:
            print(x)
        df_ctrl_sa = DataFrame(self.sa_controle)
        df_ctrl_sa = df_ctrl_sa.groupby(['idxProduto', 'descricao'])[['saldo']].sum().reset_index()
        sa_controle_json = json.loads(df_ctrl_sa.to_json(orient='records'))
        
        print(df_ctrl_sa)
        
        df_semiacabados = DataFrame(self.semiacabados_tpa)
        df_semiacabados['totalProducao'] = df_semiacabados.apply(self.calcularSaldoSemiacabados, axis=1)
        print(df_semiacabados)
        df_semiacabados = df_semiacabados.apply(self.calcularSaldoSA, controle=sa_controle_json, axis=1)
        _semiacabadosjson = json.loads(df_semiacabados.to_json(orient='records'))
        self.ctrl_semiacabados = _semiacabadosjson
        
        df_controle = DataFrame(self.p_controle)
        df_controle = df_controle.groupby(['pkProduto', 'descricao'])[['saldo']].sum().reset_index()
        controle_json = json.loads(df_controle.to_json(orient='records'))
        
        df_tpa = DataFrame(self.produtos_tpa)
        df_tpa = df_tpa.apply(self.calcularSaldo, controle=controle_json, axis=1)
        _acabadosjson = json.loads(df_tpa.to_json(orient='records'))
        
        self.ctrl_acabados = _acabadosjson
    
    
    def calcularSaldo(self, row, controle):
        if math.isnan(row['somaQuantidade']):
            row['somaQuantidade'] = 0
        for prod in controle:
            if int(row['PK_PRODUTO']) == int(prod['pkProduto']):
                row['somaQuantidade'] = prod['saldo'] - (row['somaQuantidade'] * 100)
        return row
    
    def calcularSaldoSA(self, row, controle):
        for prod in controle:
            if int(row['IDX_PRODUTO']) == int(prod['idxProduto']):
                row['totalProducao'] = prod['saldo'] - row['totalProducao']
        return row
    
    def calcularSaldoSemiacabados(self, row):
        total_producao = 0
        for acab in self.produtos_tpa:
            if row['RDX_PRODUTO'] == acab['PK_PRODUTO']:
                total_producao = row['QUANTIDADE'] * acab['somaQuantidade']
        return total_producao


# if __name__ == "__main__":
#     estoque_service = EstoqueService()
#     results = estoque_service.formatarProdutosControle()
#     print(estoque_service.ctrl_acabados)
#     print('----------')
#     print(estoque_service.ctrl_semiacabados)


# def formatarProdutosControle():
#     global produtos_tpa
#     produtos_tpa = connection.getProdutosControleEstoque()
#     p_controle = db_ctrl_estoque.getEstoqueCompleto()
#     semiacabados_tpa = connection.getControleSemiAcabados()
#     df_semiacabados = DataFrame(semiacabados_tpa)
    
#     df_semiacabados['totalProducao'] = df_semiacabados.apply(calcularSaldoSemiAcabados, acabados=produtos_tpa, axis=1)
#     print(df_semiacabados)
    
#     df_controle = DataFrame(p_controle)
#     df_controle = df_controle.groupby(['pkProduto', 'descricao'])[['saldo']].sum().reset_index()
    
#     result_json = df_controle.to_json(orient='records')
#     controle_json = json.loads(result_json)
    
#     df_tpa = DataFrame(produtos_tpa)
#     print(df_tpa)
#     df_tpa = df_tpa.apply(calcularSaldo, controle=controle_json, axis=1)
#     resultadosJson = df_tpa.to_json(orient='records')
#     dadosDesserializados = json.loads(resultadosJson)
    
#     return dadosDesserializados

# def calcularSaldo(row, controle):
#     if math.isnan(row['somaQuantidade']):
#         row['somaQuantidade'] = 0
#     for prod in controle:
#         if int(row['PK_PRODUTO']) == int(prod['pkProduto']):
#             row['somaQuantidade'] = prod['saldo'] - (row['somaQuantidade'] * 100)
#     return row

# def calcularSaldoSemiAcabados(row, acabados):
#     for acab in acabados:
#         if row['RDX_PRODUTO'] == acab['PK_PRODUTO']:
#             total_producao = row['QUANTIDADE'] * acab['somaQuantidade']
#     return total_producao 
    

    
    


    
    

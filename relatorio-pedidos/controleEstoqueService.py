import json
import math
from pandas import DataFrame
import connection
import db_ctrl_estoque

def formatarProdutosControle():
    produtos_tpa = connection.getProdutosControleEstoque()
    p_controle = db_ctrl_estoque.getEstoqueCompleto()
    
    df_controle = DataFrame(p_controle)
    df_controle = df_controle.groupby(['pkProduto', 'descricao'])[['saldo']].sum().reset_index()
    
    result_json = df_controle.to_json(orient='records')
    controle_json = json.loads(result_json)
    
    df_tpa = DataFrame(produtos_tpa)
    df_tpa = df_tpa.apply(calcularSaldo, controle=controle_json, axis=1)
    resultadosJson = df_tpa.to_json(orient='records')
    dadosDesserializados = json.loads(resultadosJson)
    
    return dadosDesserializados

def calcularSaldo(row, controle):
    if math.isnan(row['somaQuantidade']):
        row['somaQuantidade'] = 0
    for prod in controle:
        if int(row['PK_PRODUTO']) == int(prod['pkProduto']):
            row['somaQuantidade'] = prod['saldo'] - (row['somaQuantidade'] * 100)
    return row
    
    

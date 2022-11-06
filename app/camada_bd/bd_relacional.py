import psycopg2
from camada_bd.singleton import SingletonMeta

class BDRelacional(metaclass=SingletonMeta):

    connString = 'postgresql://uospmgae:kFBbjgeZBH7RFuJcY3D9hYseJXh0HZjE@motty.db.elephantsql.com/uospmgae'
    
    def __init__(self):
        pass

    #Retorna todos os estados do Brasil ordenados pelo nome
    def buscarEstados(self):
        query = "SELECT DISTINCT cod_uf, uf, nome_uf \
                FROM municipio WHERE uf IS NOT NULL \
                ORDER BY nome_uf ASC;"

        resultado = self.queryTabela(query)
        return resultado


    #Retorna todas as cidade de um estado
    def buscarCidadesPorEstado(self, estadoId):
        query = f"SELECT cod_cidade, nome_cidade FROM arr_mun\
                WHERE cod_uf = {estadoId}\
                ORDER BY nome_cidade ASC;"

        resultado = self.queryTabela(query)
        return resultado

    
    #Retorna todos municipios de um estado
    def buscarMunicipiosPorEstado(self, estadoId):
        query = f"SELECT cod_mun, nome_mun FROM municipio\
                WHERE cod_uf = {estadoId}\
                ORDER BY nome_mun ASC;"

        resultado = self.queryTabela(query)
        return resultado


    #Retorna todas as regiões de saúde de um estado
    def buscarRegioesPorEstado(self, estadoId): 
        query = f"SELECT rs.cod_reg_saude,rs.nome_reg_saude  \
                FROM regiao_saude rs \
                JOIN municipio mu ON mu.cod_reg_saude = rs.cod_reg_saude \
                WHERE mu.cod_uf = {estadoId} \
                GROUP BY rs.cod_reg_saude ORDER BY rs.nome_reg_saude ASC;"

        resultado = self.queryTabela(query)
        return resultado


    #Buscar coordenadas de uma cidade         
    def buscarCidadeCoordenadas(self, cidadeId):
        query = f"SELECT cod_cidade, nome_cidade, latitude, longitude FROM arr_mun\
                WHERE cod_cidade = {cidadeId};"

        resultado = self.queryTabela(query)[0]
        return resultado 


    #Buscar cidade pelo ID
    def buscarCidade(self, cidadeId):
        query = f"SELECT * FROM arr_mun\
                WHERE cod_cidade = {cidadeId};"

        resultado = self.queryTabela(query)[0]
        return resultado 


    #Buscar coordenadas de uma regiao saude     
    def buscarRegiaoCoordenadas(self, regiaoId):
        query = f"SELECT cod_reg_saude, nome_reg_saude, latitude, longitude FROM regiao_saude\
                WHERE cod_reg_saude = {regiaoId};"

        resultado = self.queryTabela(query)[0]
        return resultado 

    
    #Buscar todas as cidades 
    def buscarTodasCidades(self):
        query = "SELECT * FROM arr_mun;"
        resultado = self.queryTabela(query)
        return resultado


    #Buscar todas as cidades adicionando a coluna da rede sentinela
    def buscarTodasCidadesComSentinela(self):
        query = "SELECT mu.*, STRING_AGG(ss.nome_serv, ', ') rede_sentinela \
                FROM municipio mu \
                LEFT JOIN servico_sentinela ss ON mu.cod_mun = ss.cod_mun \
                GROUP BY mu.cod_mun;"
        resultado = self.queryTabela(query)
        return resultado


    #TODO: implementar funçao se necessario
    def buscarRedeSentinelaCidade(self, idCidade):
        pass


    #Busca toda a tabela de Rede Sentinela
    def buscarTodaRedeSentinela(self):
        query = "SELECT * FROM servico_sentinela;"
        resultado = self.queryTabela(query)
        return resultado
        

    # Realiza operações na tabela do BD com psycopg2
    def queryTabela(self, comandoSql):

        conn = psycopg2.connect(self.connString)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(comandoSql)
        resultadoQuery = cursor.fetchall()
        conn.commit()
        conn.close()

        return resultadoQuery

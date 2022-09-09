import psycopg2


class BDRelacional:

    connString = 'postgresql://uospmgae:kFBbjgeZBH7RFuJcY3D9hYseJXh0HZjE@motty.db.elephantsql.com/uospmgae'
    
    def __init__(self):
        pass


    def buscarEstados(self):
        query = "SELECT DISTINCT cod_uf, uf, nome_uf\
                FROM municipio WHERE uf IS NOT NULL \
                ORDER BY nome_uf ASC"

        resultado = self.queryTabela(query)
        return resultado


    def buscarCidadesPorEstado(self, estadoId):
        query = f"SELECT cod_mun, nome_mun FROM municipio\
                WHERE cod_uf = {estadoId}\
                ORDER BY nome_mun ASC"

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

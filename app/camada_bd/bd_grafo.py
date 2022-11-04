from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
from camada_bd.singleton import SingletonMeta


class BDGrafo(metaclass=SingletonMeta):

    # uri = "neo4j+s://af76534a.databases.neo4j.io"
    # password = "Ez5RDE71XQXpRO9kzufUTrVGGNtw9mo5KAa83226V6M"
    uri = "bolt://localhost:7687" #local BD
    password = "alerta_epidemia" #local BD
    user = "neo4j"
    driver = None

    def __init__(self):
        #Cria projecao do fluxo para rodar algoritmos
        self.criarProjecao()
        self.close()


    def close(self):
        self.driver.close()


    #Funcao que cria a projecao do grafo
    def criarProjecao(self):
        #Abre conexao com o BD
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        
        #Primeiro verifica se grafo existe, caso não exista cria o grafo
        existeGrafo = self.checarExistenciaGrafo('grafoFluxo')[0][1]
        if(not existeGrafo):
            with self.driver.session(database="neo4j") as session:
                result = session.read_transaction(
                    self._criarProjecaoGrafoFluxo)
                return result

    @staticmethod
    def _criarProjecaoGrafoFluxo(tx):
        query = (
                "CALL gds.graph.project("
                "'grafoFluxo',"
                "'Cidade', "
                "'FLUXO_TRANSPORTE',"
                "{"
                    "relationshipProperties: 'fluxo_invertido'"
                "})"
            )
        return tx.run(query) #TODO: Verificar se criou corretamente com o try/catch


    #Funcao que verifica a existencia do grafo
    def checarExistenciaGrafo(self, nomeGrafo):
        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(
                self._verificarGrafo, nomeGrafo)

            return result

    #Funcao com query de verificacao de grafo
    @staticmethod 
    def _verificarGrafo(tx, nomeGrafo):
        query = (
            f"CALL gds.graph.exists ('{nomeGrafo}') "
            "YIELD graphName, exists "
            "RETURN graphName, exists"
            )
        result = tx.run(query, nomeGrafo=nomeGrafo)
        return result.values("graphName","exists")


    #Funcao busca no BD fluxos que a cidade de origem possui com outras cidades
    def buscarFluxoCidade(self, idMunicipio):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(
                self._buscarFluxoCidade, idMunicipio)

            return result

    #Funcao com a query de busca
    @staticmethod
    def _buscarFluxoCidade(tx, idMunicipio):
        query = (
            "MATCH (c1)-[r]->(c2) "
            "WHERE c1.cod_mun =  $idMunicipio "
            "RETURN c2.cod_mun AS cod_mun, c2.nome AS nome, "
            "r.fluxo_geral AS fluxo_geral, r.fluxo_aereo AS fluxo_aereo, r.fluxo_rodo AS fluxo_rodo, "
            "r.saude_alta AS saude_alta, r.saude_baixa_media AS saude_baixa_media, "
            "c2.latitude AS latitude, c2.longitude AS longitude"
        )
        
        result = tx.run(query, idMunicipio=idMunicipio)
        return result.values("cod_mun","nome","latitude","longitude", 
                            "fluxo_geral", "fluxo_aereo", "fluxo_rodo",
                            "saude_alta", "saude_baixa_media")


   #Funcao busca no BD fluxos que a regiao de saude de origem possui com outras regioes
    def buscarFluxoSaudeRegiao(self, idRegiao):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(
                self._buscarFluxoSaudeRegiao, idRegiao)

            return result

    #Funcao com a query de busca
    @staticmethod
    def _buscarFluxoSaudeRegiao(tx, idRegiao):
        query = (
            "MATCH (rs:Regiao_Saude)<-[r:PERTENCE]-(c:Cidade) "
            "WHERE rs.cod_reg_saude = $idRegiao "
            "WITH collect(c) AS cs, sum(c.populacao) AS rs_pop "
            "MATCH (c_ori:Cidade)-[f:FLUXO_SAUDE]->(c_dest:Cidade)-[p:PERTENCE]->(rs_dest:Regiao_Saude) "
            "WHERE c_ori IN cs AND NOT c_dest IN cs " 
            "WITH rs_dest.cod_reg_saude AS cod_regiao, rs_dest.nome AS nome, rs_dest.latitude AS latitude, rs_dest.longitude AS longitude, "
            "collect([c_ori.populacao,f.saude_baixa_media,f.saude_alta]) AS cl, rs_pop AS rs_pop "
            "WITH cod_regiao AS cod_regiao, nome AS nome,latitude AS latitude, longitude AS longitude, " 
            "reduce(res = [0,0] , array IN cl | [res[0] + (array[0]*array[1]), res[1] + (array[0]*array[2])]) AS res, rs_pop AS rs_pop "
            "RETURN cod_regiao, nome, latitude, longitude, res[0]/rs_pop AS saude_baixa_media, res[1]/rs_pop AS saude_alta"
        )
        
        result = tx.run(query, idRegiao=idRegiao)
        return result.values("cod_regiao","nome","latitude","longitude", "saude_alta", "saude_baixa_media")


   #Funcao busca no BD fluxos que a regiao de saude de origem possui com outras regioes
    def buscarFluxoTransporteRegiao(self, idRegiao):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(
                self._buscarFluxoTransporteRegiao, idRegiao)

            return result

    #Funcao com a query de busca
    @staticmethod
    def _buscarFluxoTransporteRegiao(tx, idRegiao):
        query = (
            "MATCH (rs:Regiao_Saude)<-[r:PERTENCE]-(c:Cidade) "
            "WHERE rs.cod_reg_saude = $idRegiao "
            "WITH collect(c) AS cs, sum(c.populacao) AS rs_pop "
            "MATCH (c_ori:Cidade)-[f:FLUXO_TRANSPORTE]->(c_dest:Cidade)-[p:PERTENCE]->(rs_dest:Regiao_Saude) "
            "WHERE c_ori IN cs AND NOT c_dest IN cs " 
            "WITH rs_dest.cod_reg_saude AS cod_regiao, rs_dest.nome AS nome, rs_dest.latitude AS latitude, rs_dest.longitude AS longitude, "
            "collect([c_ori.populacao,f.fluxo_geral,f.fluxo_aereo, f.fluxo_rodo]) AS cl, rs_pop AS rs_pop "
            "WITH cod_regiao AS cod_regiao, nome AS nome,latitude AS latitude, longitude AS longitude, " 
            "reduce(res = [0,0,0] , array IN cl | [res[0] + (array[0]*array[1]), res[1] + (array[0]*array[2]), res[2] + (array[0]*array[3])]) AS res, rs_pop AS rs_pop "
            "RETURN cod_regiao, nome, latitude, longitude, res[0]/rs_pop AS fluxo_geral, res[1]/rs_pop AS fluxo_aereo, res[2]/rs_pop AS fluxo_rodo"
        )
        
        result = tx.run(query, idRegiao=idRegiao)
        return result.values("cod_regiao","nome","latitude","longitude", "fluxo_geral", "fluxo_aereo", "fluxo_rodo")


    #Funcao busca os menores caminho da cidade de origem e o conjunto de cidades especificada
    def buscarMenorCaminho(self, idMunicipioOrigem, tipoDestino):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(
                self._buscarMenorCaminhoFluxo, idMunicipioOrigem, tipoDestino)

            return result

    #Funcao com a query da busca
    @staticmethod
    def _buscarMenorCaminhoFluxo(tx, idMunicipioOrigem, tipoDestino):
        query = (
            "MATCH (c_spreader:Cidade)-[r]->(h:Hierarquia) WHERE h.hierarquia = \"" + tipoDestino+ "\"\
            WITH collect(c_spreader) AS nodes \
            UNWIND nodes AS ct \
            MATCH (source:Cidade {cod_mun:"+ idMunicipioOrigem +"}), (target:Cidade {cod_mun: ct.cod_mun}) \
            CALL gds.shortestPath.dijkstra.stream('grafoFluxo', { \
                sourceNode: source, \
                targetNode: target, \
                relationshipWeightProperty: 'fluxo_invertido'}) \
            YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path \
            RETURN \
                index, \
                gds.util.asNode(sourceNode).nome AS sourceNodeName, \
                gds.util.asNode(targetNode).nome AS targetNodeName, \
                totalCost, \
                [nodeId IN nodeIds | gds.util.asNode(nodeId).nome] AS nodeNames, \
                costs, \
                nodes(path) as path \
            ORDER BY totalCost ASC" 
        )
        
        result = tx.run(query, idMunicipioOrigem=idMunicipioOrigem, tipoDestino=tipoDestino)
        return result.values("costs","path")
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
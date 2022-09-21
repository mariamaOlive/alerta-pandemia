from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable


class BDGrafo:

    uri = "neo4j+s://af76534a.databases.neo4j.io"
    user = "neo4j"
    password = "Ez5RDE71XQXpRO9kzufUTrVGGNtw9mo5KAa83226V6M"

    def __init__(self):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))


    def close(self):
        self.driver.close()


    def buscarCidade(self, idMunicipio):
        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(
                self._buscarRetornaCidade, idMunicipio)

            return result


    @staticmethod
    def _buscarRetornaCidade(tx, idMunicipio):
        query = (
            "MATCH (c1)-[r]->(c2) "
            "WHERE c1.cod_mun =  $idMunicipio "
            "RETURN c2.cod_mun AS cod_mun, c2.nome AS nome, "
            "r.fluxo_geral AS fluxo_geral, r.fluxo_aereo AS fluxo_aereo, r.fluxo_rodo AS fluxo_rodo, "
            "c2.latitude AS latitude, c2.longitude AS longitude "
            "ORDER BY fluxo_geral DESC"
        )
        
        result = tx.run(query, idMunicipio=idMunicipio)
        return result.values("nome", "cod_mun","latitude","longitude", "fluxo_geral", "fluxo_aereo", "fluxo_rodo")



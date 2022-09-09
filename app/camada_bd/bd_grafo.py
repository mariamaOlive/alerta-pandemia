from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable


class BDGrafo:

    uri = "neo4j+s://1c1d624f.databases.neo4j.io"
    user = "neo4j"
    password = "T6tVBaYAdYjGqsncHKTr_saslM63tJ6sKJuhzd1cqcI"

    def __init__(self):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))


    def close(self):
        self.driver.close()


    def buscarCidade(self, idMunicipio):
        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(
                self._buscarRetornaPessoa, idMunicipio)

            return result


    @staticmethod
    def _buscarRetornaPessoa(tx, idMunicipio):
        query = (
            "MATCH (c1)-[r]->(c2) "
            "WHERE c1.cod_mun =  $idMunicipio "
            "RETURN c2.nome AS nome, c2.cod_mun  AS cod_mun, r.probabilidade AS score, "
            "c2.latitude AS latitude, c2.longitude AS longitude "
            "ORDER BY score DESC"
        )
        
        result = tx.run(query, idMunicipio=idMunicipio)
        return result.values("nome", "cod_mun","latitude","longitude", "score")



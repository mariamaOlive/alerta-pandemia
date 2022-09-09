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
            for row in result:
                print("Found city: {row}".format(row=row))

        self.close()


    @staticmethod
    def _buscarRetornaPessoa(tx, idMunicipio):
        query = (
            "MATCH (c1)-[r]->(c2) "
            "WHERE c1.cod_mun =  $idMunicipio "
            "AND r.probabilidade > 0.015 "
            "RETURN c2.nome AS nome"
        )
        
        result = tx.run(query, idMunicipio=idMunicipio)
        return [row["nome"] for row in result]



    # app = App(uri, user, password)
    # app.create_friendship("Alice", "David")
    # app.find_person("Alice")
    # app.close()
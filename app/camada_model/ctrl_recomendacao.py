import camada_bd.bd_grafo as BDGf

class CtrlRecomendacao:

  def __init__(self):
    pass

  def calculoRecomendacao(self, idCidade):
    bdGrafo = BDGf.BDGrafo()
    resultado = bdGrafo.buscarCidade(idCidade)
    bdGrafo.close()
    return resultado

"""Modelo com uma falha e material elástico

Modelo utilizado para comparação com a nova metodologia do CAE, 
desenvolvida pelo Pedro Lobo <plobo@tecgraf.puc-rio.br>.

Este script permite a geração paramétrica de um modelo de zona de dano
com uma falha centralizada. Ao fim, são escritos os arquivos de input
para a análise em Elementos Finitos no software comercial Abaqus.

Este script requer a instalação do pacote `damagezonemodeling`, 
desenvolvido internamente pelo grupo de Modelagem e Simulação 
Computacional do Instituto Tecgraf/PUC-Rio. O repositório está
disponível no link:
<https://git.tecgraf.puc-rio.br/geoband/damagezonemodeling>.

Este script também pode ser importado como um módulo e contém a
seguinte função:
    * main - a função principal do script
"""

from pathlib import Path

from damagezonemodeling.damagezone2D import DamageZone2D
from damagezonemodeling.fault import ParabolicDistribution
from damagezonemodeling.geo import Angle, Point
from damagezonemodeling.initial_conditions import SPLinear
from damagezonemodeling.material import MohrCoulomb


def main(debug=False, graphical_interface=True, write_input_files=True):
    # Obtendo caminho do arquivo
    path = Path(__file__)

    # Instância da classe principal
    damagezone = DamageZone2D()

    # Preparação do modo debug para testes
    # No uso normal, ignore essa linha
    damagezone.debug = debug

    # Adição da falha no modelo
    fault_length = 1000
    fault_angle = Angle(-60, "deg")
    cos_angle = abs(fault_angle.sin())
    center_point = Point(0, -1500 * cos_angle)
    damagezone.faults.add_by_len_ang(
        fault_length, fault_angle, center_point, dist=ParabolicDistribution(0.1)
    )

    # Lista de materiais
    materials = [MohrCoulomb(17000, 0.3, 34, 24, 6)] * 1

    # Cria as camadas
    divisions = []
    border_points = [Point(-1750, -3000 * cos_angle), Point(1750, 0)]
    damagezone.layers.set(materials, divisions, border_points=border_points)

    # Tensões iniciais
    damagezone.init_cond.set_stress(SPLinear(0.0, [0.012] * 1, [1] * 1))

    # Gera a malha do modelo
    damagezone.mesh.generate(recombine=True)

    # Escreve os arquivos de input do Abaqus
    if write_input_files:
        damagezone.write.time_points = None
        damagezone.write.input_file(str(path.parent.joinpath(path.stem + "_files")))

    # GUI
    if graphical_interface:
        damagezone.run_GUI()

    # Retorna o objeto
    return damagezone


if __name__ == "__main__":
    main()

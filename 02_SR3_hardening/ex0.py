"""Modelo com uma falha normal definida por seu comprimento e ângulo

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
from damagezonemodeling.geo import Angle, Point
from damagezonemodeling.initial_conditions import SPConstant
from damagezonemodeling.material import SoftRockPlasticity


def main(debug=False, graphical_interface=True, write_input_files=True):
    # Obtendo caminho do arquivo
    path = Path(__file__)

    # Instância da classe principal
    # LDA igual a zero indica que se trata de um caso onshore
    damagezone = DamageZone2D()

    # Preparação do modo debug para testes
    # No uso normal, ignore essa linha
    damagezone.debug = debug

    # Adição da falha no modelo
    fault_length = 1000
    fault_angle = Angle(-65, "deg")
    center_point = Point(0, -1500)
    damagezone.faults.add_by_len_ang(fault_length, fault_angle, center_point)

    # Lista de materiais
    materials = [
        SoftRockPlasticity(
            E=17000,
            nu=0.3,
            beta=53.964891466634235,
            psi=43.26079688581402,
            Ny=2.5,
            f0=0.125,
            f1=0.0,
            alpha=1.0,
            epsilon_pl_vol=0.0,
            pc=[
                (1.00000000000000, 0.000000000000000000),
                (7.06294763792971, 0.08263518908695248),
                (8.152297958908775, 0.1015388971442698),
                (10.955945306199055, 0.1204426052015871),
                (13.344798919631785, 0.1393463132589044),
                (17.43348001051868, 0.15825002131622173),
                (23.723810409303724, 0.17715372937353902),
                (35.212436708824725, 0.19605743743085635),
                (49.16887545672694, 0.21496114548817363),
                (62.385545121659106, 0.23386485354549097),
                (77.27333284171391, 0.25276856160280825),
                (98.25211160380559, 0.2716722696601256),
                (119.55886680662206, 0.29057597771744287),
                (147.51885837843315, 0.30947968577476015),
                (180.85532088927266, 0.3283833938320775),
                (215.36312783127278, 0.34728710188939477),
                (261.10412786810616, 0.3661908099467121),
                (309.4572259864283, 0.3850945180040294),
                (362.7885379371842, 0.4039982260613467),
                (425.09683423058186, 0.42216061223406337),
                (485.3438135473557, 0.43958167652217933),
                (545.7429823799474, 0.4553347665699437),
                (606.9112800516123, 0.4692345519062064),
                (667.2956683758367, 0.48294900677131897),
                (726.5060439553314, 0.49629280069413123),
                (788.9221778129825, 0.5087099422611925),
                (851.2556377623446, 0.5205710924148034),
                (913.5517611079636, 0.5324322425684143),
                (974.9716786721885, 0.5441080622508749),
                (1036.527866237172, 0.555042560048735),
                (1098.4212876424174, 0.5654210664331445),
                (1160.3147090476627, 0.5757995728175539),
                (1222.1654600486302, 0.5861780792019634),
                (1280.5188790681964, 0.5961859246440726),
            ],
            pt=[
                (-0.085000000000000, 0.00000000000000000),
                (-1.7924162616470767, 0.2388687762665455),
                (-3.509900033836857, 0.26036711091996523),
                (-5.744352165548889, 0.2831627588714361),
                (-8.24111787227639, 0.30466109352485576),
                (-11.610985697308934, 0.3272714110051765),
                (-14.699090650368134, 0.34932573707204667),
                (-19.560810248180587, 0.3717507240812172),
                (-24.28317907866449, 0.3936197196769372),
                (-30.57147042694737, 0.41604470668610777),
                (-36.86967680402722, 0.43809903275297796),
                (-44.39060908625834, 0.46033868929099825),
                (-52.43233912326605, 0.48257834582901865),
                (-61.232289420907364, 0.5046326718958888),
                (-70.9972473229891, 0.5270576589050593),
                (-81.1551011783074, 0.5491119849719295),
                (-92.40088622577537, 0.5713516415099499),
                (-103.68496522580017, 0.5934059675768201),
            ],
            e0=0.05,
        )
    ]

    # Cria as camadas
    damagezone.layers.set(materials)

    # Borders fixed in two directions
    for border in damagezone.layers.borders:
        border.dofs_fixed = [1, 2]

    # Definição do estado de tensões
    # Tensão vertical efetiva de compressão igual a 10 MPa e K0_x = K0_z = 1.0
    damagezone.init_cond.set_stress(SPConstant(-10, 1.0), verify_compatibility=False)

    # Gera a malha do modelo
    damagezone.mesh.generate(recombine=True)

    # Escreve os arquivos de input do Abaqus
    if write_input_files:
        damagezone.write.input_file(str(path.parent.joinpath(path.stem + "_files")))

    # GUI
    if graphical_interface:
        damagezone.run_GUI()

    # Retorna o objeto
    return damagezone


if __name__ == "__main__":
    main()

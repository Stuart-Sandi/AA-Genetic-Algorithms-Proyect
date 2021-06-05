# IMPORTS
from View.MainWindow import MainWindow
from View.FractalWindow import FractalWindow
from Model.Fractal import Tree
from Model.GeneticAlgorithm import Algoritmo


# CLASSES
class Controller:
    mainWindow = fractalWindow = None

    def __init__(self):
        '''
        Constructor
        '''

        # Window Instance
        self.mainWindow = MainWindow(self)

    def probarAlgoFractales(self):
        """
        Function: This function is going show fractal algorithm
        Inputs:
        Outputs:
        """

        self.fractalWindow = FractalWindow(self)
        self.fractalWindow.main()

        return

    def fractales(self):
        """
        Function: This function is going to create a fractal with some parameters
        Inputs:
        Outputs:
        """

        depth, thickness, branch_thickness, fork_angle, branch_quantity, base_len = self.validarDatosFractales()
        if depth != -1:
            Tree(depth, thickness, branch_thickness, fork_angle, branch_quantity, base_len)
        else:
            self.fractalWindow.showMessagesBox("¡Faltan valores o valores incorrectos!")
            self.fractalWindow.window.destroy()
            self.fractalWindow = FractalWindow(self)
            self.fractalWindow.main()
        return

    def validarDatosFractales(self):
        w = self.fractalWindow

        # OBTIENE LOS DATOS DE LA PANTALLA
        depth = w.comboBoxDepth.get()
        thickness = w.comboBoxThickness.get()
        branch_thickness = w.entryBranchT.get()
        fork_angle = w.entryForkAngle.get()
        branch_quantity = w.entryBranchQ.get()
        base_len = w.entryBaseLen.get()

        # VALIDA QUE NO SEAN NULOS
        if depth != "" and \
                thickness != "" and \
                branch_thickness != "" and \
                fork_angle != "" and \
                branch_quantity != "" and \
                base_len != "":

            try:
                depth = int(depth)
                thickness = int(thickness)

                tmp = branch_thickness.split(",")
                branch_thickness = (int(tmp[0]), int(tmp[1]))

                tmp = fork_angle.split(",")
                fork_angle = (float(tmp[0]), float(tmp[1]))

                tmp = branch_quantity.split(",")
                branch_quantity = (int(tmp[0]), int(tmp[1]))

                tmp = base_len.split(",")
                base_len = (int(tmp[0]), int(tmp[1]))

                return depth, thickness, branch_thickness, fork_angle, branch_quantity, base_len

            except:
                return -1, 0, 0, 0, 0, 0

        return -1, 0, 0, 0, 0, 0

    def main(self):
        '''
        Function: This function is going to create a Window with all its characteristics
        Inputs:
        Outputs:
        '''

        #self.mainWindow.main()
        algoritmo = Algoritmo()
        print(algoritmo.fitness("../ImagenPrueba1.png", "../ImagenPrueba3.png"))



# This is going to create a controller and call main function
if __name__ == '__main__':
    controller = Controller()
    controller.main()

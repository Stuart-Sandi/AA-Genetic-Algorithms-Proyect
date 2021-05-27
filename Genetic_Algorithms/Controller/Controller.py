
# IMPORTS
from View.MainWindow import Window
from Model.Fractal import Tree

# CLASSES
class Controller:

    tree = None

    def __init__(self):
        '''
        Constructor
        '''
        self.tree = Tree()

        # Window Instance
        self.window = Window(self)

    def main(self):
        '''
        Function: This function is going to create a Window with all its characteristics
        Inputs:
        Outputs:
        '''

        #self.window.main()


# This is going to create a controller and call main function
if __name__ == '__main__':
    controller = Controller()
    controller.main()


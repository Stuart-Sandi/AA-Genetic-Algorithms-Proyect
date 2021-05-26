
# IMPORTS
from View.MainWindow import Window

# CLASSES
class Controller:

    def __init__(self):
        '''
        Constructor
        '''

        # Window Instance
        self.window = Window(self)

    def main(self):
        '''
        Function: This function is going to create a Window with all its characteristics
        Inputs:
        Outputs:
        '''
        self.window.main()


# This is going to create a controller and call main function
if __name__ == '__main__':
    controller = Controller()
    controller.main()
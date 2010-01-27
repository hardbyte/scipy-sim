'''
Created on 23/11/2009

@author: brian
'''
from models.actors import Plotter, Ramp, Channel, Model

class RampPlot(Model):
    '''This example simulation connects a ramp source to a plotter.'''
    def __init__(self):
        '''Create the components'''
        super(RampPlot, self).__init__()
        connection = Channel()
        src = Ramp(connection)
        dst = Plotter(connection)
    
        self.components = [src, dst]

if __name__ == '__main__':
    RampPlot().run()

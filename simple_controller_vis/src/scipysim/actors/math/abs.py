'''
Created on 9/12/2009

@author: brian
'''
from scipysim.actors import Siso

class Abs(Siso):
    '''
    This actor takes a source and passes on the absolute value. 
    '''
    def __init__(self, input_queue, output_queue):
        '''
        Constructor for the absolute actor. 
        '''
        super(Abs, self).__init__(input_queue=input_queue,
                                  output_queue=output_queue)

    def siso_process(self, obj):
        if obj['value'] < 0:
            obj['value'] *= -1
        return obj

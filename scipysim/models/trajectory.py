"""
A model based on the bouncing ball example in simulink.
"""
from scipysim.actors import CompositeActor, MakeChans
from scipysim.actors.signal import Split
from scipysim.actors.math import Constant
from scipysim.actors.math import CTIntegratorForwardEuler as Integrator
from scipysim.actors.display import Plotter

import logging
logging.basicConfig(level=logging.INFO)
logging.info("Logger enabled")

class ThrownBall(CompositeActor):
    '''
    A simple example simulation where ...
    '''

    def __init__(self):
        '''
        A basic simulation that ...
        '''
        wires = MakeChans(10)

        gravity = -9.81
        initial_position = 10 # vertical meters
        initial_velocity = 15 # m/s vertical, up is positive 

        self.components = [
            Constant(wires[0], value=gravity, resolution=100, simulation_time=4),
            Integrator(wires[0], wires[1], initial_velocity),
            Split(wires[1], [wires[2], wires[3]]),
            Plotter(wires[2], title="Velocity", own_fig=True, xlabel="Time (s)", ylabel="(m/s)"),
            Integrator(wires[3], wires[4], initial_position),
            Split(wires[4], [wires[5], wires[6]]),
            Plotter(wires[5], title="Displacement", own_fig=True, xlabel="Time (s)", ylabel="(m)"),
        ]


if __name__ == '__main__':
    ThrownBall().run()

"""
A model based on the bouncing ball example in simulink.
This version compares the discrete-time and quantized-state integrators.
"""
from scipysim.actors import CompositeActor, MakeChans
from scipysim.actors.signal import Split
from scipysim.actors.math import Constant
from scipysim.actors.math import CTIntegratorForwardEuler as Integrator
from scipysim.actors.math import CTIntegratorQS1 as QSIntegrator
from scipysim.actors.display import StemPlotter

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
            # Split into fixed-step and DE streams
            Split(wires[0], [wires[1], wires[2]]),
            # Integrate to get velocity
            Integrator(wires[1], wires[3], initial_velocity),
            QSIntegrator(wires[2], wires[4], initial_velocity, delta=0.1 ),
            # Integrate to get displacement
            Integrator(wires[3], wires[5], initial_position),
            QSIntegrator(wires[4], wires[6], initial_position, delta=0.1 ),
            # Plot
            StemPlotter(wires[5], title="Displacement (discrete-time integration)", live=True, xlabel="Time (s)", ylabel="(m)"),
            StemPlotter(wires[6], title="Displacement (quantized-state integration)", live=True, xlabel="Time (s)", ylabel="(m)"),
        ]


if __name__ == '__main__':
    ThrownBall().run()

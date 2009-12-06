'''
This dynamic stemmer shows a live signal stream.
'''

from Actor import Actor
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import logging
import threading
import copy

GUI_LOCK = threading.Condition()

import time

class Stemmer(Actor):
    '''
    This actor shows a signal dynamically as it comes off the buffer with matplotlib.
    The max refresh rate is an optional input - default is 2Hz.
    '''
    # TODO: It should be possible to refactor Plotter and Stemmer actors
    # into a single actor (or subclasses of a common plotting actor).
    # Perhaps it would make more sense to do this after we've added
    # type tags to the signals.

    def __init__(self, input_queue, refresh_rate=2):
        super(Stemmer, self).__init__(input_queue=input_queue)
        self.x_axis_data = []
        self.y_axis_data = []
        assert refresh_rate != 0
        self.refresh_rate = refresh_rate
        plt.ion()
        
        # stem() doesn't seem to like empty datasets, so we'll defer creating
        # the plot until there's actually data. For now just create an
        # empty canvas
        plt.draw()
        self.markerline = None  
        self.stemlines = None
        self.baseline = None
        
        self.refreshs = 0

        self.last_update = 0

    def process(self):
        '''
        plot any values in the buffer
        '''
        obj = self.input_queue.get(True)     # this is blocking
        if obj is None:
            logging.info("We have finished processing the queue of data to be displayed")
            self.update_plot()
            self.stop = True
            return

        self.x_axis_data.append(obj['tag'])
        self.y_axis_data.append(obj['value'])
        logging.debug("Stemmer received values ( %e,%e ) Now have %i values." % (self.y_axis_data[-1], self.x_axis_data[-1], len(self.x_axis_data)))
        obj = None

        if time.time() - self.last_update > 1.0 / self.refresh_rate:
            self.update_plot()


    def update_plot(self):
        '''
        Update the internal data stored by matplotlib and cause a redraw.
        If this has been called more than 1000 times -> quit.
        '''
        logging.debug("Updating plot (refresh: %i)" % self.refreshs)
        self.last_update = time.time()

        # This is a safety check - if we are plotting over a long time period this needs removing
        if self.refreshs >= 1000:
            logging.info("We have updated the plot 1000 times - forcing a stop of the simulation now")
            self.stop = True
            return
        self.refreshs += 1

        with GUI_LOCK:
            if not self.markerline:
                self.markerline, self.stemlines, self.baseline = plt.stem(self.x_axis_data, self.y_axis_data)
            else:
                axes = self.markerline.get_axes()
                
                # The markerline can be built directly from the data
                self.markerline.set_data(self.x_axis_data, self.y_axis_data)
                self.markerline.recache()
                
                # The baseline should be built from the start and end points of
                # the x axis
                _ , baseline_y = self.baseline.get_data()
                self.baseline.set_data([min(self.x_axis_data),max(self.x_axis_data)], baseline_y.tolist())
                self.baseline.recache()
                
                # Construct new stemlines and add them to the current plot
                for x, y in zip(self.x_axis_data, self.y_axis_data)[len(self.stemlines):]:
                    stemline = lines.Line2D([0],[0])
                    stemline.update_from(self.stemlines[0]) # Copy format
                    stemline.set_data([x, x], [baseline_y[0], y])
                    stemline.recache()
                    axes.add_line(stemline)
                    self.stemlines.append(stemline)

                axes.relim()
                axes.autoscale_view()
                plt.draw() # redraw the canvas
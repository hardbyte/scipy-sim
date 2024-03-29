'''
Created on Feb 5, 2010

@author: brianthorne
'''

from scipysim.actors.io import Bundle
from scipysim.actors import Actor, DisplayActor, Channel, Event, LastEvent
from bundlePlotter import BundlePlotter

import numpy

import unittest
import os

class BundlePlotTests( unittest.TestCase ):
    def setUp( self ):
        self.q_in = Channel()
        self.q_out = Channel()
        self.q_out2 = Channel()
        self.input = [Event(value=1, tag=i) for i in xrange( 100 )]
        self.title = "test plot"
        
        self.url = os.path.join(os.getcwd() , self.title) + ".png"

    def tearDown( self ):
        del self.q_in
        del self.q_out
        try:
            os.remove(self.url)
        except OSError:
            pass
            

    def test_getting_bundle_data( self ):
        '''Test bundling a signal and getting the data back'''

        block = Bundle( self.q_in, self.q_out )
        block.start()
        [self.q_in.put( i ) for i in self.input + [LastEvent()]]
        block.join()
        bundled_data = self.q_out.get()
        self.assertEqual( len( bundled_data ), 100 )
        self.assertEqual( type( bundled_data ), numpy.ndarray )
        values = bundled_data["Value"]
        self.assertTrue( all( values == 1 ) )
        tags = bundled_data["Tag"]
        [self.assertEquals( tags[i] , i ) for i in xrange( 100 ) ]

    def test_plotting( self ):
        bundler = Bundle( self.q_in, self.q_out )
        bundlingPlotter = BundlePlotter( self.q_out, self.title )
        [block.start() for block in [bundler, bundlingPlotter]]
        [self.q_in.put( i ) for i in self.input + [LastEvent()]]
        [block.join() for block in [bundler, bundlingPlotter]]
        self.assertTrue(os.path.exists(self.url))

if __name__ == "__main__":
    unittest.main()

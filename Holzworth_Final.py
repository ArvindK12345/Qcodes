import qcodes
import socket
import logging
from qcodes import IPInstrument, Instrument, validators as vals


class HS9004A(IPInstrument):

#    qcodes IPInstrument class allows direct communication to a TCP/IP device using the "Socket" package.
#    Arguments:
#    def __init__(name, address, port, timeout, terminator, persistent, 
#                    write_confirmation, **kwargs), 
#    Name = Name given to instrument in script
#    Address = IP address of instrument
#    Port = IP port within IP address (9760 for Holzworth on BlueFors)
#    Timeout = Seconds to allow for responses
#    Terminator = Character to end each send command. ('\n' for C based devices)
#    Persistent (True/False) = Whether to leave socket open between send commands.
#    write_confirmation (True/False) – Whether there are some responses we need to read.
    
    



    def __init__(self, name, address='192.168.150.11', port=9760, timeout=5, terminator='\n', persistent=True, write_confirmation=True, **kwargs):
        
        super().__init__(name, address=address, port=port,
                         terminator=terminator, timeout=timeout, **kwargs)
        
        self._address = '192.168.150.11'
        self._port = 9760
        self._timeout = 2
        self._terminator = '\n'
        self._confirmation = write_confirmation
        self._buffer_size = 128 # TCP Buffer size. Reset to 1400 in case of error (works 
                                    # with this value)
        
        print('Syntax: "Name.ch{}_Parameter(\'Parameter_Value\')" \n Parameters: "Frequency, Power, Phase, Output (1 or 0 Boolean), Temperature (get only)"' )        
        

#    Write .format() commands to send to the instrument.
#    Write seperate set command for each setting for ease of incorporating the units.
#    getcmd works for all settings.

        
        def setfreq(channel, setting): #Works I think.
            return ':CH{}:'.format(channel) + setting + ':' + '{}' + 'MHz'
            
        def setpwr(channel, setting): #Works I think.
            return ':CH{}:'.format(channel) + setting + ':' + '{}' + 'dBm'

        def setphase(channel, setting): #Works I think.
            return ':CH{}:'.format(channel) + setting + ':' + '{}' + 'deg'
        
        def RFoutput(channel, setting): # Check mapping
            return ':CH{}:'.format(channel) + setting + ':' + '{}'
       
        def getcmd(channel, setting): # WORKS FOR ALL, DO NOT CHANGE!!
            return ':CH{}:'.format(channel) + setting + '?'
        
        
        for chan in [1,2,3,4]:
            
            self.add_parameter('ch{}_freq'.format(chan),
                               label = 'Channel {} Frequency'.format(chan),
                               get_cmd = getcmd(chan, 'FREQ'),
                               set_cmd = setfreq(chan, 'FREQ'),
                               get_parser = str,
                               set_parser = float,
                              )
            
            self.add_parameter('ch{}_pwr'.format(chan),
                               label = 'Channel {} Power'.format(chan),
                               get_cmd = getcmd(chan, 'PWR'),
                               set_cmd = setpwr(chan, 'PWR'),
                               get_parser = str,
                               set_parser = float,
                              )
            
            self.add_parameter('ch{}_phase'.format(chan),
                               label = 'Channel {} Phase'.format(chan),
                               get_cmd = getcmd(chan, 'PHASE'),
                               set_cmd = setphase(chan, 'PHASE'),
                               get_parser = str,
                               set_parser = float,
                              )
           
            self.add_parameter('ch{}_output'.format(chan),
                               label = 'Channel {} Output'.format(chan),
                               get_cmd = getcmd(chan, 'PWR:RF'),
                               set_cmd = RFoutput(chan, 'PWR:RF'),
                               get_parser = str,
                               #set_parser = float,
                               val_mapping={1:'ON', 0:'OFF'},
                              )            
            
            self.add_parameter('ch{}_temp'.format(chan),
                               label = 'Channel {} Temperature'.format(chan),
                               get_cmd = getcmd(chan, 'TEMP'),
                               get_parser = str,
                              )            
            
            
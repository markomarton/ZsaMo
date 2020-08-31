# ZsaMo
General instrument control layer for the Budapest Neutron Centre Instruments

## conf.ini file structure
The server can be configured using a configuration file read by the <code>configparser</code> module

## Command structure
The reseived commands are processed using <code>argparse</code> module...
 
getPos: get the position of an axis
move: move a target to a given position
isMoving: ask for an axis status (moving[True] or not[False])
stop: stops all movements
restart: restart the PLC if it was phisicaly stopped (not implemented)
getStatus: get the status of an axis

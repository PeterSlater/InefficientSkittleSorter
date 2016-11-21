#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  DemoIK.py - York Hack Space May 2014
#  Simple demo of meArm library to walk through some points defined in Cartesian coordinates

import meArm

def main():
    arm = meArm.meArm()
    arm.begin()
 
    #test base
    #arm.goDirectlyTo(-195, 100, 50)
    #arm.goDirectlyTo(0, 200, 50)
    #arm.goDirectlyTo(195, 100, 50)

    #test shoulder & elbow
    #arm.goDirectlyTo(0, 25, 50)
    #arm.goDirectlyTo(-25, 25, 50)
    #arm.goDirectlyTo(-25, 50, 50)    
    #arm.goDirectlyTo(0, 50, 50)
    #arm.goDirectlyTo(25, 50, 50) 
    #arm.goDirectlyTo(25, 25, 50)
    #arm.goDirectlyTo(0, 25, 50) 
    
    arm.goDirectlyTo(0, 50, 50)
    arm.goDirectlyTo(-25, 50, 50)
    arm.goDirectlyTo(-50, 50, 50)
    arm.goDirectlyTo(-75, 50, 50)
    
    #move y
    #arm.gotoPoint(0, 50, 50)  
    #arm.gotoPoint(0, 75, 50) 
    #arm.gotoPoint(0, 100, 50) 
    #arm.gotoPoint(0, 75, 50) 
    #arm.gotoPoint(0, 50, 50) 
    
    
        
    #while True:
        #arm.openGripper()
        #arm.closeGripper()

        #arm.gotoPoint(0, 150, 50)
        #arm.gotoPoint(50, 100, 50)
        #arm.gotoPoint(100, 100, 50)


if __name__ == '__main__':
    main()

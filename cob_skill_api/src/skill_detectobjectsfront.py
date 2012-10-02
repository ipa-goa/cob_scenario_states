#!/usr/bin/env python

#################################################################
##\file
#
# \note
# Copyright (c) 2012 \n
# Fraunhofer Institute for Manufacturing Engineering
# and Automation (IPA) \n\n
#
#################################################################
#
# \note
# Project name: Care-O-bot Research
# \note
# ROS package name: cob_skill_api
#
# \author
# Author: Thiago de Freitas Oliveira Araujo, 
# email:thiago.de.freitas.oliveira.araujo@ipa.fhg.de
# \author
# Supervised by: Florian Weisshardt, email:florian.weisshardt@ipa.fhg.de
#
# \date Date of creation: September 2012
#
# \brief
# Skill state detect objects re-implementation using the skills API
#
#################################################################
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer. \n
# - Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution. \n
# - Neither the name of the Fraunhofer Institute for Manufacturing
# Engineering and Automation (IPA) nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission. \n
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License LGPL as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License LGPL for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License LGPL along with this program.
# If not, see < http://www.gnu.org/licenses/>.
#
#################################################################

import abc
from abc_skill import SkillsBase
import yaml

import roslib
roslib.load_manifest('cob_skill_api')
import rospy
import smach
import smach_ros
from actionlib import *
from actionlib.msg import *
import random

import condition_check
import skill_state_approachpose

import tf
from tf.msg import tfMessage 
from tf.transformations import euler_from_quaternion

import skill_state_detectobjectsfront

import condition_check

class SkillImplementation(SkillsBase):

    def __init__(self, object_names = ['milk']):
    
        rospy.loginfo("Executing the detect object fronts Machine")
        smach.StateMachine.__init__(self,outcomes=['success', 'failed'], output_keys=['objects'])
        rospy.set_param("detect_object_table/torso_poses",['home','front','back','left','right'])
        
        self.check_pre = self.pre_conditions()
        self.check_post = self.post_conditions()
        
        with self:
            self.userdata.object_names = object_names
            self.add("PRECONDITIONS_DETECT_FRONT", self.check_pre, transitions={'success':'DETECT_OBJECT_FRONT', 'failed':'PRECONDITIONS_DETECT_FRONT'})
            self.add('DETECT_OBJECT_FRONT',skill_state_detectobjectsfront.skill_state_detectobjectsfront(object_names=self.userdata.object_names, components = self.check_pre.full_components),
                     transitions={'not_detected':'failed',
                                  'failed':'failed','detected':'success'})
    
    def pre_conditions(self):
    
        check_pre = condition_check.ConditionCheck(checkType="pre_detect_object_front_check")
        return check_pre
        
    def post_conditions(self):
        print "Some postconditions"
    
    @property    
    def inputs(self):
        return "Some Input"
    
    @property
    def outputs(self):
        return "Some Output"
    
    @property
    def requirements(self):
        return "Some Requirements"

if __name__=='__main__':
    rospy.init_node('detect_object_frontside')
    sm = SkillImplementation()
    sis = smach_ros.IntrospectionServer('SM', sm, 'SM')
    sis.start()
    outcome = sm.execute()
    rospy.spin()

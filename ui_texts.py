##########################################################################################
#	GPL LICENSE:
#-------------------------
# This file is part of FootRollBreak.
#
#    FootRollBreak is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    FootRollBreak is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with FootRollBreak.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################################
#
#	Copyright 2015 Julien Duroure (contact@julienduroure.com)
#
##########################################################################################

ui_text = '''
import bpy

rig_id = ###rig_id###

#Needed for footbreakroll still working after removing addon
bpy.types.PoseBone.footrollbreak = bpy.props.BoolProperty()
bpy.types.PoseBone.footrollbreak_return = bpy.props.BoolProperty()


class FootRollBreakUI(bpy.types.Panel):

	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = "FootRoll Break"
	bl_idname = rig_id + "_PT_FootRollBreak_ui"


	@classmethod
	def poll(self, context):
		if context.mode != 'POSE':
			return False

		try:
			return (context.active_object.data.get("rig_id") == rig_id)
		except (AttributeError, KeyError, TypeError):
			return False
		

	def draw(self, context):
		layout = self.layout
		row_ = layout.row()
		row_.prop(context.active_object.pose.bones["###bone###.L"], "footrollbreak", text="FootRoll Break (L)") 

		if context.active_object.pose.bones["###bone###.L"].footrollbreak == True:
			if context.active_object.pose.bones["###bone_roll###.L"]["complexity"] == "FULL":
				row_ = layout.row()
				box = row_.box()
				row = box.row()
				row.prop(context.active_object.pose.bones["###bone###.L"], '["footrollbreak_angle"]', text="Angle")
				row = box.row()
				col = row.column()
				col.prop(context.active_object.pose.bones["###bone###.L"], "footrollbreak_return", text="Return")
				col = row.column()
				if context.active_object.pose.bones["###bone###.L"].footrollbreak_return == True:
					row__ = col.row()
					row__.prop(context.active_object.pose.bones["###bone###.L"], '["footrollbreak_angle_max"]', text="Angle Max")
					row__ = col.row()
					col.prop(context.active_object.pose.bones["###bone###.L"], '["footrollbreak_corrective_angle"]', text="Corrective")
				
			else:
				row_.prop(context.active_object.pose.bones["###bone###.L"], '["footrollbreak_angle"]', text="Angle")
		
		row_ = layout.row()

		row_.prop(context.active_object.pose.bones["###bone###.R"], "footrollbreak", text="FootRoll Break (R)") 

		if context.active_object.pose.bones["###bone###.R"].footrollbreak == True:
			if context.active_object.pose.bones["###bone_roll###.R"]["complexity"] == "FULL":
				row_ = layout.row()
				box = row_.box()
				row = box.row()
				row.prop(context.active_object.pose.bones["###bone###.R"], '["footrollbreak_angle"]', text="Angle")
				row = box.row()
				col = row.column()
				col.prop(context.active_object.pose.bones["###bone###.R"], "footrollbreak_return", text="Return")
				col = row.column()
				if context.active_object.pose.bones["###bone###.R"].footrollbreak_return == True:
					row__ = col.row()
					row__.prop(context.active_object.pose.bones["###bone###.R"], '["footrollbreak_angle_max"]', text="Angle Max")
					row__ = col.row()
					col.prop(context.active_object.pose.bones["###bone###.R"], '["footrollbreak_corrective_angle"]', text="Corrective")
				
			else:
				row_.prop(context.active_object.pose.bones["###bone###.R"], '["footrollbreak_angle"]', text="Angle")


def register():
	bpy.utils.register_class(FootRollBreakUI)
	
def unregister():
	bpy.utils.unregister_class(FootRollBreakUI)

	
register()
'''

text_drivers = '''
import bpy
import math
import mathutils

def get_length_coeff(obj, side, toe_def, foot_def, toe_top):
	return (obj.bones[toe_def + side].matrix_local.to_translation() - obj.bones[toe_top + side ].matrix_local.to_translation()).length / (obj.bones[foot_def + side].matrix_local.to_translation() - obj.bones[toe_def + side].matrix_local.to_translation()).length

#Driver used by intermediate roll bone to follow anim roll bone (and back in case of return full method)
def driver_rollbreak(return_enable, current_angle, angle, angle_max):
	if return_enable == True:
		if current_angle <= angle:
			return angle*2* math.pi/360
		elif current_angle >= angle and current_angle < angle_max:
			return (- angle / ( angle_max - angle ) * ( current_angle - angle_max) * 2 * math.pi / 360)
		else:
			return 0.0
	else:
		return angle*2* math.pi/360

#Driver used by Top toe bone to compensate return of intermediate roll bone
def driver_rollbreak_return(side, angle, corrective):
    obj = bpy.data.armatures["###armature###"]
    a = ###a###
    b = ###b###
    c = ###c###
    d = ###d###
    coeff_length =   get_length_coeff(obj, side, "###toe_def###", "###foot_def###", "###toe_top###")
    slop         = a + b*coeff_length + c*coeff_length*coeff_length + d*coeff_length*coeff_length*coeff_length
    return (angle * slop + corrective) * 2 *math.pi / 360

bpy.app.driver_namespace["driver_rollbreak"] = driver_rollbreak
bpy.app.driver_namespace["driver_rollbreak_return"] = driver_rollbreak_return

'''

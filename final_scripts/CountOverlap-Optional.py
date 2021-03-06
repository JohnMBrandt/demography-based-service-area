
# CountOverlap.py

# Description: 
# Given a polygon feature class or layer containing overlapping polygons, creates a new feature class with the overlaps removed and the number of overlapping polygons.
# ---------------------------------------------------------------------------

# Set the necessary product code
# import arcinfo


# Import arcpy module
import arcpy

# Script arguments
Input_Features = arcpy.GetParameterAsText(0)

Output_Feature_Class = arcpy.GetParameterAsText(1)

# Local variables:
in_memory = "in_memory"
empty = "in_memory\\empty"
Spaghetti = ""
oidfield = Spaghetti
Meatballs = "in_memory\\meatballs"
count_overlaps = "in_memory\\overlap_count"
Features_to_Delete = "features_to_delete"
Features_Deleted = Features_to_Delete
Delete_succeeded = "false"

# Process: Create Feature Class
arcpy.CreateFeatureclass_management(in_memory, "empty", "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")

# Process: Feature To Polygon
arcpy.FeatureToPolygon_management("''", Spaghetti, "", "NO_ATTRIBUTES", empty)

# Process: Calculate Value
arcpy.CalculateValue_management("GetOidFieldName(r\"%Spaghetti%\")", "import arcpy\\ndef GetOidFieldName(path):\\n  fc = arcpy.Describe(path)\\n  return fc.oidfieldname\\n\\n  ", "Field")

# Process: Feature To Point
arcpy.FeatureToPoint_management(Spaghetti, Meatballs, "INSIDE")

# Process: Spatial Join
arcpy.SpatialJoin_analysis(Meatballs, Input_Features, count_overlaps, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "WITHIN", "", "")

# Process: Join Field
arcpy.JoinField_management(Spaghetti, oidfield, count_overlaps, "ORIG_FID", "Join_Count")

# Process: Make Feature Layer
arcpy.MakeFeatureLayer_management(Output_Feature_Class, Features_to_Delete, "Join_Count = 0", "", "FID_empty FID_empty VISIBLE NONE;SHAPE_length SHAPE_length VISIBLE NONE;SHAPE_area SHAPE_area VISIBLE NONE;Join_Count Join_Count VISIBLE NONE")

# Process: Delete Features
arcpy.DeleteFeatures_management(Features_to_Delete)

# Process: Delete
arcpy.Delete_management(Features_to_Delete, "")


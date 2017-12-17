import sys, math, string, arcpy, os, traceback

arcpy.env.overwriteOutput = True

try:


    # Import shapefile
    InputShapeFile = arcpy.GetParameterAsText(0)
    arcpy.AddMessage('\n' + "The input shapefile is" + InputShapeFile)

    # User input of field to be normalized by area
    InputField = arcpy.GetParameterAsText(1)
    norm_field = arcpy.GetParameterAsText(2)

    # User input of field to contain the calculated data
    OutputField = arcpy.GetParameterAsText(3)
    arcpy.AddMessage("The name of the field to be added is " + OutputField + "\n")

    # User input of location to save output shapefile
    OutputShapeFile = arcpy.GetParameterAsText(4)
    arcpy.AddMessage('\n' + "The output shapefile is" + OutputShapeFile)



    arcpy.Intersect_analysis(in_features="fuck_CalcField8 #;tl_2013_36_cousub_Dissolve #",
                             out_feature_class="C:/Users/John/Documents/ArcGIS/Default.gdb/fuck_CalcField8_Intersect",
                             join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="INPUT")

    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
    # The following inputs are layers or table views: "fuck_CalcField8_Intersect"
    arcpy.Dissolve_management(in_features="fuck_CalcField8_Intersect",
                              out_feature_class="C:/Users/John/Documents/ArcGIS/Default.gdb/fuck_CalcField8_Intersect_Di",
                              dissolve_field="COUNTYFP", statistics_fields="perc_tot SUM;DP0080001 SUM",
                              multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")


    # Create a new copy of the shapefile and save it as the output shape file
    arcpy.Copy_management(InputShapeFile, OutputShapeFile)
    arcpy.AddMessage('\n' + "Copied")

    arcpy.AddField_management(OutputShapeFile, OutputField, "DOUBLE", 20, 5)
    arcpy.AddMessage('\n' + "New Field Added")

    # Create a list of iterable records for our for loop
    ShpRecords = arcpy.UpdateCursor(OutputShapeFile)
    arcpy.AddMessage('\n' + "List made")


    # Generate variable that contains the name of the column containing shape data
    shapefield = arcpy.Describe(OutputShapeFile).shapeFieldName
    arcpy.AddMessage('\n' + "New Field made")


    # Iterate over each index in the shapefile
    for record in ShpRecords:
        # Get the data associated with the shape
        #shape = record.getValue(shapefield)
        # Get the value of the data in the column to be normalzied
        numerator = record.getValue(InputField)
        denominator = record.getValue(norm_field)
        # Normalize the numerator to the area
        result = numerator*denominator
        # Save normalized data to the newly calculated value
        record.setValue(OutputField, result)
        ShpRecords.updateRow(record)

    # Get rid of the ShpRecords
    del ShpRecords
    del record


except Exception as e:
    arcpy.AddError('\n' + "Script failed because: \t\t" + e.message )
    exceptionreport = sys.exc_info()[2]
    arcpy.AddError("at this location: \n\n" + traceback.format_tb(exceptionreport)[0]+ "\n")









import sys, math, string, arcpy, os, traceback

arcpy.env.overwriteOutput = True

try:


    # Import shapefile
    InputShapeFile = arcpy.GetParameterAsText(0)
    InputCensusFile = arcpy.GetParameterAsText(1)
    arcpy.AddMessage('\n' + "The input shapefile is" + InputShapeFile)

    # User input of field to be normalized by area
    InputField = arcpy.GetParameterAsText(2)
    norm_field = arcpy.GetParameterAsText(3)

    dissolve_field = arcpy.GetParameterAsText(4)

    # User input of field to contain the calculated data
    OutputField = arcpy.GetParameterAsText(5)
    arcpy.AddMessage("The name of the field to be added is " + OutputField + "\n")

    # User input of location to save output shapefile
    OutputShapeFile = arcpy.GetParameterAsText(6)
    arcpy.AddMessage('\n' + "The output shapefile is" + OutputShapeFile)



    outPutIntersect = arcpy.Intersect_analysis([InputShapeFile, InputCensusFile],
                             join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="INPUT")

    dissolved = arcpy.Dissolve_management(in_features=outPutIntersect,
                              out_feature_class=OutputShapeFile,
                              dissolve_field=dissolve_field, statistics_fields=norm_field + " SUM;" + InputField + " SUM",
                              multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")



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
        len_inp_field = len(InputField) # 9
        numfield = "SUM_" + InputField[:6]
        denfield = "SUM_" + norm_field[:6]
        arcpy.AddMessage(len(numfield))
        arcpy.AddMessage(numfield)
        numerator = record.getValue(numfield)
        denominator = record.getValue(denfield)
        # Normalize the numerator to the area
        result = denominator/numerator
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









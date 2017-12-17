# Import packages
import sys, math, string, arcpy, os

arcpy.env.overwriteOutput = True

try:

    # Import shapefile
    InputShapeFile = arcpy.GetParameterAsText(0)
    arcpy.AddMessage('\n' + "The input shapefile is" + InputShapeFile)

    # User input of field to be normalized by area
    InputField = arcpy.GetParameterAsText(1)

    # User input of field to contain the calculated data
    OutputField = arcpy.GetParameterAsText(2)

    # User input of location to save output shapefile
    OutputShapeFile = arcpy.GetParameterAsText(3)
    arcpy.AddMessage('\n' + "The output shapefile is" + OutputShapeFile)

    # Create a new copy of the shapefile and save it as the output shape file
    arcpy.Copy_management(InputShapeFile, OutputShapeFile)

    # Create a list of iterable records for our for loop
    ShpRecords = arcpy.UpdateCursor(OutputShapeFile)

    # Create a new field to store calculated data
    arcpy.AddField_management(OutputShapeFile, OutputField)

    # Generate variable that contains the name of the column containing shape data
    shapefield = arcpy.Describe(OutputShapeFile).shapeFieldName

    # Iterate over each index in the shapefile
    for record in ShpRecords:
        # Get the data associated with the shape
        shape = record.getValue(shapefield)
        # Get the value of the data in the column to be normalzied
        numerator = record.getValue(InputField)
        # From the shape data, extract the area
        area = shape.area
        # Normalize the numerator to the area
        result = numerator/area
        # Save normalized data to the newly calculated value
        record.setValue(OutputField, result)

    # Get rid of the ShpRecords
    del ShpRecords

except:
    # If everything above fails, log an error to the console.
    arcpy.AddMessage('\n' + "Something went wrong. \n")


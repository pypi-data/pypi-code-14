import numpy as np
from .gateway import workspace

def getSelectedRowValues( heatmap ):
    """get a 2D numpy array of values currently selected for the given heatmap in the OLIVER UI"""
    hmeui = workspace.getUIForHeatmap( heatmap )
    nCols = heatmap.getColumnCount()
    indices = hmeui.getSelectionRowIndices()
    jAllVals = heatmap.getValueMatrix();
    result = []
    for i in indices:
        rowVals = []
        for j in range( nCols ):
            rowVals.append( jAllVals[i][j] )
        result.append( rowVals )
    return np.array( result )

def getAllRowValues( heatmap ):
    """get a 2D numpy array of all values for the given heatmap"""
    nRows = heatmap.getRowCount()
    nCols = heatmap.getColumnCount()
    jAllVals = heatmap.getValueMatrix();
    result = []
    for i in range( nRows ):
        rowVals = []
        for j in range( nCols ):
            rowVals.append( jAllVals[i][j] )
        result.append( rowVals )
    return np.array( result )

def getXValues( heatmap ):
    jTimes = heatmap.getTimeLabels()
    nCols = heatmap.getColumnCount()
    result = []
    for i in range( nCols ):
        result.append( jTimes[i] )
    return np.array( result )
    
def getRowValues( heatmap, rowIndex ):
    jAllVals = heatmap.getValueMatrix();
    nCols = heatmap.getColumnCount()
    rowVals = []
    for i in range( nCols ):
        rowVals.append( jAllVals[0][i] )
    return np.array( rowVals )
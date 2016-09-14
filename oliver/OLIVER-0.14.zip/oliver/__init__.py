from .gateway import gateway, workspace
from .dataframes import getDataFrame, getHeatmap
from .numpy import getSelectedRowValues, getAllRowValues, getXValues, getRowValues
    
def getSelectedRowLabels( heatmap ):
    """get a list of row labels currently selected for the given heatmap in the OLIVER UI"""
    hmeui = workspace.getUIForHeatmap( heatmap )
    jResult = hmeui.getSelectionRowLabels( False )
    result = []
    for i in range( jResult.size() ):
        result.append( jResult.get( i ) )
    return result
    
def getAllRowLabels( heatmap ):    
    """get a list of all row labels for the given heatmap"""
    jResult = heatmap.getRowLabels( False )
    nRows = heatmap.getRowCount()
    result = []
    for i in range( nRows ):
        result.append( jResult[i] )
    return result


def copyHeatmap( heatmap, title ):
    """create a deep copy of the given heatmap and give it a new title"""
    result = gateway.jvm.oliver.map.Heatmap( heatmap )
    result.setTitle( title )
    return result
	

def getAllOpenHeatmaps():
    """Return the full list of heatmaps currently visible in the OLIVER workspace"""
    return workspace.getOpenHeatmaps()
    
    
def getAllOpenHeatmapTitles():
    """Return a list of titles of all heatmaps currently visible in the OLIVER workspace"""
    openHeatmaps = workspace.getOpenHeatmaps()
    return [hm.getTitle() for hm in openHeatmaps]


def getOpenHeatmap( title=None ):
    """Return the only open heatmap, or a heatmap with the given title"""
    openHeatmaps = workspace.getOpenHeatmaps()
    if len( openHeatmaps ) == 0:
        raise Exception( "No heatmaps are currently open" )
    if not title:
        if len( openHeatmaps ) > 1:
            raise Exception( "There are multiple heatmaps open, so you must specify a heatmap title" )
        return openHeatmaps[0]
    results = [hm for hm in openHeatmaps if hm.getTitle() == title]
    if len(results) == 0:
        raise Exception( "Could not find any open heatmap with the title \"" + title + "\"" )
    if len(results) > 1:
        raise Exception( "Found multiple open heatmaps with the title \"" + title + "\"" )
    return results[0]
	
	
def clearWorkspace():
    """close any open windows with the OLIVER workspace"""
    openWindows = workspace.getOpenInternalFrames()
    for window in openWindows:
        window.dispose()
        
	
def displayHeatmap( heatmap ):
    """Add a new heatmap window to the OLIVER workspace"""
    workspace.displayHeatmap( heatmap )
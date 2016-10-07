from ..tecutil import _tecutil, ArgList, IndexSet, lock
from ..constant import StateChange


def state_changed(what, **kwargs):
    with ArgList(statechange=what) as arglist:
        for k,v in kwargs.items():
            arglist[k.upper()] = v
        _tecutil.StateChangedX(arglist)


@lock()
def zones_added(*zones):
    with IndexSet(*zones) as zoneset:
        with ArgList(STATECHANGE=StateChange.ZonesAdded) as arglist:
            arglist['ZONELIST'] = zoneset
            _tecutil.StateChangedX(arglist)


'''
class StateChange(Enum):
    VarsAltered               =  0
    VarsAdded                 =  1
    ZonesDeleted              =  2
    ZonesAdded                =  3
    NodeMapsAltered           =  4
    FrameDeleted              =  5
    #NewTopFrame              =  6  /* deprecated: use NewActiveFrame and/or FrameOrderChange */
    Style                     =  7
    DataSetReset              =  8
    NewLayout                 =  9
    #CompleteReset            = 10  /* deprecated: no longer broadcast */
    LineMapAssignment         = 11
    ContourLevels             = 12
    ModalDialogLaunch         = 13
    ModalDialogDismiss        = 14
    QuitTecplot               = 15
    ZoneName                  = 16
    VarName                   = 17
    LineMapName               = 18
    LineMapAddDeleteOrReorder = 19
    View                      = 20
    ColorMap                  = 21
    ContourVar                = 22
    Streamtrace               = 23
    NewAxisVariables          = 24
    MouseModeUpdate           = 25
    PickListCleared           = 26
    PickListGroupSelect       = 27
    PickListSingleSelect      = 28
    PickListStyle             = 29
    JournalReset              = 30
    UnsuspendInterface        = 31
    SuspendInterface          = 32
    DataSetLockOn             = 33
    DataSetLockOff            = 34
    Text                      = 35
    Geom                      = 36
    DataSetTitle              = 37
    DrawingInterrupted        = 38
    PrintPreviewLaunch        = 39
    PrintPreviewDismiss       = 40
    AuxDataAdded              = 41
    AuxDataDeleted            = 42
    AuxDataAltered            = 43
    VarsDeleted               = 44
    TecplotIsInitialized      = 45
    ImageExported             = 46
    VariableLockOn            = 47
    VariableLockOff           = 48
    PageDeleted               = 49
    NewTopPage                = 50
    NewActiveFrame            = 51
    FrameOrderChanged         = 52
    NewUndoState              = 53
    MacroFunctionListChanged  = 54
    AnimationStart            = 55
    AnimationEnd              = 56
    MacroRecordingStarted     = 57
    MacroRecordingEnded       = 58
    MacroRecordingCanceled    = 59
    ZoneSolutionTimeAltered   = 60
    LayoutAssociation         = 61
    CopyView                  = 62
    ColorMapDeleted           = 63
    OpenLayout                = 64
    MacroLoaded               = 65
    PerformingUndoBegin       = 66
    PerformingUndoEnd         = 67
'''

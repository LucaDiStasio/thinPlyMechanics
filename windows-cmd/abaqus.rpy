# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2017 replay file
# Internal Version: 2016_09_27-23.54.59 126836
# Run by lucad on Mon Apr 01 16:52:37 2019
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=192.146408081055, 
    height=134.1328125)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
session.viewports['Viewport: 1'].setValues(displayedObject=None)
o1 = session.openOdbs(names=(
    'C:/Abaqus_WD/CurvedInterface/Job-Stiffness-RVE1_144-HSD-EvkL1_144S1_deltatheta0_0.odb', 
    'C:/Abaqus_WD/CurvedInterface/Job-Stiffness-RVE1_144-HSD-EvkL1_144S1_deltatheta10_0.odb'))
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
session.viewports['Viewport: 1'].view.fitView()
#: Model: C:/Abaqus_WD/CurvedInterface/Job-Stiffness-RVE1_144-HSD-EvkL1_144S1_deltatheta0_0.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       20
#: Number of Node Sets:          36
#: Number of Steps:              1
#: Model: C:/Abaqus_WD/CurvedInterface/Job-Stiffness-RVE1_144-HSD-EvkL1_144S1_deltatheta10_0.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       21
#: Number of Node Sets:          37
#: Number of Steps:              1
o7 = session.odbs['C:/Abaqus_WD/CurvedInterface/Job-Stiffness-RVE1_144-HSD-EvkL1_144S1_deltatheta0_0.odb']
session.viewports['Viewport: 1'].setValues(displayedObject=o7)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
o7 = session.odbs['C:/Abaqus_WD/CurvedInterface/Job-Stiffness-RVE1_144-HSD-EvkL1_144S1_deltatheta10_0.odb']
session.viewports['Viewport: 1'].setValues(displayedObject=o7)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='U', outputPosition=NODAL, refinement=(INVARIANT, 
    'Magnitude'), )

# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def Macro1():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(-25.0, 20.0), point2=(25.0, 0.0))
    p = mdb.models['Model-1'].Part(name='RVE', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['RVE']
    p.BaseSolidExtrude(sketch=s, depth=50.0)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['RVE']
    
    del mdb.models['Model-1'].sketches['__profile__']
    p = mdb.models['Model-1'].parts['RVE']
    f, e, d1 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=f[4], sketchUpEdge=e[0], 
        sketchPlaneSide=SIDE1, origin=(0.0, 10.0, 50.0))
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=146.96, gridSpacing=3.67, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['RVE']
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    s1.ArcByCenterEnds(center=(0.0, -10.0), point1=(11.01, -10.0), point2=(-11.01, 
        -10.0), direction=COUNTERCLOCKWISE)
    s1.CoincidentConstraint(entity1=v[6], entity2=g[3], addUndoState=False)
    s1.EqualDistanceConstraint(entity1=v[1], entity2=v[2], midpoint=v[6], 
        addUndoState=False)
    s1.CoincidentConstraint(entity1=v[4], entity2=g[3], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[5], entity2=g[3], addUndoState=False)
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#10 ]', ), )
    e1, d2 = p.edges, p.datums
    p.PartitionFaceBySketch(sketchUpEdge=e1[0], faces=pickedFaces, sketch=s1)
    s1.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    p = mdb.models['Model-1'].parts['RVE']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e, d1 = p.edges, p.datums
    pickedEdges =(e[0], )
    p.PartitionCellByExtrudeEdge(line=e[6], cells=pickedCells, edges=pickedEdges, 
        sense=REVERSE)
    
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#10 ]', ), )
    leaf = dgm.LeafFromGeometry(faceSeq=faces)
    
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#100 ]', ), )
    leaf = dgm.LeafFromGeometry(faceSeq=faces)
    
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#20 ]', ), )
    leaf = dgm.LeafFromGeometry(faceSeq=faces)
    
    leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
    
    leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
    
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#10 ]', ), )
    leaf = dgm.LeafFromGeometry(faceSeq=faces)
    
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#20 ]', ), )
    leaf = dgm.LeafFromGeometry(faceSeq=faces)
    
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#100 ]', ), )
    leaf = dgm.LeafFromGeometry(faceSeq=faces)
    
    p = mdb.models['Model-1'].parts['RVE']
    f1, e1, d2 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=f1[6], sketchUpEdge=e1[4], 
        sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 25.0))
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=146.96, gridSpacing=3.67, transform=t)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['RVE']
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.Line(point1=(-25.0, 3.67), point2=(-3.67, 3.67))
    s.HorizontalConstraint(entity=g[14], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[12], entity2=g[14], addUndoState=False)
    s.CoincidentConstraint(entity1=v[8], entity2=g[12], addUndoState=False)
    s.Line(point1=(0.0, 11.01), point2=(0.0, 7.34))
    s.VerticalConstraint(entity=g[15], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[15], addUndoState=False)
    s.CoincidentConstraint(entity1=v[10], entity2=g[2], addUndoState=False)
    s.EqualDistanceConstraint(entity1=v[0], entity2=v[1], midpoint=v[10], 
        addUndoState=False)
    s.ArcByCenterEnds(center=(-3.67, 7.34), point1=(0.0, 7.34), point2=(-3.67, 
        3.67), direction=CLOCKWISE)
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    f, e, d1 = p.faces, p.edges, p.datums
    p.PartitionFaceBySketchThruAll(sketchPlane=f[6], sketchUpEdge=e[4], 
        faces=pickedFaces, sketchPlaneSide=SIDE1, sketch=s)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    session.linkedViewportCommands.setValues(_highlightLinkedViewports=False)
    leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
    
    p = mdb.models['Model-1'].parts['RVE']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    leaf = dgm.LeafFromGeometry(cellSeq=cells)
    
    p = mdb.models['Model-1'].parts['RVE']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    f1 = p.faces
    p.PartitionCellByExtendFace(extendFace=f1[0], cells=pickedCells)
    
    leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
    
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    
    p = mdb.models['Model-1'].parts['RVE']
    f, e1, d2 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=f[7], sketchUpEdge=e1[9], 
        sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 25.0))
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=109.26, gridSpacing=2.73, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['RVE']
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    s1.ArcByCenterEnds(center=(-5.46, 8.19), point1=(2.73, 8.19), point2=(-2.73, 
        1.365), direction=CLOCKWISE)
    s1.Line(point1=(2.73, 8.19), point2=(2.73, 11.01))
    s1.VerticalConstraint(entity=g[17], addUndoState=False)
    s1.TangentConstraint(entity1=g[16], entity2=g[17], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[12], entity2=g[4], addUndoState=False)
    s1.Line(point1=(-2.41831036065989, 0.585775901649726), point2=(-25.0, 
        0.585775901649727))
    s1.HorizontalConstraint(entity=g[18], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[13], entity2=g[14], addUndoState=False)
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#2 ]', ), )
    f1, e, d1 = p.faces, p.edges, p.datums
    p.PartitionFaceBySketchThruAll(sketchPlane=f1[7], sketchUpEdge=e[9], 
        faces=pickedFaces, sketchPlaneSide=SIDE1, sketch=s1)
    s1.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    p = mdb.models['Model-1'].parts['RVE']
    f, e1, d2 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=f[8], sketchUpEdge=e1[14], 
        sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 25.0))
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=109.26, gridSpacing=2.73, transform=t)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['RVE']
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.ArcByCenterEnds(center=(-5.46, 8.19), point1=(-2.73, 8.19), point2=(-5.46, 
        6.1425), direction=CLOCKWISE)
    s.Line(point1=(-2.73, 8.19), point2=(-2.73, 11.01))
    s.VerticalConstraint(entity=g[19], addUndoState=False)
    s.TangentConstraint(entity1=g[18], entity2=g[19], addUndoState=False)
    s.CoincidentConstraint(entity1=v[13], entity2=g[4], addUndoState=False)
    s.Line(point1=(-5.46, 5.46), point2=(-25.0, 5.46))
    s.HorizontalConstraint(entity=g[20], addUndoState=False)
    s.TangentConstraint(entity1=g[18], entity2=g[20], addUndoState=False)
    s.CoincidentConstraint(entity1=v[14], entity2=g[16], addUndoState=False)
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#2 ]', ), )
    f1, e, d1 = p.faces, p.edges, p.datums
    p.PartitionFaceBySketchThruAll(sketchPlane=f1[8], sketchUpEdge=e[14], 
        faces=pickedFaces, sketchPlaneSide=SIDE1, sketch=s)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    session.linkedViewportCommands.setValues(_highlightLinkedViewports=False)
    session.linkedViewportCommands.setValues(_highlightLinkedViewports=False)
    leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
    session.viewports['Viewport: 1'].partDisplay.displayGroup.replace(leaf=leaf)
    p = mdb.models['Model-1'].parts['RVE']
    f, e1, d2 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=f[7], sketchUpEdge=e1[26], 
        sketchPlaneSide=SIDE1, origin=(0.0, 11.25294, 50.0))
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=146.96, gridSpacing=3.67, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['RVE']
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    s1.ConstructionLine(point1=(0.0, -11.25294), point2=(0.585775901649727, 
        -0.258533849914111))
    s1.CoincidentConstraint(entity1=v[2], entity2=g[16], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[3], entity2=g[16], addUndoState=False)
    s1.ConstructionLine(point1=(0.0, -11.25294), point2=(5.46, -1.69216074305656))
    s1.CoincidentConstraint(entity1=v[2], entity2=g[17], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[0], entity2=g[17], addUndoState=False)
    s1.ArcByCenterEnds(center=(0.0, -11.25294), point1=(7.33999999975087, 
        1.59982918337391), point2=(0.79508602049782, 3.66999999984633), 
        direction=COUNTERCLOCKWISE)
    s1.CoincidentConstraint(entity1=v[10], entity2=g[17], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[11], entity2=g[16], addUndoState=False)
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#80 ]', ), )
    e, d1 = p.edges, p.datums
    p.PartitionFaceBySketch(sketchUpEdge=e[26], faces=pickedFaces, sketch=s1)
    s1.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    p = mdb.models['Model-1'].parts['RVE']
    f1, e1, d2 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=f1[12], sketchUpEdge=e1[32], 
        sketchPlaneSide=SIDE1, sketchOrientation=BOTTOM, origin=(0.0, 4.672789, 
        50.0))
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=107.7, gridSpacing=2.69, transform=t)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['RVE']
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.ConstructionLine(point1=(0.0, -4.672789), point2=(5.46, 4.88799025694344))
    s.CoincidentConstraint(entity1=v[2], entity2=g[17], addUndoState=False)
    s.CoincidentConstraint(entity1=v[0], entity2=g[17], addUndoState=False)
    s.ConstructionLine(point1=(0.0, -4.672789), point2=(0.585775901649727, 
        6.32161715008589))
    s.CoincidentConstraint(entity1=v[2], entity2=g[18], addUndoState=False)
    s.CoincidentConstraint(entity1=v[3], entity2=g[18], addUndoState=False)
    s.ArcByCenterEnds(center=(0.0, -4.672789), point1=(4.20476478516764, 2.69), 
        point2=(0.463946199817769, 4.03499999972526), 
        direction=COUNTERCLOCKWISE)
    s.CoincidentConstraint(entity1=v[12], entity2=g[17], addUndoState=False)
    s.CoincidentConstraint(entity1=v[13], entity2=g[18], addUndoState=False)
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#1000 ]', ), )
    e, d1 = p.edges, p.datums
    p.PartitionFaceBySketch(sketchUpEdge=e[32], faces=pickedFaces, 
        sketchOrientation=BOTTOM, sketch=s)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    session.linkedViewportCommands.setValues(_highlightLinkedViewports=False)
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#800 ]', ), )
    leaf = dgm.LeafFromGeometry(faceSeq=faces)
    session.viewports['Viewport: 1'].partDisplay.displayGroup.remove(leaf=leaf)
    session.linkedViewportCommands.setValues(_highlightLinkedViewports=False)
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#100 ]', ), )
    leaf = dgm.LeafFromGeometry(faceSeq=faces)
    session.viewports['Viewport: 1'].partDisplay.displayGroup.remove(leaf=leaf)
    p = mdb.models['Model-1'].parts['RVE']
    f, e1, d2 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=f[7], sketchUpEdge=e1[27], 
        sketchPlaneSide=SIDE1, origin=(0.0, 11.25294, 50.0))
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=107.7, gridSpacing=2.69, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['RVE']
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    s1.Line(point1=(7.33999999975087, 1.59982918337391), point2=(5.46, 
        -1.69216074305656))
    s1.PerpendicularConstraint(entity1=g[8], entity2=g[18], addUndoState=False)
    s1.Line(point1=(0.78747163330064, 3.52708584923909), point2=(0.585775901649727, 
        -0.258533849914111))
    s1.PerpendicularConstraint(entity1=g[8], entity2=g[19], addUndoState=False)
    s1.Line(point1=(3.67, -0.872612452181485), point2=(4.93366300336493, 
        2.70156626304379))
    s1.PerpendicularConstraint(entity1=g[2], entity2=g[20], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[14], entity2=g[8], addUndoState=False)
    p = mdb.models['Model-1'].parts['RVE']
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#80 ]', ), )
    e, d1 = p.edges, p.datums
    p.PartitionFaceBySketch(sketchUpEdge=e[27], faces=pickedFaces, sketch=s1)
    s1.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    p = mdb.models['Model-1'].parts['RVE']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    e1 = p.edges
    pickedEdges =(e1[0], )
    p.PartitionCellBySweepEdge(sweepPath=e1[15], cells=pickedCells, 
        edges=pickedEdges)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=116.825, 
        farPlane=199.504, width=29.2754, height=19.8981, viewOffsetX=0.695148, 
        viewOffsetY=-2.57798)
    p = mdb.models['Model-1'].parts['RVE']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    e = p.edges
    pickedEdges =(e[0], )
    p.PartitionCellBySweepEdge(sweepPath=e[17], cells=pickedCells, 
        edges=pickedEdges)
    p = mdb.models['Model-1'].parts['RVE']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    e1 = p.edges
    pickedEdges =(e1[0], )
    p.PartitionCellBySweepEdge(sweepPath=e1[19], cells=pickedCells, 
        edges=pickedEdges)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=117.185, 
        farPlane=199.145, width=29.3655, height=19.9593, viewOffsetX=-2.19318, 
        viewOffsetY=-2.88006)
    p = mdb.models['Model-1'].parts['RVE']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    e = p.edges
    pickedEdges =(e[11], e[13], e[14])
    p.PartitionCellBySweepEdge(sweepPath=e[22], cells=pickedCells, 
        edges=pickedEdges)
    p = mdb.models['Model-1'].parts['RVE']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    e1 = p.edges
    pickedEdges =(e1[7], )
    p.PartitionCellBySweepEdge(sweepPath=e1[29], cells=pickedCells, 
        edges=pickedEdges)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=118.074, 
        farPlane=198.256, width=26.7925, height=18.2105, viewOffsetX=-2.21291, 
        viewOffsetY=-1.6091)
    p = mdb.models['Model-1'].parts['RVE']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    e = p.edges
    pickedEdges =(e[23], )
    p.PartitionCellBySweepEdge(sweepPath=e[20], cells=pickedCells, 
        edges=pickedEdges)
    p = mdb.models['Model-1'].parts['RVE']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    e1 = p.edges
    pickedEdges =(e1[0], )
    p.PartitionCellBySweepEdge(sweepPath=e1[23], cells=pickedCells, 
        edges=pickedEdges)



#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2018 Universite de Lorraine & Lulea tekniska universitet
Author: Luca Di Stasio <luca.distasio@gmail.com>
                       <luca.distasio@ingpec.eu>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in
the documentation and/or other materials provided with the distribution
Neither the name of the Université de Lorraine or Luleå tekniska universitet
nor the names of its contributors may be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

=====================================================================================

DESCRIPTION

Tested with Abaqus Python 2.6 (64-bit) distribution in Windows 7.

'''
import numpy as np
from os.path import isfile
from abaqus import *
from abaqusConstants import *
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
#import __main__

def createRVE(parameters):
#===============================================================================#
#                               Parameters
#===============================================================================#
    # assign most used parameters to variables
    wd = parameters['wd']
    caefilename = parameters['caefilename']
    modelname = parameters['modelname']
    L = parameters['L']
    Rf = parameters['Rf']
    theta = 0.0
    deltatheta = parameters['deltatheta'] # in degrees !!!
    deltapsi = parameters['deltapsi'] # in degrees !!!
    deltaphi = parameters['deltaphi'] # in degrees !!!
#===============================================================================#
#                          Model database creation
#===============================================================================#
# if CAE database exists, open it; otherwise create new one
    caefullpath = join(wd,caefilename)
    if isfile(caefullpath):
        openMdb(caefullpath)
    else:
        mdb.saveAs(caefullpath)
#===============================================================================#
#                             Parts creation
#===============================================================================# 
    # create model
    s = mdb.models[modelname].ConstrainedSketch(name='__profile__', 
        sheetSize=3*L)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    # create geometry
    s.rectangle(point1=(-L, 0.0), point2=(L,L))
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=138.227, 
    #     farPlane=238.897, width=390.084, height=180.104, cameraPosition=(
    #     15.9249, 26.9232, 188.562), cameraTarget=(15.9249, 26.9232, 0))
    
    # set dimension labels
    s.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(-109.506118774414, 
        57.8169174194336), value=100.0)
    s.ObliqueDimension(vertex1=v[1], vertex2=v[2], textPoint=(-36.3927574157715, 
        110.401977539063), value=200.0)
    
    p = mdb.models[modelname].Part(name='RVE', dimensionality=TWO_D_PLANAR, 
        type=DEFORMABLE_BODY)
    p = mdb.models[modelname].parts['RVE']
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[modelname].sketches['__profile__']
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=422.639, 
    #     farPlane=471.788, width=216.795, height=93.2764, viewOffsetX=2.78779, 
    #     viewOffsetY=-2.68155)
    # create partition
    p = mdb.models[modelname].parts['RVE']
    f, e, d1 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.0,0.5*L, 0.0))
    s1 = mdb.models[modelname].ConstrainedSketch(name='__profile__', 
        sheetSize=3*L, gridSpacing=L/100.0, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models[modelname].parts['RVE']
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=419.629, 
    #     farPlane=474.798, width=241.934, height=111.702, cameraPosition=(
    #     -3.26651, 51.4432, 447.214), cameraTarget=(-3.26651, 51.4432, 0))
    # draw fiber
    s1.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-Rf, -0.5*L), point2=(Rf,-0.5*L), direction=CLOCKWISE)
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=446.175, 
    #     farPlane=448.252, width=8.04875, height=3.71615, cameraPosition=(
    #     0.711616, 0.804246, 447.214), cameraTarget=(0.711616, 0.804246, 0))
    # draw circular sections for mesh generation
    s1.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-0.75*Rf, -0.5*L), point2=(0.75*Rf,-0.5*L), direction=CLOCKWISE)
    s1.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-0.5*Rf, -0.5*L), point2=(0.5*Rf,-0.5*L), direction=CLOCKWISE)
    if L>2*Rf:
        s1.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-1.25*Rf, -0.5*L), point2=(1.25*Rf,-0.5*L), direction=CLOCKWISE)
        s1.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-1.5*Rf, -0.5*L), point2=(1.5*Rf,-0.5*L), direction=CLOCKWISE)
    else:
        s1.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-(Rf+0.25*(L-Rf)), -0.5*L), point2=((Rf+0.25*(L-Rf)),-0.5*L), direction=CLOCKWISE)
        s1.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-(Rf+0.5*(L-Rf)), -0.5*L), point2=((Rf+0.5*(L-Rf)),-0.5*L), direction=CLOCKWISE)
        
    alpha = theta + deltatheta - deltapsi
    beta = theta + deltatheta + deltapsi
    gamma = theta + deltatheta + deltapsi + deltaphi
    # draw angular section for crack and mesh generation    
    s1.ConstructionLine(point1=(0.0, -0.5*L), angle=(theta+deltatheta))
    s1.CoincidentConstraint(entity1=v[6], entity2=g[11], addUndoState=False)
    
    s1.ConstructionLine(point1=(0.0, -0.5*L), angle=alpha)
    s1.CoincidentConstraint(entity1=v[6], entity2=g[12], addUndoState=False)
    
    s1.ConstructionLine(point1=(0.0, -0.5*L), angle=beta)
    s1.CoincidentConstraint(entity1=v[6], entity2=g[13], addUndoState=False)
    
    s1.ConstructionLine(point1=(0.0, -0.5*L), angle=gamma)
    s1.CoincidentConstraint(entity1=v[6], entity2=g[14], addUndoState=False)
    
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=446.654, 
    #     farPlane=447.773, width=4.33518, height=2.00158, cameraPosition=(
    #     0.833721, 0.682125, 447.214), cameraTarget=(0.833721, 0.682125, 0))
    
    Rint = 0.75*Rf
    if L>2*Rf:
        Rext = 1.25*Rf
    else:
        Rext = Rf+0.25*(L-Rf)
        
    s1.Line(point1=(Rint*np.cos(alpha*np.pi/180.0), -0.5*L+Rint*np.sin(alpha*np.pi/180.0)), point2=(
        Rext*np.cos(alpha*np.pi/180.0), -0.5*L+Rext*np.sin(alpha*np.pi/180.0))
    s1.PerpendicularConstraint(entity1=g[7], entity2=g[15], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[15], entity2=g[7], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[16], entity2=g[9], addUndoState=False)
    
    s1.Line(point1=(Rint*np.cos((theta+deltatheta)*np.pi/180.0), -0.5*L+Rint*np.sin((theta+deltatheta)*np.pi/180.0)), point2=(
        Rext*np.cos((theta+deltatheta)*np.pi/180.0), -0.5*L+Rext*np.sin((theta+deltatheta)*np.pi/180.0))
    s1.PerpendicularConstraint(entity1=g[7], entity2=g[16], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[17], entity2=g[7], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[18], entity2=g[9], addUndoState=False)
    
    s1.Line(point1=(Rint*np.cos(beta*np.pi/180.0), -0.5*L+Rint*np.sin(beta*np.pi/180.0)), point2=(
        Rext*np.cos(beta*np.pi/180.0), -0.5*L+Rext*np.sin(beta*np.pi/180.0))
    s1.PerpendicularConstraint(entity1=g[7], entity2=g[17], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[19], entity2=g[7], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[20], entity2=g[9], addUndoState=False)
    
    s1.Line(point1=(Rint*np.cos(gamma*np.pi/180.0), -0.5*L+Rint*np.sin(gamma*np.pi/180.0)), point2=(
        Rext*np.cos(gamma*np.pi/180.0), -0.5*L+Rext*np.sin(gamma*np.pi/180.0))
    s1.PerpendicularConstraint(entity1=g[7], entity2=g[21], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[25], entity2=g[7], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[26], entity2=g[9], addUndoState=False)
    
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    e1, d2 = p.edges, p.datums
    p.PartitionFaceBySketch(faces=pickedFaces, sketch=s1)
    s1.unsetPrimaryObject()
    del mdb.models[modelname].sketches['__profile__']
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=446.825, 
    #     farPlane=447.603, width=3.01417, height=1.29685, viewOffsetX=0.737959, 
    #     viewOffsetY=-49.1943)
    p = mdb.models[modelname].parts['RVE']
    v = p.vertices
    verts = v.getSequenceFromMask(mask=('[#4000 ]', ), )
    p.Set(vertices=verts, name='CrackTip')
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=446.848, 
    #     farPlane=447.579, viewOffsetX=0.754913, viewOffsetY=-49.3018)
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=446.848, 
    #     farPlane=447.579, viewOffsetX=0.900385, viewOffsetY=-49.4203)
    p = mdb.models[modelname].parts['RVE']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#20004 ]', ), )
    p.Set(edges=edges, name='Crack')
    
    
    p = mdb.models[modelname].parts['RVE']
    p.regenerate()
    
    # session.viewports['Viewport: 1'].view.setValues(nearPlane=446.727, 
    #     farPlane=447.7, width=3.77317, height=1.62341, viewOffsetX=1.23565, 
    #     viewOffsetY=-49.3176)
    
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#9c7 ]', ), )
    p.Set(faces=faces, name='Fiber')
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#3638 ]', ), )
    p.Set(faces=faces, name='Matrix')
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#8 ]', ), )
    p.Set(faces=faces, name='BulkMatrix')
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    p.Set(faces=faces, name='BulkFiber')
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#946 ]', ), )
    p.Set(faces=faces, name='OuterRingFiber')
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#80 ]', ), )
    p.Set(faces=faces, name='InnerRingFiber')
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#3430 ]', ), )
    p.Set(faces=faces, name='InnerRingMatrix')
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#200 ]', ), )
    p.Set(faces=faces, name='OuterRingMatrix')
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#940 ]', ), )
    p.Set(faces=faces, name='FiberBounded')
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#6 ]', ), )
    p.Set(faces=faces, name='FiberCrack')
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#3400 ]', ), )
    p.Set(faces=faces, name='MatrixBounded')
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#30 ]', ), )
    p.Set(faces=faces, name='MatrixCrack')
    mdb.save()
    
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    
#===============================================================================#
#                             Materials creation
#===============================================================================#    
    mdb.models[modelname].Material(name='GlassFiber')
    mdb.models[modelname].materials['GlassFiber'].Elastic(table=((70000.0, 0.2), ))
    
    mdb.models[modelname].Material(name='Epoxy')
    mdb.models[modelname].materials['Epoxy'].Elastic(table=((3500.0, 0.4), ))
    
#===============================================================================#
#                             Sections creation
#===============================================================================#
    
    mdb.models[modelname].HomogeneousSolidSection(name='FiberSection', 
        material='GlassFiber', thickness=1.0)
    mdb.models[modelname].HomogeneousSolidSection(name='MatrixSection', 
        material='Epoxy', thickness=1.0)
        
#===============================================================================#
#                             Sections assignment
#===============================================================================#         
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#9c7 ]', ), )
    region = regionToolset.Region(faces=faces)
    p = mdb.models[modelname].parts['RVE']
    p.SectionAssignment(region=region, sectionName='FiberSection', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#3638 ]', ), )
    region = regionToolset.Region(faces=faces)
    p = mdb.models[modelname].parts['RVE']
    p.SectionAssignment(region=region, sectionName='MatrixSection', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    mdb.save()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=445.377, 
        farPlane=449.05, width=16.1036, height=6.92858, viewOffsetX=5.22035, 
        viewOffsetY=-49.1912)
#===============================================================================#
#                             Instance creation
#===============================================================================#
    a = mdb.models[modelname].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    a = mdb.models[modelname].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[modelname].parts['RVE']
    a.Instance(name='RVE-1', part=p, dependent=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        adaptiveMeshConstraints=ON)
#===============================================================================#
#                             Step creation
#===============================================================================#
    mdb.models[modelname].StaticStep(name='Step-1', previous='Initial', 
        minInc=1e-10)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=445.876, 
        farPlane=448.551, width=10.3678, height=4.46076, viewOffsetX=0.497935, 
        viewOffsetY=-48.4083)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    edges1 = e1.getSequenceFromMask(mask=('[#e600c502 #40 ]', ), )
    region = regionToolset.Region(edges=edges1)
    mdb.models[modelname].YsymmBC(name='SymmetryBound', createStepName='Step-1', 
        region=region, localCsys=None)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=ON)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=445.864, 
        farPlane=448.563, width=11.8314, height=5.09047, viewOffsetX=3.97611, 
        viewOffsetY=-49.5807)
    p = mdb.models[modelname].parts['RVE']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#e600c502 #40 ]', ), )
    p.Set(edges=edges, name='SymmetryBoundary')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=428.173, 
        farPlane=466.254, width=166.569, height=71.6664, viewOffsetX=-26.2404, 
        viewOffsetY=-23.2858)
    p = mdb.models[modelname].parts['RVE']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#2000 ]', ), )
    p.Set(edges=edges, name='LeftBoundary')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=411.359, 
        farPlane=483.068, width=279.283, height=120.162, viewOffsetX=53.7961, 
        viewOffsetY=1.86796)
    p = mdb.models[modelname].parts['RVE']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#800 ]', ), )
    p.Set(edges=edges, name='RightBoundary')
    p = mdb.models[modelname].parts['RVE']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#1000 ]', ), )
    p.Set(edges=edges, name='UpperSide')
    a = mdb.models[modelname].rootAssembly
    a.regenerate()
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=415.445, 
        farPlane=478.983, width=277.443, height=119.37, viewOffsetX=20.2886, 
        viewOffsetY=6.06555)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    edges1 = e1.getSequenceFromMask(mask=('[#800 ]', ), )
    region = regionToolset.Region(edges=edges1)
    mdb.models[modelname].DisplacementBC(name='RightAppliedDisp', 
        createStepName='Step-1', region=region, u1=1.0, u2=UNSET, ur3=UNSET, 
        amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    edges1 = e1.getSequenceFromMask(mask=('[#2000 ]', ), )
    region = regionToolset.Region(edges=edges1)
    mdb.models[modelname].DisplacementBC(name='LeftAppliedDisp', 
        createStepName='Step-1', region=region, u1=-1.0, u2=UNSET, ur3=UNSET, 
        amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    mdb.save()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.641, 
        farPlane=447.786, width=4.43929, height=1.91001, viewOffsetX=1.17094, 
        viewOffsetY=-49.4948)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=444.137, 
        farPlane=450.29, width=23.8552, height=10.2637, viewOffsetX=3.98199, 
        viewOffsetY=-45.6997)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.513, 
        farPlane=447.914, width=5.43211, height=2.33717, viewOffsetX=1.53117, 
        viewOffsetY=-48.7762)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.88, 
        farPlane=447.547, width=2.58738, height=1.11322, viewOffsetX=1.11075, 
        viewOffsetY=-49.1185)
    p = mdb.models[modelname].parts['RVE']
    v = p.vertices
    verts = v.getSequenceFromMask(mask=('[#4 ]', ), )
    p.Set(vertices=verts, name='CrackTip')
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models[modelname].parts['RVE']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#60 ]', ), )
    p.Set(edges=edges, name='Crack')
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.465, 
        farPlane=447.962, width=5.80186, height=2.49626, viewOffsetX=1.66622, 
        viewOffsetY=-48.5757)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    a1 = mdb.models[modelname].rootAssembly
    a1.regenerate()
    a = mdb.models[modelname].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
        predefinedFields=OFF, interactions=ON, constraints=ON, 
        engineeringFeatures=ON)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    edges1 = e1.getSequenceFromMask(mask=('[#60 ]', ), )
    pickedRegions = regionToolset.Region(edges=edges1)
    mdb.models[modelname].rootAssembly.engineeringFeatures.assignSeam(
        regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    edges1 = e1.getSequenceFromMask(mask=('[#60 ]', ), )
    crackFront = regionToolset.Region(edges=edges1)
    a = mdb.models[modelname].rootAssembly
    v1 = a.instances['RVE-1'].vertices
    verts1 = v1.getSequenceFromMask(mask=('[#4 ]', ), )
    crackTip = regionToolset.Region(vertices=verts1)
    v11 = a.instances['RVE-1'].vertices
    e1 = a.instances['RVE-1'].edges
    a.engineeringFeatures.ContourIntegral(name='Crack-1', symmetric=OFF, 
        crackFront=crackFront, crackTip=crackTip, 
        extensionDirectionMethod=Q_VECTORS, qVectors=((v11[2], 
        a.instances['RVE-1'].InterestingPoint(edge=e1[22], rule=MIDDLE)), ), 
        midNodePosition=0.5, collapsedElementAtTip=NONE)
    mdb.save()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.275, 
        farPlane=448.152, width=7.27671, height=3.13081, viewOffsetX=1.16701, 
        viewOffsetY=-49.6886)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, 
        interactions=OFF, constraints=OFF, connectors=OFF, 
        engineeringFeatures=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    p1 = mdb.models[modelname].parts['RVE']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#2c76 ]', ), )
    p.Set(faces=faces, name='StructuredMeshRegion')
    a = mdb.models[modelname].rootAssembly
    a.regenerate()
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    a1 = mdb.models[modelname].rootAssembly
    p = mdb.models[modelname].parts['RVE']
    a1.Instance(name='RVE-2', part=p, dependent=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.29, 
        farPlane=448.137, width=7.12694, height=3.0802, viewOffsetX=0.779849, 
        viewOffsetY=-48.8554)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-2'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#2c76 ]', ), )
    a.setMeshControls(regions=pickedRegions, elemShape=QUAD, technique=STRUCTURED)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.397, 
        farPlane=448.03, width=6.29888, height=2.72232, viewOffsetX=0.602778, 
        viewOffsetY=-48.8815)
    mdb.save()
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-2'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#640028 #4 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=200, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-2'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#1a0014 #8 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=286, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-2'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#8100 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=286, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-2'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#100c0 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=80, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-2'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#800000 #12 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=40, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-2'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=9, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-2'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#2 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=3, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-2'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#11000000 #1 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=20, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-2'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#200 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=36, constraint=FINER)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=414.321, 
        farPlane=480.106, width=285.925, height=123.574, viewOffsetX=15.6247, 
        viewOffsetY=0.775002)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-2'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#2800 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=20, constraint=FINER)
    mdb.save()
    elemType1 = mesh.ElemType(elemCode=CPE8, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=CPE6, elemLibrary=STANDARD)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#3fff ]', ), )
    f2 = a.instances['RVE-2'].faces
    faces2 = f2.getSequenceFromMask(mask=('[#3fff ]', ), )
    pickedRegions =((faces1+faces2), )
    a.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=430.046, 
        farPlane=464.381, width=132.768, height=57.381, viewOffsetX=12.3062, 
        viewOffsetY=-28.8418)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-2'], )
    a.seedPartInstance(regions=partInstances, size=10.0, deviationFactor=0.1, 
        minSizeFactor=0.1)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.seedPartInstance(regions=partInstances, size=10.0, deviationFactor=0.1, 
        minSizeFactor=0.1)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], a.instances['RVE-2'], )
    a.generateMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.53, 
        farPlane=447.898, width=5.97091, height=3.41606, viewOffsetX=1.56868, 
        viewOffsetY=-48.8662)
    mdb.save()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=445.68, 
        farPlane=448.748, width=13.3916, height=7.66155, viewOffsetX=3.72768, 
        viewOffsetY=-46.2342)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-2'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#1100 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-2'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#20000000 #40 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=4, constraint=FINER)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.476, 
        farPlane=447.951, width=6.43706, height=3.68275, viewOffsetX=1.37532, 
        viewOffsetY=-48.1601)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-2'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#6000000 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=4, constraint=FINER)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=445.667, 
        farPlane=448.76, width=11.9295, height=6.82506, viewOffsetX=1.39414, 
        viewOffsetY=-46.5027)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], a.instances['RVE-2'], )
    a.generateMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=439.422, 
        farPlane=455.005, width=67.8857, height=38.8386, viewOffsetX=9.93107, 
        viewOffsetY=-30.3379)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], a.instances['RVE-2'], )
    a.deleteMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.413, 
        farPlane=448.014, width=6.17476, height=3.53269, viewOffsetX=1.34447, 
        viewOffsetY=-47.9682)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.461, 
        farPlane=447.966, width=6.17542, height=3.53306, viewOffsetX=1.23322, 
        viewOffsetY=-48.9907)
    a = mdb.models[modelname].rootAssembly
    del a.features['RVE-2']
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#2c76 ]', ), )
    a.setMeshControls(regions=pickedRegions, elemShape=QUAD, technique=STRUCTURED)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#640028 #4 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=200, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#1a0014 #8 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=286, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#8100 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=286, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#100c0 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=80, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#800000 #12 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=40, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#11000000 #1 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=20, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=9, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#2 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=3, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#200 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=36, constraint=FINER)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=410.381, 
        farPlane=484.046, width=320.139, height=183.157, viewOffsetX=20.594, 
        viewOffsetY=28.2835)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#2800 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=20, constraint=FINER)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=419.794, 
        farPlane=474.633, width=212.365, height=121.498, viewOffsetX=6.32077, 
        viewOffsetY=0.0595284)
    elemType1 = mesh.ElemType(elemCode=CPE8, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=CPE6, elemLibrary=STANDARD)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#3fff ]', ), )
    pickedRegions =(faces1, )
    a.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.655, 
        farPlane=447.772, width=4.30727, height=2.46426, viewOffsetX=0.523219, 
        viewOffsetY=-49.1655)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#1100 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#1100 ]', ), )
    a.setMeshControls(regions=pickedRegions, technique=SWEEP)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#3900 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#8000000 #20 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=10, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#3900 ]', ), )
    a.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED, 
        technique=FREE)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#1100 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#1100 ]', ), )
    a.setMeshControls(regions=pickedRegions, technique=SWEEP)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#1000 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#0 #40 ]', ), )
    a.deleteSeeds(regions=pickedEdges)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#100 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#20000000 ]', ), )
    a.deleteSeeds(regions=pickedEdges)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#1100 ]', ), )
    a.setMeshControls(regions=pickedRegions, technique=FREE)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#1100 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#1000000 #1 ]', ), )
    a.deleteSeeds(regions=pickedEdges)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#2800 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#8000000 #20 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=10, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#8000000 #20 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=6, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#8000000 #20 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=5, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#1108 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#10000200 ]', ), )
    a.deleteSeeds(regions=pickedEdges)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.603, 
        farPlane=447.825, width=4.71449, height=2.69724, viewOffsetX=0.643251, 
        viewOffsetY=-48.8833)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#8 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#200 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=72, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#200 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=36, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#1000 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#0 #1 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=25, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.deleteSeeds(regions=pickedEdges)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#2000 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#800000 #12 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=20, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.788, 
        farPlane=447.639, width=3.71255, height=2.12402, viewOffsetX=0.61176, 
        viewOffsetY=-48.9074)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#3438 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#c0850200 #17 ]', ), )
    a.deleteSeeds(regions=pickedEdges)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=18, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.73, 
        farPlane=447.697, width=4.21826, height=2.41334, viewOffsetX=0.586307, 
        viewOffsetY=-48.8347)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#208 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#200 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=36, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#3900 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#3900 ]', ), )
    a.setMeshControls(regions=pickedRegions, technique=SWEEP)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.758, 
        farPlane=447.67, width=3.98163, height=2.27796, viewOffsetX=0.68917, 
        viewOffsetY=-48.5365)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#3900 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#3900 ]', ), )
    a.setMeshControls(regions=pickedRegions, technique=FREE, algorithm=MEDIAL_AXIS)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.553, 
        farPlane=447.874, width=5.76892, height=3.3005, viewOffsetX=1.11535, 
        viewOffsetY=-48.1223)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.511, 
        farPlane=447.916, width=5.76838, height=3.30019, viewOffsetX=1.14126, 
        viewOffsetY=-48.606)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.438, 
        farPlane=447.989, width=5.9833, height=3.42315, viewOffsetX=1.23787, 
        viewOffsetY=-48.4533)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#10000000 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=50, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.435, 
        farPlane=447.992, width=6.79915, height=3.88991, viewOffsetX=1.52006, 
        viewOffsetY=-48.179)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#1100 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#1000000 #1 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=50, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.843, 
        farPlane=447.585, width=3.23881, height=1.85298, viewOffsetX=0.415233, 
        viewOffsetY=-48.6405)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#2800 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    e1 = a.instances['RVE-1'].edges
    pickedEdges = e1.getSequenceFromMask(mask=('[#800000 #12 ]', ), )
    a.seedEdgeByNumber(edges=pickedEdges, number=5, constraint=FINER)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.729, 
        farPlane=447.698, width=4.52142, height=2.58678, viewOffsetX=0.415626, 
        viewOffsetY=-48.6656)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#2800 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#2a80 ]', ), )
    a.setMeshControls(regions=pickedRegions, elemShape=TRI)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.855, 
        farPlane=447.572, width=2.76817, height=1.58372, viewOffsetX=0.383482, 
        viewOffsetY=-48.928)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#2800 ]', ), )
    a.deleteMesh(regions=pickedRegions)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-1'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#2800 ]', ), )
    a.setMeshControls(regions=pickedRegions, elemShape=QUAD_DOMINATED)
    a = mdb.models[modelname].rootAssembly
    partInstances =(a.instances['RVE-1'], )
    a.generateMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=446.531, 
        farPlane=447.896, width=5.95639, height=3.40775, viewOffsetX=2.43989, 
        viewOffsetY=-47.9197)
    mdb.save()
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF, 
        adaptiveMeshConstraints=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    mdb.models[modelname].historyOutputRequests['H-Output-1'].setValues(
        contourIntegral='Crack-1', sectionPoints=DEFAULT, rebar=EXCLUDE, 
        numberOfContours=50)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        adaptiveMeshConstraints=OFF)
#===============================================================================#
#                             Job creation
#===============================================================================#
    mdb.Job(name='Job-1', model=modelname, description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=99, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=ON, 
        modelPrint=ON, contactPrint=ON, historyPrint=ON, userSubroutine='', 
        scratch='', multiprocessingMode=DEFAULT, numCpus=12, numDomains=12, 
        numGPUs=0)
    mdb.jobs['Job-1'].submit(consistencyChecking=OFF)

def main(argv):

if __name__ == "__main__":
    main(sys.argv[1:])
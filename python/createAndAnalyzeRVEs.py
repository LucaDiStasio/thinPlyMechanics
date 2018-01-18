#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2018 Université de Lorraine or Luleå tekniska universitet
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
import sys
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
    delta = parameters['delta'] # in degrees !!!
    minElNum = parameters['minElNum']
    if ((theta+deltatheta-deltapsi)<=0.0 or (theta+deltatheta-deltapsi)/delta<minElNum) and ((theta+deltatheta+deltapsi+deltaphi)>=180.0 or (180.0-(theta+deltatheta+deltapsi+deltaphi))/delta<minElNum):
        deltapsi = 0.6*((180.0-(theta+deltatheta))-np.max([0.5*(theta+deltatheta),0.1*(180.0-(theta+deltatheta)),minElnum*delta]))
        deltaphi = 0.4*((180.0-(theta+deltatheta))-np.max([0.5*(theta+deltatheta),0.1*(180.0-(theta+deltatheta)),minElnum*delta]))
    elif (theta+deltatheta-deltapsi)<=0.0 or (theta+deltatheta-deltapsi)/delta<minElNum:
        deltapsi = (theta+deltatheta) - np.max([0.5*(theta+deltatheta),minElnum*delta])
    elif (theta+deltatheta+deltapsi+deltaphi)>=180.0 or (180.0-(theta+deltatheta+deltapsi+deltaphi))/delta<minElNum:
        deltapsi = 0.6*((180.0-(theta+deltatheta))-np.max([0.1*(180.0-(theta+deltatheta)),minElnum*delta]))
        deltaphi = 0.4*((180.0-(theta+deltatheta))-np.max([0.1*(180.0-(theta+deltatheta)),minElnum*delta]))
#===============================================================================#
#                          Model database creation
#===============================================================================#
# if CAE database exists, open it; otherwise create new one
    caefullpath = join(wd,caefilename)
    if isfile(caefullpath):
        openMdb(caefullpath)
    else:
        mdb.saveAs(caefullpath)
    # assign model object to variable for lighter code
    model = mdb.models[modelname]
#===============================================================================#
#                             Parts creation
#===============================================================================# 
    # create sketch
    RVEsketch = model.ConstrainedSketch(name='__profile__', 
        sheetSize=3*L)
    RVEsketch.setPrimaryObject(option=STANDALONE)
    # create rectangle
    RVEsketch.rectangle(point1=(-L, 0.0), point2=(L,L))
    # set dimension labels
    RVEsketch.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(-1.1*L,0.5*L), value=L)
    RVEsketch.ObliqueDimension(vertex1=v[1], vertex2=v[2], textPoint=(0.0,1.1*L), value=2*L)
    # assign to part
    RVEpart = model.Part(name='RVE',dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)
    RVEpart = model.parts['RVE']
    RVEpart.BaseShell(sketch=RVEsketch)
    RVEsketch.unsetPrimaryObject()
    del model.sketches['__profile__']
    # create reference to geometrical objects (faces, edges and vertices) of the part
    RVEfaces = RVEpart.faces
    RVEedges = RVEpart.edges
    RVEvertices = RVEpart.vertices
    # create geometrical transform to draw partition sketch
    transformToSketch = RVEpart.MakeSketchTransform(sketchPlane=RVEfaces[0], sketchPlaneSide=SIDE1, origin=(0.0,0.5*L, 0.0))
    # create sketch
    fiberSketch = model.ConstrainedSketch(name='__profile__',sheetSize=3*L, gridSpacing=L/100.0, transform=transformToSketch)
    # create reference to geometrical objects (faces, edges and vertices) of the partition sketch
    fiberGeometry = fiberSketch.geometry
    fiberVertices = fiberSketch.vertices
    fiberSketch.setPrimaryObject(option=SUPERIMPOSE)
    #p = mdb.models[modelname].parts['RVE']
    RVEpart.projectReferencesOntoSketch(sketch=fiberSketch, filter=COPLANAR_EDGES)
    # draw fiber and circular sections for mesh generation
    fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-Rf, -0.5*L), point2=(Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[6]
    fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-0.75*Rf, -0.5*L), point2=(0.75*Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[7]
    fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-0.5*Rf, -0.5*L), point2=(0.5*Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[8]
    if L>2*Rf:
        fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-1.25*Rf, -0.5*L), point2=(1.25*Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[9]
        fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-1.5*Rf, -0.5*L), point2=(1.5*Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[10]
    else:
        fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-(Rf+0.25*(L-Rf)), -0.5*L), point2=((Rf+0.25*(L-Rf)),-0.5*L), direction=CLOCKWISE) # fiberGeometry[9]
        fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-(Rf+0.5*(L-Rf)), -0.5*L), point2=((Rf+0.5*(L-Rf)),-0.5*L), direction=CLOCKWISE) # fiberGeometry[10]
    
    # calculate angles for construction lines    
    alpha = theta + deltatheta - deltapsi
    beta = theta + deltatheta + deltapsi
    gamma = theta + deltatheta + deltapsi + deltaphi
    
    # draw construction lines  
    fiberSketch.ConstructionLine(point1=(0.0, -0.5*L), angle=(theta+deltatheta)) # fiberGeometry[11]
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[6], entity2=fiberGeometry[11], addUndoState=False)
    
    fiberSketch.ConstructionLine(point1=(0.0, -0.5*L), angle=alpha) # fiberGeometry[12]
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[6], entity2=fiberGeometry[12], addUndoState=False)
    
    fiberSketch.ConstructionLine(point1=(0.0, -0.5*L), angle=beta) # fiberGeometry[13]
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[6], entity2=fiberGeometry[13], addUndoState=False)
    
    fiberSketch.ConstructionLine(point1=(0.0, -0.5*L), angle=gamma) # fiberGeometry[14]
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[6], entity2=fiberGeometry[14], addUndoState=False)
    
    # draw angular sections to identify the crack and for mesh generation
    Rint = 0.75*Rf
    if L>2*Rf:
        Rext = 1.25*Rf
    else:
        Rext = Rf+0.25*(L-Rf)
        
    fiberSketch.Line(point1=(Rint*np.cos(alpha*np.pi/180.0), -0.5*L+Rint*np.sin(alpha*np.pi/180.0)), point2=(
        Rext*np.cos(alpha*np.pi/180.0), -0.5*L+Rext*np.sin(alpha*np.pi/180.0)) # fiberGeometry[15]
    fiberSketch.PerpendicularConstraint(entity1=fiberGeometry[7], entity2=fiberGeometry[15], addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[15], entity2=fiberGeometry[7], addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[16], entity2=fiberGeometry[9], addUndoState=False)
    
    fiberSketch.Line(point1=(Rint*np.cos((theta+deltatheta)*np.pi/180.0), -0.5*L+Rint*np.sin((theta+deltatheta)*np.pi/180.0)), point2=(
        Rext*np.cos((theta+deltatheta)*np.pi/180.0), -0.5*L+Rext*np.sin((theta+deltatheta)*np.pi/180.0)) # fiberGeometry[16]
    fiberSketch.PerpendicularConstraint(entity1=fiberGeometry[7], entity2=fiberGeometry[16], addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[17], entity2=fiberGeometry[7], addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[18], entity2=fiberGeometry[9], addUndoState=False)
    
    fiberSketch.Line(point1=(Rint*np.cos(beta*np.pi/180.0), -0.5*L+Rint*np.sin(beta*np.pi/180.0)), point2=(
        Rext*np.cos(beta*np.pi/180.0), -0.5*L+Rext*np.sin(beta*np.pi/180.0)) # fiberGeometry[17]
    fiberSketch.PerpendicularConstraint(entity1=fiberGeometry[7], entity2=fiberGeometry[17], addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[19], entity2=fiberGeometry[7], addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[20], entity2=fiberGeometry[9], addUndoState=False)
    
    fiberSketch.Line(point1=(Rint*np.cos(gamma*np.pi/180.0), -0.5*L+Rint*np.sin(gamma*np.pi/180.0)), point2=(
        Rext*np.cos(gamma*np.pi/180.0), -0.5*L+Rext*np.sin(gamma*np.pi/180.0)) # fiberGeometry[18]
    fiberSketch.PerpendicularConstraint(entity1=fiberGeometry[7], entity2=fiberGeometry[18], addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[25], entity2=fiberGeometry[7], addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[26], entity2=fiberGeometry[9], addUndoState=False)
    
    pickedFaces = RVEfaces.getSequenceFromMask(mask=('[#1 ]', ), )
    p.PartitionFaceBySketch(faces=pickedFaces, sketch=fiberSketch)
    fiberSketch.unsetPrimaryObject()
    del model.sketches['__profile__']
    
    #-------------------#
    #                   #
    #    create sets    #
    #                   #
    #-------------------#
    
    # create reference to geometric elements for lighter code
    RVEvertices = RVEpart.vertices
    RVEedges = RVEpart.edges
    RVEfaces = RVEpart.faces
    
    # sets of vertices
    crackTip = RVEvertices.getByBoundingSphere(center=(Rf*np.cos((theta+deltatheta)*np.pi/180),Rf*np.sin((theta+deltatheta)*np.pi/180),0.0),radius=0.001*Rf)
    RVEpart.Set(vertices=crackTip, name='CRACKTIP')
    
    # sets of edges
    crackEdge1=RVEedges.getByBoundingSphere(center=(Rf*np.cos(0.5*alpha*np.pi/180),Rf*np.sin(0.5*alpha*np.pi/180),0.0),radius=0.01*Rf)
    crackEdge2=RVEedges.getByBoundingSphere(center=(Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180),Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0),radius=0.01*Rf)
    RVEpart.Set(edges=crackEdge1, name='CRACK-LOWER')
    RVEpart.Set(edges=crackEdge2, name='CRACK-UPPER')
    RVEpart.SetByBoolean(name='CRACK', sets=[RVEpart.sets['CRACK-LOWER'],RVEpart.sets['CRACK-UPPER']])
    
    RVEpart.Set(edges=crackEdge1, name='LOWERSIDE-CENTER')
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.001*Rf,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-CENTER')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.65*Rf,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-FIRSTRING-RIGHT')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(-0.65*Rf,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-FIRSTRING-LEFT')
    RVEpart.SetByBoolean(name='LOWERSIDE-FIRSTRING', sets=[RVEpart.sets['LOWERSIDE-FIRSTRING-RIGHT'],RVEpart.sets['LOWERSIDE-FIRSTRING-LEFT']])
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.85*Rf,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-SECONDRING-RIGHT')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(-0.85*Rf,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-SECONDRING-LEFT')
    RVEpart.SetByBoolean(name='LOWERSIDE-SECONDRING', sets=[RVEpart.sets['LOWERSIDE-SECONDRING-RIGHT'],RVEpart.sets['LOWERSIDE-SECONDRING-LEFT']])
    if L>2*Rf:
        R1 = (1+0.5*0.25)*Rf
        R2 = (1.25+0.5*0.25)*Rf
    else:
        R1 = Rf+0.5*0.25*(L-Rf)
        R2 = Rf+1.5*0.25*(L-Rf)
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(R1,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-THIRDRING-RIGHT')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(-R1,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-THIRDRING-LEFT')
    RVEpart.SetByBoolean(name='LOWERSIDE-THIRDRING', sets=[RVEpart.sets['LOWERSIDE-THIRDRING-RIGHT'],RVEpart.sets['LOWERSIDE-THIRDRING-LEFT']])
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(R2,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-FOURTHRING-RIGHT')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(-R2,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-FOURTHRING-LEFT')
    RVEpart.SetByBoolean(name='LOWERSIDE-FOURTHRING', sets=[RVEpart.sets['LOWERSIDE-FOURTHRING-RIGHT'],RVEpart.sets['LOWERSIDE-FOURTHRING-LEFT']])
    RVEpart.SetByBoolean(name='LOWERSIDE', sets=[RVEpart.sets['LOWERSIDE-FIRSTRING'],RVEpart.sets['LOWERSIDE-SECONDRING'],RVEpart.sets['LOWERSIDE-THIRDRING'],RVEpart.sets['LOWERSIDE-FOURTHRING']])
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.0,L,0.0),radius=0.001*Rf), name='UPPERSIDE')    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(L,0.5*L,0.0),radius=0.001*Rf), name='RIGHTSIDE')    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(-L,0.5*L,0.0),radius=0.001*Rf), name='LEFTSIDE')
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.5*Rf*np.cos((theta+deltatheta)*np.pi/180),0.5*Rf*np.sin((theta+deltatheta)*np.pi/180),0.0),radius=0.001*Rf), name='FIRSTCIRCLE')
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.75*Rf*np.cos(0.5*alpha*np.pi/180),0.75*Rf*np.sin(0.5*alpha*np.pi/180),0.0),radius=0.001*Rf), name='SECONDCIRCLE-LOWERCRACK')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.75*Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180),0.75*Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0),radius=0.001*Rf), name='SECONDCIRCLE-UPPERCRACK')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.75*Rf*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.75*Rf*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.0),radius=0.001*Rf), name='SECONDCIRCLE-FIRSTBOUNDED')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.75*Rf*np.cos((beta+0.5*deltaphi)*np.pi/180),0.75*Rf*np.sin((beta+0.5*deltaphi)*np.pi/180),0.0),radius=0.001*Rf), name='SECONDCIRCLE-SECONDBOUNDED')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.75*Rf*np.cos((gamma+0.5*(180.0-gamma))*np.pi/180),0.75*Rf*np.sin((gamma+0.5*(180.0-gamma))*np.pi/180),0.0),radius=0.001*Rf), name='SECONDCIRCLE-RESTBOUNDED')
    RVEpart.SetByBoolean(name='SECONDCIRCLE', sets=[RVEpart.sets['SECONDCIRCLE-LOWERCRACK'],RVEpart.sets['SECONDCIRCLE-UPPERCRACK'],RVEpart.sets['SECONDCIRCLE-FIRSTBOUNDED'],RVEpart.sets['SECONDCIRCLE-SECONDBOUNDED'],RVEpart.sets['SECONDCIRCLE-RESTBOUNDED']])
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(Rf*np.cos(0.5*alpha*np.pi/180),Rf*np.sin(0.5*alpha*np.pi/180),0.0),radius=0.001*Rf), name='THIRDCIRCLE-LOWERCRACK')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180),Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0),radius=0.001*Rf), name='THIRDCIRCLE-UPPERCRACK')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(Rf*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180),Rf*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.0),radius=0.001*Rf), name='THIRDCIRCLE-FIRSTBOUNDED')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(Rf*np.cos((beta+0.5*deltaphi)*np.pi/180),Rf*np.sin((beta+0.5*deltaphi)*np.pi/180),0.0),radius=0.001*Rf), name='THIRDCIRCLE-SECONDBOUNDED')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(Rf*np.cos((gamma+0.5*(180.0-gamma))*np.pi/180),Rf*np.sin((gamma+0.5*(180.0-gamma))*np.pi/180),0.0),radius=0.001*Rf), name='THIRDCIRCLE-RESTBOUNDED')
    RVEpart.SetByBoolean(name='THIRDCIRCLE', sets=[RVEpart.sets['THIRDCIRCLE-LOWERCRACK'],RVEpart.sets['THIRDCIRCLE-UPPERCRACK'],RVEpart.sets['THIRDCIRCLE-FIRSTBOUNDED'],RVEpart.sets['THIRDCIRCLE-SECONDBOUNDED'],RVEpart.sets['THIRDCIRCLE-RESTBOUNDED']])
    
    if L>2*Rf:
        R4 = 1.25*Rf
    else:
        R4 = Rf+0.25*(L-Rf)
        
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(R4*np.cos(0.5*alpha*np.pi/180),R4*np.sin(0.5*alpha*np.pi/180),0.0),radius=0.001*Rf), name='FOURTHCIRCLE-LOWERCRACK')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(R4*np.cos((alpha+0.5*deltapsi)*np.pi/180),R4*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0),radius=0.001*Rf), name='FOURTHCIRCLE-UPPERCRACK')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(R4*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180),R4*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.0),radius=0.001*Rf), name='FOURTHCIRCLE-FIRSTBOUNDED')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(R4*np.cos((beta+0.5*deltaphi)*np.pi/180),R4*np.sin((beta+0.5*deltaphi)*np.pi/180),0.0),radius=0.001*Rf), name='FOURTHCIRCLE-SECONDBOUNDED')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(R4*np.cos((gamma+0.5*(180.0-gamma))*np.pi/180),R4*np.sin((gamma+0.5*(180.0-gamma))*np.pi/180),0.0),radius=0.001*Rf), name='FOURTHCIRCLE-RESTBOUNDED')
    RVEpart.SetByBoolean(name='FOURTHCIRCLE', sets=[RVEpart.sets['FOURTHCIRCLE-LOWERCRACK'],RVEpart.sets['FOURTHCIRCLE-UPPERCRACK'],RVEpart.sets['FOURTHCIRCLE-FIRSTBOUNDED'],RVEpart.sets['FOURTHCIRCLE-SECONDBOUNDED'],RVEpart.sets['FOURTHCIRCLE-RESTBOUNDED']])
    
    if L>2*Rf:
        RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(1.5*Rf*np.cos((theta+deltatheta)*np.pi/180),1.5*Rf*np.sin((theta+deltatheta)*np.pi/180),0.0),radius=0.001*Rf), name='FIFTHCIRCLE')
    else:
        RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=((Rf+0.5*(L-Rf))*np.cos((theta+deltatheta)*np.pi/180),(Rf+0.5*(L-Rf))*np.sin((theta+deltatheta)*np.pi/180),0.0),radius=0.001*Rf), name='FIFTHCIRCLE')
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.85*Rf*np.cos(alpha*np.pi/180),0.75*Rf*np.sin(alpha*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-FIRSTFIBER')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(1.05*Rf*np.cos(alpha*np.pi/180),1.05*Rf*np.sin(alpha*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-FIRSTMATRIX')
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.85*Rf*np.cos((theta+deltatheta)*np.pi/180),0.75*Rf*np.sin((theta+deltatheta)*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-SECONDFIBER')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(1.05*Rf*np.cos((theta+deltatheta)*np.pi/180),1.05*Rf*np.sin((theta+deltatheta)*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-SECONDMATRIX')
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.85*Rf*np.cos(beta*np.pi/180),0.75*Rf*np.sin(beta*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-THIRDFIBER')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(1.05*Rf*np.cos(beta*np.pi/180),1.05*Rf*np.sin(beta*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-THIRDMATRIX')
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.85*Rf*np.cos(gamma*np.pi/180),0.75*Rf*np.sin(gamma*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-FOURTHFIBER')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(1.05*Rf*np.cos(gamma*np.pi/180),1.05*Rf*np.sin(gamma*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-FOURTHMATRIX')
    
    # sets of faces
    RVEpart.Set(faces=RVEfaces.findAt(((0.0, 0.25*L, 0),))), name='FIBER-CENTER')
    RVEpart.Set(faces=RVEfaces.findAt(((0.0, 0.65*L, 0),))), name='FIBER-INTERMEDIATEANNULUS')
    RVEpart.Set(faces=RVEfaces.findAt(((0.85*Rf*np.cos(0.5*alpha*np.pi/180), 0.85*Rf*np.sin(0.5*alpha*np.pi/180), 0),))), name='FIBER-EXTANNULUS-LOWERCRACK')
    RVEpart.Set(faces=RVEfaces.findAt(((0.85*Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180), 0.85*Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180), 0),))), name='FIBER-EXTANNULUS-UPPERCRACK')
    RVEpart.Set(faces=RVEfaces.findAt(((0.85*Rf*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180), 0.85*Rf*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180), 0),))), name='FIBER-EXTANNULUS-FIRSTBOUNDED')
    RVEpart.Set(faces=RVEfaces.findAt(((0.85*Rf*np.cos((beta+0.5*deltaphi)*np.pi/180), 0.85*Rf*np.sin((beta+0.5*deltaphi)*np.pi/180), 0),))), name='FIBER-EXTANNULUS-SECONDBOUNDED')
    RVEpart.Set(faces=RVEfaces.findAt(((0.85*Rf*np.cos((gamma+0.5*(180-gamma))*np.pi/180), 0.85*Rf*np.sin((gamma+0.5*(180-gamma))*np.pi/180), 0),))), name='FIBER-EXTANNULUS-RESTBOUNDED')
    RVEpart.SetByBoolean(name='FIBER-EXTANNULUS', sets=[RVEpart.sets['FIBER-EXTANNULUS-LOWERCRACK'],RVEpart.sets['FIBER-EXTANNULUS-UPPERCRACK'],RVEpart.sets['FIBER-EXTANNULUS-FIRSTBOUNDED'],RVEpart.sets['FIBER-EXTANNULUS-SECONDBOUNDED'],RVEpart.sets['FIBER-EXTANNULUS-RESTBOUNDED']])
    RVEpart.SetByBoolean(name='FIBER', sets=[RVEpart.sets['FIBER-CENTER'],RVEpart.sets['FIBER-INTERMEDIATEANNULUS'],RVEpart.sets['FIBER-EXTANNULUS']])
    
    if L>2*Rf:
        R1 = (1+0.5*0.25)*Rf
        R2 = (1.25+0.5*0.25)*Rf
    else:
        R1 = Rf+0.5*0.25*(L-Rf)
        R2 = Rf+1.5*0.25*(L-Rf)
        
    RVEpart.Set(faces=RVEfaces.findAt(((R1*np.cos(0.5*alpha*np.pi/180), R1*np.sin(0.5*alpha*np.pi/180), 0),))), name='MATRIX-INTANNULUS-LOWERCRACK')
    RVEpart.Set(faces=RVEfaces.findAt(((R1*np.cos((alpha+0.5*deltapsi)*np.pi/180), R1*np.sin((alpha+0.5*deltapsi)*np.pi/180), 0),))), name='MATRIX-INTANNULUS-UPPERCRACK')
    RVEpart.Set(faces=RVEfaces.findAt(((R1*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180), R1*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180), 0),))), name='MATRIX-INTANNULUS-FIRSTBOUNDED')
    RVEpart.Set(faces=RVEfaces.findAt(((R1*np.cos((beta+0.5*deltaphi)*np.pi/180), R1*np.sin((beta+0.5*deltaphi)*np.pi/180), 0),))), name='MATRIX-INTANNULUS-SECONDBOUNDED')
    RVEpart.Set(faces=RVEfaces.findAt(((R1*np.cos((gamma+0.5*(180-gamma))*np.pi/180), R1*np.sin((gamma+0.5*(180-gamma))*np.pi/180), 0),))), name='MATRIX-INTANNULUS-RESTBOUNDED')
    RVEpart.SetByBoolean(name='MATRIX-INTANNULUS', sets=[RVEpart.sets['MATRIX-INTANNULUS-LOWERCRACK'],RVEpart.sets['MATRIX-INTANNULUS-UPPERCRACK'],RVEpart.sets['MATRIX-INTANNULUS-FIRSTBOUNDED'],RVEpart.sets['MATRIX-INTANNULUS-SECONDBOUNDED'],RVEpart.sets['MATRIX-INTANNULUS-RESTBOUNDED']])
    RVEpart.Set(faces=RVEfaces.findAt(((0.0, R2, 0),))), name='MATRIX-INTERMEDIATEANNULUS')
    RVEpart.Set(faces=RVEfaces.findAt(((0.0, Rf+0.5*(L-Rf), 0),))), name='MATRIX-BODY')
    RVEpart.SetByBoolean(name='MATRIX', sets=[RVEpart.sets['MATRIX-BODY'],RVEpart.sets['MATRIX-INTERMEDIATEANNULUS'],RVEpart.sets['MATRIX-INTANNULUS']])
    
    RVEpart.SetByBoolean(name='RVE', sets=[RVEpart.sets['FIBER'],RVEpart.sets['MATRIX']])
                                    
    # sets of cells (none, i.e. 2D geometry)
    
    mdb.save()
    
#===============================================================================#
#                             Materials creation
#===============================================================================#    
    
    for material in parameters['materials']:
        mdb.models[modelname].Material(name=material['name'])
        try:
            values = material['elastic']['values']
            tuplelist = []
            valuelist = []
            for v,value in enumerate(values):
                if v>0 and v%8=0:
                    tuplelist.append(tuple(valuelist))
                    valuelist = []
                valuelist.append(value)
            tuplelist.append(tuple(valuelist))    
            mdb.models[modelname].materials[material['name']].Elastic(type=material['elastic']['type'],table=tuple(tuplelist))
        except Exception, error:
            sys.exc_clear()
        try:
            values = material['density']['values']
            tuplelist = []
            valuelist = []
            for v,value in enumerate(values):
                if v>0 and v%8=0:
                    tuplelist.append(tuple(valuelist))
                    valuelist = []
                valuelist.append(value)
            tuplelist.append(tuple(valuelist))    
            mdb.models[modelname].materials[material['name']].Density(table=tuple(tuplelist))
        except Exception, error:
            sys.exc_clear()
        try:
            values = material['thermalexpansion']['values']
            tuplelist = []
            valuelist = []
            for v,value in enumerate(values):
                if v>0 and v%8=0:
                    tuplelist.append(tuple(valuelist))
                    valuelist = []
                valuelist.append(value)
            tuplelist.append(tuple(valuelist))    
            mdb.models[modelname].materials[material['name']].Expansion(type=material['thermalexpansion']['type'],table=tuple(tuplelist))
        except Exception, error:
            sys.exc_clear()
        try:
            values = material['thermalconductivity']['values']
            tuplelist = []
            valuelist = []
            for v,value in enumerate(values):
                if v>0 and v%8=0:
                    tuplelist.append(tuple(valuelist))
                    valuelist = []
                valuelist.append(value)
            tuplelist.append(tuple(valuelist))    
            mdb.models[modelname].materials[material['name']].Conductivity(type=material['thermalconductivity']['type'],table=tuple(tuplelist))
        except Exception, error:
            sys.exc_clear()

    mdb.save()

#===============================================================================#
#                             Sections creation
#===============================================================================#
    
    for section in parameters['sections']:
        if 'HomogeneousSolidSection' in section['type'] or 'Homogeneous Solid Section' in section['type'] or 'somogeneoussolidsection' in section['type'] or 'homogeneous solid section' in section['type'] or 'Homogeneous solid section' in section['type']:
        mdb.models[modelname].HomogeneousSolidSection(name=section['name'], 
            material=section['material'], thickness=section['thickness'])
    
    mdb.save()
    
#===============================================================================#
#                             Sections assignment
#===============================================================================#  
    for sectionRegion in parameters['sectionRegions']:
        RVEpart.SectionAssignment(region=RVEpart.sets[sectionRegion['set']], sectionName=sectionRegion['name'], offset=0.0,offsetType=sectionRegion['offsetType'], offsetField=sectionRegion['offsetField'],thicknessAssignment=sectionRegion['thicknessAssignment'])
    
    # p.SectionAssignment(region=region, sectionName='MatrixSection', offset=0.0, 
    #     offsetType=MIDDLE_SURFACE, offsetField='', 
    #     thicknessAssignment=FROM_SECTION)
        
    mdb.save()
    
#===============================================================================#
#                             Instance creation
#===============================================================================#

    model.rootAssembly.DatumCsysByDefault(CARTESIAN)
    model.rootAssembly.Instance(name='RVE-assembly', part=RVEpart, dependent=OFF)
    
    mdb.save()
    
#===============================================================================#
#                             Step creation
#===============================================================================#
    
    model.StaticStep(name='Load-Step', previous='Initial', 
        minInc=1e-10)

    mdb.save()

#===============================================================================#
#                             Boundary conditions
#===============================================================================#
    
    # SOUTH side: symmetry line
    
    model.YsymmBC(name='SymmetryBound', createStepName='Load-Step', 
        region=model.rootAssembly.instances['RVE-assembly'].sets['LOWERSIDE'], localCsys=None)
    
    # NORTH side
    
    # if 'periodic' in parameters['boundaryConditions']['north']['type']:
    #     
    # elif 'rigidbar' in parameters['boundaryConditions']['north']['type']:
    # 
    # elif 'homogeneousdisplacement' in parameters['boundaryConditions']['north']['type']:
    #
    # else free
    
    # EAST side
    
    # if 'periodic' in parameters['boundaryConditions']['north']['type']:
    #
    # else free
    
    # WEST side
    
    # if 'periodic' in parameters['boundaryConditions']['north']['type']:
    #
    # else free
    
    mdb.save()
    
#===============================================================================#
#                                Applied load
#===============================================================================#    
    
    for load in parameters['loads']:
        if 'appliedstrain' in load['type'] or 'appliedStrain' in load['type'] or 'Applied Strain' in load['type'] or 'applied strain' in load['type']:
            model.DisplacementBC(name=load['name'],createStepName='Load-Step',region=model.rootAssembly.instances['RVE-assembly'].sets[load['set']], u1=load['value'][0]*L, u2=load['value'][1]*L, ur3=load['value'][2]*L, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='',localCsys=None)
        elif 'applieddisplacement' in load['type'] or 'appliedDisplacement' in load['type'] or 'Applied Displacement' in load['type'] or 'applied displacement' in load['type']:
            model.DisplacementBC(name=load['name'],createStepName='Load-Step',region=model.rootAssembly.instances['RVE-assembly'].sets[load['set']], u1=load['value'][0], u2=load['value'][1], ur3=load['value'][2], amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='',localCsys=None)
        # elif 'appliedstress' in load['type'] or 'appliedStress' in load['type'] or 'Applied Stress' in load['type'] or 'applied stress' in load['type']:
        # 
        # elif 'appliedforce' in load['type'] or 'appliedForce' in load['type'] or 'Applied Force' in load['type'] or 'applied Force' in load['type']:
    
    mdb.save()

#===============================================================================#
#                                   Crack
#===============================================================================#
   
    # assign seam
    model.rootAssembly.engineeringFeatures.assignSeam(regions=model.rootAssembly.instances['RVE-assembly'].sets['CRACK'])
        
    # contour integral
    xC = Rf*np.cos((theta+deltatheta)*np.pi/180)
    yC = Rf*np.sin((theta+deltatheta)*np.pi/180)
    xA = Rf*np.cos((theta+1.025*deltatheta)*np.pi/180)
    yA = -xC*(xA-xC)/yC + yC
    model.rootAssembly.engineeringFeatures.ContourIntegral(name='Debond',symmetric=OFF,crackFront=model.rootAssembly.instances['RVE-assembly'].sets['CRACK'],crackTip=model.rootAssembly.instances['RVE-assembly'].sets['CRACKTIP'],extensionDirectionMethod=Q_VECTORS, qVectors=(((xC,yC,0.0),(xA,yA,0.0)), ), midNodePosition=0.5, collapsedElementAtTip=NONE)
    
    mdb.save()

#===============================================================================#
#                                   Mesh
#===============================================================================#
    
    # assign mesh controls
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['FIBER-EXTANNULUS-LOWERCRACK'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['FIBER-EXTANNULUS-UPPERCRACK'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['FIBER-EXTANNULUS-FIRSTBOUNDED'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['MATRIX-INTANNULUS-LOWERCRACK'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['MATRIX-INTANNULUS-UPPERCRACK'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['MATRIX-INTANNULUS-FIRSTBOUNDED'], elemShape=QUAD, technique=STRUCTURED)
    
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['FIBER-CENTER'], elemShape=QUAD_DOMINATED, technique=FREE)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['FIBER-INTANNULUS'], elemShape=QUAD_DOMINATED, technique=FREE)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['FIBER-EXTANNULUS-SECONDBOUNDED'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['FIBER-EXTANNULUS-RESTBOUNDED'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['MATRIX-INTANNULUS-SECONDBOUNDED'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['MATRIX-INTANNULUS-RESTBOUNDED'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['MATRIX-EXTANNULUS'], elemShape=QUAD_DOMINATED, technique=FREE)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['MATRIX-BODY'], elemShape=QUAD_DOMINATED, technique=FREE)
    
    # assign seeds
    nTangential = np.floor(deltapsi/delta) 
    nRadialFiber = np.floor(0.25/delta)
    if L>2*Rf:
        nRadialMatrix = np.floor(0.25/delta)
    else:
        nRadialMatrix = np.floor(0.25*(L-Rf)/delta)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['SECONDCIRCLE-UPPERCRACK'], number=nTangential, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['SECONDCIRCLE-FIRSTBOUNDED'], number=nTangential, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['THIRDCIRCLE-UPPERCRACK'], number=nTangential, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['THIRDCIRCLE-FIRSTBOUNDED'], number=nTangential, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['FOURTHCIRCLE-UPPERCRACK'], number=nTangential, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['FOURTHCIRCLE-FIRSTBOUNDED'], number=nTangential, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-FIRSTFIBER'], number=nRadialFiber, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-FIRSTMATRIX'], number=nRadialMatrix, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-SECONDFIBER'], number=nRadialFiber, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-SECONDMATRIX'], number=nRadialMatrix, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-THIRDFIBER'], number=nRadialFiber, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-THIRDMATRIX'], number=nRadialMatrix, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['LOWERSIDE-SECONDRING-RIGHT'], number=nRadialFiber, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['LOWERSIDE-THIRDRING-RIGHT'], number=nRadialMatrix, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['LOWERSIDE-CENTER'], number=6, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['FIRSTCIRCLE'], number=18, constraint=FINER)
    nTangential1 = np.floor(deltaphi/parameters['delta2'])
    nTangential2 = np.floor((180-(theta+deltatheta+deltapsi+deltaphi))/parameters['delta3'])
    nTangential3 = np.floor(alpha/parameters['delta1'])
    nRadialFiber1 = np.floor(0.25/parameters['delta3'])
    if L>2*Rf:
        nRadialMatrix1 = np.floor(0.25/parameters['delta3'])
    else:
        nRadialMatrix1 = np.floor(0.25*(L-Rf)/(Rf*parameters['delta3']))
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['SECONDCIRCLE-SECONDBOUNDED'], number=nTangential1, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['SECONDCIRCLE-RESTBOUNDED'], number=nTangential2, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['THIRDCIRCLE-SECONDBOUNDED'], number=nTangential1, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['THIRDCIRCLE-RESTBOUNDED'], number=nTangential2, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['FOURTHCIRCLE-SECONDBOUNDED'], number=nTangential1, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['FOURTHCIRCLE-RESTBOUNDED'], number=nTangential2, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-FOURTHFIBER'], number=nRadialFiber1, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-FOURTHMATRIX'], number=nRadialMatrix1, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['SECONDCIRCLE-LOWERCRACK'], number=nTangential3, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['THIRDCIRCLE-LOWERCRACK'], number=nTangential3, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['FOURTHCIRCLE-LOWERCRACK'], number=nTangential3, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['FIFTHCIRCLE'], number=90, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['RIGHTSIDE'], number=30, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['LEFTSIDE'], number=30, constraint=FINER)
    
    # select element type
    if 'first' in parameters['elements']['order']:
        elemType1 = mesh.ElemType(elemCode=CPE4, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=CPE3, elemLibrary=STANDARD)
    elif 'second' in parameters['elements']['order']:
        elemType1 = mesh.ElemType(elemCode=CPE8, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=CPE6, elemLibrary=STANDARD)
    model.rootAssembly.setElementType(regions=model.rootAssembly.instances['RVE-assembly'].sets['RVE'], elemTypes=(elemType1, elemType2))
    
    # mesh part
    model.rootAssembly.generateMesh(regions=model.rootAssembly.instances['RVE-assembly'])
    
    mdb.save()
    
    p1 = mdb.models[modelname].parts['RVE']
    
    p = mdb.models[modelname].parts['RVE']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#2c76 ]', ), )
    p.Set(faces=faces, name='StructuredMeshRegion')
    a = mdb.models[modelname].rootAssembly
    a.regenerate()
    
    a1 = mdb.models[modelname].rootAssembly
    p = mdb.models[modelname].parts['RVE']
    a1.Instance(name='RVE-2', part=p, dependent=OFF)
    a = mdb.models[modelname].rootAssembly
    f1 = a.instances['RVE-2'].faces
    pickedRegions = f1.getSequenceFromMask(mask=('[#2c76 ]', ), )
    
    model.rootAssembly.setMeshControls(regions=pickedRegions, elemShape=QUAD, technique=STRUCTURED)
    
    mdb.save()
    
#===============================================================================#
#                                   Output
#===============================================================================#
    
    # field output
    
    # history output
    model.historyOutputRequests['H-Output-1'].setValues(contourIntegral='Debond',sectionPoints=DEFAULT,rebar=EXCLUDE,numberOfContours=2)

#===============================================================================#
#                                Job creation
#===============================================================================#
    mdb.Job(name='Job-' + modelname, model=modelname, description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=99, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=ON, modelPrint=ON, contactPrint=ON, historyPrint=ON, userSubroutine='',scratch='', multiprocessingMode=DEFAULT, numCpus=12, numDomains=12,numGPUs=0)
    mdb.jobs['Job-1'].submit(consistencyChecking=OFF)

def main(argv):

if __name__ == "__main__":
    main(sys.argv[1:])
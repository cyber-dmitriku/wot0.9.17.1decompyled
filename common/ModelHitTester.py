# Source Generated with Decompyle++
# File: ModelHitTester.pyc (Python 2.6)

import math
import random
import BigWorld
import ResMgr
from Math import Vector3, Vector2, Matrix
from debug_utils import *

class ModelHitTester(object):
    bbox = None
    
    def _ModelHitTester__setBspModelName(self, value):
        self.releaseBspModel()
        self._ModelHitTester__bspModelName = value

    bspModelName = property((lambda self: self._ModelHitTester__bspModelName), _ModelHitTester__setBspModelName)
    
    def __init__(self, dataSection = None):
        self._ModelHitTester__bspModel = None
        self._ModelHitTester__bspModelName = None
        if dataSection is not None:
            self._ModelHitTester__bspModelName = dataSection.readString('collisionModel')
            if not self._ModelHitTester__bspModelName:
                raise Exception, '<collisionModel> is missing or wrong'
        

    
    def isBspModelLoaded(self):
        return self._ModelHitTester__bspModel is not None

    
    def loadBspModel(self):
        if self._ModelHitTester__bspModel is not None:
            return None
        bspModel = BigWorld.WGBspCollisionModel()
        if not bspModel.setModelName(self.bspModelName):
            raise Exception, "wrong collision model '%s'" % self.bspModelName
        bspModel.setModelName(self.bspModelName)
        self._ModelHitTester__bspModel = bspModel
        self.bbox = bspModel.getBoundingBox()

    
    def releaseBspModel(self):
        if self._ModelHitTester__bspModel is not None:
            self._ModelHitTester__bspModel = None
            del self.bbox
        

    
    def localAnyHitTest(self, start, stop):
        return self._ModelHitTester__bspModel.collideSegmentAny(start, stop)

    
    def localHitTest(self, start, stop):
        return self._ModelHitTester__bspModel.collideSegment(start, stop)

    
    def worldHitTest(self, start, stop, worldMatrix):
        worldToLocal = Matrix(worldMatrix)
        worldToLocal.invert()
        testRes = self._ModelHitTester__bspModel.collideSegment(worldToLocal.applyPoint(start), worldToLocal.applyPoint(stop))
        if testRes is None:
            return None
        res = []
        for (dist, normal, hitAngleCos, matKind) in testRes:
            res.append((dist, worldMatrix.applyVector(normal), hitAngleCos, matKind))
        
        return res

    
    def localSphericHitTest(self, center, radius, bOutsidePolygonsOnly = True):
        return self._ModelHitTester__bspModel.collideSphere(center, radius, bOutsidePolygonsOnly)



class VehicleHitTester(object):
    
    def __init__(self, chassisHt, hullHt, hullOffset):
        self._VehicleHitTester__args = (chassisHt, hullHt, hullOffset)
        self._VehicleHitTester__bbox = None
        self._VehicleHitTester__boundingRadiusSquared = None

    
    def mayHit(self, start, stop, center = Vector3()):
        radiusSquared = self._VehicleHitTester__boundingRadiusSquared
        if radiusSquared is None:
            self._VehicleHitTester__getBbox()
            radiusSquared = self._VehicleHitTester__boundingRadiusSquared
        
        start = start - center
        stop = stop - center
        ao = Vector2(-(start.x), -(start.z))
        bo = Vector2(-(stop.x), -(stop.z))
        ab = ao - bo
        e = ao.dot(ab)
        if e <= 0:
            return ao.lengthSquared <= radiusSquared
        if e >= ab.lengthSquared:
            return bo.length <= radiusSquared
        return ao.lengthSquared - e * e / ab.lengthSquared <= radiusSquared

    
    def _VehicleHitTester__getBbox(self):
        if self._VehicleHitTester__bbox is None:
            (bbox1, bbox2, offs) = self._VehicleHitTester__args
            bbox1 = bbox1.bbox
            bbox2 = bbox2.bbox
            minPt = _combineChassisHullCorners(bbox1[0], bbox2[0], offs, min)
            maxPt = _combineChassisHullCorners(bbox1[1], bbox2[1], offs, max)
            p0 = Vector3()
            radiusSquared = max(minPt.flatDistSqrTo(p0), maxPt.flatDistSqrTo(p0))
            self._VehicleHitTester__bbox = (minPt, maxPt, math.sqrt(radiusSquared))
            self._VehicleHitTester__boundingRadiusSquared = radiusSquared
        
        return self._VehicleHitTester__bbox

    bbox = property(_VehicleHitTester__getBbox)


def _combineChassisHullCorners(c, h, hullOffs, selector):
    return Vector3(selector(c.x, h.x + hullOffs.x), c.y, selector(c.z, h.z + hullOffs.z))



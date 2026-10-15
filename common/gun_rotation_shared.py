# Source Generated with Decompyle++
# File: gun_rotation_shared.pyc (Python 2.6)

import BigWorld
from math import pi
from constants import DEFAULT_GUN_PITCH_LIMITS_TRANSITION

def calcPitchLimits(turretYaw, basicLimits, frontLimits, backLimits, transition):
    if transition is None:
        transition = DEFAULT_GUN_PITCH_LIMITS_TRANSITION
    
    if frontLimits is not None:
        absYaw = abs(turretYaw)
        if absYaw < frontLimits[2]:
            return (frontLimits[0], frontLimits[1])
        if absYaw < frontLimits[2] + transition:
            t = (absYaw - frontLimits[2]) / transition
            minPitch = frontLimits[0] * (1 - t) + basicLimits[0] * t
            maxPitch = frontLimits[1] * (1 - t) + basicLimits[1] * t
            return (minPitch, maxPitch)
    
    if backLimits is not None:
        absYawDiff = abs(abs(turretYaw) - pi)
        if absYawDiff < backLimits[2]:
            return (backLimits[0], backLimits[1])
        if absYawDiff < backLimits[2] + transition:
            t = (absYawDiff - backLimits[2]) / transition
            minPitch = backLimits[0] * (1 - t) + basicLimits[0] * t
            maxPitch = backLimits[1] * (1 - t) + basicLimits[1] * t
            return (minPitch, maxPitch)
    
    return basicLimits


def calcPitchLimitsFromDesc(turretYaw, pitchLimitsDesc):
    return calcPitchLimits(turretYaw, pitchLimitsDesc['basic'], pitchLimitsDesc.get('front'), pitchLimitsDesc.get('back'), pitchLimitsDesc.get('transition'))


def encodeAngleToUint(angle, bits):
    mask = (1 << bits) - 1
    return int(round((mask + 1) * (angle + pi) / pi * 2)) & mask


def decodeAngleFromUint(code, bits):
    return pi * 2 * code / (1 << bits) - pi


def encodeRestrictedAngleToUint(angle, bits, minBound, maxBound):
    t = (angle - minBound) / (maxBound - minBound)
    t = _clamp(0, t, 1)
    mask = (1 << bits) - 1
    return int(round(mask * t)) & mask


def decodeRestrictedAngleFromUint(code, bits, minBound, maxBound):
    t = float(code) / ((1 << bits) - 1)
    return minBound + t * (maxBound - minBound)


def encodeGunAngles(yaw, pitch, pitchLimits):
    return encodeAngleToUint(yaw, 10) << 6 | encodeRestrictedAngleToUint(pitch, 6, *pitchLimits)


def decodeGunAngles(code, pitchLimits):
    return (decodeAngleFromUint(code >> 6 & 1023, 10), decodeRestrictedAngleFromUint(code & 63, 6, *pitchLimits))


def _clamp(minBound, value, maxBound):
    if value < minBound:
        return minBound
    if value > maxBound:
        return maxBound
    return value



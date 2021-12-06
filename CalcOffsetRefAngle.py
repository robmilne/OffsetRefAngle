#!/usr/bin/python3

import numpy as np


class OffsetRefAngle(object):
    def __init__(self, precision, debug):
        self.precision = precision
        self.debug = debug

    '''
    GetDegrees - Mirror reflection both solutions (degree input)
    '''
    def GetDegrees(self, ref_angle, dist_ratio):
        ref_angle = np.deg2rad(ref_angle)
        outer_angle = np.rad2deg(self.Calc(ref_angle, dist_ratio))
        inner_angle = np.rad2deg(self.Calc(ref_angle, dist_ratio, False))
        return(outer_angle, inner_angle)

    '''
    GetDegree - Mirror reflection outer solution (angle > ref_angle/2)
    '''
    def GetOuterDegree(self, ref_angle, dist_ratio):
        ref_angle = np.deg2rad(ref_angle)
        return (np.rad2deg(self.Calc(ref_angle, dist_ratio)))

    '''
    GetRadians - Mirror reflection both solutions
    '''
    def GetRadians(self, ref_angle, dist_ratio):
        outer_angle = self.Calc(ref_angle, dist_ratio)
        inner_angle = self.Calc(ref_angle, dist_ratio, False)
        return(outer_angle, inner_angle)

    '''
    GetRadian - Mirror reflection outer solution (angle > ref_angle/2)
    '''
    def GetOuterRadian(self, ref_angle, dist_ratio):
        return (self.Calc(ref_angle, dist_ratio))

    '''
    Calc
    Approximate the reflection angle of a mirror offset from its axis of
    rotation.

    The first argument is the origin reflection angle (centre of rotation).
    The second argument is the target distance ratio (ratio of target-origin
    distance to the radius of mirror rotation)

    The algorithm has two possible solutions since the result is asymptotic as
    the result approaches origin_reflection_angle/2 from either the positive or
    negative side.  The third argument selects the side.

    Iteration concludes when the distance_ratio approximation deviates from the
    actual value by less than the set precision.
    '''
    def Calc(self, ref_angle, dist_ratio, is_outer=True):
        i = 0
        angle = 0.0

        if is_outer:
            x = 3
        else:
            x = 1

        while True:
            angle = (x / np.power(2, i + 2)) * ref_angle
            temp_ratio = np.abs( np.sin(angle)
                                 /
                                 np.sin(
                                            (
                                                (x - np.power(2, i + 1))
                                                /
                                                np.power(2, i + 1)
                                            ) * ref_angle
                                        )
                               )
            if self.debug:
                print(f'i:{i} x:{x} angle:{np.rad2deg(angle)}'
                      f' temp_ratio:{temp_ratio}')

            if temp_ratio == dist_ratio:
                break

            i += 1
            if temp_ratio < dist_ratio:
                # Make the next approximation closer to ref_angle/2
                if is_outer:
                    x = x * 2 - 1
                else:
                    x = x * 2 + 1
                if dist_ratio - temp_ratio < self.precision:
                    break
            else:
                # Make the next approximation further away from ref_angle/2
                if is_outer:
                    x = x * 2 + 1
                else:
                    x = x * 2 - 1
                if temp_ratio - dist_ratio < self.precision:
                    break

        if self.debug:
            if is_outer:
                print(f'Outer Angle: {np.rad2deg(angle):.6f}' + '\u00b0'
                      f'  ({angle:.6f} radians)')
            else:
                print(f'Inner Angle: {np.rad2deg(angle):.6f}' + '\u00b0'
                      f'  ({angle:.6f} radians)')
            print(f'  {i} iterations\n')
        return (angle)

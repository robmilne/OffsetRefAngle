#!/usr/bin/python

from CalcOffsetRefAngle import OffsetRefAngle

def main():
    offset_ref_angle = OffsetRefAngle(0.0001, True)
    angle = offset_ref_angle.GetDegrees(22.5, 5)
    print(f'angle: {angle}')

if __name__ == '__main__':
    main()

# HW1 – Free Fall
# Write a program that calculates the time it takes for
# a ball to drop from a user specified height to reach the ground.
# Use argparse.
# Allow the user to choose different values of gravity.
# And any other features you think maybe interesting.

import argparse
import string

#import height_convert

parser = argparse.ArgumentParser(
                   prog = "FreeFall",
                   description="Calculates the time [s] for an object "
                               "to fall h meters in a gravity of "
                               "g = 9.81 m/s^2")

parser.add_argument( "h",
                    type=float,
                    help = "Height of object above ground IN METERS")


parser.add_argument('-g',
                    default = 9.81,
                    type = float,
                    help = "value of gravity the object experiences in m/s^2 "
                           "--> defaults to 9.81 m/s^2 (Earth gravity)")

parser.add_argument("-round",
                    default = None,
                    type = int,
                    help = "rounds output to a specified place")

args = parser.parse_args()
#parser.print_help()

if args.round:
    print("This object takes ~", f"{round((2 * args.h / args.g) ** 0.5, args.round)}",
          f"seconds to fall {args.h} meters when gravity is {args.g} m/s^2")
else:
    print("This object takes", (2 * args.h / args.g) ** 0.5, f"seconds to fall {args.h} meters when gravity is "
                                                               f"{args.g} m/s^2")

# A robot controller

This project contains `python` libraries needed to drive a home-made lego robot. Human interface devices like a mouse, a trackpad or a SNES-style gamepad issue commands to the robot and make it move. Control is limited to a robot with four degrees of freedom at present without clever kinematics ie. commands from the controller simply move single joints or the end-effector (grasper) rather than moving multiple joints simultaneously and mapping to the end-effector frame of reference.

## Installation

**Note**: _No wheel is available on pypi.org. You will have to either build the wheel yourself and install that or install as develop._

The following commands should install as develop...
```
$ cd daveshed-adafruit-jc/daveshed
$ pip install -e .
$ cd daveshed-legobot/daveshed
$ pip install -e .
```
## Getting started

Check out `examples/` for ideas on how to fire up the application. You will find examples on how to connect up different input devices and a stub robot implementation in case you don't have any hardware available and want to get a flavour of how this works. This might be a good place to start if you have a regular mouse handy...
```
$ python -i examples/mouse.py
```
Issuing a keyboard interrupt or `application.terminate()` command should stop the application when you're ready.

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import platform
import subprocess


class MachineInfo(object):
  def __init__(self):
    pass

  def run(self):
    self._system_information()
    self._environment_settings()
    self._python_installation()
    self._module_import()
    return 0

  def _system_information(self):
    print("Information about the Operating System")
    print("  Operating System:\t{0}".format(platform.system()))
    print("  Architecture:\t\t{0}".format(platform.machine()))
    print("  Platform:\t\t{0}".format(platform.platform()))
    print("  Version:\t\t{0}".format(platform.version()))
    print("  Processor:\t\t{0}".format(platform.processor()))

    if sys.platform == "linux2":
      process = subprocess.Popen("lsb_release", stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)
      output, errors = process.communicate()
      if len(errors) > 0:
        print("  LSB:\t\t\t{0}".format(errors))
      else:
        print("  LSB:\t\t\t{0}".format(output))

    print

  def _python_installation(self):
    print("Information about the used Python environment")
    print("  Version:\t\t{0}".format(platform.python_version()))
    print("  Implementation:\t{0}".format(platform.python_implementation()))
    print("  Compiler:\t\t{0}".format(platform.python_compiler()))
    print("  Build:\t\t{0}, {1}".format(platform.python_build()[0],
                                        platform.python_build()[1]))
    print("  Location:\t\t{0}".format(sys.executable))
    print("  Byteorder:\t\t{0}".format(sys.byteorder))

    print

  def _module_import(self):
    print("Trying to import modules")
    try:
      import numpy
      print("  numpy:\t\t{0}".format(numpy.__version__))
    except ImportError as e:
      print("  numpy:\t\t{0}".format(e))

    try:
      import pcraster
      print("  pcraster:\t\tmodule found")
    except ImportError as e:
      print("  pcraster:\t\t{0}".format(e))

  def _environment_settings(self):
    print("Information about the used environment settings")

    env_vars = ["PATH", "PYTHONPATH"]

    if sys.platform == "linux2":
      env_vars.append("LD_LIBRARY_PATH")
    if sys.platform == "darwin":
      env_vars.append("DYLD_LIBRARY_PATH")

    for var in env_vars:
      try:
        print("  {0}:\n{1}".format(var, os.environ[var]))
      except KeyError:
        print("  {0}: not found".format(var))

    print

if __name__ == "__main__":
  sys.exit(MachineInfo().run())

mgz2imgslices 1.0
=================

Quick Overview
--------------

-  Convert ``.mgz`` inputs to ``jpg`` or ``png`` outputs.

Overview
--------

``mgz2imgslices`` is a simple Python utility which converts mgz files to readable formats like PNG/JPEG, separately for each label defined within it.

It takes an ``mgz`` volume as input, masks it based on different labels (creating separate directories for each label) and converts it into slices of PNG/JPG format for each label. 

Dependencies
------------

Make sure that the following dependencies are installed on your host system (or even better, a ``python3`` virtual env):

-  ``pfmisc`` : (a general miscellaneous module for color support, etc)
-  ``nibabel`` : (to read NIfTI files)
-  ``numpy`` : (to support large, multidimensional arrays and matrices)
-  ``imageio`` : (interface to read and write image data) 
-  ``pandas`` : (data manipulation and analysis)
-  ``re`` : (support for regular expressions)
-  ``time`` : (support for various time related functions)

Assumptions
-----------

This document assumes UNIX conventions and a ``bash`` shell. The script should work fine under Windows, but we have not actively tested on that platform -- our dev envs are Linux Ubuntu and macOS.

Installation
~~~~~~~~~~~~

Python module
~~~~~~~~~~~~~

One method of installing this script and all of its dependencies is by fetching it from `PyPI <https://pypi.org/project/med2image/>`_.

.. code:: bash

        pip3 install mgz2imgslices

Should you get an error about ``python3-tk`` not installed, simply do (for example on Ubuntu):

.. code:: bash

        sudo apt-get update
        sudo apt-get install -y python3-tk

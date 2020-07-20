mgz2imgslices 1.0.1
===================

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

Docker container
~~~~~~~~~~~~~~~~

We also offer a docker container of ``mgz2imgslices`` as a ChRIS-conformant platform plugin here https://github.com/FNNDSC/pl-mgz2imgslices -- please consult that page for information on running the dockerized container. The containerized version exposes a similar CLI and functionality as this module.

How to Use
----------

``mgz2imgslices`` needs at a minimum the following required command line arguments:

- ``-i | --inputFile <inputFile>`` : Input ``.mgz`` file to convert

- ``-d | --outputDir <outputDir> :`` The directory to contain the converted output label directories containing image slices

Examples
--------

First, let's create a directory, say ``devel`` wherever you feel like it. We will place some test data in this directory to process with this plugin.

.. code:: bash

    cd ~/
    mkdir devel
    cd devel
    export DEVEL=$(pwd)

Now, we need to fetch sample MGZ data. 

Pull MGZ data
~~~~~~~~~~~~~

- We provide a sample directory of a few ``.mgz`` volumes here. (https://github.com/FNNDSC/mgz_converter_dataset.git)

- Clone this repository (``mgz_converter_dataset``) to your local computer.

.. code:: bash

    git clone https://github.com/FNNDSC/mgz_converter_dataset.git

Make sure the ``mgz_converter_dataset`` directory is placed in the devel directory.

- Make sure your current working directory is ``devel``. At this juncture it should contain `mgz_converter_dataset``.

- Create an output directory named ``results`` in ``devel``.

.. code:: bash

    mkdir results && chmod 777 results

**EXAMPLE-1**

- Run ``mgz2imgslices`` using the following command. Change the arguments according to your need. 

.. code:: bash

    mgz2imgslices  
        -I ${DEVEL}/mgz_converter_dataset/100307/                              \
        -inputFile aparc.a2009s+aseg.mgz                                       \
        --outputDir ${DEVEL}/results/                                          \ 
        --outputFileStem sample                                                \
        --outputFileType jpg                                                   \
        --label label                                                          \         
        --wholeVolume FullVolume                                               \
        --lookuptable __val__                                                  \
        --skipLabelValueList 0,4,7                                              

The above command shall create the following directories and files within the ``results`` directory similar to the following structure:

.. code:: bash

    results/label-002/sample-000.jpg
    ...
    results/label-002/sample-00255.jpg

    ......

    results/label-0012175/sample-000.jpg
    ...
    results/label-0012175/sample-00255.jpg


**EXAMPLE-2**

- This example uses the "FreeSurferColorLUT.txt" file to name the label directories instead of numerical values.

- Make sure that your LUT.txt file is present in the ``([-I] [--inputDir])`` (in this case: ``${DEVEL}/mgz_converter_dataset/100307/``) and follows the format of the ``FreeSurferColorLUT.txt`` file. (https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/AnatomicalROI/FreeSurferColorLUT)

- Run ``mgz2imgslices`` using the following command. Change the arguments according to your need. 

.. code:: bash

   mgz2imgslices  
        -I ${DEVEL}/mgz_converter_dataset/100307/                              \
        -inputFile aparc.a2009s+aseg.mgz                                       \
        --outputDir ${DEVEL}/results/                                          \ 
        --outputFileStem sample                                                \
        --outputFileType jpg                                                   \
        --label label                                                          \         
        --wholeVolume FullVolume                                               \
        --lookuptable FreeSurferColorLUT.txt                                                  \
        --skipLabelValueList 0,4,7                                               

The above command will create resultant directories named after the ``Label Names`` within the ``results`` directory as shown below:

.. code:: bash

    results/label-Left-Cerebral-White-Matter/sample-000.jpg
    ...
    results/label-Left-Cerebral-White-Matter/sample-00255.jpg

    ......

    results/label-ctx_rh_S_temporal_transverse/sample-000.jpg
    ...
    results/label-ctx_rh_S_temporal_transverse/sample-00255.jpg


Command Line Arguments
----------------------

::

    ARGS

        [-i] [--inputFile] <inputFile>
        Input file to convert. Should be a .mgz file.

        [-o] [--outputFileStem] <outputFileStem>
        The output file stem to store conversion. If this is specified
        with an extension, this extension will be used to specify the
        output file type.

        [-t] [--outputFileType] <outputFileType>
        The output file type. If different to <outputFileStem> extension,
        will override extension in favour of <outputFileType>. Should be a 'png' or 'jpg'.

        [--label] <prefixForLabelDirectories>
        Adds a prefix to each Label directory name.

        [-n] [--normalize]
        If specified, will normalize the output image pixels to 0 and 1 values.

        [-l] [--lookuptable] <LUTcolumnToNameDirectories>
        Specifies if the label directories that are created should be named 
        according to Label Number or Label Name. 
        Can be wither "__val__" or <LUTFilename.txt> provided by user from the inputdir
        Default is "__val__" which is Label Numbers.

        [-s] [--skipLabelValueList] <ListOfLabelNumbersToSkip>
        If specified as a comma separated string of label numbers,
        will not create directories of those label numbers.

        [-w] [--wholeVolume]
        If specified, creates a diretory called "WholeVolume" (within the outputdir) 
        containing PNG/JPG files including all labels.

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta np_data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 

        [-y] [--synopsis]
        Show short synopsis.
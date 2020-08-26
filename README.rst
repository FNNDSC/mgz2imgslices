mgz2imgslices 1.0.18
====================

Quick Overview
--------------

-   Filters ``mgz`` volume files by voxel value to well organized directories of image files.

Overview
--------

``mgz2imgslices`` is a simple Python utility that fiters "labels" from ``mgz`` volume files and saves each label set as slices of (by default) ``png`` files, organized into a series of directories, one per label set.

An ``mgz`` format file simply contains a 3D volume data structure of image values. Often these values are interpreted to be image intensities. Sometimes, however, they can be interpreted as label identifiers. Regardless of the interpretation, the volume image data is simply a number value in each voxel of the volume.

This script will scan across the input ``mgz`` volume, and for each voxel value create a new output directory. In that directory will be a set of (typically) ``png`` images, one per slice of the original volume. These images will only contain the voxels in the original dataset that all had that particular voxel value.

In this manner, ``mgz2imgslices`` can also be thought of as a dynamic filter of an ``mgz`` volume file that filters each voxel value into its own output directory of ``png`` image files.

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

Docker container
~~~~~~~~~~~~~~~~

We also offer a docker container of ``mgz2imgslices`` as a ChRIS-conformant platform plugin here https://github.com/FNNDSC/pl-mgz2imgslices -- please consult that page for information on running the dockerized container. The containerized version exposes a similar CLI and functionality as this module.

How to Use
----------

``mgz2imgslices`` needs at a minimum the following required command line arguments:

- ``-i | --inputFile <inputFile>``: The input ``.mgz`` file to convert.

- ``-d | --outputDir <outputDir>``:  The output directory. This in turn will contain several subdirectores, one per image voxel value in the input ``mgz`` file. Each of these sub directories will contain ``png`` files, filtered to that voxel value.

Examples
--------

First, let's create a directory, say ``devel`` wherever you feel like it. We will place some test data in this directory to process with this plugin.

.. code:: bash

    cd ~/
    mkdir devel
    cd devel
    export DEVEL=$(pwd)

Now, we need to fetch sample MGZ data.

Pull ``mgz`` data
~~~~~~~~~~~~~~~~~

- We provide a sample directory of a few ``.mgz`` volumes here. (https://github.com/FNNDSC/mgz_converter_dataset.git)

- Clone this repository (``mgz_converter_dataset``) to your local computer.

.. code:: bash

    git clone https://github.com/FNNDSC/mgz_converter_dataset.git

Make sure the ``mgz_converter_dataset`` directory is placed in the devel directory.

- Make sure your current working directory is ``devel``. At this juncture it should contain ``mgz_converter_dataset``.

- Create an output directory named ``results`` in ``devel``.

.. code:: bash

    mkdir results && chmod 777 results

EXAMPLE 1
^^^^^^^^^

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

The ``skipLabelValueList`` will skip any voxels in the input ``mgz`` that have numerical values of, in this case, ``0, 4, 7``. Note that each output filtered directory will have a name prefix string of ``label`` and should appear something similar to:

.. code:: bash

    results/label-002/sample-000.jpg
                        ...
    results/label-002/sample-00255.jpg

    ...
    ...

    results/label-0012175/sample-000.jpg
                        ...
    results/label-0012175/sample-00255.jpg


EXAMPLE 2
^^^^^^^^^

- This example uses the ``FreeSurferColorLUT.txt`` file to lookup textual names of the voxel values and use more descriptive string for the directory stem.

- Make sure that your ``LUT.txt`` file is present in the ``([-I] [--inputDir])`` (in this case: ``${DEVEL}/mgz_converter_dataset/100307/``) and follows the format of the ``FreeSurferColorLUT.txt`` file. (https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/AnatomicalROI/FreeSurferColorLUT)

- Run ``mgz2imgslices`` using the following command. Change the arguments according to your need.

.. code:: bash

   mgz2imgslices
        -I ${DEVEL}/mgz_converter_dataset/100307/                               \
        -inputFile aparc.a2009s+aseg.mgz                                        \
        --outputDir ${DEVEL}/results/                                           \
        --outputFileStem sample                                                 \
        --outputFileType jpg                                                    \
        --label label                                                           \
        --wholeVolume FullVolume                                                \
        --lookuptable FreeSurferColorLUT.txt                                    \
        --skipLabelValueList 0,4,7

As above, this will skip some values in the input ``mgz`` file and create filtered directories in the output. However, instead of naming the output directories with the numerical value of the filtered (labelled) voxel value, the directory names will be looked up in the ``lookuptable`` file which associates a given voxel numerical value with a text name.

Note that as above also, the output filtered directories are prefixed in this case with the text string ``label``.

.. code:: bash

    results/label-Left-Cerebral-White-Matter/sample-000.jpg
                            ...
    results/label-Left-Cerebral-White-Matter/sample-00255.jpg

    ...
    ...

    results/label-ctx_rh_S_temporal_transverse/sample-000.jpg
                            ...
    results/label-ctx_rh_S_temporal_transverse/sample-00255.jpg


Command Line Arguments
----------------------

::

    ARGS

        [-i|--inputFile  <inputFile>]
        Input file to convert. Should be an ``mgz`` file.

        [-o|--outputFileStem <outputFileStem>]
        The output file stem to store image conversion. If this is specified
        with an extension, this extension will be used to specify the
        output file type.

        [-t|--outputFileType <outputFileType>]
        The output file type. If different to <outputFileStem> extension,
        will override extension in favour of <outputFileType>.

        Should be a ``png`` or ``jpg``.

        [--label <prefixForLabelDirectories>]
        Prefixes the string <prefixForLabelDirectories> to each filtered
        directory name. This is mostly for possible downstream processing,
        allowing a subsequent operation to easily determine which of the output
        directories correspond to labels.

        [-n|--normalize]
        If specified, will normalize the output image pixel values to
        0 and 1, otherwise pixel image values will retain the value in
        the original input volume.

        [-l|--lookuptable <LUTfile>]
        If passed, perform a looktup on the filtered voxel label values
        according to the contents of the <LUTfile>. This <LUTfile> should
        conform to the FreeSurfer lookup table format (documented elsewhere).

        Note that the special <LUTfile> string ``__val__`` can be passed which
        effectively means "no <LUTfile>". In this case, the numerical voxel
        values are used for output directory names. This special string is
        really only useful for scripted cases of running this application when
        modifying the CLI is more complex than simply setting the <LUTfile> to
        ``__val__``.

        [-s|--skipLabelValueList <ListOfLabelNumbersToSkip>]
        If specified as a comma separated string of label numbers,
        will not create directories of those label numbers.

        [-f|--filterLabelValues <ListOfVoxelValuesToInclude>]
        The logical inverse of the [skipLabelValueList] flag. If specified,
        only filter the comma separated list of passed voxel values from the
        input volume.

        The detault value of "-1" implies all voxel values should be filtered.

        [-w|--wholeVolume <wholeVolDirName>]
        If specified, creates a diretory called <wholeVolDirName> (within the
        outputdir) containing PNG/JPG images files of the entire input.

        This effectively really creates a PNG/JPG conversion of the input
        mgz file.

        Values in the image files will be the same as the original voxel
        values in the ``mgz``, unless the [--normalize] flag is specified
        in which case this creates a single-value mask of the input image.

        [-h|--help]
        If specified, show help message and exit.

        [--json]
        If specified, show json representation of app and exit.

        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta np_data and exit.

        [--savejson <DIR>]
        If specified, save json representation file to DIR and exit.

        [-v <level>|--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number and exit.

        [-y|--synopsis]
        Show short synopsis.


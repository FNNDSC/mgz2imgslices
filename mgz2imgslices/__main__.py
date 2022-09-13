#!/usr/bin/env python3
#
#
# (c) 2017-2022 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                     Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

# System imports

import  os
import  sys
import  argparse

try:
    from    .               import mgz2imgslices
    from    .               import __pkg, __version__
except:
    from mgz2imgslices      import mgz2imgslices
    from __init__           import __pkg, __version__

from    mgz2imgslices       import mgz2imgslices
from    argparse            import RawTextHelpFormatter
from    argparse            import ArgumentParser
from    pfmisc._colors      import Colors
import  pudb

str_desc    = Colors.CYAN + """

                      _____ _                     _ _
                     / __  (_)                   | (_)
 _ __ ___   __ _ ____`' / /'_ _ __ ___   __ _ ___| |_  ___ ___  ___
| '_ ` _ \ / _` |_  /  / / | | '_ ` _ \ / _` / __| | |/ __/ _ \/ __|
| | | | | | (_| |/ / ./ /__| | | | | | | (_| \__ \ | | (_|  __/\__ \\
|_| |_| |_|\__, /___|\_____/_|_| |_| |_|\__, |___/_|_|\___\___||___/
            __/ |                        __/ |
           |___/                        |___/

    Filters mgz volume files by voxel value to well organized
    directories of image files.

                    -- version """ + \
           Colors.YELLOW + __version__ + Colors.CYAN + """ --

    'mgz2imgslices' filters .mgz files to more web-friendly formats such as
    png and jpg, and organizes these images in group-directories, each of
    which is filtered to one value in the original input.

""" + Colors.NO_COLOUR

package_CLIcore = '''
        -i|--inputFile <inputFile>                                              \\
        [-d|--outputDir <outputDir>]                                            \\
        [-I|--inputDir <inputDir>]                                              \\
        [-h|--help]                                                             \\
        [--json]                                                                \\
        [--man]                                                                 \\
        [--meta]                                                                \\
        [--savejson <DIR>]                                                      \\
        [-v|--verbosity <level>]                                                \\
        [--version]                                                             \\
        [-y|--synopsis]
'''

package_CLI = '''
        [-o|--outputFileStem]<outputFileStem>]                                  \\
        [-t|--outputFileType <outputFileType>]                                  \\
        [--saveImages]                                                          \\
        [--label <prefixForLabelDirectories>]                                   \\
        [-n|--normalize]                                                        \\
        [-l|--lookupTable <LUTfile>]                                            \\
        [--skipAllLabels]                                                       \\
        [-s|--skipLabelValueList <ListOfVoxelValuesToSkip>]                     \\
        [-f|--filterLabelValueList <ListOfVoxelValuesToInclude>]                \\
        [-w|--wholeVolume <wholeVolDirName>]                                    \\'''

package_argSynopsisCore = '''
        [-I|--inputDir <inputDir>]
        Directory containing input filespace.

        -i|--inputFile  <inputFile>
        Input file to convert (relative to <inputDir>).
        Should be an ``mgz`` file.

        [-d|--outputDir <outputDir>]
        Directory containing output filespace.

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

        '''

package_argSynopsis = '''
        [-o|--outputFileStem <outputFileStem>]
        The output file stem to store image conversion. If this is specified
        with an extension, this extension will be used to specify the
        output file type.

        [-t|--outputFileType <outputFileType>]
        The output file type. If different to <outputFileStem> extension,
        will override extension in favour of <outputFileType>.

        Should be a ``png`` or ``jpg``.

        [--saveImages]
        If specified as True(boolean), will save the slices of the mgz file as
        ".png" (or ".jpg") files along with the numpy files.

        [--label <prefixForLabelDirectories>]
        Prefixes the string <prefixForLabelDirectories> to each filtered
        directory name. This is mostly for possible downstream processing,
        allowing a subsequent operation to easily determine which of the output
        directories correspond to labels.

        [-n|--normalize]
        If specified, will normalize the output image pixel values to
        0 and 1, otherwise pixel image values will retain the value in
        the original input volume.

        [-l|--lookupTable <LUTfile>]
        If passed, perform a lookup on the filtered voxel label values
        according to the contents of the <LUTfile>. This <LUTfile> should
        conform to the FreeSurfer lookup table format (documented elsewhere).

        Note that the special <LUTfile> string ``__val__`` can be passed which
        effectively means "no <LUTfile>". In this case, the numerical voxel
        values are used for output directory names. This special string is
        really only useful for scripted cases of running this application when
        modifying the CLI is more complex than simply setting the <LUTfile> to
        ``__val__``.

        [--skipAllLabels]
        Skips all labels and converts only the whole mgz volume to png/jpg images.

        [-s|--skipLabelValueList <ListOfLabelNumbersToSkip>]
        If specified as a comma separated string of label numbers,
        will not create directories of those label numbers.

        [-f|--filterLabelValueList <ListOfVoxelValuesToInclude>]
        The logical inverse of the [skipLabelValueList] flag. If specified,
        only filter the comma separated list of passed voxel values from the
        input volume.

        The default value of "-1" implies all voxel values should be filtered.

        [-w|--wholeVolume <wholeVolDirName>]
        If specified, creates a diretory called <wholeVolDirName> (within the
        outputdir) containing PNG/JPG images files of the entire input.

        This effectively really creates a PNG/JPG conversion of the input
        mgz file.

        Values in the image files will be the same as the original voxel
        values in the ``mgz``, unless the [--normalize] flag is specified
        in which case this creates a single-value mask of the input image.
'''

def synopsis(ab_shortOnly=False):
    scriptName = os.path.basename(sys.argv[0])
    shortSynopsis = '''

    NAME

       %s

    SYNOPSIS ''' % __pkg.name + Colors.GREEN + '''

        %s  '''  % __pkg.name + package_CLI +  package_CLIcore +  Colors.NO_COLOUR + '''

    BRIEF EXAMPLE

        * Bare bones execution

            mgz2imgslices -i aparc+aseg.mgz -d /tmp/filtered

    '''

    description = '''

    DESCRIPTION

        ``mgz2imgslices`` is a simple Python utility that filters "labels"
        from ``mgz`` volume files and saves each label set as slices of
        (by default) ``png`` files, organized into a series of directories,
        one per label set.

        An ``mgz`` format file simply contains a 3D volume data structure of
        image values. Often these values are interpreted to be image
        intensities. Sometimes, however, they can be interpreted as label
        identifiers. Regardless of the interpretation, the volume image data
        is simply a number value in each voxel of the volume.

        This script will scan across the input ``mgz`` volume, and for each
        voxel value create a new output directory. In that directory will be
        a set of (typically) ``png`` images, one per slice of the original
        volume. These images will only contain the voxels in the original
        dataset that all had that particular voxel value.

        In this manner, ``mgz2imgslices`` can also be thought of as a dynamic
        filter of an ``mgz`` volume file that filters each voxel value into
        its own output directory of ``png`` image files.

    ARGS
    ''' + Colors.YELLOW + package_argSynopsis + package_argSynopsisCore + Colors.NO_COLOUR + '''

    GITHUB

        o See https://github.com/FNNDSC/mgz2imgslices for more help and source.

    '''
    if ab_shortOnly:
        return shortSynopsis
    else:
        return shortSynopsis + description

#define script arguments
parser  = ArgumentParser(description = str_desc, formatter_class = RawTextHelpFormatter)

parser.add_argument('-i', '--inputFile',
                    help='name of the input file within the inputDir',
                    dest='inputFile'
                    )
parser.add_argument("-I", "--inputDir",
                    help    = "input directory",
                    dest    = 'inputDir',
                    default = '')
parser.add_argument("-d", "--outputDir",
                    help    = "output image directory",
                    dest    = 'outputDir',
                    default = '.')
parser.add_argument('-o', '--outputFileStem',
                    help='name of the output files within the outputDir',
                    dest='outputFileStem'
                    )
parser.add_argument('-t', '--outputFileType',
                    help='output image file format',
                    dest='outputFileType',
                    default = 'png'
                    )
parser.add_argument('--saveImages',
                    help='store png images for each slice of mgz file',
                    dest='saveImages',
                    action= 'store_true',
                    default = False
                    )
parser.add_argument('--label',
                    help='prefix a label to all the label directories',
                    dest='label',
                    default = 'label'
                    )
parser.add_argument('-n', '--normalize',
                    help='normalize the pixels of output image files',
                    dest='normalize',
                    action= 'store_true',
                    default = False
                    )
parser.add_argument('-l', '--lookupTable',
                    help='file contain text string lookups for voxel values',
                    dest='lookupTable',
                    default = '__none__'
                    )
parser.add_argument('--skipAllLabels',
                    help='skip all labels and create only whole Volume images',
                    dest='skipAllLabels',
                    action='store_true',
                    default=False)
parser.add_argument('-s', '--skipLabelValueList',
                    help='Comma separated list of voxel values to skip',
                    dest='skipLabelValueList',
                    default = ''
                    )
parser.add_argument('-f', '--filterLabelValueList',
                    help='Comma separated list of voxel values to include',
                    dest='filterLabelValueList',
                    default = "-1"
                    )
parser.add_argument('-w', '--wholeVolume',
                    help='Converts entire mgz volume to png/jpg instead of individually masked labels',
                    dest='wholeVolume',
                    default = 'wholeVolume'
                    )
parser.add_argument("--printElapsedTime",
                    help    = "print program run time",
                    dest    = 'printElapsedTime',
                    action  = 'store_true',
                    default = False)
parser.add_argument("-x", "--man",
                    help    = "man",
                    dest    = 'man',
                    action  = 'store_true',
                    default = False)
parser.add_argument("-y", "--synopsis",
                    help    = "short synopsis",
                    dest    = 'synopsis',
                    action  = 'store_true',
                    default = False)
parser.add_argument('-v', '--version',
                    help    = 'if specified, print version number',
                    dest    = 'b_version',
                    action  = 'store_true',
                    default = False)
parser.add_argument("--verbosity",
                    help    = "verbosity level for app",
                    dest    = 'verbosity',
                    default = "1")

def main(argv = None):
    # parse passed arguments
    args = parser.parse_args()

    # Do some minor CLI checks
    if args.b_version:
        print("Name:    %s\nVersion: %s" % (__pkg.name, __version__))
        return 1

    if args.man or args.synopsis:
        print(str_desc)
        if args.man:
            str_help = synopsis(False)
        else:
            str_help = synopsis(True)
        print(str_help)
        return 2

    # Create the object
    imgConverter    = mgz2imgslices.object_factoryCreate(args).C_convert

    # And now run it!
    imgConverter.tic()
    imgConverter.run()
    if args.printElapsedTime: print("Elapsed time = %f seconds" % imgConverter.toc())
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3

# System dependency imports

import os
import sys
import numpy as np
import nibabel as nib
import imageio
import pandas as pd
import re
import time
sys.path.append(os.path.dirname(__file__))
import  pfmisc
from    pfmisc._colors      import  Colors
from    pfmisc.debug        import  debug

class mgz2imgslices(object):
    """
        mgz2imgslices accepts as input an .mgz volume
        and converts each slice of the .mgz volume to a graphical
        display format such as png or jpg.

    """
    def log(self, *args):
        '''
        get/set the internal pipeline log message object.

        Caller can further manipulate the log object with object-specific
        calls.
        '''
        if len(args):
            self._log = args[0]
        else:
            return self._log

    def name(self, *args):
        '''
        get/set the descriptive name text of this object.
        '''
        if len(args):
            self.__name = args[0]
        else:
            return self.__name

    def description(self, *args):
        '''
        Get / set internal object description.
        '''
        if len(args):
            self.str_desc = args[0]
        else:
            return self.str_desc

    def __init__(self, **kwargs):

        self.str_desc                   = ""
        self.__name__                   = "mgz2imgslices"

        self.str_inputDir               = ""
        self.str_outputDir              = ""
        self.str_inputFile              = ""
        self.str_outputFileStem         = ""
        self.str_outputFileType         = "png"
        self.str_label                  = "label"
        self._b_normalize               = False
        self.str_lookuptable            = "__val__"
        self.str_skipLabelValueList     = ""
        self.str_filterLabelValueList   = "-1"
        self.str_wholeVolume            = ""
        self.l_skip                     = []
        self.__name__                   = "mgz2imgslices"
        self.verbosity                  = 1
        self.dp                         = pfmisc.debug(    
                                            verbosity   = self.verbosity,
                                            within      = self.__name__
                                            )

        for key, value in kwargs.items():
            if key == "inputFile":              self.str_inputFile          = value
            if key == "inputDir":               self.str_inputDir           = value
            if key == "outputDir":              self.str_outputDir          = value
            if key == "outputFileStem":         self.str_outputFileStem     = value
            if key == "outputFileType":         self.str_outputFileType     = value
            if key == "label":                  self.str_label              = value
            if key == "normalize":              self._b_normalize           = value
            if key == "lookuptable":            self.str_lookuptable        = value
            if key == "skipLabelValueList":     self.str_skipLabelValueList = value
            if key == "filterLabelValueList":   self.str_filterLabelValueList = value
            if key == "wholeVolume":            self.str_wholeVolume        = value

        if len(self.str_inputDir):
            self.str_inputFile  = '%s/%s' % (self.str_inputDir, self.str_inputFile)
        if not len(self.str_inputDir):
            self.str_inputDir = os.path.dirname(self.str_inputFile)
        if not len(self.str_inputDir): self.str_inputDir = '.'
        str_fileName, str_fileExtension  = os.path.splitext(self.str_outputFileStem)
        if len(self.str_outputFileType):
            str_fileExtension            = '.%s' % self.str_outputFileType

        if len(str_fileExtension) and not len(self.str_outputFileType):
            self.str_outputFileType     = str_fileExtension

        if not len(self.str_outputFileType) and not len(str_fileExtension):
            self.str_outputFileType     = '.png'

    def tic(self):
        """
            Port of the MatLAB function of same name
        """
        global Gtic_start
        Gtic_start = time.time()

    def toc(self, *args, **kwargs):
        """
            Port of the MatLAB function of same name

            Behaviour is controllable to some extent by the keyword
            args:


        """
        global Gtic_start
        f_elapsedTime = time.time() - Gtic_start
        for key, value in kwargs.items():
            if key == 'sysprint':   return value % f_elapsedTime
            if key == 'default':    return "Elapsed time = %f seconds." % f_elapsedTime
        return f_elapsedTime

    def readFSColorLUT(self, str_filename):
        l_column_names = ["#No", "LabelName"]

        df_FSColorLUT = pd.DataFrame(columns=l_column_names)

        with open(str_filename) as f:
            for line in f:
                if line and line[0].isdigit():
                    line = re.sub(' +', ' ', line)
                    l_line = line.split(' ')
                    l_labels = l_line[:2]
                    df_FSColorLUT.loc[len(df_FSColorLUT)] = l_labels
            
        return df_FSColorLUT

    def lookup_table(self, item):
        if self.str_lookuptable == "__val__":
            str_dirname = "00"+str(int(item))
        elif self.str_lookuptable == "__fs__":
            df_FSColorLUT = self.readFSColorLUT("../FreeSurferColorLUT.txt")
            str_dirname = df_FSColorLUT.loc[df_FSColorLUT['#No'] == str(int(item)), 'LabelName'].iloc[0]
        else:
            df_FSColorLUT = self.readFSColorLUT("%s/%s" % (self.str_inputDir, self.str_lookuptable))
            str_dirname = df_FSColorLUT.loc[df_FSColorLUT['#No'] == str(int(item)), 'LabelName'].iloc[0]

        return str_dirname    

    def nparray_to_imgs(self, np_mgz_vol, item):
        #mask voxels other than the current label to 0 values
            if(self._b_normalize):
                np_single_label = np.where(np_mgz_vol!=item, 0, 1)
            else:
                np_single_label = np.where(np_mgz_vol!=item, 0, item)
            
            i_total_slices = np_single_label.shape[0]

            str_dirname = self.lookup_table(item)

            # iterate through slices
            for current_slice in range(0, i_total_slices):
                np_data = np_single_label[:, :, current_slice]
                
                # prevents lossy conversion
                np_data=np_data.astype(np.uint8)

                current_slice = "00"+str(current_slice)

                str_image_name = "%s/%s-%s/%s-%s.%s" % (self.str_outputDir, self.str_label, str_dirname, 
                    self.str_outputFileStem, current_slice, self.str_outputFileType)
                self.dp.qprint("Saving %s" % str_image_name, level = 2)
                imageio.imwrite(str_image_name, np_data)

    def convert_whole_volume(self, np_mgz_vol):
        i_total_slices = np_mgz_vol.shape[0]

        str_whole_dirname = self.str_label+"-"+self.str_wholeVolume

        os.mkdir("%s/%s" % (self.str_outputDir, str_whole_dirname))

        # iterate through slices
        for current_slice in range(0, i_total_slices):
            np_data = np_mgz_vol[:, :, current_slice]
            
            # prevents lossy conversion
            np_data=np_data.astype(np.uint8)

            current_slice = "00"+str(current_slice)
            
            str_image_name = "%s/%s/%s-%s.%s" % (self.str_outputDir, str_whole_dirname, 
                self.str_outputFileStem, current_slice, self.str_outputFileType)
            self.dp.qprint("Saving %s" % str_image_name, level = 2)
            imageio.imwrite(str_image_name, np_data)

    def run(self):
        """
        Define the code to be run by this plugin app.
        """

        if len(self.str_skipLabelValueList):
            self.l_skip         = self.str_skipLabelValueList.split(',')

        mgz_vol = nib.load("%s" % (self.str_inputFile))

        np_mgz_vol = mgz_vol.get_fdata()
        
        unique, counts = np.unique(np_mgz_vol, return_counts=True)
        labels = dict(zip(unique, counts))

        if len(self.str_wholeVolume):
            self.convert_whole_volume(np_mgz_vol)

        for item in labels:
            if str(int(item)) in self.l_skip: 
                continue

            str_dirname = self.lookup_table(item)

            self.dp.qprint("Processing %s-%s.." % (self.str_label, str_dirname), level = 1)
                
            os.mkdir("%s/%s-%s" % (self.str_outputDir, self.str_label, str_dirname))

            self.nparray_to_imgs(np_mgz_vol, item)

class object_factoryCreate:
    """
    A class that examines input file string for extension information and
    returns the relevant convert object.
    """

    def __init__(self, args):
        """
        Parse relevant CLI args.
        """
        str_outputFileStem, str_outputFileExtension = os.path.splitext(args.outputFileStem)
        if len(str_outputFileExtension):
            str_outputFileExtension = str_outputFileExtension.split('.')[1]
        # try:
        #     str_inputFileStem, str_inputFileExtension = os.path.splitext(args.inputFile)
        # except:
        #     sys.exit(1)

        if not len(args.outputFileType) and len(str_outputFileExtension):
            args.outputFileType = str_outputFileExtension

        if len(str_outputFileExtension):
            args.outputFileStem = str_outputFileStem

        self.C_convert = mgz2imgslices(
            inputFile            = args.inputFile,
            inputDir             = args.inputDir,
            outputDir            = args.outputDir,
            outputFileStem       = args.outputFileStem,
            outputFileType       = args.outputFileType,
            label                = args.label,
            normalize            = args.normalize,
            lookuptable          = args.lookuptable,
            skipLabelValueList   = args.skipLabelValueList,
            filterLabelValueList = args.filterLabelValueList,
            wholeVolume          = args.wholeVolume
        )



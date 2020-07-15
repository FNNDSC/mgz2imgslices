#!/usr/bin/env python3

# System dependency imports

import os
import sys
import numpy as np
import nibabel as nib
import imageio
import pandas as pd
import re
sys.path.append(os.path.dirname(__file__))
import  pfmisc
from    pfmisc._colors      import  Colors
from    pfmisc.debug        import  debug

def initialize(self, options):

        self.l_skip             = []
        self.__name__           = "mgz2imgslices"
        self.verbosity          = int(options.verbosity)
        self.dp                 = pfmisc.debug(    
                                            verbosity   = self.verbosity,
                                            within      = self.__name__
                                            )

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

def lookup_table(self, options, item):
    if options.lookuptable == "__val__":
        str_dirname = "00"+str(int(item))
    elif options.lookuptable == "__fs__":
        df_FSColorLUT = self.readFSColorLUT("/usr/src/mgz2imgslices/FreeSurferColorLUT.txt")
        str_dirname = df_FSColorLUT.loc[df_FSColorLUT['#No'] == str(int(item)), 'LabelName'].iloc[0]
    else:
        df_FSColorLUT = self.readFSColorLUT("%s/%s" % (options.inputdir, options.lookuptable))
        str_dirname = df_FSColorLUT.loc[df_FSColorLUT['#No'] == str(int(item)), 'LabelName'].iloc[0]

    return str_dirname    

def nparray_to_imgs(self, options, np_mgz_vol, item):
    #mask voxels other than the current label to 0 values
        if(options.normalize):
            np_single_label = np.where(np_mgz_vol!=item, 0, 1)
        else:
            np_single_label = np.where(np_mgz_vol!=item, 0, item)
        
        i_total_slices = np_single_label.shape[0]

        str_dirname = self.lookup_table(options, item)

        # iterate through slices
        for current_slice in range(0, i_total_slices):
            np_data = np_single_label[:, :, current_slice]
            
            # prevents lossy conversion
            np_data=np_data.astype(np.uint8)

            str_image_name = "%s/%s/%s-%00d.%s" % (options.outputdir, str_dirname, 
                options.outputFileStem, current_slice, options.outputFileType)
            self.dp.qprint("Saving %s" % str_image_name, level = 2)
            imageio.imwrite(str_image_name, np_data)

def convert_whole_volume(self, options, np_mgz_vol):
    i_total_slices = np_mgz_vol.shape[0]

    str_whole_dirname = options.wholeVolume

    os.mkdir("%s/%s" % (options.outputdir, str_whole_dirname))

    # iterate through slices
    for current_slice in range(0, i_total_slices):
        np_data = np_mgz_vol[:, :, current_slice]
        
        # prevents lossy conversion
        np_data=np_data.astype(np.uint8)

        str_image_name = "%s/%s/%s-%00d.%s" % (options.outputdir, str_whole_dirname, 
            options.outputFileStem, current_slice, options.outputFileType)
        self.dp.qprint("Saving %s" % str_image_name, level = 2)
        imageio.imwrite(str_image_name, np_data)


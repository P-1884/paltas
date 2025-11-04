import numpy as np
import sys
import difflib

file_affix_list = ["",'_no_RSP','_goodseeing','_no_subtr','_no_subtr_LS_light']

for cov_matrix in ["",'_fullcov']:
    for file_new in file_affix_list:
        print('\n\nNEXT FILE:',file_new,cov_matrix)
        if cov_matrix =="": template_file = 'train_config_LSST_Lenspop.py'
        else: 
            print('Just checking full-cov config file is the same as the diag-cov config file of the same type.')
            template_file = 'train_config_LSST_Lenspop'+file_new+'.py' #Just checks the full-cov file is the same as the diag-cov file of the same type.
        with open(template_file, 'r') as file_template:
            with open('train_config_LSST_Lenspop'+file_new+cov_matrix+'.py', 'r') as file_updated:
                diff = difflib.unified_diff(
                    file_template.readlines(),
                    file_updated.readlines(),
                    fromfile=template_file,
                    tofile='train_config_LSST_Lenspop'+file_new+cov_matrix+'.py',
                    n=0, #Gives no context to the line differences (i.e. doesn't print additional lines)
                )
                for line in diff:
                    sys.stdout.write(line)

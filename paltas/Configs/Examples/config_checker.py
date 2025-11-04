import numpy as np
import sys
import difflib

file_affix_list = ["",'_no_RSP','_goodseeing','_no_subtr','_no_subtr_LS_light']
file_affix_list += [elem+'_mu3' for elem in file_affix_list]
for train_or_test in ["","_catalogue"]:
    for file_new in file_affix_list:
        if train_or_test == "_catalogue" and 'mu3' in file_new: continue
        print('\n\nNEXT FILE:',file_new,train_or_test)
        if train_or_test =="": template_file = 'config_LSST_Lenspop.py'
        else: 
            print('Just checking test config file is the same as the training config file of the same type.')
            template_file = 'config_LSST_Lenspop'+file_new+'.py' #Just checks the full-cov file is the same as the diag-cov file of the same type.
        if train_or_test == "": file_to_check = 'config_LSST_Lenspop'+file_new+'.py'
        elif train_or_test =='_catalogue': file_to_check = 'config_LensPop_catalogue'+file_new+'.py'
        # print('Comparing {} to {}'.format(template_file,file_to_check))
        with open(template_file, 'r') as file_template:
            with open(file_to_check, 'r') as file_updated:
                diff = difflib.unified_diff(
                    file_template.readlines(),
                    file_updated.readlines(),
                    fromfile=template_file,
                    tofile=file_to_check,
                    n=0, #Gives no context to the line differences (i.e. doesn't print additional lines)
                )
                for line in diff:
                    sys.stdout.write(line)
        del file_to_check

from functools import reduce  # forward compatibility for Python 3
import operator
import numpy as np
import pandas as pd

class generate_config_file:
     '''
     Generates a new configuration file, based on a template config (located at old_config_file_path)
     which is updated using the values in the new_config_dict_values dictionary.

     #### An important note on formatting:
     The template config file must be formatted in a specific way for this config-generator to work: 
     1) All '}' must be on their own line (comma's don't matter), i.e. 
     'main_deflector':{
     'class': PEMDShear
     }
     is ok, but:
     'main_deflector':{
     'class': PEMDShear}
     is not.
     #### End of note.

     '''
     def __init__(self,old_config_file_path,new_config_file_path,db,input_indx=None):
          '''
          Inputs: 
          old_config_file_path: Path to the template config file, on which the new config file is based.
          new_config_file: Path to the config file to be generated
          db: pandas dataframe, containing parameters for a population of lenses. A given (random) lensed system is chosen, and 
          a config file for that system is generated. Note: If a whole database isn't available, the new_config_dict_values dictionary (set below)
          can just be set to the parameters to be updated instead. 
          '''
          self.old_config_file_path = old_config_file_path
          self.new_config_file_path = new_config_file_path
          if input_indx is None: random_db_indx = np.random.randint(len(db))
          else: random_db_indx = input_indx
          self.zL = db['zL'][random_db_indx]
          self.zS = db['zS'][random_db_indx]
          self.mag_app = db['i_source'][random_db_indx] #i-band apparent source magnitude
          self.mag_app_lens = db['i_lens'][random_db_indx] #i-band apparent lens magnitude
          self.tE = db['tE'][random_db_indx]
          self.Re_source = db['Re_source'][random_db_indx]
          self.x_source = db['xs'][random_db_indx]
          self.y_source = db['ys'][random_db_indx]
          self.e1_source = db['e1_source'][random_db_indx]
          self.e2_source = db['e2_source'][random_db_indx]
          self.Re_lens = db['Re_lens'][random_db_indx]
          non_essential_values_dict = {} #'Non-essential' is a bit of a misnomer, but just means if they aren't provided, a default value is set instead.
          for var_with_default_0 in ['defl_e1_light','defl_e2_light','defl_e1_mass','defl_e2_mass',
                                     'defl_light_x','defl_light_y','defl_mass_x','defl_mass_y',
                                     'defl_gamma1','defl_gamma2']:
               if var_with_default_0 in db.columns:
                    non_essential_values_dict[var_with_default_0] = db[var_with_default_0][random_db_indx]
               else: 
                    print(f'Setting {var_with_default_0} to 0')
                    non_essential_values_dict[var_with_default_0] = 0.0 
          #
          if 'defl_gamma' in db.columns:
               non_essential_values_dict['defl_gamma']=db['defl_gamma'][random_db_indx]
          else: print('Setting gamma to 2');non_essential_values_dict['defl_gamma']=2.0
          #
          if 'Ns' in db.columns:
               non_essential_values_dict['Ns']=db['Ns'][random_db_indx]
          else: print('Setting N_sersic (Source) to 1');non_essential_values_dict['Ns']=1.0
          #
          if 'defl_Ns' in db.columns:
               non_essential_values_dict['defl_Ns']=db['defl_Ns'][random_db_indx]
          else: print('Setting N_sersic (Lens) to 4');non_essential_values_dict['defl_Ns']=4.0
          #
          for k_i in non_essential_values_dict.keys():
               non_essential_values_dict[k_i]=float(non_essential_values_dict[k_i]) #All values must be floats not int
          #
          self.new_config_dict_values = { #Dictionary from which the config file is generated
               'main_deflector':{
                    'parameters':{
                         'z_lens':self.zL,
                         'theta_E':self.tE,
                         'center_x':non_essential_values_dict['defl_mass_x'],
                         'center_y':non_essential_values_dict['defl_mass_y'],
                         'e1':non_essential_values_dict['defl_e1_mass'],
                         'e2':non_essential_values_dict['defl_e1_mass'],
                         'gamma':non_essential_values_dict['defl_gamma'],
                         'gamma1':non_essential_values_dict['defl_gamma1'],
                         'gamma2':non_essential_values_dict['defl_gamma2'],
                    },
               },
               'lens_light':{
                    'parameters':{
                         'z_source':self.zL,
                         'e1':non_essential_values_dict['defl_e1_light'],
                         'e2':non_essential_values_dict['defl_e2_light'],
                         'mag_app':self.mag_app_lens,
                         'center_x':non_essential_values_dict['defl_light_x'],
                         'center_y':non_essential_values_dict['defl_light_y'],
                         'n_sersic':non_essential_values_dict['defl_Ns'],
                         'R_sersic':self.Re_lens
                    }
               },
               'source':{
                    'parameters':{
                         'z_source':self.zS,
                         'mag_app':self.mag_app,
                         'R_sersic':self.Re_source,
                         'n_sersic':non_essential_values_dict['Ns'], #Fixed in LensPop to 1
                         'center_x':self.x_source,
                         'center_y':self.y_source,
                         'e1':self.e1_source,
                         'e2':self.e2_source
                    }
               }
          }
     def count_number_of_values_in_dict(self,d):
        return sum([self.count_number_of_values_in_dict(v) if isinstance(v, dict) else 1 for v in d.values()])

     def getFromDict(self,dataDict, mapList):
          return reduce(operator.getitem, mapList, dataDict)

     def write_new_config(self):
          '''
          This code proceeds line by line through the template config file, writing amended lines to the new config file.
          '''
          N_new_values = self.count_number_of_values_in_dict(self.new_config_dict_values)
          N_values_changed = 0
          begin_config=False
          key_tracker = []
          with open(self.new_config_file_path,'w') as f_new:
               for line in open(self.old_config_file_path,'r'):
#                    print('LINE',line)
                    if not begin_config:
                         f_new.write(line)
                    if begin_config:
                         line_0 = line.replace('\t','').replace('\n','') #Removing junk
                         if len(line_0)>1:
                              if line_0[0] =='#': 'Continuing'; continue #Ignoring lines which are commented out
                         line_3 = line_0.replace("'",'').split(':')[0]
                         line_4 = line_0.strip().split(':')[0].replace("'",'')
                         if '{' in line_0:
                              key_tracker.append(line_4)
               #			print(key_tracker)
                         if '}' in line_0:
                              assert line_0.replace(',','').strip()=='}'
                              key_tracker = key_tracker[:-1]
               #			print(key_tracker)
                         try:
                              #If the update-dictionary contains these keys (and the corresponding value is a float), the 
                              #value needs to be updated
                              if isinstance(self.getFromDict(self.new_config_dict_values,key_tracker+[line_3]),float):
#                                   print('Writing',"'"+line_3+"':"+
#                                   str(self.getFromDict(self.new_config_dict_values,key_tracker+[line_3]))+",\n")
                                   f_new.write("'"+line_3+"':"+
                                   str(self.getFromDict(self.new_config_dict_values,key_tracker+[line_3]))+",\n")
                                   N_values_changed+=1
                              else:
                                   print('Else',line_0,type(self.getFromDict(self.new_config_dict_values,key_tracker+[line_3])))
                         except Exception as ex:
#                              print('EX',line_0)
                              f_new.write(str(line_0)+'\n')
                              pass
                    if 'config_dict' in line: begin_config=True
          print(f'Have changed {N_values_changed} out of {N_new_values} values')
          assert N_values_changed==N_new_values #Assert that the same number of value have been updated as in the new_config_dict_values dictionary.  


def generate_config_file_based_on_database(old_config_file_path,new_config_file_path,
                                           list_of_properties,list_of_means,list_of_std,list_of_sigma_to_zero,list_of_truc_bool,add_crossmatch=False):
     '''
     Generates a new configuration file, based on a template config (located at old_config_file_path).
     This differs from the above class as instead of generating a config file for a single lensed system, it takes as an in put
     mean and standard deviations of given parameters for the lens population, then writes these distributions to the config file instead.

     #### An important note on formatting:
     The template config file must be formatted in a specific way for this config-generator to work: 
     1) All '}' must be on their own line (comma's don't matter), i.e. 
     'main_deflector':{
     'class': PEMDShear
     }
     is ok, but:
     'main_deflector':{
     'class': PEMDShear}
     is not.
     #### End of note.
     Inputs:
      'list_of_properties': List of lens properties: should be formatted as key1*key2*key3, where the keys are the keys in the config dictionary
      (e.g. [main_deflector*parameters*z_lens,main_deflector*parameters*theta_E,...]).
      list_of_means: List of the mean parameter values for each parameter, over the lens population
      list_of_std: """           standard deviation """
      list_of_sigma_to_zero: List of the number of standard deviations between the mean and 0 (i.e. just =mean/std). Relevant if the distribution
      is a truncated normal distribution, where the parameter cannot be negative.
      list_of_truc_bool: Whether the population distributions should be truncated at 0 (i.e. be non-negative). 

     '''
     new_config_dict_values = {
             'main_deflector':{
                  'parameters':{
                       'z_lens':None,
                       'theta_E':None,
                       'center_x':None,
                       'center_y':None,
			            'gamma': None,
			            'e1': None,
			            'e2': None,
			            'gamma1': None,
			            'gamma2': None,
                  }
             },
            'lens_light':{
                    'parameters':{
                        'z_source' :None,
                        'mag_app':None,
                        'output_ab_zeropoint':None,
                        'R_sersic':None,
                        'n_sersic':None, #Fixed to 4 in Simpipeline
                        'e1':None,
                        'e2':None,
                        'center_x':None,
                        'center_y':None
                }
	        },
             'source':{
                  'parameters':{
                       'z_source':None,
                       'mag_app':None,
                       'R_sersic':None,
                       'n_sersic':None,#Fixed to 1 in LensPop and Simpipeline
                       'center_x':None,
                       'center_y':None,
                       'e1':None,
                       'e2':None
                  }
             }
        }
     def generate_new_config_dict():
          for v_i, key_iii in enumerate(list_of_properties):
               key_1,key_2,key_3 = key_iii.split('*')
               if list_of_std[v_i]==0:
                    new_config_dict_values[key_1][key_2][key_3] = list_of_means[v_i]
               elif list_of_truc_bool[v_i]==False:
                    new_config_dict_values[key_1][key_2][key_3] = f'norm(loc={list_of_means[v_i]},scale={list_of_std[v_i]}).rvs'
               else:
                    if list_of_sigma_to_zero[v_i]==-np.inf:
                         list_of_sigma_to_zero[v_i]='-np.inf'
                    new_config_dict_values[key_1][key_2][key_3] = f'truncnorm({list_of_sigma_to_zero[v_i]},np.inf,'+\
                                                                  f'loc={list_of_means[v_i]},scale={list_of_std[v_i]}).rvs'
          return new_config_dict_values

     new_config_dict_values = generate_new_config_dict()
     print(generate_new_config_dict())
#
     def count_number_of_values_in_dict(d):
        return sum([count_number_of_values_in_dict(v) if isinstance(v, dict) else 1 for v in d.values()])

     def getFromDict(dataDict, mapList):
          return reduce(operator.getitem, mapList, dataDict)

     def write_new_config():
          N_new_values = len(list_of_properties)
          N_values_changed = 0
          begin_config=False
          key_tracker = []
          with open(new_config_file_path,'w') as f_new:
               for line in open(old_config_file_path,'r'):
#                    print('LINE',line)
                    if not begin_config:
                         f_new.write(line)
                    if begin_config:
                         line_0 = line.replace('\t','').replace('\n','') #Removing junk
                         if len(line_0)>1:
                              if line_0[0] =='#': 'Continuing'; continue #Ignoring lines which are commented out
                         line_3 = line_0.replace("'",'').split(':')[0]
                         line_4 = line_0.strip().split(':')[0].replace("'",'')
                         if '{' in line_0:
                              key_tracker.append(line_4)
                              print(key_tracker)
                         if '}' in line_0:
                              assert line_0.replace(',','').strip()=='}'
                              key_tracker = key_tracker[:-1]
                              print(key_tracker)
                         try:
                              #If the update-dictionary contains these keys (and the corresponding value is a float), the 
                              #value needs to be updated
                              if getFromDict(new_config_dict_values,key_tracker+[line_3]) is None: #Don't update if the new_config value is None.
                                   f_new.write(str(line_0)+'\n')
                              elif isinstance(getFromDict(new_config_dict_values,key_tracker+[line_3]),float):
                                   f_new.write("'"+line_3+"':"+
                                   str(getFromDict(new_config_dict_values,key_tracker+[line_3]))+",\n")
                                   N_values_changed+=1
                              elif isinstance(getFromDict(new_config_dict_values,key_tracker+[line_3]),str):
                                   f_new.write("'"+line_3+"':"+
                                   str(getFromDict(new_config_dict_values,key_tracker+[line_3]))+",\n")
                                   N_values_changed+=1
                              else:
                                   print('Something broke here',line_0,type(getFromDict(new_config_dict_values,key_tracker+[line_3])))
                         except Exception as ex:
                              print('EX',ex,line_0)
                              f_new.write(str(line_0)+'\n')
                              pass
                    if 'config_dict' in line: begin_config=True
          assert N_values_changed==N_new_values #Assert that the same number of value have been updated as in the new_config_dict_values dictionary.  
     write_new_config()
     def add_on_cross_object(list_of_properties,list_of_means,list_of_std,redshift=True,position=True):
          '''
          Function to add 'cross-objects', i.e. inter-dependent parameters in the config file (e.g. where z_L has to be < z_S, or where the
          lens light position is the same as the lens mass position).
          Inputs: redshift: Whether to require z_L<z_S as a cross-object. position: Whether to require lens_light_centre=lens_mass_centre.
          '''
          assert redshift or position #Have to add at least one cross-matched object
          with open(new_config_file_path,'r') as f_new:
               with open(f'{new_config_file_path}_interim','w') as f_interim:
                    n_line = 0
                    for line in f_new:
                         f_interim.write(line)
                         n_line+=1
          with open(new_config_file_path,'w') as f_new:
               with open(f'{new_config_file_path}_interim','r') as f_interim:
                    n_line_i = 1
                    for line in f_interim:
                         if n_line_i!=n_line:
                              f_new.write(line)
                         else: assert line.strip()=='}' #Assert the last line is a close bracket
                         n_line_i+=1
               list_of_properties=np.array(list_of_properties)
               centre_x_indx = np.where(list_of_properties=='main_deflector*parameters*center_x')[0];assert len(centre_x_indx)==1
               centre_y_indx = np.where(list_of_properties=='main_deflector*parameters*center_y')[0];assert len(centre_y_indx)==1
               zL_indx = np.where(list_of_properties=='main_deflector*parameters*z_lens')[0];assert len(zL_indx)==1
               zS_indx = np.where(list_of_properties=='source*parameters*z_source')[0];assert len(zS_indx)==1
               lens_centre_x_mean = float(np.array(list_of_means)[centre_x_indx])
               lens_centre_y_mean = float(np.array(list_of_means)[centre_y_indx])
               lens_centre_x_std = float(np.array(list_of_std)[centre_x_indx])
               lens_centre_y_std = float(np.array(list_of_std)[centre_y_indx])
               zL_mean = float(np.array(list_of_means)[zL_indx])
               zS_mean = float(np.array(list_of_means)[zS_indx])
               zL_std = float(np.array(list_of_std)[zL_indx])
               zS_std = float(np.array(list_of_std)[zS_indx])
               f_new.write("'cross_object':{\n")
               f_new.write("'parameters':{\n")
               if position:
                    f_new.write("('main_deflector:center_x,main_deflector:center_y,lens_light:center_x,lens_light:center_y'):\n")
                    f_new.write(f"dist.DuplicateXY(\n"+
                                             f"x_dist=norm(loc={lens_centre_x_mean},scale={lens_centre_x_std}).rvs, \n"+\
                                             f"y_dist=norm(loc={lens_centre_y_mean},scale={lens_centre_y_std}).rvs),\n")
               if redshift:
                    f_new.write(f"'main_deflector:z_lens,source:z_source':dist.RedshiftsTruncNorm( \n"+\
                         f"z_lens_min=0,z_lens_mean={zL_mean},z_lens_std={zL_std},\n"+\
                         f"z_source_min=0,z_source_mean={zS_mean},z_source_std={zS_std})\n")
               f_new.write("}\n")
               f_new.write("}\n")
               f_new.write("}")

     if add_crossmatch: add_on_cross_object(list_of_properties,list_of_means,list_of_std)
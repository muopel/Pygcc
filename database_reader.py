# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 23:22:21 2023

@author: awolayoa
"""
import re

def readSourceGWBdb(sourcedb_dir): #defining a function with the parameters - in this case the source databasel
    #def readSourcePHREEQdb(sourcedb_dir):
    """
    This function reads source GWB thermodynamic database and reaction coefficients of 'eh'
    and 'e-' has been added at the bottom returns all reaction coefficients and species,
    group species into redox, minerals, gases, oxides and aqueous species
    Parameters
    ----------
        sourcedb      :     filename of the source database
    Returns
    ----------
        sourcedic     :     dictionary of reaction coefficients and species
        specielist    :     list of species segmented into the different categories
                            [element, basis, redox, aqueous, minerals, gases, oxides]
        speciecat     :     list of species categories listed in 'specielist'
        chargedic     :     dictionary of charges of species
        MWdic         :     dictionary of MW of species
        Mineraltype   :     mineral type for minerals
        fugacity_info :     fugacity information as stored in new tdat database for chi and critical ppts
    Usage:
    ----------
    [sourcedic, specielist, chargedic, MWdic, Mineraltype, fugacity_info, activity_model] = readSourceGWBdb()
    """
    #would need to intialize empty dictionaries:
    #sourcedic
    #specielist
    #speciecat
    #chargedic
    #MWdic
    #Mineraltype
    #fugacity_info
    with open(sourcedb_dir) as g:
        for line in g:
            if line.startswith('activity model'):
                break
    #May not need this section 
            
    #line31: opening the file located at the path as specified by sourcedb_dir, the with statement ensures that the file is closed after it is read, even with an exception
    #line32: iterates over each line in the opened file, g is a file object, the line var holds onto content of each line as its read during an iteration
    #line33: this is a condition, its checking whether the current line starts with the string 'activity model', then if block executed
    #line34: if condition met, exits the loop, so no more iteration through the file 
            
    #if line.startswith('debye huckel')
    #would replace instances of activity coeff with debye huckel 
    #For each section in the input file:
    #If the section matches the format "#element    species    alk    gfw_formula    element_gfw":
        #Parse the section and extract relevant information to populate specielist, speciecat, and chargedic dictionaries
    #If the section matches the format "NAMED_EXPRESSIONS":
        #Parse the section and extract relevant information to populate sourcedic dictionary
    #If the section matches the format "SOLUTION_MASTER_SPECIES":
        #Parse the section and extract relevant information to populate MWdic and Mineraltype dictionaries
    #If the section matches the format you desire, extract relevant information accordingly
            
    with open(sourcedb_dir) as g:
        Rd = g.readlines()
    activity_model = line.strip('\n').split()[-1]
    data_fmt = [x for x in Rd if 'dataset format' in x][0].strip('\n').split(':')[-1].strip()
    fugacity_model = [x for x in Rd if 'fugacity model' in x][0].strip('\n').split(': ')[-1] if data_fmt != 'oct94' else ''
    #39:opening file at path and the with statement just makes sure to close after reading file
    #40:this reads all lines in the file storing it as Rd
    #41:extracts the last word from the last line of file
    #42:looks for a line in file that contains the substring, 'dataset format', extracts the part after the colon and removes leading/trailing whitespaces
    #43:this line is similar to the previous one but looks for the substring 'fugacity model'. If the value of data_fmt is not equal to 'oct94', it extracts the part after the colon (':') and removes leading and trailing whitespaces. If data_fmt is 'oct94', it assigns an empty string to fugacity_model.
    unwanted = ['elements', 'basis species', 'redox couples', 'aqueous species',
                'free electron', 'minerals', 'solid solutions', 'gases', 'oxides', 'stop.' ]
    #capture line numbers with line break
    # list of strings representing categories of lines that are not wanted or needed. Lines containing these strings will be used to identify line numbers
    d=[]; previousline = ''
    #intialize empty list 'd' stroing identified line numbers and a var , keeping track of previous line iteration
    with open(sourcedb_dir) as fid:
        #opening a file and create a file object
        for idx, line in enumerate(fid, 1):
            #iterate through lines, using enumertae to get both line content and its line number, it starts from 1
            if line.strip().rstrip('\n').lstrip('0123456789.- ') in unwanted:
                #Check if the stripped and rstripped version of the line (removing leading and trailing whitespaces and newline characters) is in the list of unwanted strings (unwanted). If true, add the line number minus one (x-1) to the list d.
                x=idx
                d.append(x-1)
            #elif line.strip(' \n*').startswith(('virial coefficients', 'Virial coefficients', 'SIT epsilon coefficients', 'Pitzer parameters')):
            elif previousline.startswith('-end-') and line.startswith('*'):
                #The * will change to an #

                #Check if the current line (line) starts with '*' and the previous line (previousline) starts with '-end-'. If true, add the current line number plus one (x+1) to the list d and break out of the loop
                x=idx; #print(x)
                d.append(x+1)
                break
            previousline = line
            #update previous line var to store line content for next iteration

    if activity_model == 'h-m-w':
        if all([i.startswith('*') for i in Rd[d[-1]:d[-1]+30]]) == False:
            #If the condition evaluates to False, it means that not all lines in the specified range in Rd start with '*'. This block calculates the value of d_act based on the index of the first empty line in a sublist of Rd.
            d_act = [i for i, x in enumerate(Rd[d[-1]:]) if x.strip('\n') ==''][0]
        else:
            #If the condition in the previous if statement is True, this block calculates the value of d_act based on the index of the first empty line in a different sublist of Rd.
            d_act = [i for i, x in enumerate(Rd[d[-2]:]) if x.strip('\n') ==''][0]
    f = open(sourcedb_dir, 'r')
    #skip first 11 lines of database  .lstrip('0123456789.- ')
    for i in range(d[1]+2):
      #skips first 11 lines of the file by iterating over range of d[1]+2 and using readline method to read and discard each line, the var s1 not used here?
      s1 = f.readline()
      #Overall: chekcing if activity model var is equal to h-m-w, if true, it checks condition related to lines in Rd, it then calcs the value of the var d_act, opens the file specified by sourcedb_dir in read mode
      #then, skips first 11 ines of the file using a lopp and the readline method

    sourcedic = {} # initialize dictionary
    for i in range(d[-1]-d[1]): 
        #iterates through range of vlaues, where range determined by difference between the last and second last elements in list d
        s1 = f.readline()
        #reads a line from file f and assigns var s1
        if s1.strip(' \n*').startswith(("references", 'virial coefficients', 'Virial coefficients', 'SIT epsilon coefficients', 'Pitzer parameters')) :
            break
        #Checks if the stripped and rstripped version of the line (s1) starts with any of the specified substrings. If true, the loop is terminated using the break statement.
        if not s1.startswith((' ', '*'), 0) | (s1.rstrip('\n') == "") | (len(s1) !=0 and s1[0] == "-") :
            #checks if line does not start with a space or asterisk, is not an empty line, and does not start with hyphen
            if s1.rstrip('\n').lstrip('0123456789.- ') in unwanted:
                continue
            #skips the current iteration if the stripped and rstripped version of line matches anything in unwanted list
            elif s1.rstrip('\n').lstrip('0123456789.- ') == '':
                continue
            #skips the current iteration if the stripped and rstripped version of the line is an empty string.
            else:
                specie_name = s1.strip().split()[0]
                #extracts first wors from stripped version of the line
                s2 = f.readline(); s3 = f.readline() if s2.rstrip('\n') != '' else ''
                s4 = f.readline() if s3.rstrip('\n') != '' else ''
                s5 = f.readline() if s4.rstrip('\n') != '' else ''
                #Reads the next four lines from the file and assigns them to s2, s3, s4, and s5 respectively, only if the previous line is not an empty line.
                if data_fmt == 'mar21' and not s3.split()[0].isdigit() and'mole' not in [s3.split()[0], s2.split()[0]] :
                    #checks if data is format mar21 and conditions are met involving the content on 3rd line as s3
                    if (s2.rstrip('\n') != "" and s3.rstrip('\n') == ""):
                        ss_details = [s1, s2, s3]
                    elif (s3.rstrip('\n') != "" and s4.rstrip('\n') == ""):
                        ss_details = [s1, s2, s3, s4]
                    elif (s4.rstrip('\n') != "" and s5.rstrip('\n') == ""):
                        ss_details = [s1, s2, s3, s4, s5]
                    elif (s5.rstrip('\n') != ""):
                        s6 = f.readline()
                        ss_details = [s1, s2, s3, s4, s5, s6]
                        #reads next line (s6) and creates a list with current line and previous 5 lines if fifth line is not empty
                        if (s6.rstrip('\n') != ""):
                            s7 = f.readline()
                            ss_details = [s1, s2, s3, s4, s5, s6, s7]
                            if (s7.rstrip('\n') != ""):
                                s8 = f.readline()
                                ss_details = [s1, s2, s3, s4, s5, s6, s7, s8]
                                if (s8.rstrip('\n') != ""):
                                    s9 = f.readline()
                                    ss_details = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
                                    #reads more lines and appends them to list if not empty, list contents are increasing
                    specie_formula = []; species_num = []; reactant = []
                    #Initializes empty lists for specie_formula, species_num, and reactant
                else:
                    #only runs of the if statement is not satisfied - if the fith line is not empty is not satisfied
                    if (s5.rstrip('\n') != ""):
                        #checks if stripped version of the fifth line is not an empty string
                        s6 = f.readline()
                        #reads the next line from file and assigns to s6
                        if (s6.rstrip('\n') != ""):
                            #Checks if the stripped version of the sixth line (s6) is not an empty string
                            s7 = f.readline()
                            #reads next line and assigns to s7
                            if not s2.startswith('*',0):
                                #Checks if the second line (s2) does not start with an asterisk ('*') at the beginning
                                if (len(s2.split()) > 1) and (s2.split()[0] != 'formula='):
                                    #Checks if the second line has more than one word and the first word is not 'formula='
                                    if len(s1.split('formula=')) <= 1:
                                        specie_formula = ""
                                        #Checks if the first line (s1) does not contain the substring 'formula='. If true, assigns an empty string to specie_formula
                                    else:
                                        specie_formula = s1.rstrip('\n').split('formula=')[1]
                                        #if substring 'formula=' is in 1st line, extracts the portion after fromula= and assigns to specie_formula
                                    if not s3.lstrip().startswith(('chi', 'Pcrit'), 0):
                                        #Checks if the stripped version of the third line (s3) does not start with 'chi' or 'Pcrit' at the beginning
                                        species_num = int(s3.split()[0])
                                        #Extracts the first word (presumably a numeric value) from the stripped and split version of the third line and converts it to an integer, assigning it to species_num
                                        if species_num <= 3:
                                            reactant = s4.split()
                                            #split version of the 4th line plus the split version of the 5th line (s5)
                                        elif species_num <= 6:
                                            reactant = s4.split() + s5.split()
                                            #split version of the 4th line plus the split version of the 5th line (s5)
                                        else:
                                            reactant = s4.split() + s5.split() + s6.split()
                                            #split version of the 4th plus 5th plus the 6th 
                                    else:
                                        #here the condition it works against- if second line starts with an asterisk
                                        if not s4.lstrip().startswith(('chi','Pcrit'),0):
                                            # Checks if the stripped version of the fourth line (s4) does not start with 'chi' or 'Pcrit' at the beginning
                                            species_num = int(s4.split()[0])
                                            #Extracts the first word (presumably a numeric value) from the stripped and split version of the fourth line and converts it to an integer, assigning it to species_num
                                            if species_num <= 3:
                                                reactant = s5.split()
                                                #assigned to split version of 5th line
                                            elif species_num <= 6:
                                                reactant = s5.split() + s6.split()
                                                #assigned the split version of the 5th plus the split version of 6th line
                                            else:
                                                reactant = s5.split() + s6.split() + s7.split()
                                                #assigned the split version of the fifth line plus the split version of the sixth line plus the split version of the seventh line 
                                        else: #if false
                                            species_num = int(s5.split()[0])
                                            #Extracts the first word (presumably a numeric value) from the stripped and split version of the fifth line and converts it to an integer, assigning it to species_num
                                            if species_num <= 3:
                                                reactant = s6.split()
                                                #assigned the split version of the sixth line (s6)
                                            else:
                                                reactant = s6.split() + s7.split()
                                                #assigned the split version of the sixth line plus the split version of the seventh line (s7)
                                else:
                                    if len(s2.split('formula=')) <= 1:
                                        #hecks if the second line (s2) does not contain the substring 'formula=' more than once (splitting on 'formula=' results in a list with at most one element)
                                        specie_formula = ""
                                        #if true: Assigns an empty string to specie_formula
                                    else:
                                        specie_formula = s2.rstrip('\n').split('formula=')[1]
                                        #if false: f the substring 'formula=' is present in the second line, extracts the portion after 'formula=' and assigns it to specie_formula
                                    species_num = int(s4.split()[0])
                                    #Extracts the first word (presumably a numeric value) from the stripped and split version of the fourth line (s4) and converts it to an integer, assigning it to species_num
                                    if species_num <= 3:
                                        reactant = s5.split()
                                        #assigned the split version of the fifth line (s5)
                                    elif species_num <= 6:
                                        reactant = s5.split() + s6.split()
                                        #assigned the split version of the fifth line plus the split version of the sixth line (s6)
                                    else:
                                        reactant = s5.split() + s6.split() + s7.split()
                                        #assigned the split version of the fifth line plus the split version of the sixth line plus the split version of the seventh line (s7)
                            else:
                                #its not satsified when checking for asterisk in 2nd line
                                specie_formula = s2.split()[2]
                                #Extracts the third word (presumably a formula) from the split version of the second line (s2) and assigns it to specie_formula
                                species_num = int(s4.split()[0])
                                #Extracts the first word (presumably a numeric value) from the stripped and split version of the fourth line (s4) and converts it to an integer, assigning it to species_num
                                if species_num <= 3:
                                    reactant = s5.split()
                                    #If species_num is less than or equal to 3, reactant is assigned the split version of the fifth line (s5)
                                elif species_num <= 6:
                                    reactant = s5.split() + s6.split()
                                    #If species_num is less than or equal to 6, reactant is assigned the split version of the fifth line plus the split version of the sixth line (s6)
                                else:
                                    reactant = s5.split() + s6.split() + s7.split()
                                    #If species_num is greater than 6, reactant is assigned the split version of the fifth line plus the split version of the sixth line plus the split version of the seventh line (s7)
                        else:
                            specie_formula = ""
                            #Assigns an empty string to specie_formula
                            species_num = int(s3.split()[0])
                            #Extracts the first word (presumably a numeric value) from the stripped and split version of the third line (s3) and converts it to an integer, assigning it to species_num
                            if species_num <= 3:
                                reactant = s4.split()
                                #If species_num is less than or equal to 3, reactant is assigned the split version of the fourth line (s4)
                            elif species_num <= 6:
                                reactant = s4.split() + s5.split()
                                #If species_num is less than or equal to 6, reactant is assigned the split version of the fourth line plus the split version of the fifth line (s5)
                            else:
                                reactant = s4.split() + s5.split() + s6.split()
                                #If species_num is greater than 6, reactant is assigned the split version of the fourth line plus the split version of the fifth line plus the split version of the sixth line
                    else:
                        #this block is same as before but runs for if statemtn on line 136 - if stripped version of the fifth line is not an empty string
                        specie_formula = ""
                        species_num = int(s3.split()[0])
                        if species_num <= 3:
                            reactant = s4.split()
                        elif species_num <= 6:
                            reactant = s4.split() + s5.split()
                        else:
                            reactant = s4.split() + s5.split() + s6.split()
                    ss_details = []
                    #Resets the ss_details list for the next iteration

        dt = [specie_formula, species_num] + reactant + ss_details
        #Creates a list dt by concatenating the following lists
        sourcedic[specie_name] = dt[2:] if any(isinstance(el, list) for el in dt) else dt
        #Assigns the value of dt to the dictionary sourcedic with the key specie_name
        #The value is a sublist of dt starting from the third element (dt[2:]) if any element in dt is a list; otherwise, the entire dt list is assigned
    sourcedic['eh'] = ['eh', 3, '-2.0000', 'H2O', '1.0000', 'O2(g)', '4.0000', 'H+']
    #keys are eh and e- and the values are lisst containing info about these species
    sourcedic['e-'] = ['e-', 3, '0.50000', 'H2O', '-0.2500', 'O2(g)', '-1.0000', 'H+']

    f.close()
    #closing file opened earlier

    element = []; basis = []; redox = []; aqueous = []; minerals = []; gases = []; oxides = []
    solidsolutions = []
    #empty lists meant to store information
    charge = []; MW = []; electron = []; fugacity_chi = {}; fugacity_Pcrit = {}; Mineraltype = {}
    #charge, MW, electron store chare and molecular ifno while the others are dictionaries
    with open(sourcedb_dir) as fid:
        #file reading loop - Opens the specified file (sourcedb_dir) for reading and assigns it to the variable fid
        for i, line in enumerate(fid, 1):
            # Iterates through the lines of the file, keeping track of the line number (i)
            previousline = line
            #Updates the previousline variable with the current line
            if (line.strip(' \n*').startswith(("references", 'Pitzer parameters', 'virial coefficients', 'Virial coefficients', 'SIT epsilon coefficients'))):
                break
            #Checks if the stripped version of the current line starts with any of the specified keywords
            #If true, breaks out of the loop, effectively ending the iteration through the file

            # elif previousline.startswith('-end-') and line.startswith('*'):
            #     break
            if not line.startswith((' ','*'),0) | (line.rstrip('\n') == "") | (line[0] == "-") :
                #Checks if the line does not start with a space or asterisk, is not an empty line, and does not start with a hyphen
                if not line.split()[0].replace('.','',1).isnumeric():
                    #Checks if the first word of the line (after splitting) is not numeric and does not start with a specific format
                    if not line.startswith(('charge', 'mole', 'formula'), 0):
                        #Checks if the line does not start with specific keywords 
                        if d[0] < i < d[1]:
                            element.append(line.split()[0])
                            #If the line number (i) is within the range specified by the first two elements of list d, appends the first word of the line to the element list
                        elif d[1] < i < d[2]:
                            basis.append(line.split()[0])
                            #If the line number is within the range specified by the second and third elements of list d, appends the first word of the line to the basis list
                        elif d[2] < i < d[3]:
                            redox.append(line.split()[0])
                            #If the line number is within the range specified by the third and fourth elements of list d, appends the first word of the line to the redox list
                        elif d[3] < i < d[4]:
                            aqueous.append(line.split()[0])
                            #If the line number is within the range specified by the fourth and fifth elements of list d, appends the first word of the line to the aqueous list
                        elif d[4] < i < d[5]:
                            if data_fmt == 'oct94':
                                minerals.append(line.split()[0])
                            elif data_fmt in ['jul17', 'jan19', 'apr20', 'mar21'] :
                                electron.append(line.split()[0])
                                #If the line number is within the range specified by the fifth and sixth elements of list d, appends the first word of the line to either the minerals or electron list based on the data format
                        elif d[5] < i < d[6]:
                            if data_fmt == 'oct94':
                                gases.append(line.split()[0])
                            elif data_fmt in ['jul17', 'jan19', 'apr20', 'mar21'] :
                                minerals.append(line.split()[0])
                                #If the line number is within the range specified by the sixth and seventh elements of list d, appends the first word of the line to either the gases or minerals list based on the data format
                        elif i > d[6]:
                            if data_fmt == 'oct94':
                                oxides.append(line.split()[0])
                                #If the line number is greater than the seventh element of list d, appends the first word of the line to the oxides list if the data format is 'oct94'
                            elif d[6] < i < d[7]:
                                if data_fmt in ['jul17', 'jan19', 'apr20'] :
                                    gases.append(line.split()[0])
                                elif data_fmt == 'mar21':
                                    solidsolutions.append(line.split()[0])
                            elif i > d[7]:
                                if data_fmt in ['jul17', 'jan19', 'apr20'] :
                                    oxides.append(line.split()[0])
                                elif data_fmt == 'mar21':
                                    if d[7] < i < d[8]:
                                        gases.append(line.split()[0])
                                    elif i > d[8]:
                                        oxides.append(line.split()[0])
                                        #conditions based on the data format and line numbers to append the first word of the line to different lists (gases, solidsolutions, oxides) accordingly

            if (re.compile(r"charge").search(line) != None) and not line.startswith('*'):
                charge.append(line)
                #Checks if the line contains the word "charge" using a regular expression. If the condition is met and the line does not start with an asterisk, appends the line to the charge list
            if (re.compile(r"mole wt.=").search(line) != None) and not line.startswith('*'):
                MW.append(re.sub('[^0123456789\.]', '', line.strip('\n').split('wt.=')[1]))
                #Checks if the line contains the pattern "mole wt.=" using a regular expression. If the condition is met and the line does not start with an asterisk, extracts the molecular weight
                # appends it to the MW list after removing non-numeric characters
            if (re.compile(r"type=").search(line) != None) and not line.startswith('*'):
                if len(line.split()) <= 2:
                    Mineraltype[line.split()[0]] = ''
                else:
                    Mineraltype[line.split()[0]] = line.split()[2]
                    #Checks if the line contains the pattern "type=" using a regular expression
                    #If condition is met and the line does not start with an asterisk, extracts information related to mineral type and adds it to the Mineraltype dictionary
            if (re.compile(r"chi=").search(line) != None) and not line.startswith('*'):
                fugacity_chi[gases[-1]] = line
                #Checks if the line contains the pattern "chi=" using a regular expression. If the condition is met and the line does not start with an asterisk
                #ssociates the fugacity information with the last element in the gases list in the fugacity_chi dictionary
            if (re.compile(r"Pcrit=").search(line) != None) and not line.startswith('*'):
                fugacity_Pcrit[gases[-1]] = line
                #Checks if the line contains the pattern "Pcrit=" using a regular expression
                # If condition is met and the line does not start with an asterisk, associates the critical pressure information with the last element in the gases list in the fugacity_Pcrit 

    act_list = []; #previousline = ''
    # Initializes an empty list named act_list to store lines 
    if activity_model == 'h-m-w':
        #hecks if the variable activity_model is equal to the string 'h-m-w
        with open(sourcedb_dir) as fid:
            #Opens the specified file (sourcedb_dir) for reading and assigns it to the variable fid
            for i, line in enumerate(fid, 1):
                #Iterates through the lines of the file, keeping track of the line number (i)
                num = d[-1] + d_act if all([i.startswith('*') for i in Rd[d[-1]:d[-1]+30]]) == False else d[-2] + d_act
                #Calculates the threshold line number (num) based on the values in lists d and Rd, considering conditions related to lines starting with an asterisk
                if i > num: #d[-1] + d_act:
                    #hecks if the current line number is greater than the calculated threshold num
                    if not line.startswith(('  ', '\n', '-end-', '*')):
                        #Checks if the line does not start with specific patterns (' ', '\n', '-end-', '*')
                        act_list.append(line)
                        #appends the line to act_list

    act_param = {'activity_model': activity_model, 'act_list': act_list, 'dataset_format' : data_fmt}
    #Creates a dictionary act_param containing information about the activity model, a list of activity-related lines (act_list), and the dataset format (data_fmt)
    fugacity_info = {'fugacity_model': fugacity_model, 'fugacity_chi': fugacity_chi,'fugacity_Pcrit': fugacity_Pcrit}
    #Creates a dictionary fugacity_info containing information about the fugacity model, fugacity chi, and fugacity Pcrit
    res = basis + redox + aqueous + electron
    chargedic = {res[i]: charge[i].rstrip('\n') for i in range(len(charge))}
    #Creates a dictionary chargedic where keys are elements from the combined list basis + redox + aqueous + electron
    #alues are corresponding charge information from the charge list
    res = element + basis + redox + aqueous + electron + minerals + gases + oxides
    MWdic = {res[i]: float(MW[i]) for i in range(len(MW))}
    #Creates a dictionary MWdic where keys are elements from the combined list 
    #values are corresponding molecular weight information from the MW list, converted to floats
    if data_fmt != 'mar21':
        specielist = [element, basis, redox, aqueous, electron, minerals, gases, oxides]
        speciecat = ['element', 'basis', 'redox', 'aqueous', 'electron', 'minerals', 'gases', 'oxides']
    else:
        specielist = [element, basis, redox, aqueous, electron, minerals, solidsolutions, gases, oxides]
        speciecat = ['element', 'basis', 'redox', 'aqueous', 'electron', 'minerals', 'solidsolutions', 'gases', 'oxides']
        #Determines the lists and categories (specielist and speciecat) based on the dataset format (data_fmt)

    return sourcedic, act_param, fugacity_info, chargedic, MWdic, specielist, speciecat
#Returns a tuple containing dictionaries and lists: sourcedic (presumably containing information about the source), act_param, fugacity_info, chargedic, MWdic, specielist, and speciecat
#allows the caller to access and use this structured information


sourcedb_dir = 'GWB_Thermoddem.dat'
#ead and process a database file,
db = readSourceGWBdb(sourcedb_dir)
#would be to read and process a GWB (Geochemist's Workbench) database file and perform the functions needed such as extraction

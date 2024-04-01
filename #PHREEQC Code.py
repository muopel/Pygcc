#PHREEQC Code

import re
def readSourcePHREEQCdb(sourcedb_dir): #defining a function with the parameters - in this case the source databasel
    #def readSourcePHREEQdb(sourcedb_dir):
    """
    This function reads source PHREEQC thermodynamic database and reaction coefficients of 'eh'
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

   # Initialize empty dictionaries
    sourcedic = {}
    specielist = {}
    speciecat = {}
    chargedic = {}
    MWdic = {}
    Mineraltype = {}
    fugacity_info = {}

    # Initialize variables
    with open(sourcedb_dir) as g:
        Rd = g.readlines()
    debye_huckel_flag = False
    activity_model = line.strip('\n').split()[-1]
    data_fmt = [x for x in Rd if 'dataset format' in x][0].strip('\n').split(':')[-1].strip()
    fugacity_model = [x for x in Rd if 'fugacity model' in x][0].strip('\n').split(': ')[-1] if data_fmt != 'oct94' else ''
    unwanted = ['elements', 'basis species', 'redox couples', 'aqueous species',
                'free electron', 'minerals', 'solid solutions', 'gases', 'oxides', 'stop.' ]
    d=[]; previousline = ''
    with open(sourcedb_dir) as fid:
        for idx, line in enumerate(fid, 1):
            #iterate through lines, using enumertae to get both line content and its line number, it starts from 1
            if line.strip().rstrip('\n').lstrip('0123456789.- ') in unwanted:
                #Check if the stripped and rstripped version of the line (removing leading and trailing whitespaces and newline characters) is in the list of unwanted strings (unwanted). If true, add the line number minus one (x-1) to the list d.
                x=idx
                d.append(x-1)
            #elif line.strip(' \n*').startswith(('virial coefficients', 'Virial coefficients', 'SIT epsilon coefficients', 'Pitzer parameters')):
            elif previousline.startswith('-end-') and line.startswith('#'):
                #Check if the current line (line) starts with '*' and the previous line (previousline) starts with '-end-'. If true, add the current line number plus one (x+1) to the list d and break out of the loop
                x=idx; #print(x)
                d.append(x+1)
                break
            previousline = line
    # Function to parse the input file
    def parse_input_file(input_file):
        nonlocal debye_huckel_flag

        with open(input_file, 'r') as file:
            for line in file:
                if line.startswith('debye huckel'):
                    # Set flag to replace instances of activity coefficients with Debye Huckel
                    debye_huckel_flag = True

                if line.startswith("#element    species    alk    gfw_formula    element_gfw"):
                    # Parse species section and populate dictionaries
                    parse_species_section(line)

                elif line.startswith("NAMED_EXPRESSIONS"):
                    # Parse named expressions section and populate sourcedic dictionary
                    parse_named_expressions(line)

                elif line.startswith("SOLUTION_MASTER_SPECIES"):
                    # Parse solution master species section and populate dictionaries
                    parse_solution_master_species(line)

                elif line.startswith("desired_format"):
                    # Parse desired format section and extract relevant information
                    parse_desired_format(line)
        f = open(sourcedb_dir, 'r')
        #skip first 11 lines of database  .lstrip('0123456789.- ')
        for i in range(d[1]+2):
            s1 = f.readline()

    sourcedic = {} # initialize dictionary
    for i in range(d[-1]-d[1]): 
        #iterates through range of vlaues, where range determined by difference between the last and second last elements in list d
        s1 = f.readline()
        #reads a line from file f and assigns var s1
        if s1.strip(' \n*').startswith(("references", 'virial coefficients', 'Virial coefficients', 'SIT epsilon coefficients', 'Pitzer parameters')) :
            break
        #Checks if the stripped and rstripped version of the line (s1) starts with any of the specified substrings. If true, the loop is terminated using the break statement.
        if not s1.startswith((' ', '#'), 0) | (s1.rstrip('\n') == "") | (len(s1) !=0 and s1[0] == "-") :
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

    # Function to parse species section
   # def parse_species_section(line):
    #    global specielist, speciecat, chargedic

        # Placeholder: Parse section and populate specielist, speciecat, and chargedic dictionaries
        # Integrate the code you provided here
        #pass

    # Function to parse named expressions
    #def parse_named_expressions(line):
     #   global sourcedic

        # Placeholder: Parse section and populate sourcedic dictionary
        # Integrate the code you provided here
        #pass

    # Function to parse solution master species
    #def parse_solution_master_species(line):
      #  global MWdic, Mineraltype

        # Placeholder: Parse section and populate MWdic and Mineraltype dictionaries
        # Integrate the code you provided here
      #  pass

    # Function to parse other desired formats
    #def parse_desired_format(line):
        # Placeholder: Parse section and extract relevant information accordingly
        # Integrate the code you provided here
    
#include "RVE_mesh.h"

//=====================  BODY  ==========================

RVE_mesh::RVE_mesh(){}

RVE_mesh::~RVE_mesh(){}

const string RVE_mesh::currentDateTime() {
    time_t     now = time(0);
    struct tm  tstruct;
    char       buf[80];
    tstruct = *localtime(&now);
    strftime(buf, sizeof(buf), "%Y-%m-%d.%X", &tstruct);

    return buf;
}

void RVE_mesh::print_intro(){
  date = currentDateTime();
  WorkDir = "~/workspace/Thin_Ply_Mechanics/WD";
  InpDir = "Input_files";
  OutDir = "Output_files";
  InpFileName = "benchmark.inp";
 
  cout << " " << endl;
  cout << " " << endl;
  cout << "********************************************************************************* " << endl;
  cout << "                          " << date << endl;
  cout << " " << endl;
  cout << " " << endl;
  cout << "                                     EUSMAT" << endl;
  cout << "                         European School of Materials" << endl;
  cout << " " << endl;
  cout << "                                     DocMASE" << endl;
  cout << "                  DOCTORATE IN MATERIALS SCIENCE AND ENGINEERING" << endl;
  cout << " " << endl;
  cout << " " << endl;
  cout << "       MECHANICS OF EXTREME THIN COMPOSITE LAYERS FOR AEROSPACE APPLICATIONS" << endl;
  cout << " " << endl;
  cout << " " << endl;
  cout << " Micromechanics of fiber/matrix debonding: Reference Volume Element (RVE) analysis" << endl;
  cout << " " << endl;
  cout << "                 Mesh generation and ABAQUS input file creation" << endl;
  cout << " " << endl;
  cout << "                                      by" << endl;
  cout << " " << endl;
  cout << "                             Luca Di Stasio, 2015" << endl;
  cout << " " << endl;
  cout << " " << endl;
  cout << "********************************************************************************* " << endl;
  cout << " " << endl;
  cout << " " << endl;
  cout << " " << endl;
}

void RVE_mesh::parse_commandline(){
  // Add descriptive text for display when help argument is supplied
  options_description desc(
    "\nMicromechanics of fiber/matrix debonding: Reference Volume Element (RVE) analysis: Mesh generation and ABAQUS input file creation.\n\nThe program allows for the generation of structured meshes and creation of ABAQUS input files for the simulation of RVE mechanics in ABAQUS.\n\nAllowed arguments");
    
    // Define command line arguments using either formats:
    //
    //     (“long-name,short-name”, “Description of argument”)
    //     for flag values or
    //
    //     (“long-name,short-name”, <data-type>, 
    //     “Description of argument”) arguments with values
    //
    // Remember that arguments with values may be multi-values and must be vectors
    desc.add_options()
    ("help,h", "Produce this help message.")
    ("mode,m", value< vector<string> >(), "Mode of operation. Options: gui: start graphical user interface; shell: start interactive shell mode in current console; file: read data from file and start computation, without user interaction.")
    ("input,i", value< vector<string> >(), "Input file name.");
    
    // Map positional parameters to their tag valued types (e.g. –input-file parameters)
    positional_options_description p;
    p.add("input", -1);
    
    // Parse the command line catching and displaying any parser errors
    variables_map vm;
    try
    {
      store(command_line_parser(argc, argv).options(desc).positional(p).run(), vm);
        notify(vm);
    } catch (std::exception &e)
    {
      cout << endl << e.what() << endl;
      cout << desc << endl;
    }
    // Display help text when requested
    if (vm.count("help"))
    {
      cout << "Help" << endl;
      cout << desc << endl;
    }
    // Get the state of the arguments supplied
    if (vm.count("mode"))
    {
      vector<string> mode =
      vm["mode"].as< vector<string> >();
      RunMode = algorithm::join(mode, "");
    }
    if (vm.count("input"))
    {
      vector<string> input =
      vm["input"].as< vector<string> >();
      InpFileName = algorithm::join(input, "");
    }
}

void RVE_mesh::set_IO(){
  string input = "";
  cout << "=============================== I/O settings ==================================== " << endl;
  cout << " " << endl;
  cout << "Current working directory: " << WorkDir << endl;
  cout << "Would you like to change it? (y/n) ";
  cin >> input;
  if (input == "y" || input == "yes" || input == "YES" || input == "Y"){
    cout << endl;
    WorkDir = "";
    cout << "Input the full path of the working directory: ";
    cin >> WorkDir;
    cout << endl;
    cout << "Working directory set to: " << WorkDir << endl;
  }
  path workdirpath(WorkDir);
  if(!exists(workdirpath)){
    create_directory(workdirpath);
    cout << " " << endl;
    cout << "Directory created." << endl;
    cout << " " << endl;
  }
  else{
   cout << " " << endl;
   cout << "Directory already exists." << endl;
   cout << " " << endl;
  }
  string FullInpDir = WorkDir + "/" + InpDir;
  cout << " " << endl;
  input = "";
  cout << "Current input directory: " << FullInpDir << endl;
  cout << "Would you like to change it? (y/n) ";
  cin >> input;
  if (input == "y" || input == "yes" || input == "YES" || input == "Y"){
    cout << endl;
    InpDir = "";
    FullInpDir = "";
    cout << "Input the relative (to WD, without initial slash) path of the input directory: ";
    cin >> InpDir;
    FullInpDir = WorkDir + "/" + InpDir;
    cout << endl;
    cout << "Input directory set to: " << FullInpDir << endl;
  }
  path inpdirpath(FullInpDir);
  if(!exists(inpdirpath)){
    create_directory(inpdirpath);
    cout << " " << endl;
    cout << "Directory created." << endl;
    cout << " " << endl;
  }
  else{
   cout << " " << endl;
   cout << "Directory already exists." << endl;
   cout << " " << endl;
  }
  string FullOutDir = WorkDir + "/" + OutDir;
  cout << " " << endl;
  input = "";
  cout << "Current output directory: " << FullOutDir << endl;
  cout << "Would you like to change it? (y/n) ";
  cin >> input;
  if (input == "y" || input == "yes" || input == "YES" || input == "Y"){
    cout << endl;
    OutDir = "";
    FullOutDir = "";
    cout << "Input the relative (to WD, without initial slash) path of the output directory: ";
    cin >> OutDir;
    FullOutDir = WorkDir + "/" + OutDir;
    cout << endl;
    cout << "Output directory set to: " << FullOutDir << endl;
  }
  path outdirpath(FullOutDir);
  if(!exists(outdirpath)){
    create_directory(outdirpath);
    cout << " " << endl;
    cout << "Directory created." << endl;
    cout << " " << endl;
  }
  else{
   cout << " " << endl;
   cout << "Directory already exists." << endl;
   cout << " " << endl;
  }
  cout << " " << endl;
  cout << " " << endl;
}

void RVE_mesh::edit_inpfile(){
  string input = "";
  cout << "=========================== Edit/Create Input File ============================== " << endl;
  cout << " " << endl;
  cout << "Current input file: " << InpFileName << endl;
  cout << "Would you like to change it? (y/n) ";
  cin >> input;
  if (input == "y" || input == "yes" || input == "YES" || input == "Y"){
    cout << endl;
    InpFileName = "";
    cout << "Input the name of the input file (with extension .inp): ";
    cin >> InpFileName;
    cout << endl;
    cout << "Input file set to: " << InpFileName << endl;
  }
  cout << "Would you like to edit the file? (y/n) ";
  cin >> input;
  if (input == "y" || input == "yes" || input == "YES" || input == "Y"){
    string commandstring = "vim " + WorkDir + "/" + InpDir + "/" + InpFileName;
    const char * command = commandstring.c_str();
    system(command);
    cout << " " << endl;
    cout << InpFileName << " edited on " << currentDateTime() << endl;
  }
  cout << " " << endl;
  cout << " " << endl;
}

void RVE_mesh::read_inpfile(){
  string InpFilePathString = WorkDir + "/" + InpDir + "/" + InpFileName;
  const char * InpFilePath = InpFilePathString.c_str();
  string line;
  string comment = "//";
  ifstream inpfile;
  inpfile.open(InpFilePath);
  if(inpfile.is_open()){
   while(!inpfile.eof()){
    getline(inpfile,line);
    size_t found = line.find(comment);
    if(found>1){
     vector<string> stringvec;
     istringstream iss(line);
     copy(istream_iterator<string>(iss),istream_iterator<string>(),back_inserter(stringvec));
     if(stringvec[0]=="type"){
       type = atoi(stringvec[2].c_str());
     }
     else if(stringvec[0]=="Rf"){
       Rf = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="Vff"){
       Vff = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="tr"){
       tratio = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="theta"){
       theta = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="deltatheta"){
       deltatheta = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="Ef"){
       Ef = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="Gf"){
       Gf = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="nuf"){
       nuf = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="Em"){
       Em = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="Gm"){
       Gm = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="num"){
       num = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="fmesh"){
       fmesh = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="gmesh"){
       gmesh = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="hmesh"){
       hmesh = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="Niter"){
       Niter = atof(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="Nalpha"){
       Nalpha = atoi(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="Nbeta"){
       Nbeta = atoi(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="Ngamma"){
       Ngamma = atoi(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="Ndelta"){
       Ndelta = atoi(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="Nepsilon"){
       Nepsilon = atoi(stringvec[2].c_str()); 
     }
     else if(stringvec[0]=="Nzeta"){
       Nzeta = atoi(stringvec[2].c_str()); 
     }
    }
   }
   inpfile.close();
  }
}

void RVE_mesh::print_inputdata(){
  cout << "============================= Import Input Data ================================= " << endl;
  cout << " " << endl;
  cout << "Material geometry" << endl;
  cout << " " << endl;
  cout << "Rf = " << Rf << " : Fiber radius" << endl;
  cout << "Vff = " << Vff << " : Fiber volume fraction" << endl;
  cout << " " << endl;
  cout << "Crack geometry" << endl;
  cout << " " << endl;
  cout << "theta = " << theta << " : Crack reference angular position [°]" << endl;
  cout << "deltatheta = " << deltatheta << " : Crack angular semi-aperture" << endl;
  cout << " " << endl;
  cout << " " << endl;
}

void RVE_mesh::compute_parameters(){
  double pi = 3.1415926535897;
  l = 0.5*Rf*sqrt(pi/Vff);
}

void RVE_mesh::initialize(){
  parse_commandline();
  print_intro();
  if(RunMode=="gui"){
    
  } else if(RunMode=="shell"){
    
  } else if(RunMode=="file"){
    
  } else{
    cout << "Option for mode not recognized. Starting interactive shell mode (default).";
  }
}

void RVE_mesh::write_abaqusinpfile(){
  string Rfstring;
  string Vffstring;
  string Nfstring;
  string Nmstring;
  
  stringstream convertRf;
  convertRf << Rf;
  Rfstring = convertRf.str();
  
  stringstream convertVff;
  convertVff << Vff;
  Vffstring = convertVff.str();
  
  stringstream convertf;
  convertf << Nalpha*Nalpha+4*(Nbeta+Ngamma)*Nalpha;
  Nfstring = convertf.str();
  
  stringstream convertm;
  convertm << 4*(Ndelta+Nepsilon)*Nalpha;
  Nmstring = convertm.str();
  
  string abaqusinpfilenamestring = WorkDir + "/" + OutDir + "/" + date + "_" + "Rf" + Rfstring + "_" + "Vff" + Vffstring + "_" + "Nf" + Nfstring + "_" + "Nm" + Nmstring + "RVE_analysis.inp";
  const char * abaqusinpfilename = abaqusinpfilenamestring.c_str();
  ofstream abaqusinpfile;
  abaqusinpfile.open(abaqusinpfilename);
  
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "**--                                                                                                                             --" << endl;
  abaqusinpfile << "**--                                                                                                                             --" << endl;
  abaqusinpfile << "**--                                                         EUSMAT                                                              --" << endl;
  abaqusinpfile << "**--                                            European School of Materials                                                     --" << endl;
  abaqusinpfile << "**--                                                                                                                             --" << endl;
  abaqusinpfile << "**--                                                        DocMASE                                                              --" << endl;
  abaqusinpfile << "**--                                    DOCTORATE IN MATERIALS SCIENCE AND ENGINEERING                                           --" << endl;
  abaqusinpfile << "**--                                                                                                                             --" << endl;
  abaqusinpfile << "**--                                                                                                                             --" << endl;
  abaqusinpfile << "**--                        MECHANICS OF EXTREME THIN COMPOSITE LAYERS FOR AEROSPACE APPLICATIONS                                --" << endl;
  abaqusinpfile << "**--                                                                                                                             --" << endl;
  abaqusinpfile << "**--                                                                                                                             --" << endl;
  abaqusinpfile << "**--                  Micromechanics of fiber/matrix debonding: Reference Volume Element (RVE) analysis                          --" << endl;
  abaqusinpfile << "**--                                                                                                                             --" << endl;
  abaqusinpfile << "**--                                                    Mesh generation                                                          --" << endl;
  abaqusinpfile << "**--                                                                                                                             --" << endl;
  abaqusinpfile << "**--                                                          by                                                                 --" << endl;
  abaqusinpfile << "**--                                                                                                                             --" << endl;
  abaqusinpfile << "**--                                                 Luca Di Stasio, 2015                                                        --" << endl;
  abaqusinpfile << "**--                                                                                                                             --" << endl;
  abaqusinpfile << "**--                                                                                                                             --" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "**" << endl;
  abaqusinpfile << "*HEADING" << endl;
  abaqusinpfile << "Micromechanics of fiber/matrix debonding: Reference Volume Element (RVE) analysis" << endl;
  abaqusinpfile << "*PREPRINT,MODEL=YES,HISTORY=YES,CONTACT=YES" << endl;
  abaqusinpfile << "**" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "**-------------------------------------------------------- PARAMETERS -------------------------------------------------------------" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "*PARAMETER" << endl;
  abaqusinpfile << "**" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "**----------------------------------------------------------- MESH ----------------------------------------------------------------" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "**" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "**-------------------------------------------------------- MATERIALS --------------------------------------------------------------" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "**" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "**--------------------------------------------------- SURFACE DEFINITIONS ---------------------------------------------------------" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "**" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "**--------------------------------------------------- BOUNDARY CONDITIONS ---------------------------------------------------------" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "**" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  abaqusinpfile << "**------------------------------------------------------ LOADING CYCLE ------------------------------------------------------------" << endl;
  abaqusinpfile << "**---------------------------------------------------------------------------------------------------------------------------------" << endl;
  
  abaqusinpfile.close();
}

void RVE_mesh::write_schemetotikz(){
  string Rfstring;
  string Vffstring;
  
  stringstream convertRf;
  convertRf << Rf;
  Rfstring = convertRf.str();
  
  stringstream convertVff;
  convertVff << Vff;
  Vffstring = convertVff.str();
  
  string texfilenamestring = WorkDir + "/" + OutDir + "/" + date + "_" + "Rf" + Rfstring + "_" + "Vff" + Vffstring + "_tikz_scheme.tex";
  const char * texfilename = texfilenamestring.c_str();
  ofstream texfile;
  texfile.open(texfilename);
  
  texfile << "\\documentclass{minimal}" << endl;
  texfile << "" << endl;
  texfile << "%----------------- Packages -----------------%" << endl;
  texfile << "\\usepackage{tikz}" << endl;
  texfile << "\\usepackage{verbatim}" << endl;
  texfile << "\\usepackage{pgf,tikz}" << endl;
  texfile << "\\usepackage{mathrsfs}" << endl;
  texfile << "" << endl;
  texfile << "%------------- Global definitions -----------%" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  
  texfile.close();
}

void RVE_mesh::write_reporttolatex(){
  string Rfstring;
  string Vffstring;
  string Nfstring;
  string Nmstring;
  
  stringstream convertRf;
  convertRf << Rf;
  Rfstring = convertRf.str();
  
  stringstream convertVff;
  convertVff << Vff;
  Vffstring = convertVff.str();
  
  stringstream convertf;
  convertf << Nalpha*Nalpha+4*(Nbeta+Ngamma)*Nalpha;
  Nfstring = convertf.str();
  
  stringstream convertm;
  convertm << 4*(Ndelta+Nepsilon)*Nalpha;
  Nmstring = convertm.str();
  
  string texfilenamestring = WorkDir + "/" + OutDir + "/" + date + "_" + "Rf" + Rfstring + "_" + "Vff" + Vffstring + "_" + "Nf" + Nfstring + "_" + "Nm" + Nmstring + "report.tex";
  const char * texfilename = texfilenamestring.c_str();
  ofstream texfile;
  texfile.open(texfilename);
  
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  texfile << "" << endl;
  
  texfile.close();
}

void RVE_mesh::compute_regionalpha(){
  
}

void RVE_mesh::compute_regionbeta(){
  
}

void RVE_mesh::compute_regiongamma(){
  
}

void RVE_mesh::compute_regiondelta(){
  
}

void RVE_mesh::compute_regionepsilon(){
  
}

void RVE_mesh::compute_regionzeta(){
  
}

void RVE_mesh::compute_singlemesh(){
  
  //=================== Region alpha ============================
  compute_regionalpha();
  //=================== Region beta ============================
  compute_regionbeta();
  //=================== Region gamma ============================
  compute_regiongamma();
  //=================== Region delta ============================
  compute_regiondelta();
  //=================== Region epsilon ============================
  compute_regionepsilon();
}

void RVE_mesh::compute_boundedmesh(){
  
}

void RVE_mesh::compute_mesh(){
  switch(type){
    case 0:
      compute_singlemesh();
    case 1:
      compute_boundedmesh();
    case 2:
      compute_singlemesh();
  }
}
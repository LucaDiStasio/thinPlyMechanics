/**
        Project: Mechanics of Extreme Thin Composite Layers for Aerospace applications
         Author: Luca Di Stasio
    Institution: Université de Lorraine & Luleå University of Technology
        Version: 10.2015
  Creation date: October 20th, 2015
    Last update: February 1st, 2016

    Description: 
          Input: 
         Output:
         
    @author Luca Di Stasio
    @version 10.2015
*/

#include <boost/program_options/options_description.hpp>
#include <boost/program_options/parsers.hpp>
#include <boost/program_options/variables_map.hpp>

#include "RVE_mesh.h"

using namespace std;
using namespace boost;
using namespace boost::program_options;

//==================  MAIN  =======================
int main(int argc, char** argv)
{
    string runmode, inpfilename;
    
    options_description desc(
    "\n2D FEM Analysis of Fiber-Matrix Debonding.\n\nThe program provides tools for the generation of the mesh.\n\nAllowed arguments");
    
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
    ("mode,m", value< vector<string> >(), "Mode of operation. Options: gui: start graphical user interface;\nshell: start interactive shell mode in current console;\nfile: read data from file and start computation, without user interaction.")
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
      return 0;
    }
    // Get the state of the arguments supplied
    if (vm.count("mode"))
    {
      vector<string> mode =
      vm["mode"].as< vector<string> >();
      runmode = algorithm::join(mode, "");
    }
    if (vm.count("input"))
    {
      vector<string> input =
      vm["input"].as< vector<string> >();
      inpfilename = algorithm::join(input, "");
    }
  
    RVE_mesh mesh(runmode);
    
    //mesh.initialize(inpfilename);
    
    //mesh.read_coordinates();
  
    
 
  return 0;
}
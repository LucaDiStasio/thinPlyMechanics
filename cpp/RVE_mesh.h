#include <iostream>
#include <sstream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <string>
#include <stdio.h>
#include <time.h>
#include <cmath>
#include <stdlib.h>
#include <cstdlib>     //to get current directory
#include <unistd.h>    //to get home directory
#include <sys/types.h> //to get home directory
#include <pwd.h>       //to get home directory 
#include <sys/stat.h>     //create new directory
#include <sys/types.h>    //create new directory
#include <boost/filesystem.hpp>
#include <boost/tokenizer.hpp>
#include <boost/token_functions.hpp>
#include <boost/algorithm/string/join.hpp>
#include <exception>
#include <typeinfo>
#include <omp.h>

using namespace std;
using namespace boost;
using namespace boost::filesystem;

//===================================================
//==================  HEADER  =======================
//===================================================

class diffgeom {

//===================================================  
//                  Variables
//===================================================
private:
  
// I/O management
  string date,                                                // Current date and time
         WorkDir,                                             // Working directory (for input and output files, not code)
	       InpDir,                                              // Input files directory
	       OutDir,                                              // Output files directory
	       InpFileName,                                         // Input file name with data and settings to run the simulation
	       OutFileName,                                         // Output filename to save results
	       RunMode,                                             // Mode of operation. Options: gui: start graphical user interface; shell: start interactive shell mode in current console; file: read data from file and start computation, without user interaction. 
	       EndMapManFileName,                                   // CSV file with coordinates of points describing the co-domain manifold
	       BaseMapManFileName;                                  // CSV file with coordinates of points describing the domain manifold
 
// Input parameters
  int Dim,                                                    // Space dimensions 
      Nx,                                                     // Number of points in x-direction
      Ny,                                                     // Number of points in x-direction
      Nz;                                                     // Number of points in x-direction
	 
// Control parameters
  vector<bool> computed_quantities;                           // Keep track of geometrical quantities computed
  unsigned int float_operations;                              // Number of floating point operations performed

// Output quantities
  vector<vector<double> > comp_nodes;                         // List of nodes' coordinates in computational space, ordered by helical numbering
  vector<vector<double> > phys_nodes;                         // List of nodes' coordinates in physical space, ordered by helical numbering
  vector<vector<double> > cov_base;                           // Covariant base vectors
  vector<vector<double> > contr_base;                         // Contravariant base vectors
  vector<vector<double> > cov_metric;                         // Covariant metric tensor
  vector<vector<double> > contr_metric;                       // Contravariant metric tensor
  vector<vector<double> > first_christoffel;                  // First Christoffel symbols
  vector<vector<double> > second_christoffel;                 // Second Christoffel symbols
  vector<vector<double> > contr_Riemann;                      // Contravariant Riemann curvature tensor
  vector<vector<double> > cov_Riemann;                        // Covariant Riemann curvature tensor
  vector<vector<double> > cov_Ricci;                          // Covariant Ricci curvature tensor
  double Ricci_scalar;                                        // Ricci scalar curvature

  
//===================================================  
//                      Methods
//===================================================  
public:
  
  // Constructor (default)
  diffgeom();
  
  // Constructor when specific run-mode is provided
  diffgeom(string input);
  
  //Destructor
  ~diffgeom();
  
  // Functions
  const string currentDateTime();                                                // Get current system date and time

  void print_intro(),                                                            // Print header to screen
       set_IO(),                                                                 // Set I/O parameters interactively
       get_inpfilename(const string&),                                           // Get the input file name from string variable in main, which depends on command line input
       edit_inpfile(),                                                           // Edit the input file
       read_inpfile(),                                                           // Read the input file
       print_inputdata(),                                                        // Print data read from input file
       initialize(const string&),                                                // Initialize the simulation
       read_coordinates(),                                                       // Read coordinates from .csv files
       get_coordinates(vector<vector<double> >, vector<vector<double> >),        // Get coordinates from API
       compute_covbase(),                                                        // Compute covariant base vectors
       compute_contrbase(),                                                      // Compute contravariant base vectors
       compute_covmetric(),                                                      // Compute covariant metric tensor
       compute_contrmetric(),                                                    // Compute contravariant metric tensor
       compute_firstChristoffel(),                                               // Compute first Christoffel symbols
       compute_secondChristoffel(),                                              // Compute second Christoffel symbols
       compute_contrRiemann(),                                                   // Compute contravariant Riemann curvature tensor
       compute_covRiemann(),                                                     // Compute covariant Riemann curvature tensor
       compute_covRicci(),                                                       // Compute covariant Ricci tensor
       compute_Ricciscalar();                                                    // Compute Ricci scalar curvature
  
  vector<vector<double> > compute_metricdet(),                                   // Compute the determinant of the covariant metric tensor
                          compute_invmetricdet(),                                // Compute the determinant of the contravariant metric tensor
                          compute_covveccomp(vector<vector<double> >),           // Compute covariant components of given vector
                          compute_contrveccomp(vector<vector<double> >),         // Compute contravariant components of given vector
                          compute_vecfromcovcomp(vector<vector<double> >),       // Compute vector given its covariant components
                          compute_vecfromcontrcomp(vector<vector<double> >);     // Compute vector given its contravariant components
       
  void save_geometry();                                                          // Save computed geometric quantities to file
  
  vector<vector<double> > provide_compdomain(),                                  // Provide computational domain to external program
                          provide_physdomain(),                                  // Provide physical domain to external program
                          provide_covbase(),                                     // Provide covariant base vectors to external program
                          provide_contrbase(),                                   // Provide contravariant base vectors to external program
                          provide_covmetric(),                                   // Provide covariant metric tensor to external program
                          provide_contrmetric(),                                 // Provide contravariant metric tensor to external program
                          provide_firstChristoffel(),                            // Provide first Christoffel symbols to external program
                          provide_secondChristoffel(),                           // Provide second Christoffel symbols to external program
                          provide_contrRiemann(),                                // Provide contravariant Riemann curvature tensor to external program
                          provide_covRiemann(),                                  // Provide covariant Riemann curvature tensor to external program
                          provide_covRicci();                                    // Provide covariant Ricci tensor to external program
  double provide_Ricciscalar();                                                  // Provide Ricci scalar curvature to external program
};
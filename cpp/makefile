CXX = g++
CXXFLAGS = -I/usr/lib/x86_64-linux-gnu/
INCLUDES = 
LD = icc
LDFLAGS := -L/usr/lib/x86_64-linux-gnu/ -lboost_filesystem -lboost_program_options -lboost_system

#/home/ubuntu/workspace/boost
#/home/ubuntu/workspace/boost/stage/lib

SOURCES = RVE_mesh.cpp
HEADERS = RVE_mesh.h
OBJ     = main.o RVE_mesh.o

.SUFFIXES: .cpp

all: RVE

geometry: $(OBJ)
	$(CXX) $(CXXFLAGS) $(OBJ) -o RVE $(LDFLAGS)
	
main.o: main.cpp
	$(CXX) $(CXXFLAGS) -c main.cpp
	
diffgeom.o: RVE_mesh.cpp RVE_mesh.h
	$(CXX) $(CXXFLAGS) -c RVE_mesh.cpp

clean:
	rm -f main
	rm -f *.o
	rm -f *.i
	rm -f *.lst
	rm -f output.*
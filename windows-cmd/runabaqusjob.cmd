SET wd=%1
SET projectname=%2
SET cpusnum=%3
SET runmode=%4
SET abaquswd=%wd%/%projectname%/abaqus
SET inputfile=../abqinp/%projectname%.inp

CD %abaquswd%

abaqus job=%projectname% analysis input=%inputfile% information=all %runmode% cpus=%cpusnum%

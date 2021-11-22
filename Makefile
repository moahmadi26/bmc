# These are directories which I created for the BMC counterexample generator
KSP_JAVA_FILES_GRAPH := $(wildcard src/graph/*.java) 
KSP_JAVA_FILES_BMC := $(wildcard src/bmc/*.java)





# Need to link to a PRISM distribution
PRISM_DIR = ../prism

# For compilation, just need access to classes/jars in the PRISM distribution
# We look in both the top-level and the prism sub-directory
# (currently svn/git repos and downloaded distributions differ in structure)
PRISM_CLASSPATH = $(PRISM_DIR)/prism/classes:$(PRISM_DIR)/prism/lib/*

CLASSPATH = $(PRISM_CLASSPATH):classes

PRISM_LIB_PATH = $(PRISM_DIR)/prism/lib

PRISM_JAVA=`/usr/libexec/java_home`/bin/java


# This Makefile just builds all java files in src and puts the class files in classes

default: all

.PHONY: all
all: init bmc

.PHONY: init
init:	
	@mkdir -p classes

.PHONY: cex
bmc:
	javac -cp $(CLASSPATH) -d classes $(KSP_JAVA_FILES_BMC) $(KSP_JAVA_FILES_GRAPH)

.PHONY: run
run:
	export DYLD_LIBRARY_PATH=$(PRISM_LIB_PATH);\
	$(PRISM_JAVA) -Xmx8g -Djava.library.path=$(PRISM_LIB_PATH) -classpath $(CLASSPATH) bmc_tandem $(prob_bound)



.PHONY: clean

clean:
	@rm -rf classes
	@rm -rf src/KSP/classes 
celan: clean

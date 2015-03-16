Setting up nightly tests of WrapITK

# Introduction #

Testing frequently WrapITK on as much configurations as possible is the best way to be sure that it works on those configurations. As shown many times in the past, testing a program from time to time is not enough to claim that it works with a given configuration.

WrapITK can use the same test infrastructure than ITK to run nightly tests in a quite easy way. At the time of the writing, 6 builds are submitted nightly to the ITK dashboard. From the perspective of a maintainer of a nightly test build, it is the best way to ensure that WrapITK runs on its host, with the options he use.

Because WrapITK developments and bug fixes are closely related to ITK ones, testing the last version of WrapITK from the subversion repository implies to use the last version of ITK from CVS repository. The easiest way to go is to set up both ITK and WrapITK nightly builds, and to use ITK build to build WrapITK.

# Requirements #

  * CVS - It's the tool used to manage changes in ITK.
  * subversion - It's the tool used to manage changes in WrapITK.
  * a C++ compiler.
  * swig - The C++ code generator in charge of the code genaration in WrapITK. You'll have to use a fairly recent version to avoid reporting already fixed warning or errors caused by bugs in swig.
  * cmake - It's the tool used by WrapITK to manage the template instantiations according to the user options, to manage the build, and to run the tests.
  * CableSwig - gccxml, cableidx TODO: document those tools
  * arount 3 GB of free space on your hard drive.

# Getting a working copy of last versions of ITK and WrapITK #

There is no fixed way to organize the directory layout of sources and build directories. Here, we will assume that all the tests are made in a directory "tests" in home directory of the user. The build directory are subdirs of the working copy.

## Getting ITK sources ##
```
cd tests
cvs -d :pserver:anonymous@www.itk.org:/cvsroot/Insight login
```
When asked for a password, reply "insight".
```
cvs -d :pserver:anonymous@www.itk.org:/cvsroot/Insight co Insight
cd Insight
mkdir build
```

## Getting WrapITK sources ##

```
cd tests
svn checkout http://wrapitk.googlecode.com/svn/trunk/ wrapitk
cd wrapitk
mkdir build
```

# Builds configurations #

The configuration is made with cmake (or ccmake or similar tools, depending on the OS).

You are free to use the configuration options you like. The more diversity we have, the best coverage we'll have for WrapITK!

A few ones must have some specific values though, and some may be useful for enhancing the test efficiency, like the use of ccache.

## ITK configuration ##

In addition to the options required in ITK to build WrapITK, the ITK should be configured with ITK\_LEGACY\_SILENT set to ON to avoid reporting ITK's deprecation warnings in WrapITK builds.

ccache can be used to greatly reduce the rebuild time of ITK. It is compatible with gcc (TODO: maybe others - icc?). To you it, the environment variables CC and CXX must be set properly before running cmake. It is simply used as follow:
```
export CC="ccache-swig gcc"
export CXX="ccache-swig c++"
cmake ..
```

## WrapITK configuration ##

A few configuration parameters are important:
  * SITE - the name of your build host
  * BUILDNAME - the name of the build is used to describe in a very short way the configuration used for your build. It must begin with "WrapITK", to be able to find WrapITK builds easily on the ITK dashboard. For example, "WrapITK-Darwin-c++-4.2" is a WrapITK build on Mac OS X with gcc 4.2.
  * ITK\_DIR - the ITK directory to use to build WrapITK. It must be the build directory of a nightly updated ITK, like the one you've just set up in the previous section.

Using ccache both for c++, with in the same way than with ITK, and for other cachable outputs within WrapITK (gccxml and swig) can highly reduce the rebuild time. To use is for WrapITK non C++ files, simply turn WRAP\_ITK\_USE\_CCACHE on.

# Experimental builds #

First test your build with

```
ctest -D Experimental
```

or

```
ctest -D Experimental -C Release
```

depending on the generator used by cmake.

TODO: say more!

# Nightly builds #

Then the nightly builds are run with

```
make clean
ctest -D Nightly
```

or

```
make clean
ctest -D Nightly -C Release
```

TODO: say more, add visual studio case


# Ressource usage #

The ressources used on your computer are highly dependent on how you have configured your build. The tests are highly CPU demanding, so the computationnal capabilities of the hosts where the tests are run have a great impact on build time.

Here are a few example of ressource usage on different hosts:

  * marvin.jouy.inra.fr - Dell Precision T5500, Intel X5570 8 cores 2.93 GHz, 24 GB of RAM, OpenSolaris 2009.06, Release build, Java/Python/Tcl on, all other options to default values.
    * ITK: ~30 minutes, 580 MB
    * WrapITK: ~1.5 hours, 2.0 GB

  * voxel2.jouy.inra.fr - Dell PowerEdge 1750, 2 Intel Pentium4 2.4 GHz, 1 GB of RAM, Windows XP, Release build, Java/Python/Tcl on, all other options to default
    * ITK: ~2.5 hours, 2.23 GB
    * WrapITK: ~12 hours, 1.93 GB

  * cmac.jouy.inra.fr - iMac 20″, Core 2 duo 2.4 GHz, 2 GB of RAM, Mac OS X 10.5, Release build, Java/Python/Tcl on, all other options to default
    * ITK: ~1 hour, 1.1 GB
    * WrapITK: ~5 hours, 3.6 GB
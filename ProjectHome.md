# WrapITK #
## Automated dynamic language binding for Insight Toolkit (ITK) ##

<img src='http://wrapitk.googlecode.com/files/wrapitk_.png' align='right'>

WrapITK is an effort to automate the language binding process of one of the largest highly template-oriented c++ libraries, the <a href='http://www.itk.org'>Insight Toolkit</a>  image processing library.<br>
<br>
Currently Python, Java and Tcl language bindings are implemented, but only Python is fully supported. For ITK .NET languages wrapper you may refer to <a href='http://code.google.com/p/manageditk/'>ManagedITK</a>.<br>
<br>
<h3>Download binaries <sup><font color='#3366cc' size='1'>NEW</font></sup></h3>
Binaries for multiple platforms and architectures, including Linux, Mac and Windows, are available. See the <a href='http://code.google.com/p/wrapitk/wiki/WrapITKBinaries'>binaries wiki page</a> for currently supported platforms and installation instructions.<br>
<br>
<h3>Compilation instructions</h3>
This project involves the development version of WrapITK which normally requires the development version of ITK accessible from <a href='http://www.itk.org/ITK/resources/software.html'>here</a>. In addition, the following tools and libraries are required:<br>
<br>
<ul><li><a href='http://www.cmake.org'>CMake</a> (>= 2.4.8): For configuring the compilation system.</li></ul>

<ul><li><a href='http://www.itk.org/ITK/resources/CableSwig.html'>CableSwig</a> (>= 0.1.0): For parsing and automatic instantiation of c++ templates.</li></ul>

<ul><li><a href='http://www.swig.org'>SWIG</a> (>= 1.3.35): For language binding. >= 1.3.38 is recommended for documentation wrapping.</li></ul>

<ul><li><a href='http://www.python.org'>Python</a> (>= 2.4): Some code generating processes are currently implemented in python. Mac OS X requires Python >= 2.5 for Python support, because of a bug in previous releases on that plateform.</li></ul>

<ul><li><a href='http://www.doxygen.org'>Doxygen</a> (>= 1.3.9.1, optional): For automatic generation of <i>inline</i> documentation in the target language (coming soon). This is optional, but highly recommended, as ITK is a huge library. Enabling this feature provides the access to instant documentation in a modern IDE with code assistance.</li></ul>

<ul><li>Language binding development libraries: The interfacing libraries for wrapping language of choice, eg, JNI for java binding.</li></ul>


<h3>Language support</h3>
Since WrapITK uses SWIG for language binding, in principle, any languages supported by SWIG may be used to wrap ITK. If you are interested in adding an additional language, you are encouraged to participate to the project.<br>
<br>
<h3>Interface to other libraries</h3>
In addition to language binding, WrapITK also implements import/export of image data from/to the following libraries:<br>
<br>
<ul><li><a href='http://www.vtk.org'>Visualization Toolkit (VTK)</a>
</li><li><a href='http://numpy.scipy.org'>NumPy</a>
</li><li><a href='http://www.fenics.org'>FEniCS DOLFIN</a> (Coming soon)</li></ul>

To enable these features, you need to first compile WrapITK. The code for each interface can be found in <a href='http://code.google.com/p/wrapitk/source/browse/#svn/trunk/ExternalProjects'>ExternalProjects</a> directory. Simply use CMake to start building these interfaces.<br>
<br>
<h3>Help</h3>
Please report WrapITK related bugs using the <a href='http://code.google.com/p/wrapitk/issues/list'>issues page</a>. You may also ask for configuration and compilation help in the <a href='http://www.itk.org/ITK/help/mailing.html'>ITK mailing list</a>.<br>
<br>
<h3>Authors</h3>

<ul><li><b>Gaëtan Lehmann</b>, INRA, UMR1198 Biologie du développement et reproduction, Domaine de Vilvert, F-78352 Jouy-en-Josas, France ; CNRS, Domaine de Vilvert, F-78352 Jouy-en-Josas, France ; ENVA, F-94704 Maisons Alfort, France.</li></ul>

<ul><li><b>Zachary Pincus</b>, Program in Biomedical Informatics and Department of Biochemistry, Stanford University School of Medicine, Stanford, California</li></ul>

<ul><li><b>Benoit Regrain</b>, CREATIS, CNRS UMR 5515, Inserm U630, Univ. Lyon1, INSA Lyon, 69621 Villeurbanne, France</li></ul>

<ul><li><b>Ali Tonddast-Navaei</b></li></ul>

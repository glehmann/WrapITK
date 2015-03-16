WrapITK release page for version 0.3.0.



# Introduction #

After a long time since its integration into ITK, WrapITK 0.3.0 is officially released on Friday 26 June 2009. A significant amount of effort was put to the architecture of the whole wrapping process, and enhancing the class coverage, target languages integration and user experience.

# Wrapping process re-design #

  * The use of stand-alone swig instead of CableSwig, the tool created to wrap ITK. This decreases the developing maintenance, and makes the connection with other tool wrapped with swig easier. Note that two tool packaged with CableSwig are still needed — gccxml and cableidx — that's why you still have to install CableSwig package to build WrapITK.

  * Full separation of types declaration and code generation. It is now possible to use WrapITK to wrap more than simple language binding. The Doc module for example can automatically generate the unix manpages for the classes instantiated in WrapITK.

  * Code generation based on callback macros. This makes WrapITK more flexible and more easily extensible.

  * Automatic inline documentation generation from c++ to target language using Doxygen.

  * Options stored in installed tree which makes them re-usable in external project, and thus simplify the configuration of those projects by the user.

  * CPack. WrapITK binaries can now be automatically bundled as installation files for several OS.

  * CCache. WrapITK is able to used CCache to cache some internal files. This considerably speeds up the rebuild process, making the life of the developers easier.

  * Nightly tests. On a nightly base, WrapITK tests are reported on ITK dashboard in order to monitor the development quality on a large number of platforms.

# Class coverage #

WrapITK can now manipulates RGBAPixel types. The classes in the itk::Statistics namespace are now usable (they where empty before this release).

The filter coverage has raised to 75% with 279 filters available.

# Target languages changes #

Although most of the changes are focused on python, some new language bindings are introduced in this release.

## Python ##

### Smaller binary size ###

Binary size is about 50% smaller than before. Even with a larger number of classes wrapped, this new version produces 222MB of binaries, to be compared to the 388MB produced by the one included in ITK¹.

### Faster ###

WrapITK is remarkably faster than before. Here some measures made with this release and the previous one¹:

| **Action**    | **Old WrapITK release** | **New WrapITK release** | **Speed up** |
|:--------------|:------------------------|:------------------------|:-------------|
| load        | 23.8312721252         | 3.18670701981         | 7.48       |
| index       | 1.23672509193         | 0.613842010498        | 2.01       |
| index2      | 2.80786514282         | 1.45068907738         | 1.94       |
| integer     | 1.9988951683          | 0.988557100296        | 2.02       |
| list        | 2.09374189377         | 1.02638506889         | 2.04       |
| tuple       | 2.09267783165         | 1.05574297905         | 1.98       |
| new         | 1.45943212509         | 0.429218053818        | 3.40       |
|extended\_new | 2.02460122108         | 1.38173890114         | 1.47       |

See [timing.py](http://code.google.com/p/wrapitk/source/browse/trunk/Languages/Python/Tests/timing.py) tests for more details.

Load time is remarkably decreased — more than 7 times faster!

Those good results can be explained by:

  * the use of more recent version of swig;

  * the use of simple python objects instead of wrapping itk::SmartPointers (see below).

Note that psyco, which has _not_ been used for those measures, can even further enhance the speed (see below).

### `itk::SmartPointer` is not wrapped anymore ###

SmartPointers are not wrapped any more. Here are some significant improvements

  * Smaller binaries ;

  * Faster load ;

  * GetPointer() is no more needed to pass a smart pointed object to a function which require a super class of the object. However, GetPointer() is still available for backward compatibility. A warning will be displayed when this method is called and it will disappear in one of the next releases.

### No optional patch — the features are available by default ###

In previous versions, python integration was enhanced by patching ITK code. The integration is now made with the standard swig mechanisms and doesn't require any patch. Everything is there by default.

### No more std::basic\_string ###

Many methods were not accessible in python as required std::basic\_string instead of std::string. Several users have reported this problem when trying to use dicom reader from python. All those methods are now wrapped and can be called.

### Better `repr()` for simple types ###

Even with optional patches, it was quite difficult to read the content of simple types like itk::Index. The simplest way (with optional patches) to make a print — repr, was the standard swig one:

```
>>> print idx
[0, 0, 0]
>>> idx
<C itk::Index<(3u)> instance at _401df009_p_itk__IndexT3u_t>
```

things are more easier and more presentable now:

```
>>> idx
itkIndex3([0, 0, 0])
```
and makes useless the use of the print command in the interpreter.

### Casting ###

All the subclasses of LightObject now provide a cast() static method which let the user to convert objects at run time.

```
>>> median = itk.MedianImageFilter.IUS3IUS3.New()
>>> obj = itk.LightObject.cast(median)
>>> obj
<ITKCommonBasePython.itkLightObject; proxy of <Swig Object of type 'itkLightObject *' at 0xa5f4990> >
>>> itk.ImageSource.IUS3.cast(obj)
<itkImageSourcePython.itkImageSourceIUS3; proxy of <Swig Object of type 'itkImageSourceIUS3 *' at 0xa5f4990> >
```

Additionnaly, itk module provides the down\_cast() which automatically cast the object to the most specialized know type:

```
>>> itk.down_cast(obj)
<itkMedianImageFilterPython.itkMedianImageFilterIUS3IUS3; proxy of <Swig Object of type 'itkMedianImageFilterIUS3IUS3 *' at 0xa5f4990> >
```

### `[]` is a better `GetOutput()` ###

Up to now, the user had to use GetOutput() to get the images produced by a filter. However, the GetOutput() method is not bounded (one can use it with a higher value than the actual number of outputs in that filter. GetOutput() also produce a non casted output and may fail to give a valid if the outputs of the filter are of different types.

The `[]` function checks the bounds, casts the output to its real type, and also accepts the slice notation.

```
>>> dmap = itk.DanielssonDistanceMapImageFilter.IUS3IF3.New()
>>> dmap[0]
<itkImagePython.itkImageF3; proxy of <Swig Object of type 'itkImageF3 *' at 0xacd0718> >
>>> dmap[10]
IndexError: index out of range
>>> dmap[:]
[<itkImagePython.itkImageF3; proxy of <Swig Object of type 'itkImageF3 *' at 0xacd0718> >,
 <itkImagePython.itkImageF3; proxy of <Swig Object of type 'itkImageF3 *' at 0xacd0508> >,
 <itkImagePython.itkImageO33; proxy of <Swig Object of type 'itkImageO33 *' at 0xacd0918> >]
```

### () is a better `UpdateLargestPossibleRegion()` ###

One thing the user quickly notes when using WrapITK is the required usage of UpdateLargestPossibleRegion() when working with images of different sizes. The simpler Update() does not work in this case, as it doesn't trigger the re-negotiation of the regions in the pipeline. UpdateLargestPossibleRegion() is the right method to use, but is painfully long to write.

WrapITK provide the () notation to make the update of the pipeline less verbose. This notation also allows to change some input values before the update, as in the New() method, and return the filter to make easier to get a specific output.

The following example change the input of the filter dmap, change UseImageSpacing to True, update the pipeline and return the first input of dmap.

```
>>> dmap(img, UseImageSpacing=True)[0]
<itkImagePython.itkImageF3; proxy of <Swig Object of type 'itkImageF3 *' at 0xacd0718> >
```

Keep in mind that this notation doesn't change the pipeline behavior at all. In accordance with the pipeline model, the following example _doesn't_ produce 3 different images:

```
>>> img1 = dmap(input1)[0]
>>> img2 = dmap(input2)[0]
>>> img3 = dmap(input3)[0]
```

, but a single one which is a result of the dmap filter with input3 as input:

```
>>> img1 == img2 == img3
True
```

### Python callbacks ###

WrapITK now hides the complexity of the PyCommand class. Adding a python callback can be done in a single line. The following example displays the progress of the median filter on stderr:

```
median.AddObserver(itk.ProgressEvent(), lambda: sys.stderr.write(str(median.GetProgress())+"\n"))
```

### `itk.show2D()` enhancements ###

itk.show2D() can now display labeled images and itk::LabelMap objects.

Also, imview is not the only option. With defining some environment variables, the user can change the viewer in use. Here is an example with ImageJ:

```
export WRAPITK_SHOW2D_COMMAND="/usr/java/jdk1.6.0/bin/java -Xmx1024m -jar /home/glehmann/ImageJ/ij.jar %s  -run 'View 100%%' &"
export WRAPITK_SHOW2D_LABEL_COMMAND="/usr/java/jdk1.6.0/bin/java -Xmx1024m -jar /home/glehmann/ImageJ/ij.jar %s  -run 'View 100%%' -run '3-3-2 RGB' &"
export WRAPITK_SHOW2D_COMPRESS=off
export WRAPITK_SHOW2D_EXTENSION=.tif
```

### Python composite filters ###

Many filters in ITK are internally made of a pipeline of several filters — let us call this _composite filters_.

Some tools have been added in WrapITK for creating such filters in python: itk.pipeline, auto\_pipeline, templated\_class, and the build options (DIMS, USIGN\_INTS, SIGN\_INTS, REALS, VECTOR\_REALS, COV\_VECTOR\_REALS, RGBS, RGBAS, COMPLEX\_REALS, INTS, SCALARS, VECTORS, COLORS, and ALL\_TYPES).

See [templated\_pipeline.py](http://code.google.com/p/wrapitk/source/browse/trunk/Languages/Python/Tests/templated_pipeline.py) for an example.

### Documentation integration ###

Docstrings are now automatically generated in python, based on the C++ signatures, and using the documentation generated by doxygen. Here is an example in IPython:

```
10> area.SetInput?
Type:		instancemethod
Base Class:	<type 'instancemethod'>
String Form:	<bound method itkAreaOpeningImageFilterIUC3IUC3.itkImageToImageFilterIUC3IUC3_SetInput of <itkAre <...> terIUC3IUC3; proxy of <Swig Object of type 'itkAreaOpeningImageFilterIUC3IUC3 *' at 0x1a9fbd8> >>
Namespace:	Interactive
Docstring:
    SetInput(itkImageUC3 input)
    itkImageToImageFilterIUC3IUC3_SetInput(itkImageToImageFilterIUC3IUC3 self, unsigned int index, 
        itkImageUC3 image)
    
    Set/Get the image input of
    this process object. 
```

### psyco ###

WrapITK loads psyco, if available, to improve the performances.

Here are some results²:

| **Action**    | **Without psyco**       | **With psyco**          | **Speed up** |
|:--------------|:------------------------|:------------------------|:-------------|
| load        | 17.5761048794         | 17.571958065          | 1.00       |
| index       | 1.28790211678         | 1.04161691666         | 1.24       |
| index2      | 4.10891604424         | 3.36609005928         | 1.22       |
| integer     | 2.43840312958         | 2.01709103584         | 1.21       |
| list        | 2.54752993584         | 2.09809708595         | 1.21       |
| tuple       | 2.50614404678         | 2.02894997597         | 1.24       |
| new         | 1.87332892418         | 1.80359697342         | 1.04       |
|extended\_new | 4.80319905281         | 6.23383378983         | 0.77       |

Overall, the performance is improved, excepted for extended\_new. Fortunately, the user shouldn't call the New() method often. The load time is kept unchanged, probably because most of the load time is spent in loading binary files.

No memory usage study has been performed yet.

## Java ##

### Smaller binary size ###

WrapITK produces smaller java binaries with this release — 43 MB, compared to the 78 MB of the previous release.

### Simulating java `new` ###

Before this release, the objects where created this way:

```
itkImageUS2_Pointer img = itkImageUS2.itkImageUS2_New();
```

Now, objects can be created ina  more java-native way:

```
itkImageUS2 img = new itkImageUS2();
```

### `itk::SmartPointer` is not wrapped anymore ###

SmartPointers are not wrapped anymore in java. Here are some significant improvements:

  * Binary size is about 50% smaller than before;

  * Load time is remarkably decreased;

  * GetPointer(), which passes a smart pointer object to a function which requires a super class of the object, is no more required.

### Wrapping to multiple java packages ###

Each ITK shared library is now automatically wrapped to a separate java package. For instance, the IO library is wrapped to `org.itk.io`. If you have developed your own library based on ITK and wish to wrap it to java, it is possible to have it as your own custom package.

### toString() ###

itk::LightObject now has a toString() method which returns what is printed by the standard Print(std::stream) method of itk::LightObject.

### External projects ###

WrapITK external projects can now be built in java.

## TCL ##

Nothing really new for TCL in this realease, excepted that it uses the stand-alone swig instead of the on in CableSwig. A noticeable thing though: it is still there!

Any contributions are welcome to improve this language support.

## New languages ##

Some work has been done on ruby support. It is possible to build a WrapITK with Ruby support at this time, but the integration is not of desirable quality.

Contributions are also welcome for ruby binding.

# Supported platforms #

WrapITK is tested on the following platforms:

  * Mac OS X 10.5 Intel
  * GNU/Linux
  * OpenSolaris
  * Microsoft Windows

It may also work on other platforms, but has not been tested yet.

# Known issues #

  * Due to swig [bug #2583160](https://code.google.com/p/wrapitk/issues/detail?id=2583160), python modules can't be loaded with python 2.6 when built with swig 1.3.37 or 1.3.38. Workaround: use swig 1.3.39 or newer, or swig 1.3.36 or older, or python 2.5 or older;

  * Due to swig [bug #2552048](https://code.google.com/p/wrapitk/issues/detail?id=2552048), python generated doc doesn't contain method signature when built with swig 1.3.37. Workaround: use another version of swig;

  * BinaryDilateImageFilter has no SetKernel() method in Tcl for unknown reasons. This may affect other classes. Workaround: not available at the moment;

  * Due to OpenSolaris [bug #6634042](https://code.google.com/p/wrapitk/issues/detail?id=6634042), WrapITK generates a core dump on (Open)Solaris x86 when built in 64 bits with gcc. Workaround: preload libgcc\_s.so.1 with
```
export LD_PRELOAD_64=libgcc_s.so.1
```

  * WrapITK generates invalid code in VoronoiSegmentationImageFilter wrapper when build with with Microsoft Visual Studio 8 (and maybe other versions) and ITK 3.14. Workaround: patch ITK 3.14 with [this fix](http://public.kitware.com/cgi-bin/viewcvs.cgi/Code/Algorithms/itkVoronoiSegmentationImageFilterBase.h?root=Insight&r1=1.30&r2=1.31&sortby=date) already in ITK cvs.

  * Python 3 is not supported. No workaround is available at this time.

# Binary downloads and installation #

Binaries and installation procedures are available on [WrapITKBinaries](WrapITKBinaries.md).

# Source downloads and build #

Download the sources from http://wrapitk.googlecode.com/files/wrapitk-0.3.0.tar.bz2 .

The following tools and libraries are required:

  * [CMake](http://www.cmake.org) (>= 2.4.8): For configuring the compilation system.

  * [CableSwig](http://www.itk.org/ITK/resources/CableSwig.html) (>= 0.1.0): For parsing and automatic instantiation of c++ templates.

  * [SWIG](http://www.swig.org) (>= 1.3.35): For language binding. >= 1.3.38 is recommended for documentation wrapping.

  * [Python](http://www.python.org) (>= 2.4): Some code generating processes are currently implemented in python. Mac OS X requires Python >= 2.5 for Python support, because of a bug in previous releases on that plateform.

  * [Doxygen](http://www.doxygen.org) (>= 1.3.9.1, optional): For automatic generation of _inline_ documentation in the target language (coming soon). This is optional, but highly recommended, as ITK is a huge library. Enabling this feature provides the access to instant documentation in a modern IDE with code assistance.

  * Language binding development libraries: The interfacing libraries for wrapping language of choice, eg, JNI for java binding.

# Bug reports #

Please report WrapITK related bugs using the [issues page](http://code.google.com/p/wrapitk/issues/list). You may also ask for configuration and compilation help in the [ITK mailing list](http://www.itk.org/ITK/help/mailing.html).

# Authors #

Gaëtan Lehmann, INRA, UMR1198 Biologie du développement et reproduction, Domaine de Vilvert, F-78352 Jouy-en-Josas, France ; CNRS, Domaine de Vilvert, F-78352 Jouy-en-Josas, France ; ENVA, F-94704 Maisons Alfort, France.

Ali Tonddast-Navaei


---

¹ Measured on a Dell Precision T5500, Intel X5570 8 cores 2.93 GHz, 24 GB of RAM running OpenSolaris 2009.06. ITK and WrapITK are built with gcc 4.3.2 in 64 bits, Release mode with the default options.
² Measured on a Dell Precision GX380, Intel Pentium4 CPU 3.20 GHz, 4 GB of RAM running Mandriva Linux 2009. ITK and WrapITK are built with gcc 4.3.2 in 32 bits, Release mode with the default options and support for unsigned char, rgb unsigned char and rgba unsigned char.


# Linux #
## Ubuntu ##
### 9.04 Jaunty ###
### 8.10 Intrepid ###
## Debian ##
### 5.0 Lenny ###
| **Architectures** | **ITK**<br> version<table><thead><th> <b>Binding</b><br> languages</th><th> <b>Image</b><br> dimensions</th><th> <b>Pixel types</b> </th><th> <b>Runtime</b><br> packages</th><th> <b>Development</b><br> packages </th></thead><tbody>
<tr><td> x86 <br> x86_64 </td><td> 3.14 </td><td> Python 2.6 (<i>Ubuntu 9.04</i>) <br> Python 2.5 (<i>Debian 5.0, Ubuntu 8.10</i>) </td><td> 2, 3 </td><td> Unsigned char <br> Unsigned short <br> Float <br> Double <br> Complex float <br> Complex double <br> Vector float <br> Vector double <br> Co-variant vector float <br> Co-variant vector double <br> RGB unsigned short <br> RGBA unsigned short</td><td> libitk <br> python-itk <br> python-itk-numpy </td><td> libitk-dev </td></tr></tbody></table>

<ul><li>Adding the repository:<br>
<ul><li>Ubuntu 9.04 Jaunty <sup><font color='#3366cc' size='1'>NEW</font></sup>
<pre><code>sudo wget http://wrapitk.googlecode.com/files/wrapitk-ubuntu-9.04.list -O /etc/apt/sources.list.d/wrapitk.list<br>
</code></pre>
</li><li>Ubuntu 8.10 Intrepid<br>
<pre><code>sudo wget http://wrapitk.googlecode.com/files/wrapitk-ubuntu-8.10.list -O /etc/apt/sources.list.d/wrapitk.list<br>
</code></pre>
</li><li>Debian 5.0 Lenny <sup><font color='#3366cc' size='1'>NEW</font></sup>
<pre><code>sudo wget http://wrapitk.googlecode.com/files/wrapitk-debian-5.0.list -O /etc/apt/sources.list.d/wrapitk.list<br>
</code></pre>
</li></ul></li><li>Installation:<br>
<pre><code>sudo apt-get update<br>
sudo apt-get install libitk libitk-dev python-itk<br>
</code></pre>
</li></ul><blockquote>Package libitk-dev may be used for developing custom ITK classes as well as automatically wrapping them. Other packages, such as python-itk-numpy, may be installed for interfacing to external libraries.</blockquote>

<h1>Mac OS X</h1>
<table><thead><th> <b>Architectures</b> </th><th> <b>ITK</b><br> version</th><th> <b>Binding</b><br> languages</th><th> <b>Image</b><br> dimensions</th><th> <b>Pixel types</b> </th><th> <b>Runtime and Development</b><br> packages </th></thead><tbody>
<tr><td> x86 </td><td> 3.14 </td><td> Python 2.5 <br> Java <br> TCL </td><td> 2, 3 </td><td> Unsigned short <br> Float <br> Complex float <br> Vector float <br> Co-variant vector float <br> RGB unsigned short <br> RGBA unsigned short</td><td> ITK-3.12.0-Darwin.dmg <br> WrapITK-0.3.0-Darwin.dmg  </td></tr></tbody></table>

Installation files can be downloaded from <a href='http://voxel.jouy.inra.fr/itk/wrapitk-0.3.0/'>http://voxel.jouy.inra.fr/itk/wrapitk-0.3.0/</a>. You will need to update these environment variables afterwards:<br>
<br>
<pre><code>export DYLD_LIBRARY_PATH=/usr/local/lib/InsightToolkit/:$DYLD_LIBRARY_PATH<br>
export PYTHONPATH=/usr/local/lib/InsightToolkit/WrapITK/Python/:$PYTHONPATH<br>
</code></pre>

<h1>Microsoft Windows</h1>
<table><thead><th> <b>Architectures</b> </th><th> <b>ITK</b><br> version</th><th> <b>Binding</b><br> languages</th><th> <b>Image</b><br> dimensions</th><th> <b>Pixel types</b> </th><th> <b>Runtime and Development</b><br> packages </th></thead><tbody>
<tr><td> x86 </td><td> 3.14 </td><td> Python 2.5 <br> Java <br> TCL </td><td> 2, 3 </td><td> Unsigned short <br> Float <br> Complex float <br> Vector float <br> Co-variant vector float <br> RGB unsigned short <br> RGBA unsigned short</td><td> ITK-3.14.0-win32.exe <br> WrapITK-0.3.0-win32.exe  </td></tr></tbody></table>

Installation files can be downloaded from <a href='http://voxel.jouy.inra.fr/itk/wrapitk-0.3.0/'>http://voxel.jouy.inra.fr/itk/wrapitk-0.3.0/</a>. You will need to update a couple of environment variables afterwards. Assuming the default installation path was chosen, append:<br>
<br>
<pre><code>C:\Program Files\InsightToolkit-3.14\bin<br>
</code></pre>

to PATH, and<br>
<br>
<pre><code>C:\Program Files\WrapITK 0.3.0\lib\InsightToolkit\WrapITK\Python<br>
</code></pre>

to PYTHONPATH.
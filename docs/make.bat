@ECHO OFF

REM Command file for Sphinx documentation

REM recreate using this command:
REM sphinx-quickstart --extensions=gunicorn_ext --templatedir=_templates --makefile --batchfile --no-use-make-mode --master=index

pushd %~dp0

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set BUILDDIR=_build
set SOURCEDIR=source
set ALLSPHINXOPTS=-d %BUILDDIR%/doctrees %SPHINXOPTS% %O% %SOURCEDIR%
set I18NSPHINXOPTS=%SPHINXOPTS% %SOURCEDIR%
if NOT "%PAPER%" == "" (
	set ALLSPHINXOPTS=-D latex_elements.papersize=%PAPER%paper %ALLSPHINXOPTS%
	set I18NSPHINXOPTS=-D latex_elements.papersize=%PAPER%paper %I18NSPHINXOPTS%
)

if "%1" == "" goto help

if "%1" == "help" (
	:help
	echo.Please use `make ^<target^>` where ^<target^> is one of
	echo.  html       to make standalone HTML files
	echo.  dirhtml    to make HTML files named index.html in directories
	echo.  singlehtml to make a single large HTML file
	echo.  pickle     to make pickle files
	echo.  json       to make JSON files
	echo.  htmlhelp   to make HTML files and an HTML help project
	echo.  qthelp     to make HTML files and a Qt help project
	echo.  devhelp    to make HTML files and a Devhelp project
	echo.  epub       to make an EPUB
	echo.  latex      to make LaTeX files (you can set PAPER=a4 or PAPER=letter)
	echo.  latexpdf   to make LaTeX files and then PDFs out of them
	echo.  text       to make text files
	echo.  man        to make manual pages
	echo.  texinfo    to make Texinfo files
	echo.  gettext    to make PO message catalogs
	echo.  changes    to make an overview over all changed/added/deprecated items
	echo.  xml        to make Docutils-native XML files
	echo.  pseudoxml  to make pseudoxml-XML files for display purposes
	echo.  linkcheck  to check all external links for integrity
	echo.  doctest    to run all doctests embedded in the documentation if enabled
	echo.  coverage   to run coverage check of the documentation if enabled
	echo.  dummy      to check syntax errors of document sources
	echo.  clean      to remove everything in the build directory
	goto end
)

if "%1" == "clean" (
	for /d %%i in (%BUILDDIR%\*) do rmdir /q /s %%i
	del /q /s %BUILDDIR%\*
	goto end
)

REM Check if sphinx-build is available and fallback to Python version if any
%SPHINXBUILD% 1>NUL 2>NUL
if errorlevel 9009 goto sphinx_python
goto sphinx_ok

:sphinx_python

set SPHINXBUILD=python -m sphinx.__init__
%SPHINXBUILD% 2> nul
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.https://www.sphinx-doc.org/
	exit /b 1
)

:sphinx_ok

if "%1" == "latexpdf" (
	%SPHINXBUILD% -b latex %ALLSPHINXOPTS% %BUILDDIR%/latex
	cd %BUILDDIR%/latex
	make all-pdf
	cd %~dp0
	echo.
	echo.Build finished; the PDF files are in %BUILDDIR%/latex.
	goto end
)

if "%1" == "latexpdfja" (
	%SPHINXBUILD% -b latex %ALLSPHINXOPTS% %BUILDDIR%/latex
	cd %BUILDDIR%/latex
	make all-pdf-ja
	cd %~dp0
	echo.
	echo.Build finished; the PDF files are in %BUILDDIR%/latex.
	goto end
)

if "%1" == "gettext" (
	%SPHINXBUILD% -b gettext %I18NSPHINXOPTS% %BUILDDIR%/locale
	if errorlevel 1 exit /b 1
	goto end
)

%SPHINXBUILD% -b %1 %ALLSPHINXOPTS% %BUILDDIR%/%1
goto end

:end
popd

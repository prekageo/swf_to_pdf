## Adobe Flash (SWF) to SVG and PDF

Recently, I found some documents exported as [SWF](https://en.wikipedia.org/wiki/SWF). It would be certainly more convenient for me if I could read these documents in my PDF reader. So I needed a utility to convert content from [Adobe Flash](https://en.wikipedia.org/wiki/Adobe_Flash) to [PDF](https://en.wikipedia.org/wiki/Portable_Document_Format). For this reason, I’ve written a small Python program that utilizes the [SWFTools](http://www.swftools.org/) in order to parse the SWF and exports output in [SVG](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics) and PDF file formats.

The utility is still very experimental and will certainly need some tuning in order to produce perfect output. In order to use it, you need, of course, Python and, also, the SWFTools. You need to add a few lines in lib/Makefile of SWFTools in order to create a dynamic library for Python:

```
librfxswf.$(SLEXT): $(rfxswf_objects) rfxswf.$(O) drawer.$(O) $(lame_in_source) $(h263_objects) $(as12compiler_in_source) $(as3compiler_objects) libbase$(A)
  $(L) -g -shared -o $@ $^ -lz
```

The utility is split into two parts. The `swf_lib.py` uses [Python ctypes](https://docs.python.org/library/ctypes) in order to communicate with the dynamic library and the `swf_to_pdf.py` is the main engine that performs the transformation. Currently shapes and text are supported. Eventually, more stuff could be implemented. It should be possible to transform a Flash application completely into an equivalent HTML5 application. I’ll leave that as an exercise for the reader!

You can see here an example of the utility:

* The [original PDF](https://github.com/prekageo/swf_to_pdf/blob/master/examples/original.pdf).
* The [SWF](https://github.com/prekageo/swf_to_pdf/blob/master/examples/input.swf) produced by SWFTools’ pdf2swf tool.
* The [output SVG](https://github.com/prekageo/swf_to_pdf/blob/master/examples/output.svg) produced by the SWF to SVG/PDF utility presented here.
* The [output PDF](https://github.com/prekageo/swf_to_pdf/blob/master/examples/output.pdf) produced by the SWF to SVG/PDF utility presented here.

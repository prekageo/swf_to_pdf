#!/usr/bin/python
# coding=utf-8

"""
Transform a Flash file to SVG and PDF. It is very experimental and needs manual
tuning. Nevertheless, it serves as a good base for accomplishing this task. It
uses swftools in order to parse the SWF and reportlab in order to generate the
PDF.
"""

import swf_lib
from xml.etree import ElementTree
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

""" Open a reference to the librfxswf dynamic library. """
s = swf_lib.SWF()

""" Parse an SWF file and return the shapes and texts found. """
def parse_swf(filename):
    texts = []
    shapes = []

    swf_d = s.open_swf(filename)
    swf = swf_d['swf']
    fonts = s.font_enumerate(swf)
    tag = swf.contents.firstTag
    while tag:
        id = tag.contents.id
        if id in [swf_lib.Tags.ST_DEFINETEXT, swf_lib.Tags.ST_DEFINETEXT2]:
            text = {}
            text['data'] = s.parse_define_text(fonts, tag)
            text['matrix'] = s.get_matrix(tag)
            texts.append(text)
        elif id in [
                swf_lib.Tags.ST_DEFINESHAPE,
                swf_lib.Tags.ST_DEFINESHAPE2,
                swf_lib.Tags.ST_DEFINESHAPE3,
                swf_lib.Tags.ST_DEFINESHAPE4
            ]:
            shape = s.parse_define_shape(tag);
            shapes.append(shape)
        tag = tag.contents.next

    size = swf_d['movie_size']
    size = (size['xmax'] - size['xmin'], size['ymax'] - size['ymin'])
    return {
        'size': size,
        'texts': texts,
        'shapes': shapes
    }

""" Generate and write the SVG file. """
def to_svg(parsed, filename):
    def color(element, color):
        r,g,b,a = color
        element.attrib['fill'] = '#%02x%02x%02x' % (r,g,b)
        element.attrib['fill-opacity'] = '%.2f' % (a/255.0)

    svg = ElementTree.Element('svg')
    svg.attrib['xmlns'] = 'http://www.w3.org/2000/svg'
    svg.attrib['viewBox'] = '0 0 %d %d' % parsed['size']
    g = ElementTree.SubElement(svg, 'g')

    for shape in parsed['shapes']:
        path = ElementTree.SubElement(g, 'path')
        d = []
        for op in shape['ops']:
            if op['type'] == swf_lib.SHAPELINETYPE.moveTo:
                d.append('M %.2f %.2f' % (op['x'], op['y']))
            elif op['type'] == swf_lib.SHAPELINETYPE.lineTo:
                d.append('L %.2f %.2f' % (op['x'], op['y']))

        fill = shape['ops'][0]['fillstyle0']
        if fill is not None:
            color(path, fill['color'])
        path.attrib['d'] = ' '.join(d)

    for text in parsed['texts']:
        m = text['matrix']
        gg = ElementTree.SubElement(g, 'g')
        gg.attrib['transform'] = 'matrix(%.2f %.2f %.2f %.2f %.2f %.2f)' % (
                m['sx'], m['r0'], m['r1'], m['sy'], m['tx'], m['ty'])
        for text2 in text['data']:
            text_el = ElementTree.SubElement(gg, 'text')
            text_el.attrib['font-family'] = 'arial'
            text_el.attrib['font-size'] = str(text2['fontsize'])
            color(text_el, text2['color'])
            text_el.attrib['y'] = str(text2['starty'])
            for i in xrange(len(text2['string'])):
                tspan = ElementTree.SubElement(text_el, 'tspan')
                tspan.attrib['x'] = str(text2['startx'] + text2['xpos'][i])
                tspan.text = text2['string'][i]

    open(filename,'w').write(ElementTree.tostring(svg))

""" Generate the PDF page. """
def to_pdf_page(c, parsed):
    def color(color):
        r,g,b,a = color
        c.setFillColorRGB(r/255.0,g/255.0,b/255.0)
        c.setFillAlpha(a/255.0)

    c.setPageSize(parsed['size'])

    for shape in parsed['shapes']:
        ops = shape['ops']
        if len(ops) > 0 and ops[0]['type'] != swf_lib.SHAPELINETYPE.moveTo:
            continue
        path = c.beginPath()
        for op in ops:
            if op['type'] == swf_lib.SHAPELINETYPE.moveTo:
                path.moveTo(op['x'], op['y'])
            elif op['type'] == swf_lib.SHAPELINETYPE.lineTo:
                path.lineTo(op['x'], op['y'])
        fill = shape['ops'][0]['fillstyle0']
        if fill is not None:
            color(fill['color'])
        c.drawPath(path, stroke = 0, fill = 1)

    for text in parsed['texts']:
        m = text['matrix']
        c.resetTransforms()
        c.transform(m['sx'], m['r0'], m['r1'], m['sy'], m['tx'], m['ty'])
        for text2 in text['data']:
            c.setFont('Arial', text2['fontsize'])
            color(text2['color'])
            for i in xrange(len(text2['string'])):
                c.drawString(text2['startx'] + text2['xpos'][i],
                        text2['starty'], text2['string'][i])

    c.showPage()

""" Generate and write the PDF file. """
def to_pdf(parsed_list, filename):
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    c = Canvas(filename, bottomup = 0, pageCompression = 1)

    for parsed in parsed_list:
        to_pdf_page(c, parsed)

    c.save()

def main():
    parsed = parse_swf('input.swf')
    to_svg(parsed, 'output.svg')
    to_pdf([parsed], 'output.pdf')

if __name__ == '__main__':
    main()

#!/usr/bin/python
# coding=utf-8

LIB_PATH = 'librfxswf.dll'

from ctypes import *

class Tags:
    ST_END                 = 0
    ST_SHOWFRAME           = 1
    ST_DEFINESHAPE         = 2
    ST_FREECHARACTER       = 3
    ST_PLACEOBJECT         = 4
    ST_REMOVEOBJECT        = 5
    ST_DEFINEBITS          = 6
    ST_DEFINEBITSJPEG      = 6
    ST_DEFINEBUTTON        = 7
    ST_JPEGTABLES          = 8
    ST_SETBACKGROUNDCOLOR  = 9
    ST_DEFINEFONT          = 10
    ST_DEFINETEXT          = 11
    ST_DOACTION            = 12
    ST_DEFINEFONTINFO      = 13
    ST_DEFINESOUND         = 14
    ST_STARTSOUND          = 15
    ST_DEFINEBUTTONSOUND   = 17
    ST_SOUNDSTREAMHEAD     = 18
    ST_SOUNDSTREAMBLOCK    = 19
    ST_DEFINEBITSLOSSLESS  = 20
    ST_DEFINEBITSJPEG2     = 21
    ST_DEFINESHAPE2        = 22
    ST_DEFINEBUTTONCXFORM  = 23
    ST_PROTECT             = 24
    ST_PLACEOBJECT2        = 26
    ST_REMOVEOBJECT2       = 28
    ST_FREEALL             = 31
    ST_DEFINESHAPE3        = 32
    ST_DEFINETEXT2         = 33
    ST_DEFINEBUTTON2       = 34
    ST_DEFINEBITSJPEG3     = 35
    ST_DEFINEBITSLOSSLESS2 = 36
    ST_DEFINEEDITTEXT      = 37
    ST_DEFINEMOVIE         = 38
    ST_DEFINESPRITE        = 39
    ST_NAMECHARACTER       = 40
    ST_SERIALNUMBER        = 41
    ST_GENERATORTEXT       = 42
    ST_FRAMELABEL          = 43
    ST_SOUNDSTREAMHEAD2    = 45
    ST_DEFINEMORPHSHAPE    = 46
    ST_DEFINEFONT2         = 48
    ST_TEMPLATECOMMAND     = 49
    ST_GENERATOR3          = 51
    ST_EXTERNALFONT        = 52
    ST_EXPORTASSETS        = 56
    ST_IMPORTASSETS        = 57
    ST_ENABLEDEBUGGER      = 58
    ST_DOINITACTION        = 59
    ST_DEFINEVIDEOSTREAM   = 60
    ST_VIDEOFRAME          = 61
    ST_DEFINEFONTINFO2     = 62
    ST_MX4                 = 63
    ST_ENABLEDEBUGGER2     = 64
    ST_SCRIPTLIMITS        = 65
    ST_SETTABINDEX         = 66
    ST_FILEATTRIBUTES      = 69
    ST_PLACEOBJECT3        = 70
    ST_IMPORTASSETS2       = 71
    ST_RAWABC              = 72
    ST_DEFINEFONTALIGNZONES= 73
    ST_CSMTEXTSETTINGS     = 74
    ST_DEFINEFONT3         = 75
    ST_SYMBOLCLASS         = 76
    ST_METADATA            = 77
    ST_DEFINESCALINGGRID   = 78
    ST_DOABC               = 82
    ST_DEFINESHAPE4        = 83
    ST_DEFINEMORPHSHAPE2   = 84
    ST_SCENEDESCRIPTION    = 86
    ST_DEFINEBINARY        = 87
    ST_DEFINEFONTNAME      = 88

class TAG(Structure):
    pass

TAG._fields_ = [
    ('id', c_ushort),
    ('data', c_void_p),
    ('memsize', c_uint),
    ('len', c_uint),
    ('pos', c_uint),
    ('next', POINTER(TAG)),
    ('prev', POINTER(TAG)),
    ('readBit', c_ubyte),
    ('writeBit', c_ubyte),
]

class SRECT(Structure):
    _fields_ = [
        ('xmin', c_int),
        ('ymin', c_int),
        ('xmax', c_int),
        ('ymax', c_int),
    ]

class SWF_STRUCT(Structure):
    _fields_ = [
        ('fileVersion', c_ubyte),
        ('compressed', c_ubyte),
        ('fileSize', c_uint),
        ('movieSize', SRECT),
        ('frameRate', c_ushort),
        ('frameCount', c_ushort),
        ('firstTag', POINTER(TAG)),
        ('fileAttributes', c_uint),
    ]

class SWFFONT(Structure):
    _fields_ = [
        ('id', c_uint),
        ('version', c_ubyte),
        ('name', c_char_p),
        ('layout', c_void_p),
        ('numchars', c_uint),
        ('maxascii', c_uint),
        ('style', c_ubyte),
        ('encoding', c_ubyte),
        ('glyph2ascii', POINTER(c_ushort)),
        ('ascii2glyph', POINTER(c_uint)),
        ('glyph2glyph', POINTER(c_uint)),
        ('glyph', c_void_p),
        ('alignzones', c_void_p),
        ('alignzone_flags', c_ubyte),
        ('language', c_ubyte),
        ('glyphnames', POINTER(c_char_p)),
        ('use', c_void_p),
    ]

class MATRIX(Structure):
    _fields_ = [
        ('sx', c_int),
        ('r1', c_int),
        ('tx', c_int),
        ('r0', c_int),
        ('sy', c_int),
        ('ty', c_int),
    ]

class RGBA(Structure):
    _fields_ = [
        ('a', c_ubyte),
        ('r', c_ubyte),
        ('g', c_ubyte),
        ('b', c_ubyte),
    ]

class LINESTYLE(Structure):
    _fields_ = [
        ('width', c_ushort),
        ('color', RGBA),
    ]

class GRADIENT(Structure):
    _fields_ = [
        ('num', c_uint),
        ('ratios', POINTER(c_ubyte)),
        ('rgba', POINTER(RGBA)),
    ]

class FillTypes:
    FILL_SOLID   = 0x00
    FILL_LINEAR  = 0x10
    FILL_RADIAL  = 0x12
    FILL_TILED   = 0x40
    FILL_CLIPPED = 0x41

class FILLSTYLE(Structure):
    _fields_ = [
        ('type', c_ubyte),
        ('color', RGBA),
        ('m', MATRIX),
        ('id_bitmap', c_ushort),
        ('gradient', GRADIENT),
    ]

class SHAPELINETYPE:
    moveTo = 0
    lineTo = 1
    splineTo = 2

class SHAPELINE(Structure):
    pass

SHAPELINE._fields_ = [
    ('type', c_uint),
    ('x', c_int),
    ('y', c_int),
    ('sx', c_int),
    ('sy', c_int),
    ('fillstyle0', c_uint),
    ('fillstyle1', c_uint),
    ('linestyle', c_uint),
    ('next', POINTER(SHAPELINE)),
]

class SHAPE2(Structure):
    _fields_ = [
        ('linestyles', POINTER(LINESTYLE)),
        ('numlinestyles', c_uint),
        ('fillstyles', POINTER(FILLSTYLE)),
        ('numfillstyles', c_uint),
        ('lines', POINTER(SHAPELINE)),
        ('bbox', POINTER(SRECT)),
    ]

class SWF:
    def __init__(self):
        self.lib = cdll.LoadLibrary(LIB_PATH)
        self.lib.swf_OpenSWF.restype = POINTER(SWF_STRUCT)

    def open_swf(self, filename):
        res = self.lib.swf_OpenSWF(filename)
        return {
            'swf': res,
            'movie_size': {
                'xmin': res.contents.movieSize.xmin / 20.0,
                'ymin': res.contents.movieSize.ymin / 20.0,
                'xmax': res.contents.movieSize.xmax / 20.0,
                'ymax': res.contents.movieSize.ymax / 20.0,
            }
        }

    FONT_ENUM_FUNC = CFUNCTYPE(None, c_int, c_int, c_char_p)

    def font_enumerate(self, swf):
        fonts = {}
        def callback(self_, id, name):
            font = pointer(SWFFONT())
            self.lib.swf_FontExtract(swf, id, byref(font))
            fonts[font.contents.id] = font.contents
        self.lib.swf_FontEnumerate(swf, self.FONT_ENUM_FUNC(callback), 0)
        return fonts

    PARSE_DEF_TEXT_FUNC = CFUNCTYPE(None, c_void_p, POINTER(c_int), POINTER(c_int), c_int, c_int, c_int, c_int, c_int, POINTER(RGBA))

    def parse_define_text(self, fonts, tag):
        texts = []
        def callback(self_, glyphs, xpos, nr, fontid, fontsize, startx, starty, color):
            string = [0] * nr
            xpos_ = [0] * nr
            font = fonts[fontid]
            for i in xrange(nr):
                string[i] = unichr(font.glyph2ascii[glyphs[i]])
                xpos_[i] = 1.0*xpos[i]/20
            string = u''.join(string)

            texts.append({
                'self': self_,
                'string': string,
                'xpos': xpos_,
                'font': font,
                'fontsize': 1.0*fontsize/20 if fontsize > 100 else fontsize,
                'startx': 1.0*startx/20,
                'starty': 1.0*starty/20,
                'color': self.color(color.contents),
            })
        self.lib.swf_ParseDefineText(tag, self.PARSE_DEF_TEXT_FUNC(callback), 0)
        return texts

    def get_matrix(self, tag):
        self.lib.swf_SetTagPos(tag, 0)
        self.lib.swf_GetU16(tag)
        self.lib.swf_GetRect(tag, 0)
        self.swf_ResetReadBits(tag)
        m = MATRIX()
        self.lib.swf_GetMatrix(tag, byref(m))
        self.lib.swf_SetTagPos(tag, 0)
        return {
            'sx': 1.0*m.sx/65356,
            'r1': 1.0*m.r1/65356,
            'r0': 1.0*m.r0/65356,
            'sy': 1.0*m.sy/65356,
            'tx': 1.0*m.tx/20,
            'ty': 1.0*m.ty/20
        }

    def swf_ResetReadBits(self, tag):
        if (tag.contents.readBit):
            tag.contents.pos+=1
            tag.contents.readBit = 0

    def swf_ResetWriteBits(self, tag):
        if (tag.contents.writeBit):
            tag.contents.writeBit = 0

    def parse_define_shape(self, tag):
        ops = []
        fillstyles = {}
        linestyles = {}
        shape = SHAPE2()
        self.lib.swf_ParseDefineShape(tag, byref(shape))

        for i in xrange(shape.numfillstyles):
            fillstyles[i+1] = {
                'color': self.color(shape.fillstyles[i].color),
            }

        for i in xrange(shape.numlinestyles):
            linestyles[i+1] = {
                'color': self.color(shape.linestyles[i].color),
            }

        line = shape.lines
        while line:
            type = line.contents.type
            op = {
                'type': line.contents.type,
                'x': line.contents.x/20.0,
                'y': line.contents.y/20.0,
                'sx': line.contents.sx/20.0,
                'sy': line.contents.sy/20.0,
                'fillstyle0': None,
                'fillstyle1': None,
                'linestyle': None,
            }
            if line.contents.fillstyle0 != 0: op['fillstyle0'] = fillstyles[line.contents.fillstyle0]
            if line.contents.fillstyle1 != 0: op['fillstyle1'] = fillstyles[line.contents.fillstyle1]
            if line.contents.linestyle != 0: op['linestyle'] = linestyles[line.contents.linestyle]

            ops.append(op)
            line = line.contents.next
        return {
            'ops': ops,
            'fillstyles': fillstyles,
            'linestyles': linestyles
        }

    def color(self, rgba):
        return (rgba.r, rgba.g, rgba.b, rgba.a)

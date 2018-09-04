import xml.sax as sax
from xml.sax.saxutils import unescape

from reportlab.platypus.flowables import PageBreak
from reportlab.platypus import Paragraph

caracteres_especiais_dict_convert = {
    '&Aacute;': u'\xc1',
    '&aacute;': u'\xe1',
    '&Acirc;': u'\xc2',
    '&acirc;': u'\xe2',
    '&acute;': u'\xb4',
    '&AElig;': u'\xc6',
    '&aelig;': u'\xe6',
    '&Agrave;': u'\xc0',
    '&agrave;': u'\xe0',
    '&alefsym;': u'\u2135',
    '&Alpha;': u'\u0391',
    '&alpha;': u'\u03b1',
    '&and;': u'\u2227',
    '&ang;': u'\u2220',
    '&Aring;': u'\xc5',
    '&aring;': u'\xe5',
    '&asymp;': u'\u2248',
    '&Atilde;': u'\xc3',
    '&atilde;': u'\xe3',
    '&Auml;': u'\xc4',
    '&auml;': u'\xe4',
    '&bdquo;': u'\u201e',
    '&Beta;': u'\u0392',
    '&beta;': u'\u03b2',
    '&brvbar;': u'\xa6',
    '&bull;': u'\u2022',
    '&cap;': u'\u2229',
    '&Ccedil;': u'\xc7',
    '&ccedil;': u'\xe7',
    '&cedil;': u'\xb8',
    '&cent;': u'\xa2',
    '&Chi;': u'\u03a7',
    '&chi;': u'\u03c7',
    '&circ;': u'\u02c6',
    '&clubs;': u'\u2663',
    '&cong;': u'\u2245',
    '&copy;': u'\xa9',
    '&crarr;': u'\u21b5',
    '&cup;': u'\u222a',
    '&curren;': u'\xa4',
    '&dagger;': u'\u2020',
    '&Dagger;': u'\u2021',
    '&darr;': u'\u2193',
    '&dArr;': u'\u21d3',
    '&deg;': u'\xb0',
    '&delta;': u'\u03b4',
    '&Delta;': u'\u2206',
    '&diams;': u'\u2666',
    '&divide;': u'\xf7',
    '&Eacute;': u'\xc9',
    '&eacute;': u'\xe9',
    '&Ecirc;': u'\xca',
    '&ecirc;': u'\xea',
    '&Egrave;': u'\xc8',
    '&egrave;': u'\xe8',
    '&empty;': u'\u2205',
    '&emsp;': u'\u2003',
    '&ensp;': u'\u2002',
    '&Epsilon;': u'\u0395',
    '&epsilon;': u'\u03b5',
    '&epsiv;': u'\u03b5',
    '&equiv;': u'\u2261',
    '&Eta;': u'\u0397',
    '&eta;': u'\u03b7',
    '&ETH;': u'\xd0',
    '&eth;': u'\xf0',
    '&Euml;': u'\xcb',
    '&euml;': u'\xeb',
    '&euro;': u'\u20ac',
    '&exist;': u'\u2203',
    '&fnof;': u'\u0192',
    '&forall;': u'\u2200',
    '&frac12;': u'\xbd',
    '&frac14;': u'\xbc',
    '&frac34;': u'\xbe',
    '&frasl;': u'\u2044',
    '&Gamma;': u'\u0393',
    '&gamma;': u'\u03b3',
    '&ge;': u'\u2265',
    '&harr;': u'\u2194',
    '&hArr;': u'\u21d4',
    '&hearts;': u'\u2665',
    '&hellip;': u'\u2026',
    '&Iacute;': u'\xcd',
    '&iacute;': u'\xed',
    '&Icirc;': u'\xce',
    '&icirc;': u'\xee',
    '&iexcl;': u'\xa1',
    '&Igrave;': u'\xcc',
    '&igrave;': u'\xec',
    '&image;': u'\u2111',
    '&infin;': u'\u221e',
    '&int;': u'\u222b',
    '&Iota;': u'\u0399',
    '&iota;': u'\u03b9',
    '&iquest;': u'\xbf',
    '&isin;': u'\u2208',
    '&Iuml;': u'\xcf',
    '&iuml;': u'\xef',
    '&Kappa;': u'\u039a',
    '&kappa;': u'\u03ba',
    '&Lambda;': u'\u039b',
    '&lambda;': u'\u03bb',
    '&lang;': u'\u2329',
    '&laquo;': u'\xab',
    '&larr;': u'\u2190',
    '&lArr;': u'\u21d0',
    '&lceil;': u'\uf8ee',
    '&ldquo;': u'\u201c',
    '&le;': u'\u2264',
    '&lfloor;': u'\uf8f0',
    '&lowast;': u'\u2217',
    '&loz;': u'\u25ca',
    '&lrm;': u'\u200e',
    '&lsaquo;': u'\u2039',
    '&lsquo;': u'\u2018',
    '&macr;': u'\xaf',
    '&mdash;': u'\u2014',
    '&micro;': u'\xb5',
    '&middot;': u'\xb7',
    '&minus;': u'\u2212',
    '&mu;': u'\xb5',
    '&Mu;': u'\u039c',
    '&nabla;': u'\u2207',
    '&nbsp;': u'\xa0',
    '&ndash;': u'\u2013',
    '&ne;': u'\u2260',
    '&ni;': u'\u220b',
    '&notin;': u'\u2209',
    '&not;': u'\xac',
    '&nsub;': u'\u2284',
    '&Ntilde;': u'\xd1',
    '&ntilde;': u'\xf1',
    '&Nu;': u'\u039d',
    '&nu;': u'\u03bd',
    '&Oacute;': u'\xd3',
    '&oacute;': u'\xf3',
    '&Ocirc;': u'\xd4',
    '&ocirc;': u'\xf4',
    '&OElig;': u'\u0152',
    '&oelig;': u'\u0153',
    '&Ograve;': u'\xd2',
    '&ograve;': u'\xf2',
    '&oline;': u'\uf8e5',
    '&omega;': u'\u03c9',
    '&Omega;': u'\u2126',
    '&Omicron;': u'\u039f',
    '&omicron;': u'\u03bf',
    '&oplus;': u'\u2295',
    '&ordf;': u'\xaa',
    '&ordm;': u'\xba',
    '&or;': u'\u2228',
    '&Oslash;': u'\xd8',
    '&oslash;': u'\xf8',
    '&Otilde;': u'\xd5',
    '&otilde;': u'\xf5',
    '&otimes;': u'\u2297',
    '&Ouml;': u'\xd6',
    '&ouml;': u'\xf6',
    '&para;': u'\xb6',
    '&part;': u'\u2202',
    '&permil;': u'\u2030',
    '&perp;': u'\u22a5',
    '&phis;': u'\u03c6',
    '&Phi;': u'\u03a6',
    '&phi;': u'\u03d5',
    '&piv;': u'\u03d6',
    '&Pi;': u'\u03a0',
    '&pi;': u'\u03c0',
    '&plusmn;': u'\xb1',
    '&pound;': u'\xa3',
    '&prime;': u'\u2032',
    '&Prime;': u'\u2033',
    '&prod;': u'\u220f',
    '&prop;': u'\u221d',
    '&Psi;': u'\u03a8',
    '&psi;': u'\u03c8',
    '&radic;': u'\u221a',
    '&rang;': u'\u232a',
    '&raquo;': u'\xbb',
    '&rarr;': u'\u2192',
    '&rArr;': u'\u21d2',
    '&rceil;': u'\uf8f9',
    '&rdquo;': u'\u201d',
    '&real;': u'\u211c',
    '&reg;': u'\xae',
    '&rfloor;': u'\uf8fb',
    '&Rho;': u'\u03a1',
    '&rho;': u'\u03c1',
    '&rlm;': u'\u200f',
    '&rsaquo;': u'\u203a',
    '&rsquo;': u'\u2019',
    '&sbquo;': u'\u201a',
    '&Scaron;': u'\u0160',
    '&scaron;': u'\u0161',
    '&sdot;': u'\u22c5',
    '&sect;': u'\xa7',
    '&shy;': u'\xad',
    '&sigmaf;': u'\u03c2',
    '&sigmav;': u'\u03c2',
    '&Sigma;': u'\u03a3',
    '&sigma;': u'\u03c3',
    '&sim;': u'\u223c',
    '&spades;': u'\u2660',
    '&sube;': u'\u2286',
    '&sub;': u'\u2282',
    '&sum;': u'\u2211',
    '&sup1;': u'\xb9',
    '&sup2;': u'\xb2',
    '&sup3;': u'\xb3',
    '&supe;': u'\u2287',
    '&sup;': u'\u2283',
    '&szlig;': u'\xdf',
    '&Tau;': u'\u03a4',
    '&tau;': u'\u03c4',
    '&there4;': u'\u2234',
    '&thetasym;': u'\u03d1',
    '&thetav;': u'\u03d1',
    '&Theta;': u'\u0398',
    '&theta;': u'\u03b8',
    '&thinsp;': u'\u2009',
    '&THORN;': u'\xde',
    '&thorn;': u'\xfe',
    '&tilde;': u'\u02dc',
    '&times;': u'\xd7',
    '&trade;': u'\uf8ea',
    '&Uacute;': u'\xda',
    '&uacute;': u'\xfa',
    '&uarr;': u'\u2191',
    '&uArr;': u'\u21d1',
    '&Ucirc;': u'\xdb',
    '&ucirc;': u'\xfb',
    '&Ugrave;': u'\xd9',
    '&ugrave;': u'\xf9',
    '&uml;': u'\xa8',
    '&upsih;': u'\u03d2',
    '&Upsilon;': u'\u03a5',
    '&upsilon;': u'\u03c5',
    '&Uuml;': u'\xdc',
    '&uuml;': u'\xfc',
    '&weierp;': u'\u2118',
    '&Xi;': u'\u039e',
    '&xi;': u'\u03be',
    '&Yacute;': u'\xdd',
    '&yacute;': u'\xfd',
    '&yen;': u'\xa5',
    '&yuml;': u'\xff',
    '&Yuml;': u'\u0178',
    '&Zeta;': u'\u0396',
    '&zeta;': u'\u03b6',
    '&zwj;': u'\u200d',
    '&zwnj;': u'\u200c',
}

# I place this in the public domain

# This only handles non-nested lists, emphasis, headings and horizontal rules (which are converted to page breaks)
# Sufficient for converting Markdown generated HTML to reportlab flowables...
def html_to_rl(html, styleSheet):
    elements = list()

    class Handler(sax.ContentHandler):
        mode = ""
        buffer = ""
        listcounter = 0
        listtype = ""

        def startElement(self, name, attrs):
            if name in ["strong", "em", "i", "b", "u"]:
                self.mode = name
            elif name == "ol":
                self.listcounter = 1
                self.listtype = "ol"
            elif name == "ul":
                self.listtype = "ul"
            elif name == "hr":
                elements.append(PageBreak())

        def endElement(self, name):
            if name.startswith("h") and name[-1] in ["1", "2", "3", "4", "5", "6"]:
                elements.append(Paragraph(self.buffer, styleSheet["Heading%s" % name[-1]]))
            elif name in ["strong", "em", "i", "b", "u"]:
                self.mode = ""
            elif name == "p":
                elements.append(Paragraph(self.buffer, styleSheet["Normal"]))
            elif name == "li":
                if self.listtype == "ul":
                    elements.append(Paragraph(self.buffer, styleSheet["Normal"], bulletText=u"•"))
                else:
                    elements.append(Paragraph(self.buffer, styleSheet["Normal"], bulletText="%s." % self.listcounter))
                    self.listcounter += 1
            elif name in ["ol", "ul"]:
                self.listcounter = 0
                self.listtype = ""

            if name in ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li"]:
                self.buffer = ""

        def characters(self, chars):
            surrounding = None

            if self.mode in ["strong", "em", "i", "b", "u"]:
                if self.mode in ["strong", "b"]:
                    surrounding = "b"
                elif self.mode == "u":
                    surrounding = "u"
                else:
                    surrounding = "i"

            if surrounding:
                chars = u"<%s>%s</%s>" % (surrounding, chars, surrounding)

            self.buffer += chars

    # Yeah I know... this makes Jesus cry, but unfortunately SAX wants a document element
    # surrounding everything
    html = unescape(html.replace('<br>', '&nbsp;<br />'), caracteres_especiais_dict_convert)
    sax.parseString(u"<doc><p>%s</p></doc>" % html, Handler())

    return elements
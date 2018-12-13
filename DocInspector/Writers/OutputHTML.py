from yattag import Doc

from DocInspector.Writers.HtmlTemplate import *


def outputHTML(stats: DocStats):
    doc, tag, text = Doc().tagtext()
    doc = getHeaderTemplate(doc, stats)
    with tag("body"):
        with tag("div", klass="stats"):
            doc = getGeneralStats(doc, stats)
            doc = getIndividualStats(doc, stats)
        doc = getTimelineStats(doc, stats)
    return doc.getvalue()

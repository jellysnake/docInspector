from datetime import datetime, timezone
from math import ceil

from DocInspector.DocStats import DocStats


def getHeaderTemplate(doc, stats: DocStats):
    doc, tag, text, line = doc.ttl()
    with tag("head"):
        line("title", stats.general.name)
        with tag("style"):
            doc.asis("* {"
                     "  box-sizing: border-box;"
                     "}")
            doc.asis("body {"
                     " background-color: #474e5d;"
                     " font-family: Helvetica, sans-serif;"
                     "}")
            # Stats
            doc.asis(".stats {"
                     "  position: fixed;"
                     "  left: 20px;"
                     "  width: 61%;"
                     "}")

            # Container for each stat
            doc.asis(".stat_container {"
                     "  padding: 10px 0px 10px 0px;"
                     "  position: relative;"
                     "  background-color: inherit;"
                     "  width: 100%;"
                     "}")

            # Content for each stat
            doc.asis(".stat_content {"
                     "  padding: 20px 30px;"
                     "  background-color: white;"
                     "  position: relative;"
                     "  border-radius: 6px;"
                     "}")

            # td element in Stats container
            doc.asis("table.general_stats_table td {"
                     "  padding: 0px 20px 10px 0px;"
                     "  word-break: break-word;"
                     "}")

            # The timeline container
            doc.asis(".timeline {"
                     "  position: absolute;"
                     "  right: 10px;"
                     "  width: 40%;"
                     "  margin: 0 auto;"
                     "}")
            # The actual timeline (the vertical ruler)
            doc.asis(".timeline::after {"
                     "  content: '';"
                     "  position: absolute;"
                     "  width: 6px;"
                     "  background-color: white;"
                     "  top: -10px;"
                     "  bottom: -1px;"
                     "  right: 4.8%;"
                     "}")
            # Add arrows to the left container (pointing right)
            doc.asis(".container::before {"
                     "  content: " ";"
                     "  height: 0;"
                     "  position: absolute;"
                     "  top: 22px;"
                     "  width: 0;"
                     "  z-index: 1;"
                     "  right: 30px;"
                     "  border: medium solid white;"
                     "  border-width: 10px 0 10px 10px;"
                     "  border-color: transparent transparent transparent white;"
                     "}")
            # Container around content
            doc.asis(".container {"
                     "  padding: 10px 40px;"
                     "  position: relative;"
                     "  background-color: inherit;"
                     "  width: 90%;"
                     "  right: -4.7%;"
                     "}")
            # The circles on the timeline
            doc.asis(".container::after {"
                     "  content: '';"
                     "  position: absolute;"
                     "  width: 25px;"
                     "  height: 25px;"
                     "  right: -17px;"
                     "  background-color: white;"
                     "  border: 4px solid #FF9F55;"
                     "  top: 15px;"
                     "  border-radius: 50%;"
                     "  z-index: 1;"
                     "}")
            # The actual content
            doc.asis(".content {"
                     "  padding: 20px 30px;"
                     "  background-color: white;"
                     "  position: relative;"
                     "  border-radius: 6px;"
                     "}")
            # Span that shows additions
            doc.asis(".add_span {"
                     "  background-color: #0017ffa3;"
                     "  float: right;"
                     "}")
            # Span that shows removals
            doc.asis(".rem_span {"
                     "  background-color: #fc4349d9;"
                     "  float: left;"
                     "}")
    return doc


def getGeneralStats(doc, stats: DocStats):
    doc, tag, text, line = doc.ttl()
    # Doc name
    with tag("div", klass="stat_container"):
        line("div", stats.general.name, klass="stat_content")

    # General Stat Info
    with tag("div", klass="stat_container"):
        with tag("div", klass="stat_content"):
            line("h2", "General Stats")
            with tag("table", klass="general_stats_table"):
                # File Id
                with tag("tr"):
                    with tag("td"):
                        line("b", 'ID:')
                    line("td", stats.general.id)

                # File date
                with tag("tr"):
                    with tag("td"):
                        line("b", 'Creation Date:')
                    creation_date = datetime \
                        .strptime(stats.general.creationDate, "%Y-%m-%dT%H:%M:%S.%fZ") \
                        .replace(tzinfo=timezone.utc) \
                        .astimezone(tz=None) \
                        .strftime('%d/%m/%Y - %I:%M:%S %p')
                    line("td", creation_date)

                # File URL
                with tag("tr"):
                    with tag("td"):
                        line("b", 'Link:')
                    line("tr", f"https://docs.google.com/document/d/{stats.general.id}/view")
    return doc


def getIndividualStats(doc, stats: DocStats):
    doc, tag, text, line = doc.ttl()
    with tag("div", klass="stat_content"):
        line("h2", "Individual Stats")
        with tag("table", "style", style="width: 100%;"):
            # Make Chart Divs
            with tag("tr"):
                with tag("td", align="center", width="50%;"):
                    line("div", "", id="additions_chart")
                with tag("td", align="center", width="50%;"):
                    line("div", "", id="removals_chart")
                with tag("td", "", align="center", colspan="2"):
                    line("div", "", id="percent_chart")

            # Make javadoc for charts
            doc.stag("script", type="text/javascript", src="https://www.gstatic.com/charts/loader.js")
            doc = getChartScript("additions", doc, stats)
            doc = getChartScript("removals", doc, stats)
            doc = getChartScript("percent", doc, stats)
    return doc


def getChartScript(attribute: str, doc, stats: DocStats):
    doc, tag, text, line = doc.ttl()
    # Additions Chart
    with tag("script", type="text/javascript"):
        editorLines = []
        for i in stats.individuals.getEditors():
            editor = stats.individuals.getEditor(i)
            editorLines.append(f"['{editor.name}', {editor.__getattribute__(attribute) or 0}],")
        editorLines = "\n".join(editorLines)
        doc.asis(f"""
                google.charts.load('current', {{'packages': ['corechart']}});
                google.charts.setOnLoadCallback(drawChart);
                
                function drawChart() {{
                    var data = google.visualization.arrayToDataTable([
                        ['Editor', '{attribute.title()}'],
                        {editorLines}
                        ]);
                    var options = {{
                        title: '{attribute.title()}',
                        titleTextStyle: {{'fontSize': 20}},
                        width: 500,
                        height: 200,
                        pieHole: 0.4
                    }};
                    var chart = new google.visualization.PieChart(document.getElementById('additions_chart'));
                    chart.draw(data, options);
                }}
                """)
    return doc


def getTimelineStats(doc, stats: DocStats):
    doc, tag, text, line = doc.ttl()
    start_time = stats.timeline.timelineStart

    with tag("div", klass="timeline"):
        for i in range(stats.timeline.getNumIncrements()):
            increment = stats.timeline.getIncrement(i)
            if len(increment.editors) == 0:
                continue
            dt = start_time + (i * stats.timeline.incrementSize)
            with tag("div", klass="container"):
                with tag("div", klass="content"):
                    line("h2", datetime.fromtimestamp(dt / 1000)
                         .replace(tzinfo=timezone.utc)
                         .astimezone(tz=None)
                         .strftime('%d/%m/%Y - %I:%M:%S %p'))
                    with tag("table", width="100%", cellpadding="0"):
                        for editorId in increment.getEditors():
                            doc = getEditorEntry(doc, increment, editorId)
    return doc


def getEditorEntry(doc, increment, editorId):
    doc, tag, text, line = doc.ttl()
    editor = increment.getEditor(editorId)
    adds_percent = ceil(((editor.additions / increment.total.additions) * 100)
                        if increment.total.additions
                        else 0)
    rems_percent = ceil(((editor.removals / increment.total.removals) * 100)
                        if increment.total.removals
                        else 0)
    with tag("tr"):
        line("td", editor.name, width="80%")
        line("td", editor.additions or 0, align="right")
        with tag("td", width="10%", align="right"):
            line("span", "", klass="add_span", style=f"width:{adds_percent}%;")
        with tag("td", width="10%", align="left"):
            line("span", "", klass="rem_span", style=f"width:{rems_percent}%;")
        line("td", editor.removals or 0, align="right")
    return doc

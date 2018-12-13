from datetime import datetime, timezone

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
    return doc


def getGeneralStats(doc, stats: DocStats):
    doc, tag, text, line = doc.ttl()
    # Doc name
    with tag("div", klass="stat_container"):
        with tag("div", klass="stat_content"):
            line("h1", stats.general.name)

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
                    with tag("td"):
                        line("a", f"https://docs.google.com/document/d/{stats.general.id}/view",
                             href=f"https://docs.google.com/document/d/{stats.general.id}/view")
    return doc


def getIndividualStats(doc, stats: DocStats):
    doc, tag, text, line = doc.ttl()
    with tag("div", klass="stat_container"):
        with tag("div", klass="stat_content"):
            line("h2", "Individual Stats")
            with tag("table", "style", style="width: 100%;"):
                # Make Chart Divs
                with tag("tr"):
                    with tag("td", align="center", width="50%;"):
                        line("div", "", id="additions_chart")
                    with tag("td", align="center", width="50%;"):
                        line("div", "", id="removals_chart")
                with tag("tr"):
                    with tag("td", "", align="center", colspan="2"):
                        line("div", "", id="percent_chart")

                # Make javadoc for charts
                line("script", "", type="text/javascript", src="https://www.gstatic.com/charts/loader.js")

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
                    var chart = new google.visualization.PieChart(document.getElementById('{attribute}_chart'));
                    chart.draw(data, options);
                }}
                """)
    return doc


def getTimelineStats(doc, stats: DocStats):
    doc, tag, text, line = doc.ttl()
    time = stats.timeline.timelineStart
    editors = stats.individuals.getEditors()
    total = 0

    with tag("div", klass="timeline", id="timeline_div"):
        incrementLines = []
        for increment in stats.timeline.increments:
            row = f"[new Date({time}), {str(total)}"
            time += stats.timeline.incrementSize
            if increment.editors:
                for editor in editors:
                    if editor in increment.editors:
                        row += "," + str(increment.getEditor(editor).additions or 0)
                    else:
                        row += ",0 "
                for editor in editors:
                    if editor in increment.editors:
                        row += "," + str(-1 * increment.getEditor(editor).removals or 0)
                    else:
                        row += ",0 "
            else:
                row += ",0" * len(editors) * 2
            total += (increment.total.additions or 0) - (increment.total.removals or 0)
            incrementLines.append(row + "],")

        editorNames = ", ".join([f"'{stats.individuals.getEditor(editorId).name}'" for editorId in editors])
        incrementLines = "\n".join(incrementLines)
        with tag("script", type="text/javascript"):
            doc.asis(f"""google.charts.load("current", {{packages: ["corechart"]}});
                google.charts.setOnLoadCallback(drawChart);
    
                function drawChart() {{
                    var data = google.visualization.arrayToDataTable([
                        ['Date', "Total Count", {editorNames + "," + editorNames}],
                        {incrementLines}
                        ]);
                    var options = {{
                        title: "Changes",
                        colors: ['grey', 'red', 'green', 'blue', 'pink', 'red', 'green', 'blue', 'pink'],
                        vAxis: {{title: 'Date', direction: -1}},
                        hAxis: {{title: "Characters Edited"}},
                        isStacked: true,
                        animation: {{startup: true, duration: 700}},
                        orientation: "vertical",
                        series:{{ 0: {{type: 'steppedArea'}}}},
                        height: 25 * {len(stats.timeline.increments)},
                        seriesType: 'bars',
                        explorer: {{keepInBounds: true, axis: "horizontal"}}
                    }};
            
                    var chart = new google.visualization.ComboChart(document.getElementById("timeline_div"));
                    chart.draw(data, options);
                }}""")
    return doc

from datetime import datetime, timezone
from os import path

from DocInspector.DocStats import DocStats

folder = path.dirname(__file__) + "/templates/"


def getHeaderTemplate(doc, stats: DocStats):
    doc, tag, text, line = doc.ttl()
    with tag("head"):
        line("title", stats.general.name)
        with tag("style"):
            with open(path.abspath(folder + "style.css"), 'r') as file:
                doc.asis(file.read())
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

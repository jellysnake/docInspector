function makeTimeline(editorNames, incrementLines, incrementCount) {
    google.charts.load("current", {packages: ["corechart"]});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = google.visualization.arrayToDataTable([
            ['Date', "Total Count"].concat(editorNames).concat(editorNames)]
            .concat(incrementLines));
        var options = {
            title: "Changes",
            vAxis: {title: 'Date', direction: -1},
            hAxis: {title: "Characters Edited"},
            isStacked: true,
            animation: {startup: true, duration: 700},
            orientation: "vertical",
            series: {0: {type: 'steppedArea'}},
            height: 25 * incrementCount,
            seriesType: 'bars',
            explorer: {keepInBounds: true, axis: "horizontal"}
        };

        var chart = new google.visualization.ComboChart(document.getElementById("timeline_div"));
        chart.draw(data, options);
    }
}
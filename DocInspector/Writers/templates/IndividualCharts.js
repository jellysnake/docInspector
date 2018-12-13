function getIndividualChart(name, lines) {
    google.charts.load('current', {'packages': ['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = google.visualization.arrayToDataTable([
            ['Editor', name]].concat(lines));
        var options = {
            title: name,
            titleTextStyle: {'fontSize': 20},
            pieHole: 0.4
        };
        var chart = new google.visualization.PieChart(document.getElementById(name.toLowerCase() + "_chart"));
        chart.draw(data, options);
    }

}
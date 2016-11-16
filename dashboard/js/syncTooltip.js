var charts = [],
    options;
function syncTooltip(container, p) {
    var i = 0;
    for (; i < charts.length; i++) {
        if (container.id != charts[i].container.id) {
            if(charts[i].tooltip.shared) {
                charts[i].tooltip.refresh([charts[i].series[0].data[p]]);
            }
            else {
                charts[i].tooltip.refresh(charts[i].series[0].data[p]);
            }
        }
    }
}


options = {
    plotOptions: {
        series: {
            point: {
                events: {
                    mouseOver: function () {
                        syncTooltip(this.series.chart.container, this.x - 1);
                    }
                }
            }
        }
    },
    xAxis: {
        type: 'datetime'
    }
};

charts[0] = new Highcharts.Chart($.extend(true, {}, options, {
    chart: {
        renderTo: 'container1'
    },
    tooltip: {
        shared: true,
        crosshairs: true,
        valueDecimals: 2
    },
    series: [{
        data: [
            [1, 29.9],
            [2, 71.5],
            [3, 106.4]
        ]
    }, {
        data: [
            [1, 59.9],
            [2, 91.5],
            [3, 136.4]
        ]
    }]
}));


charts[1] = new Highcharts.Chart($.extend(true, {}, options, {
    chart: {
        renderTo: 'container2'
    },
    tooltip: {
        shared: false
    },
    series: [{
        data: [
            [1, 29.9],
            [2, 71.5],
            [3, 106.4]
        ]
    }]
}));

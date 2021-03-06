function addtocartAPIfull(campaign){
    $.get('http://54.213.146.237:5000/2501_addtocart/'+campaign,function(data){
    //$.get('http://54.213.146.237/dashboard/json/addtocart_pbuy_'+campaign+'.json',function(data){
    var d3Colors = d3.scale.linear().domain([-1,0,1,5,10,30,50,100]).range(['#000000','#8F00FF','#4B0082','#0000FF','#00FF00','#FFFF00','#FF7F00','#FF0000']);  
    var browsers = data.map(function(d){
        return {x:d.x,y:d.y,name:d.name,AD:d.AD,color:d3Colors(d.AD)};
        // return {x:d.x,y:d.y,name:d.name,AD:d.AD,color:d3Colors(Math.log10(d.AD))};
        //return {x:d.x,y:d.y,name:d.name,AD:d.AD,color:d3.rgb(0,0,255*(Math.log10(d.AD)))};
        // return {x:d.x,y:d.y,name:d.name,AD:d.AD,color:d3.rgb(255,255,255)};
    });
    console.log(browsers);
    $('#addtocart_buy').highcharts({
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: '產品被購買次數 v.s. 產品被加入購物車數目'
        },
        xAxis: {
            title: {
                // enabled: true,
        		style:{
        		   fontSize: '18px'
        		},
                text: '加入購物車數目'
            },
            min:1,
    	    labels:{
        		style:{
        		   fontSize: '14px'
        		}
    	    },
            type: 'logarithmic',
            minorTickInterval: 0.1,
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
        		style:{
        		   fontSize: '18px'
        		},
                text: '產品被購買數目'
            },
            min:1.0,
    	    labels:{
        		style:{
        		   fontSize: '14px'
        		}
    	    },
            type: 'logarithmic',
            minorTickInterval: 0.1
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
            borderWidth: 1
        },
        tooltip: {
            formatter: function(){
                // console.log(this);
                return this.point.name+' </b><br> 購物車'+this.point.x+'次, 購買'+this.point.y+'次,'+this.point.AD+'廣告clicks'
            }
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 4,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                }
            }
        },
        series: [{
            colorByPoint:true,
            name: campaign,
            // color: 'rgba(83, 83, 223, .8)',
            data : browsers
        }]
    });
    });
}
function addtocartAPI(campaign){
    $.get('http://54.213.146.237:5000/2501_addtocart/'+campaign,function(data){
    //$.get('http://54.213.146.237/dashboard/json/addtocart_pbuy_'+campaign+'.json',function(data){
    var d3Colors = d3.scale.linear().domain([-1,0,1,5,10,30,50,100]).range(['#000000','#8F00FF','#4B0082','#0000FF','#00FF00','#FFFF00','#FF7F00','#FF0000']);  
    var browsers = data.map(function(d){
        return {x:d.x,y:d.y,name:d.name,AD:d.AD,color:d3Colors(d.AD)};
    });
    console.log(browsers);
    $('#addtocart_buy').highcharts({
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: '產品被購買次數 v.s. 產品被加入購物車數目'
        },
        xAxis: {
            title: {
                // enabled: true,
                style:{
                   fontSize: '18px'
                },
                text: '加入購物車數目'
            },
            min:1,
            labels:{
                style:{
                   fontSize: '14px'
                }
            },
            type: 'logarithmic',
            minorTickInterval: 0.1,
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                style:{
                   fontSize: '18px'
                },
                text: '產品被購買數目'
            },
            min:1.0,
            labels:{
                style:{
                   fontSize: '14px'
                }
            },
            type: 'logarithmic',
            minorTickInterval: 0.1
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
            borderWidth: 1
        },
        tooltip: {
            formatter: function(){
                // console.log(this);
                // return this.point.name+' </b><br> 購物車'+this.point.x+'次, 購買'+this.point.y+'次,'+this.point.AD+'廣告clicks'
                return this.point.name+' </b><br> 購物車'+this.point.x+'次, 購買'+this.point.y+'次'
            }
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 6,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                }
            }
        },
        series: [{
            colorByPoint:true,
            name: campaign,
            // color: 'rgba(83, 83, 223, .8)',
            data : browsers
        }]
    });
    });
}
$('li a').on('click',function(d){
    var campaign = $(this).attr('type');
    if(campaign=='full'){
        addtocartAPIfull(campaign);
    }else{
        addtocartAPI(campaign);
    }
    
    console.log(campaign);
});

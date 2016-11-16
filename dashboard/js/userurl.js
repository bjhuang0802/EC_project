$(document).ready(function () {
    $.ajaxSetup({
	    timeout: 120000
    });
    //$.get('http://54.213.146.237/test',function(data){
    $.get('http://54.213.146.237:5000/2501_userurl',function(data){
	    $('#userurl').DataTable({
	    fixedHeader: {
	    header: true
	    },
	   data: data,
	   "order": [[2,"desc" ]],
	   "lengthMenu": [[250, 500, 750, -1], [250, 500, 750, "All"]],
	   "columns": [
	           {"data":"fid"},
	           { "data": "event" }, 
	           { "data": "time",'width':'30%'},
	           { "data": "url" },
	           { "data": "campaign" }
	   ],
	   'fnCreatedRow':function(row,data,index){
	   	// if(index==0)
	   	// 	console.log(data);
	   	if(data.event=='ViewContent')
   		{
   			$(row).css('background-color','#FDF5C9');
   		}
   		else if(data.event=='AddToCart')
   		{
   			$(row).css('background-color','pink');
   		}
   		else if(data.event=='Checkout')
   		{
   			$(row).css('background-color','#FA8072');
   		}
   		else if(data.event=='Payment')
   		{
   			$(row).css('background-color','#FF80BF')
   		}
   		else if(data.event=='Purchase')
   		{
   			// $(row).css('background-color','#FF3399');
   			$(row).css('background-color','red');
   		}

	   },
	    // columnDefs:[{width:200, targets:0}],
	   fixedColumns:false
	   });
	   // $("tr:contains('AddToCart')").css("background-color","pink");
	   // $("tr:contains('Purchase')").css("background-color","red");
	   // $("tr:contains('ViewContent')").css("background-color","yellow");
    });
});

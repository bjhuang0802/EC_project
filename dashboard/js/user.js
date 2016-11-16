$(document).ready(function () {

    $.get('http://54.213.146.237:5000/2501_user',function(data){
	    $('#user').DataTable({
	    fixedHeader: {
	    header: true
	    },
	   data: data,
	   "order": [[2,"asc"],[ 20,"desc" ]],
	   "lengthMenu": [[50, 100, 750, -1], [50, 100, 200, "All"]],
	   "columns": [
	           // { "data": "fid",'render':function(d){return d.substring(0,8)}},
	           // { "data": "member" },
	           {"data":"fid"},
	           { "data": "AD_clicks" },
	           { "data": "buys" },
	           { "data": "Cart1" },
	           { "data": "Cart2" },
	           { "data": "Cart3" },
	           { "data": "Cart4" },
	           { "data": "Cart5" },
	           { "data": "session1" },
	           { "data": "session2" },
	           { "data": "session3" },
	           { "data": "session4" },
	           { "data": "session5" },
	           { "data": "T_pv1" },
	           { "data": "T_pv2" },
	           { "data": "T_pv3" },
	           { "data": "T_pv4" },
	           { "data": "T_pv5" },
	           { "data": "buy_YN" },
	           { "data": "SVC" },
	           { "data": "Kscore" }
	   ],
	   'fnCreatedRow':function(row,data,index){
	   	// if(index==0)
	   	// 	console.log(data);
	   		if(data.buys==0 && data.Kscore>0.4)
	   		{
	   			$(row).css('background-color','#ebb73d');
	   		}
			if(data.buy_YN=='2')
	   		{
	   			$(row).css('background-color','#ffbfdf');
	   		}
	   		if(data.buys==0 && data.Kscore>0.4 && data.buy_YN=='2')
			{
	   			$(row).css('background-color','#c597f4');
			}
		   },
		   fixedColumns:false
	    });
	});
});

$(document).ready(function(){
	
	$(".package_counters").hide();
	$(".package_counters").eq(0).show();
	
	console.log($(".package_counters").length);
	
	
});


/********************************************************
// Packages Counters
********************************************************/

function package_counters(elem){
	
	$(".package_counters").hide();
	
	id = $(elem).attr("id");
	id = id.replace("id_package_counter_", "id_package_");
		
	$("#"+id).show();
	
}
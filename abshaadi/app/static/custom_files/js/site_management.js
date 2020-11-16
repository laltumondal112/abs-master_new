$(document).ready(function(){});


//
//
//

function start_religion_auto_renew(){
	
	var r = confirm("This operation will remove previous enteries and re-insert all the religions and castes from initial file. Do you want to continue");
	if (r == true) {
		$("#data_process_modal").modal('show');
	
		$.get("/load_religions_into_db/", function(data){
			if(data == 1){
				location.reload();
			}
		});
	} 	
}


//
//
//

function validate_add_religion_form(elem){
	
	$.post("/add_religion/", $(elem).serialize(), function(data){
		
		data = $.parseJSON(data);
		
		if(data["code"] == 1){
			location.reload();			
		}
		else{
			if(data["error"].length == 0) $(elem).find(".modal-body >  .error-div").empty().append(data["error"]);
			else{				
				$(elem).find(".modal-body >  .error-div").empty().append(data["error"]["religion_name"][0]);
				$(elem).find(".modal-body >  .error-div").show();
			}
		}		
	});
	
	return false;
}


//
//
//

function validate_add_caste_form(elem){
	$.post("/add_caste/", $(elem).serialize(), function(data){
		
		data = $.parseJSON(data);
		
		if(data["code"] == 1){
			location.reload();			
		}
		else{
			if(data["error"].length == 0) $(elem).find(".modal-body >  .error-div").empty().append(data["error"]);
			else{				
				$(elem).find(".modal-body >  .error-div").empty().append(data["error"]["caste_name"][0]);
				$(elem).find(".modal-body >  .error-div").show();
			}
		}		
	});
	
	return false;
}


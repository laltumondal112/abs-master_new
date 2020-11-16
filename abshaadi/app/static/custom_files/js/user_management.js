$(document).ready(function(){

});


function delete_user(id){
	$("#data_process_modal").modal('show');
	
	$.get('/staff/user_management/users/delete/'+id+'/', function(data){
		if(data == 1){
			localtion.reload();
		}else{
			$("#data_process_modal").modal('hide');	
			if(data == 0){
				alert("Invalid operation");
			}
			if(data == 2){
				alert("User not Found, Contact Administrator");
			}
		}
	});
}

function add_staff(){
	$("#data_process_modal").modal('show');
	
	$.post("/staff/user_management/staff/add/", $("#add_staff_form").serialize(), function(){
		if(data==1){
			location.reload();
		}
		else if(data==0){
			$("#data_process_modal").modal('hide');	
			alert("In Valid Operation");
		}
		else{
			$("#data_process_modal").modal('hide');	
			$("#error_modal").find(".modal-body").empty().append(data);
			$("#error_modal").modal('show');	
		}
	});
}
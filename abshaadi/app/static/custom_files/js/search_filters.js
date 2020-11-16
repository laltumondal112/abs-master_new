$(document).ready(function(){
	
	//*******************************************************************************
	// SET CLASS
	//*******************************************************************************
	
	$("select").addClass("form-control");
	$("input").addClass("form-control");
	
	//*******************************************************************************
	// AGE SLIDER
	//*******************************************************************************
	
	age_to = document.getElementById('id_aged_from');
	age_from = document.getElementById('id_aged_to');
	
	var inputs = [age_to, age_from];
	
	if(age_to.value == '') age_to_val = 25;
	else age_to_val = age_to.value;
	
	if(age_from.value == '') age_from_val = 18;
	else age_from_val = age_from.value;
	
	var stepsSlider  = document.getElementById('age_slider');
	
	noUiSlider.create(stepsSlider , {
		start: [age_from_val, age_to_val],
		connect: true,
		step: 1,
		range: {
			'min': 18,
			'max': 70
		},
		tooltips: [true, wNumb({decimals: false,})],
		format : wNumb({decimals: false,}),
	});
	
	stepsSlider.noUiSlider.on('update', function (values, handle) {
		inputs[handle].value = values[handle];
	});
	
	//*******************************************************************************
	//*******************************************************************************
	
	
	$("textarea#word_count").on('keyup', function() {
		
		var mlen = $(this).val().length;
		
		if(mlen <= 250){
			$("#display_count").empty().text(250 - mlen);
		}else{
			alert("Maximum reached");
		}
	});
	
});



//*******************************************************************************
// Connect/Message Modal
//*******************************************************************************

function open_connect_modal(to_id){
	$("#connect_modal_form").modal('show');
	$("#to_user_id").val(to_id);
}


function connect_modal_form_cancel(){
	$("#display_count").empty().text(250);
	$("#connect_modal_form").modal('hide');
}

function on_connect_save(){
	
	if($.trim($("textarea#word_count").val()).length == 0){
		alert('Cannot')
	}else{
		formdata = $("#connect_save_form").serialize();
		
		$.post("/connect_msg_save/", formdata, function(data){
			
		});
	}
}


function profile_like(to_user){
	$.get("/profile_like/"+to_user+"/", function(data){});
}
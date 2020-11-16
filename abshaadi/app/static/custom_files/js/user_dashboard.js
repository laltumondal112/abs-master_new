$(document).ready(function(){

    
	
	//
	//***********************************************************************************
    // Start upload preview image
    //***********************************************************************************
	
	$(".gambar").attr("src", "https://user.gadjian.com/static/images/personnel_boy.png");
	
	var $uploadCrop,
	tempFilename,
	rawImg,
	imageId;
	
	$uploadCrop = $('#upload-demo').croppie({
		viewport: {
			width: 150,
			height: 150,
		},
		enforceBoundary: false,
		enableExif: true
	});
	
	
	function readFile(input) {
		if (input.files && input.files[0]) {
		  var reader = new FileReader();
			reader.onload = function (e) {
				$('#upload-demo').show();
				rawImg = e.target.result;
				
				$uploadCrop.croppie('bind', {
					url: rawImg
				}).then(function(){
					console.log('jQuery bind complete');
				});	
			}
			reader.readAsDataURL(input.files[0]);
		}
		else {
			swal("Sorry - you're browser doesn't support the FileReader API");
		}
	}

	//
	//
	
	$('.item-img').on('change', function () { 
		imageId = $(this).data('id'); 
		tempFilename = $(this).val();
		$('#cancelCropBtn').data('id', imageId); 
		readFile(this); 
		
		$("#cropImageBtn, #cropImageSubmitBtn").show();
	});
	
	
	//
	//
	
	$('#cropImageBtn').on('click', function (ev) {
		$uploadCrop.croppie('result', {
			type: 'base64',
			format: 'png',
			size: {width: 150, height: 200}
		}).then(function (resp) {
			$('#item-img-output').attr('src', resp);
		});
	});
	
	//
	//
	
	$('#cropImageSubmitBtn').on('click', function (ev) {
				
		$("#file_uploading_loader_modal").modal('show');
		
		$uploadCrop.croppie('result', {
			type: 'base64',
			format: 'png',
			size: {width: 170, height: 200}
		}).then(function (resp) {
			
			var block = resp.split(";");
			var contentType = block[0].split(":")[1];
			var realData = block[1].split(",")[1];
			
			var blob = b64toBlob(realData, contentType);
			
			var form = document.getElementById("upload_profile_pic_form");
			
			var formDataToUpload = new FormData(form);
			formDataToUpload.append("picture", blob);
			formDataToUpload.append("csrfmiddlewaretoken", csrfmiddlewaretoken);
			
			
			$.ajax({
				url:"/upload_profile_pic/",
				data: formDataToUpload,
				type:"POST",
				contentType:false,
				processData:false,
				cache:false,
				error:function(err){
					console.error(err);
				},
				success:function(data){
					console.log(data);
				},
				complete:function(){
					location.reload();
				}
			});
			
			
		});	
			
	});
	
	
	//
	//
	
	$('#cancelCropBtn').on('click', function (ev){
		console.log('hhh')
		$("#profile_picture_modal").modal('hide');
	});
	
		
	//
	//
	$("#profile_picture_modal").on('hidden.bs.modal', function (e) {
		
		$('.item-img').val('');
		$('#upload-demo').hide();
		$(".gambar").attr("src", "https://user.gadjian.com/static/images/personnel_boy.png");
	});


});
function showPassword() {
	              
	var pd = document.getElementById('pd');
	var check = document.getElementById('check');
	var otra = pd.type;

	if(check.checked) {
	      
	    pd.type='text';
	      
	} else {
	      
	    pd.type='password';
	      
	}   

}

function validarIngreso(){
	var usu = document.getElementById('us');
	var pd = document.getElementById('pd');

}
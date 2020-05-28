<html>
<head>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
 integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<body style="background:url('images/homepage4.jpg') no-repeat center fixed; background-size:100%;">
<div style="background-color:#e60000;color:#ffffff;height:100px"></br><h1 class="display-5"><p class="text-center">Times of India Text to Speech</p></h1></div>
<div  class="container-fluid" style="height:75px">
</div>
</br>
<div class="container-fluid">
<div class="row">
<div class="col">
	</div>
	<div class ="col-7">
		<div class="card">
			<div class="card-body" style="background-color:#e60000;color:#ffffff; ">
			<h5> Generated Audios </h5>
			</div>
			<div class="card-body">
			<table class="table table-striped">
				<thead>
					<tr>
						<th scope="col"></th>					  <!-- Serial No.-->
						<th scope="col">Author's Name</th>		
						<th scope="col">Article Published</th>
					</tr>
				</thead>
				<tbody>
				{%for i in info%}									<!-- Loop yaha se.-->
				<tr>	
						<td> {{i}}</td>								<!-- Serial No.1,2,3 etc  -->
						<td> {{ i.author }} </td>
						<td> {{ i.doc }} </td>
				{%endfor%}
				</tr>
				</tbody>
			</table>	
			</div>
		</div>
		</div>
		<div class="col">
		</div>
</div>
</div>







<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" 
integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>



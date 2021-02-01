var database = [{
	username: 'Tammy',
	password: 123
},
{
	username: 'Sally',
	password: 456
},
{
	username: 'Andy',
	password: 234
}];
var newsFeed = [
	{
		username: 'Sally',
		timelines: 'this is fun!!!'
	},
	{
	username: 'John',
	timelines: 'Cool!'
	}
];

/*
username found and password correct -> show feed 
username found but wrong password -> passowrd incorrect 
username unmatch -> show sign up!
*/

var button = document.getElementById('enter');
var username = document.getElementById('username');
var password = document.getElementById('password');


button.addEventListener('click', 
function signin(){
	signup =0;
	for (i=0; i<database.length; i++) {
		if (username.value === database[i].username 
			&& password.value == database[i].password){
			
			var h2 = document.createElement('h2');
			h2.innerText = [newsFeed[0].username, newsFeed[0].timelines];
			document.body.appendChild(h2);

			signup =1;
		}
		else if (username.value === database[i].username 
			&& password.value != database[i].password){
			alert('Password incorrect!');
		signup =1;
		}	
	}
	if (signup==0){
		alert('Sign up!')
	}
}

)



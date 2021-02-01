
var body = document.getElementsByTagName('body')
var listM = document.getElementById('inputM');
var listC = document.getElementById('inputC');


// create new li
function createNewList(){
	if (event.target === listM) {
		var list = listM;			
	}
	else if (event.target === listC){
    	var list = listC;
    }
	
	if (event.target === listM && list.parentElement.childElementCount >1){
		alert('Focus on one thing at one time!')
        list.value ='';
		return;
	}
	if (list.value.length > 0 & event.which === 13) {
    var ul = list.parentElement;
    var li = document.createElement('li');
    li.appendChild(document.createTextNode(list.value));
    var btn = document.createElement("BUTTON");
    btn.innerHTML = "del";
	li.appendChild(btn);
    ul.appendChild(li);
    list.value =''; 
	}
}


// cross line and click button
function CrossOrDel(e){			
	if (e.target.tagName ==='LI') {		
		var finish = document.getElementById('finish');
    	var li = document.createElement('li');
    	li.innerHTML = e.target.innerHTML;    	 	
    	finish.querySelector('ul').appendChild(li);
    	e.target.parentElement.removeChild(e.target);
	}
    else if (e.target.tagName ==='BUTTON') {    	
    	e.target.parentElement.parentElement.removeChild(e.target.parentElement);
    }
}



body[0].addEventListener('keypress', createNewList);
body[0].addEventListener('click', CrossOrDel);




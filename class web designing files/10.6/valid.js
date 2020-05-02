function A(f)
{
	if(require(f.t1,"Enter your name")==false)
	{
		f.t1.focus();
		return false;
	}
	else if(onlyalpha(f.t1,"only alphabet")==false)
	{
		f.t1.focus();
		return false;
	}
	else if(require(f.t2,"Enter your address")==false)
	{
		f.t2.focus();
		return false;
	}
	else if(require(f.t3,"Enter your Contact")==false)
	{
		f.t3.focus();
		return false;
	}
	else if(onlynumber(f.t3,"Only numbers")==false)
	{
		f.t3.focus();
		return false;
	}
	else if(mobilerange(6000000000,9999999999,f.t3,"Invalid no.")==false)
	{
		f.t3.focus();
		return false;
	}
	else if(match_pass(f.t5,f.t6,"password does not match")==false)
	{
		f.t6.value="";
		f.t5.value="";
		f.t5.focus();
		return false;
	}
}















function require(ele,msg)
{
	if(ele.value==null||ele.value=="")
	{
		alert(msg);
		return false;
	}
	else
	{
		return true;
	}
}

function onlyalpha(ele,msg)
{
	var letter=/^[A-Za-z]+$/;
	if(ele.value.match(letter))
	{
		return true;
	}
	else
	{
		alert(msg);
		return false;
	}
	
	
}

function onlynumber(ele,msg)
{
	var digit=/^[0-9,.]+$/;
	if(ele.value.match(digit))
	{
		return true;
	}
	else
	{
		alert(msg);
		return false;
	}	
}

function mobilerange(mn,mx,ele,msg)
{
	if(ele.value<mn||ele.value>mx)
	{
		alert(msg);
		return false;
	}
	else
	{
		return true;
	}
}

function match_pass(ele1,ele2,msg)
{
	if(ele1.value!=ele2.value)
	{
		alert(msg);
		return false;
	}
	else
	{
		return true;
	}
}
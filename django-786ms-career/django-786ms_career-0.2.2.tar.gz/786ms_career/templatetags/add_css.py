from django import template
register = template.Library()

@register.filter(name='addData')
def addData(field,data):
	data=data.split(";")
	l=len(data)
	if l==3:
		return field.as_widget(attrs={"class":data[0],"placeholder":data[1],"required":data[2]})
	elif l==2:
		return field.as_widget(attrs={"class":data[0],"placeholder":data[1]})
	elif l==1:
		return field.as_widget(attrs={"class":data[0]})
		

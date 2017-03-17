from bs4 import BeautifulSoup as bs

def isTag(tag):
    if tag and  str(type(tag)) == "<class 'bs4.element.Tag'>":
        return True
    else: return False
def findAllTagWithName(name,tag):
    arr=list()
    for item in tag.descendants:

        if str(type(item))=="<class 'bs4.element.Tag'>" and item.name==name:
            arr.append(item)
    return arr
def findTagWithName(name,tag):
    var=None
    for item in tag.descendants:
        if str(type(item))=="<class 'bs4.element.Tag'>" and item.name==name:
            var=item
            break
    return var
def findClass(className,tag):
    var = None
    for item in tag.descendants:
        if str(type(item)) == "<class 'bs4.element.Tag'>" and 'class' in item.attrs and item.attrs['class'][0]==className:
            var = item
            break
    return var
def findAllClass(className,tag):
    arr = list()
    for item in tag.descendants:
        if str(type(item)) == "<class 'bs4.element.Tag'>" and 'class' in item.attrs and item.attrs['class'][0] == className:
            arr.append(item)
    return arr

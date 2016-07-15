#! /usr/bin/python

import cgi, cgitb, re
cgitb.enable()

def search(pn, desc):

    form=cgi.FieldStorage()
    
    type=None
    word=None
    if str(pn)=='None':
        type = 'Keyword'
        word=str(desc)
    else:
        type = 'Part Number'
        word=str(pn)
    print "<b>Searching for %s:</b>  %s<br><br>" % (type,word)
    print "<table border='0' width='100%'>"
    print "<tr><th align=left width='10%'> Part Number </th> \
		<th align=left>Part Name</th> \
		<th align=left>Alternate Part Number</th> \
		<th align=left>Vendor</th> \
		<th align=left>Manufacturer</th> \
		<th align=left>Location</th> \
		<th align=left>Sub-System</th> \
		<th align=left>Description</th> \
		<th align=left>Quantity</th> \
		<th align=left>Quantity to Maintain</th> \
		<th align=left>Cost</th></tr>"
    f=open('parts.dat','r')
    pn_arr=[]
    #search and sort
    for line in f:
        l=line.rstrip('\n').split('\t')
        if str(pn) in l[0] and type=='Part Number':
            pn_arr.append((l[0], l[1],l[2],l[3],l[4],l[5],l[9],l[6], l[7], l[8], l[10]))
        elif str(desc).lower() in line.lower() and type =='Keyword':
            pn_arr.append((l[0], l[1],l[2],l[3],l[4],l[5],l[9],l[6], l[7], l[8], l[10]))
    pn_arr=sorted(pn_arr, key=lambda s:s[0])
    #display sorted list
    for part in pn_arr:
        print "<tr><form action='spares.py' method='post'>"
        for index,p in enumerate(part):
            print "<td align=left>%s</td>" % str(p)
            if index==2 and p != 'NA':
                print "<input type='hidden' name='description' value='%s'>" % str(p)
            if index==0 and p !='NA' :
                print "<input type='hidden' name='pn' value='%s'>" % str(p)
                
        print "<td><input type='submit' value='Item' /></form></td>"
        print "</tr>"
    f.close()
    print "</table>"
    



def main():
	print "Content-type:text/html\r\n\r\n"
        print "<html>"
        print "<head>"
	print "<title>Search Results</title>"
        print "</head>"
        print "<body bgcolor='#bbbbb'>"
	form = cgi.FieldStorage()
	part_number = form.getvalue('pn')
	desc = form.getvalue('description')
	search(part_number, desc)
        print "<br><br><form action='sdss.py' method='post'><input type='submit' value='Main Page' /></form>"
        print "</body>"
        print "</html>"

main()

#! /usr/bin/python

import cgi, cgitb 
cgitb.enable()
def main():
	print "Content-type:text/html\r\n\r\n"
	print "<html>"
	print "<head>"
	print "<title>SDSS Engineering Web Interface</title>"
	print "</head>"
	print "<body bgcolor='#bbbbb'>"
	print "<h2> SDSS Engineering Web Interface</h2>"
	print "<hr>"
	print "<h3>Spares Inventory</h3>"
	print ""
	print "<table border='0' width='400'>"
	print "<tr><form action='search.py' method='post'><td alight='right'> Part Number: </td> <td><input type='text' name='pn'></td><td><input type='submit' value='Search Part Number' /></form></td></tr>"
	print "<tr><form action='search.py' method='post'><td alight='right'> Keyword: </td> <td><input type='text' name='description'></td><td><input type='submit' value='Search Keyword' /></form></td></tr>"
	print "</table>"
	print "<table border='0'>"
	print "<form action= 'add.py'>"
	print "<td><input type='submit' value='Add' /></td>"
	print "</form>"
	print "<form action= 'inventory.py' method='post'>"
        print "<td><input type='submit' value='Full Inventory' /></td></form>"
	print "<td><form action='revert.py' method='post'><td><input type='submit' value='Recover' /></form></td>"
	print "<td><form action='ExportXLS.py' method='post'><td><input type='submit' value='Make Excel Spreadsheet' /></form></td>"
	print "<td><a href='help.html'><button>Information</button></a></td>"
	print "</tr></table>"
	print "</body>"
	"""print "<hr>"
	print "<h3>Month Engineering Handoff</h3>"
	print "<form method='post' action='EngHandOff/EngChecks.py'>"
        print "<table border='0' width='300'>"
        print "<tr>"
        print "<select name='engDropDown'>"
        f_in=open('EngHandOff/EngDates.dat')
        for line in f_in:
            l=line.rstrip('\n').split('\t')
            n=str(l[0])+'-'+str(l[1])
            print "<option value=%s>%s</option>" % (n,str(n))
        f_in.close()
        print "</table>"
        print "<table border='0'>"
        print "<input type= hidden name= 'action' value= 'display'>"
        print "<tr><td><input type='submit' value='Submit' /></td>"
	print "</form>"
	"""

	print "</html>"




main()


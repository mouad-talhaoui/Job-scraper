import requests
from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup
import pandas as pd
from tkhtmlview import HTMLLabel


def generatefile(m):
    if m.isnumeric():
        n =int(m)
    else:
        n = 1
    # URL of the website to scrape
    url = "https://www.emploi-public.ma/fr/index.asp?p="
    concours = []
    for i in range(1,n+1):
        # Send an HTTP GET request to the website to the page number i
        response = requests.get(url+str(i))

        # Parse the HTML code using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the relevant information from the HTML code
        for row in soup.find_all("tr"):
            for row2 in row.find_all("td"):
                data = row2.find_all("a", href=True)
                if len(data)!=0:
                    title1 = data[0].get_text()
                    link = data[0]['href']
                    concours.append([title1,link])

    # Store the information in a pandas dataframe
    df = pd.DataFrame(concours, columns=['Title',"link"])


    # Export the data to a CSV file
    df.to_csv('concours.csv', index=False)
    return concours

value = []

def searchAndGeneratefile(m):
    global value 
    value = generatefile(m)
    visaluserConcours(frm, value)
    

def filterData(word):
    global e1
    global value
    searchAndGeneratefile(e1.get())
    value = list(filter(lambda x: word.lower() in x[0].lower(), value))
    print("Ffff")
    print(value)
    visaluserConcours(frm, value)

root = Tk()
root.title("Find public job | Mouad")


global frm 
frm= ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="how mauch pages you want").grid(column=0, row=0)
e1 = ttk.Entry(frm)
e1.grid(column=1, row=0)
e2 = ttk.Entry(frm)
ttk.Label(frm, text="Do you want to filter data").grid(column=0, row=1)
e2.grid(row=1, column=1)
ttk.Button(frm, text="Search and generate file", command=lambda:searchAndGeneratefile(e1.get())).grid(column=1, row=2)
ttk.Button(frm, text="filter data", command=lambda:filterData(e2.get())).grid(column=0, row=2)
labels = []
btns = []
def visaluserConcours(frm, value):
    global labels
    global btns
    for lb in labels:
        if lb is not None:
            lb.destroy()
    for btn in btns:
        if btn is not None:
            btn.destroy()
    if len(value)!=0:
        for i in range(len(value)):
            label = ttk.Label(frm, text=value[i][0])
            labels.append(label)
            label.grid(column=1, row=3+i)
            
        for i in range(len(value)):
            button = ttk.Button(frm, text="voir details", command=lambda:moreDetails(value[i][1]))
            btns.append(button)
            button.grid(column=0, row=3+i)

visaluserConcours(frm, value)

def moreDetails(link):
    print(link)
    url = "https://www.emploi-public.ma/fr/"
    response = requests.get(url+link)

    # Parse the HTML code using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    data = []
    title = soup.find_all("h1")
    data.append(title[0].get_text())
    tds = soup.find_all("td")
    print("tds")
    ths = soup.find_all("th")
    print("ths")
    print(ths)
    openNewWindow(data,tds,ths)
    

def openNewWindow(data,tds,ths):
     
    # Toplevel object which will 
    # be treated as a new window
    global root
    newWindow = Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title(data[0]+" | Mouad")
    l2 = Label(newWindow, text = data[0])
    l2.pack()
    htmlContent = ""
    for i in range(0,len(tds)):
        htmlContent = htmlContent  + "<tr>"+"<th style='color:blue;border: 1px solid;width: 100%;'>"+ths[i].get_text()+"</th><td style='border: 1px solid;width: 100%;'>"+tds[i].get_text()+"</td></tr>"

        # Add label
    htmlContent = "<table style='border: 1px solid;width: 100%;border-collapse: collapse;'><tbody>"+htmlContent+"</tbody><table>"
    print(htmlContent)
    my_label = HTMLLabel(newWindow, html=htmlContent)
        
    # Adjust label
    my_label.pack()
 
    
root.mainloop()

from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkhtmlview import HTMLLabel

root = Tk()
root.title("Find Job")
#root.iconbitmap("path")
root.geometry("500x500")

#Create a main frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)
#create a canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

# add a scrollbar to the canvas
my_scrollbary = ttk.Scrollbar(main_frame,orient=VERTICAL, command=my_canvas.yview)

my_scrollbarx = ttk.Scrollbar(main_frame,orient=HORIZONTAL, command=my_canvas.xview)
my_scrollbarx.pack(side=BOTTOM,fill=X)
my_scrollbary.pack(side=RIGHT,fill=Y)
#configure the canvas
my_canvas.configure(xscrollcommand=my_scrollbarx.set, yscrollcommand=my_scrollbary.set)
my_canvas.bind('<Configure>',lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))

#create anthoer frame inside the canvas
second_frame = Frame(my_canvas)


#add that new frame to a window in the canvas
my_canvas.create_window((0,0),window=second_frame,anchor="nw")


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
                    concours.append([title1,"https://www.emploi-public.ma/fr/"+link])

    # Store the information in a pandas dataframe
    df = pd.DataFrame(concours, columns=['Title',"link for more details"])


    # Export the data to a CSV file
    df.to_csv('concours.csv', index=False)
    return concours

value = []

def searchAndGeneratefile(m):
    global value 
    value = generatefile(m)
    visaluserConcours(second_frame, value)
    

def filterData(word):
    global e1
    global value
    searchAndGeneratefile(e1.get())
    value = list(filter(lambda x: word.lower() in x[0].lower(), value))
    print("Ffff")
    print(value)
    visaluserConcours(second_frame, value)


ttk.Label(second_frame, text="how mauch pages you want").grid(column=0, row=0)
e1 = ttk.Entry(second_frame)
e1.grid(column=1, row=0)
e2 = ttk.Entry(second_frame)
ttk.Label(second_frame, text="Do you want to filter data").grid(column=0, row=1)
e2.grid(row=1, column=1)
ttk.Button(second_frame, text="Search and generate file", command=lambda:searchAndGeneratefile(e1.get())).grid(column=1, row=2)
ttk.Button(second_frame, text="filter data", command=lambda:filterData(e2.get())).grid(column=0, row=2)
labels = []
btns = []

def visaluserConcours(second_frame, value):
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
            label = ttk.Label(second_frame, text=value[i][0])
            labels.append(label)
            label.grid(column=1, row=3+i)
            
        for i in range(len(value)):
            button = ttk.Button(second_frame, text="voir details", command=lambda:moreDetails(value[i][1]))
            btns.append(button)
            button.grid(column=0, row=3+i)

visaluserConcours(second_frame, value)

def moreDetails(link):
    response = requests.get(link)
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

    #Create a main frame
    main_frame = Frame(newWindow)
    main_frame.pack(fill=BOTH, expand=1)
    #create a canvas
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # add a scrollbar to the canvas
    my_scrollbary = ttk.Scrollbar(main_frame,orient=VERTICAL, command=my_canvas.yview)

    my_scrollbarx = ttk.Scrollbar(main_frame,orient=HORIZONTAL, command=my_canvas.xview)
    my_scrollbarx.pack(side=BOTTOM,fill=X)
    my_scrollbary.pack(side=RIGHT,fill=Y)
    #configure the canvas
    my_canvas.configure(xscrollcommand=my_scrollbarx.set, yscrollcommand=my_scrollbary.set)
    my_canvas.bind('<Configure>',lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    #create anthoer frame inside the canvas
    second_frame = Frame(my_canvas)


    #add that new frame to a window in the canvas
    my_canvas.create_window((0,0),window=second_frame,anchor="nw")
 
    # sets the title of the
    # Toplevel widget
    newWindow.title(data[0]+" | Mouad")
    l2 = Label(second_frame, text = data[0])
    l2.pack()
    htmlContent = ""
    for i in range(0,len(tds)):
        htmlContent = htmlContent  + "<tr>"+"<th style='color:blue;border: 1px solid;width: 100%;'>"+ths[i].get_text()+"</th><td style='border: 1px solid;width: 100%;'>"+tds[i].get_text()+"</td></tr>"

        # Add label
    htmlContent = "<table style='border: 1px solid;width: 100%;border-collapse: collapse;'><tbody>"+htmlContent+"</tbody><table>"
    print(htmlContent)
    my_label = HTMLLabel(second_frame, html=htmlContent)
        
    # Adjust label
    my_label.pack()
 
root.mainloop()
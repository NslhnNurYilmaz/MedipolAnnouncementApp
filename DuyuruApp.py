import requests
from bs4 import BeautifulSoup
import tkinter as tk
from urllib.parse import urljoin

base_url = "https://www.medipol.edu.tr/en/announcements?page=" #Base URL of the pages containing the announcements

announcement_links = [] #An empty list has been created for announcement links.


for page in range(6):  # The URL of 5 pages from which announcements will be received is created.
    url = base_url + str(page)
    response = requests.get(url)

    if response.status_code == 200: #If the request to access the page is successful, that is, if status_code = 200, there are 'div's containing the announcements in HTML.
        soup = BeautifulSoup(response.content, 'html.parser')
        divs = soup.find_all('div', class_='col-md-4 col-sm-6 list-card')

        for div in divs:
            a_tags = div.find_all('a') #The 'a' in each 'div' element is found.
            for a in a_tags:
                if 'href' in a.attrs:
                    full_link = urljoin("https://www.medipol.edu.tr", a['href']) #If 'a' contains 'href', it is converted to url.
                    if "/en/announcements" in full_link:
                        announcement_links.append(full_link) #The resulting link is added to the list where links are stored.


announcements = [] #A list where announcement contents will be stored has been created.

for announcement_url in announcement_links:
    response = requests.get(announcement_url)

    if response.status_code == 200: #If the request to access the page is approved, that is, if status_code = 200
        soup = BeautifulSoup(response.content, 'html.parser')
        a_tags = soup.find_all('a') #All 'a's in HTML content are found

        title = soup.find('h1', class_='page-title').text.strip() #The announcement title is found in the page.title class and converted to text.

        content_links = []
        for a in a_tags: #All links in the content were converted to url and added to the content link list.
            if 'href' in a.attrs:
                href = a['href']
                if href.endswith('.pdf'):
                    link = urljoin("https://www.medipol.edu.tr", href)
                    content_links.append(link)

        paragraph_tags = soup.find_all('p') #All paragraph tags on the page found
        date = None
        if paragraph_tags:
            date = paragraph_tags[0].get_text(strip=True) #The first paragraph tag is assigned to the date variable.

        content = '\n'.join(paragraph.get_text(strip=True) for paragraph in paragraph_tags)#Content was created by combining paragraph texts.

        #Announcement titles, links, date and content have been added to the announcements list as a dictionary.
        announcements.append({
            'title': title,
            'link': content_links,
            'date': date,
            'content': content
        })


def update_gui(event): #It is a function that updates the GUI according to the selected announcement.

    selected_index = listbox.curselection()

    if selected_index:  # If an item is selected

        selected_announcement = announcements[selected_index[0]] ## Retrieved announcement details based on the selected directory


        content_text.delete(1.0, tk.END)  # Previous content cleared
        content_text.insert(tk.END, selected_announcement['content']) #The content of the selected announcement has been added to content_text.

        url_text.delete(1.0, tk.END)  # Previous URL cleared
        url_text.insert(tk.END, '\n'.join(selected_announcement['link'])) #The URL of the selected announcement has been added to url_text.

        date_label.config(text=selected_announcement['date']) #The date of the selected announcement has been added to date_label.

        window.title(f"Medipol University Announcements | {selected_announcement['title']}") #The title of the selected announcement appears next to the window title.

        listbox.itemconfig(selected_index, {'bg': 'dark gray', 'fg': 'black'}) #The color of the announcement read was changed to dark grey.


def gui(): #It is the function that creates the window where information about announcements can be read.
    global listbox, content_text, url_text, date_label, window

    window = tk.Tk() #window created
    window.title("Medipol University Announcements") #window title is set.


    listbox = tk.Listbox(window, width=100, height=60) #A listbox containing announcement titles was created.
    listbox.grid(row=1, column=0, rowspan=2) #listbox position in window determined
    listbox.bind('<<ListboxSelect>>', update_gui)

    for announcement in announcements: #Announcement titles were added to the listbox
        listbox.insert(tk.END, announcement['title'])

    label1 = tk.Label(window, text="Announcements") #title label
    label1.grid(row=0, column=0) #label1 position in window determined

    content_text = tk.Text(window, height=60, width=100) #content_text created to display content.
    content_text.grid(row=1, column=1, rowspan=2) #content_text position in window determined

    label2 = tk.Label(window, text="Content of Announcements") #title label
    label2.grid(row=0, column=1) #label2 position in window determined

    date_label = tk.Label(window, text="00.00.00") #date_label created to display date.
    date_label.grid(row=0, column=2) #date_label position in window determined

    url_text = tk.Text(window, height=30, width=100) #url_text created to display links.
    url_text.grid(row=2, column=1, rowspan=2) #url_text position in window determined

    window.mainloop()


gui()
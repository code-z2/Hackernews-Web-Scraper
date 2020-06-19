import requests
from bs4 import BeautifulSoup
from tkinter import *
import webbrowser


res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')

soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select(".storylink")
links2 = soup2.select(".storylink")

subtext = soup.select(".subtext")
subtext2 = soup2.select(".subtext")

mega_link = links + links2
mega_subtext = subtext + subtext2


def sort_stories_by_vote(hnlist):
    return sorted(hnlist, key=lambda x: x['votes'], reverse=True)


def create_custom_hacker_news(item, subtext):
    hn = []
    for idx, item in enumerate(item):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')

        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title,
                           'link': href,
                           'votes': f'{points} votes'
                           })
    print(len(hn))

    return sort_stories_by_vote(hn)


news = create_custom_hacker_news(mega_link, mega_subtext)

var_range, count, rower = range(50), 0, 0

# generate variable names for tk labels
title_var = ['var' + str(i) for i in var_range if i > 0]
link_var = ['link' + str(i) for i in var_range if i > 0]
pt_var = ['pt' + str(i) for i in var_range if i > 0]


def callback(url):
    webbrowser.open_new(url)


def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


root = Tk()

Frame1 = Frame(root, bg="whitesmoke")
Frame1.pack(fill="both", expand=True)
Frame1.rowconfigure(0, weight=1)
Frame1.columnconfigure(0, weight=1)

canvas = Canvas(Frame1, bg="whitesmoke")
canvas.grid(row=0, column=0, sticky="nsew")

canvasFrame = Frame(canvas, bg="whitesmoke")
canvas.create_window(0, 0, window=canvasFrame, anchor='nw')

for item in news:
    a, b, c = title_var[count], link_var[count], pt_var[count]

    a = Label(canvasFrame,
              text=item['title'],
              fg="#1A1C1A",
              bg='whitesmoke',
              font=("Georgia", 14))
    a.grid(row=rower, padx=12, sticky='w')

    b = Label(canvasFrame,
              text=item['link'],
              fg="#007fff",
              cursor="hand2",
              bg='whitesmoke')
    b.grid(row=rower + 1, padx=12, sticky='w')
    b.bind("<Button-1>", lambda e: callback(b.cget("text")))

    c = Label(canvasFrame,
              text=item['votes'],
              fg="green",
              bg='whitesmoke')
    c.grid(row=rower + 2, padx=24, sticky='w')

    count += 1
    rower += 3

scrollbar = Scrollbar(Frame1, orient=VERTICAL)
scrollbar.config(command=canvas.yview)

canvas.config(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="ns")

canvasFrame.bind("<Configure>", update_scrollregion)

root.mainloop()

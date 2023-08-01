# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        text = text.lower()
        for i in string.punctuation:
            text = ' '.join(text.split(i))

        return ' '+self.phrase+' ' in ' '+' '.join([x for x in text.split(' ') if x != ''])+' '


# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def evaluate(self, news_item):
        return self.is_phrase_in(news_item.get_title().lower())


# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, news_item):
        return self.is_phrase_in(news_item.get_description().lower())


# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, date_string):
        self.date = datetime.strptime(date_string, '%d %b %Y %H:%M:%S').replace(tzinfo=pytz.timezone("EST"))


# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, news_item):
        datetime_item = news_item.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        return self.date > datetime_item


class AfterTrigger(TimeTrigger):
    def evaluate(self, news_item):
        datetime_item = news_item.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        return self.date < datetime_item


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, another_Trigger):
        self.another_Trigger = another_Trigger

    def evaluate(self, news_item):
        return not self.another_Trigger.evaluate(news_item)


# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, *Triggers):
        self.Triggers = Triggers

    def evaluate(self, news_item):
        for i in self.Triggers:
            if not i.evaluate(news_item):
                return False

        return True


# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, *Triggers):
        self.Triggers = Triggers

    def evaluate(self, news_item):
        for i in self.Triggers:
            if i.evaluate(news_item):
                return True

        return False

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    filtered_stories = []
    for i in stories:
        for j in triggerlist:
            if j.evaluate(i):
                filtered_stories.append(i)
                break

    return filtered_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    triggerlist = []
    for i in lines:
        new_i = i.split(',')
        if new_i[0] != 'ADD':
            if new_i[1] == 'TITLE':
                globals()[new_i[0]] = TitleTrigger(new_i[2])

            elif new_i[1] == 'DESCRIPTION':
                globals()[new_i[0]] = DescriptionTrigger(new_i[2])

            elif new_i[1] == 'AFTER':
                globals()[new_i[0]] = AfterTrigger(new_i[2])

            elif new_i[1] == 'BEFORE':
                globals()[new_i[0]] = BeforeTrigger(new_i[2])

            elif new_i[1] == 'NOT':
                globals()[new_i[0]] = NotTrigger(globals()[new_i[2]])

            elif new_i[1] == 'AND':
                globals()[new_i[0]] = AndTrigger(*[globals()[ii] for ii in new_i[2:]])

            elif new_i[1] == 'OR':
                globals()[new_i[0]] = OrTrigger(*[globals()[ii] for ii in new_i[2:]])

        else:
            for j in new_i[1:]:
                triggerlist.append(globals()[j])

    return triggerlist


def read_trigger_config2(filename):
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    dict = {}
    triggerlist = []

    for i in lines:
        new_i = i.split(',')
        if new_i[0] != 'ADD':
            if new_i[1] == 'TITLE':
                dict[new_i[0]] = TitleTrigger(new_i[2])

            elif new_i[1] == 'DESCRIPTION':
                dict[new_i[0]] = DescriptionTrigger(new_i[2])

            elif new_i[1] == 'AFTER':
                dict[new_i[0]] = AfterTrigger(new_i[2])

            elif new_i[1] == 'BEFORE':
                dict[new_i[0]] = BeforeTrigger(new_i[2])

            elif new_i[1] == 'NOT':
                dict[new_i[0]] = NotTrigger(dict[new_i[2]])

            elif new_i[1] == 'AND':
                dict[new_i[0]] = AndTrigger(dict[new_i[2]], dict[new_i[3]])

            elif new_i[1] == 'OR':
                dict[new_i[0]] = OrTrigger(dict[new_i[2]], dict[new_i[3]])

        else:
            for j in new_i[1:]:
                triggerlist.append(dict[j])

    return triggerlist


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Biden")
        t4 = AndTrigger(t2, t3)
        t5 = TitleTrigger('covid')
        t6 = TitleTrigger('coronavirus')
        t7 = OrTrigger(t5, t6)
        triggerlist = [t1, t4, t7]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "World's Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        def get_news(*links):
            all_news = []
            for i in links:
                all_news.extend(process(i))

            return all_news

        while True:
            print("Polling . . .", end=' ')
            # Get stories from many sites' RSS news feeds (e.g. Google, NY Times)
            stories = get_news(
                'http://news.google.com/news?output=rss',
                'https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml',
                'http://feeds.bbci.co.uk/news/world/rss.xml',
                'https://www.theguardian.com/world/rss',
                'https://www.cnbc.com/id/100727362/device/rss/rss.html',
                'https://www.latimes.com/world/rss2.0.xml',
                'http://www.independent.co.uk/news/world/rss'
            )

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()


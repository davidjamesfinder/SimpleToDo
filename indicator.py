#!/usr/bin/python
 
from gi.repository import AppIndicator3 as AppIndicator
from gi.repository import Notify
from gi.repository import Gtk
import pdb
import os
import json
import jsonpickle
import ast
import time
import thread
import uuid
class AddItemPopup(Gtk.Window): #We need this to be destructable, so we make it its own class.
    def __init__(self):
        super(AddItemPopup,self).__init__() #Inherits constructor from GTK window
        self.set_position(Gtk.WindowPosition.CENTER) #Set position of window to the middle of the screen
        self.set_title("Add A New Item") #Set title of window
        self.set_border_width(20) #Set border width to 20
        #Add an icon?
        self.connect('delete-event', self.quit) #Connect deletion field
        self.vbox = Gtk.VBox(spacing=6)
        self.add(self.vbox)
        self.boxone = Gtk.HBox(spacing=6) #Use a horizontal box. I probably could try to use a grid instead
        self.add(self.box) #Add box
        #self.label = Gtk.Label("Add A New Item") #Honestly, takes up too much space and is repetitive
        self.entryField = Gtk.Entry() #Needs to be an attribute, because we reference it later.
        submitbutton = Gtk.Button(label="Add", stock=None) #Add a rather generic button

        submitbutton.connect("clicked", indicator.AddItem, self) #Connect it to the add item function on indicator
        #self.box.pack_start(self.label, False, True, 0)
        self.box.pack_start(self.entryField, True, True, 0) #Pack in the entry field
        self.box.pack_start(submitbutton, False, True, 0) #Pack in the submit button
        self.show_all() #Showtime
 
    def quit(self,window,connection):
            Gtk.Widget.destroy(self) #Destroy self. This is necessary so we don't quit the application as a whole
 
class AppIndicator(object):
        def __init__(self):
                self.ind = AppIndicator.Indicator.new("Reminder Application",
                    'distributor-logo', AppIndicator.IndicatorCategory.APPLICATION_STATUS)
                self.ind.set_status (AppIndicator.IndicatorStatus.ACTIVE)
                #self.label=AppIndicator.Indicator.new_label("Testing")
                self.ind.set_label("Tikkun Atzmi","Tikkun Atzmi") 
                if not os.path.exists('data.json'):
                        file('data.json','w+') #(If the file doesn't exist, initialize it)
                file_attributes=os.stat('./data.json') #Read the statistics for our data file
                self.itemList = [] #Initialize local copy of the item list
                if file_attributes.st_size > 0: #If the file has at least one line... Otherwise, attempting to read lines throws an error
                        #For whatever reason, there isn't a good way to essentially unfreeze objects from a data-store. Pickling doesn't work with objects, JSONPickle doesn't unformat properly, but does provide easily readable data
                        self.file = open('./data.json', 'r') #Read the file, read only.
                        for line in self.file: #For each of the lines...
                                print line
                                if not line.isspace(): #If we don't have a single line
                                                #print json.loads(line)
                                                #myLine=type('NewItem', (object,), )  #Interpret our JSON line as an array, and construct this as an instance of a new object. We can't simply construct an instance of our old object
                                                #We use type so that I don't have to use an array
                                                #print myLine.__dict__
                                                #myLine.category = None

                                                currentItem = jsonpickle.decode(line)
                                                self.itemList.append(currentItem) #Append this item to our item list
                                               
                        self.file.close()
                self.render() #Render
 
        def notification(self, MenuItem): #This is a sample notification test
                Notify.init("Hello World")
                Test=Notify.Notification.new("Hello World", "This is an example notification")
                Test.show()
 
        def render(self):
                self.menu = Gtk.Menu()
                menuItemList = []
                categoryDict = {}
                if  len(self.itemList) >= 1 :
                    for item in self.itemList:
                        #print str(myItem.__dict__)
                        if item.category == None:
                            itemListSub=Gtk.MenuItem(item.name)
                            subMenu=Gtk.Menu()
                            itemListSub.set_submenu(subMenu)
                            deleteItem = Gtk.MenuItem("Delete")
                            deleteItem.connect('activate',item.delete,self)
                            subMenu.append(deleteItem)
                            menuItemList.append(itemListSub)
                        else:
                            print item
                            if item.category in list(categoryDict.keys()):
                                categoryDict[item.category].append(item)
                            else:
                                categoryDict[item.category]=[item]
                print categoryDict
 
                itemAdder = Gtk.MenuItem("Add Item")
                itemAdder.connect("activate", lambda x: AddItemPopup()) #We have to use a lambda because... Python.
 
                notifytester = Gtk.MenuItem("Test Notifications")
                notifytester.connect('activate', self.notification)
 
                seperator = Gtk.SeparatorMenuItem()    
    
                exit = Gtk.MenuItem("Exit")
                exit.connect('activate', Gtk.main_quit)
 
                if len(self.itemList) >=1 : #Append all the items in the list
                        for menuItem in menuItemList:
                                self.menu.append(menuItem)
                self.menu.append(seperator)
                self.menu.append(itemAdder)
                self.menu.append(notifytester)
                self.menu.append(exit)
                self.menu.show_all()
                self.ind.set_menu(self.menu)
 
        def AddItem(indicator,button,myWindow):

                myItem = Item(myWindow.entryField.get_text())#Create an item
                indicator.itemList.append(myItem)#Add item to local list
                myFile = open('data.json', 'a+')#Write to the storage file starting at the end.
                #print json.dump(myItem.__dict__)
                encodement=jsonpickle.encode(myItem)#Encode Item object as a line.
                myFile.write("\n")#Seperate lines. Putting this line after the next one is ugly because when we delete whitespace, it would remove the useful whitespace
                myFile.write(encodement)#Write the object JSON to the file
                indicator.render()#Re-render, now that we have changed the number of items.
                Gtk.Widget.destroy(myWindow)#Destroy the add-object box.
 
class Item(object):
        def __init__(self, name, category=None):
            self.id = uuid.uuid1()
            self.name = name
            self.category = None
            #self.category = category
        #def set_item_id(self):
        #    myFile=open('data.json','a+') #Delete the data, so that we can conveniently rewrite it
        #    self.id = uuid.uuid1()
        #    encodement=jsonpickle.encode(self)
        #    myFile.write(encodement)
        #    myFile.write("\n")       
        #    myFile.close()
        def delete(self,connection,indicator):
                myFile = open('data.json', 'r')
                lines=myFile.readlines() #Read all the lines from our file
                myFile.close() #Is this necessary?
                myFile=open('data.json','w') #Delete the data, so that we can conveniently rewrite it
                for line in lines: #For each of the lines in the file
                        if self.id.hex not in line: #If the name of our item isn't in the line, don't write
                            if line != '\n': #Don't write extraneous lines. These mainly occur if we delete a line in the middle.
                                myFile.write(line) #But write all the other lines
                indicator.itemList.remove(self) #Remove the item from our local copy
                myFile.close()
                indicator.render() #Re-render the applet, now that we have altered the view

 
indicator = AppIndicator()
#thread.start_new_thread #For when I get around to implimenting threading

Gtk.main()
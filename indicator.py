#!/usr/bin/python
#David Finder
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
import boto3
import re
class AddItemPopup(Gtk.Window): #We need this to be destructable, so we make it its own class.
    def __init__(self):
        super(AddItemPopup,self).__init__() #Inherits constructor from GTK window
        self.set_position(Gtk.WindowPosition.CENTER) #Set position of window to the middle of the screen
        self.set_title("Add A New Item") #Set title of window
        self.set_border_width(20) #Set border width to 20
        #Add an icon?
        self.connect('delete-event', self.quit) #Connect deletion field

        self.table = Gtk.Grid()
        #self.table 
        self.add(self.table)

        #self.vbox = Gtk.VBox(spacing=6)
        #self.add(self.vbox)
        #self.boxone = Gtk.HBox(spacing=6) #Use a horizontal box. I probably could try to use a grid instead

        self.nameLabel = Gtk.Label("Name") #Honestly, takes up too much space and is repetitive
        self.nameField = Gtk.Entry() #Needs to be an attribute, because we reference it later.
        self.categoryLabel = Gtk.Label("Category")
        self.categoryField = Gtk.Entry()
        self.submitButton = Gtk.Button(label="Add", stock=None) #Add a rather generic button
        self.submitButton.connect("clicked", indicator.AddItem, self) #Connect it to the add item function on indicator
        self.table.attach(self.nameLabel,0,0,1,1)
        self.table.attach(self.nameField,1,0,2,1)
        self.table.attach(self.categoryLabel,0,1,1,1)
        self.table.attach(self.categoryField,1,1,2,1)
        self.table.attach(self.submitButton,0,2,3,1)
        self.table.set_column_spacing(6)
        #self.box.pack_start(self.label, False, True, 0)
        #self.boxone.pack_start(self.entryField, True, True, 0) #Pack in the entry field
        #self.boxone.pack_start(submitbutton, False, True, 0) #Pack in the submit button
        self.show_all() #Showtime
 
    def quit(self,window,connection):
            Gtk.Widget.destroy(self) #Destroy self. This is necessary so we don't quit the application as a whole
 
class ChangeCategoryPopup(Gtk.Window):
    def __init__(self,item):
        super(AddItemPopup,self).__init__()
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title("Change Category")
        self.set_border_width(20)
        self.connect('delete-event',self.quit)
        self.table = Gtk.Grid()
        self.add(self.table)
        self.categoryField = Gtk.Entry()
        self.categoryField.set_text(item.Category)
        self.submitButton = Gtk.Button(label="Set",stock=None)
        self.submitButton.connect("clicked", item.changeCategory)
        self.show_all()
    def quit(self, window,connection):
        Gtk.Widget.destroy(self)

class ToDoIndicator(object):
        def __init__(self):
                self.ind = AppIndicator.Indicator.new("Reminder Application",
                    'distributor-logo', AppIndicator.IndicatorCategory.APPLICATION_STATUS)
                self.ind.set_status (AppIndicator.IndicatorStatus.ACTIVE)
                #self.label=AppIndicator.Indicator.new_label("Testing")
                self.ind.set_label("Tikkun Atzmi","Tikkun Atzmi") 
                if not os.path.exists('data.json'):
                        file(storageLocation,'w+') #(If the file doesn't exist, initialize it)
                file_attributes=os.stat(storageLocation) #Read the statistics for our data file
                self.itemList = [] #Initialize local copy of the item list
                #print os.system("ls")
                if file_attributes.st_size > 0: #If the file has at least one line... Otherwise, attempting to read lines throws an error
                        #For whatever reason, there isn't a good way to essentially unfreeze objects from a data-store. Pickling doesn't work with objects, JSONPickle doesn't unformat properly, but does provide easily readable data
                        self.file = open(storageLocation, 'r') #Read the file, read only.
                        for line in self.file: #For each of the lines...
                                #print line
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
                settings = open(theActualPath+"/settings")
                
                for line in settings:
                    print line
                    pattern = re.compile('"(.*?)"')
                    number = pattern.search(line).group(0).strip("\"")
                    response = client.publish(PhoneNumber=number, Message="<Insert MessageHere>")
                    return 0
                #Notify.init("Hello World")
                #Test=Notify.Notification.new("Hello World", "This is an example notification")
                #Test.show()
 
        def render(self):
                self.menu = Gtk.Menu()
                menuItemList = []
                categoryDict = {}
                if  len(self.itemList) >= 1 :
                    for item in self.itemList:
                        #print str(myItem.__dict__)
                        if item.category == None or item.category == "":
                            itemListSub=Gtk.MenuItem(item.name)
                            subMenu=Gtk.Menu()
                            itemListSub.set_submenu(subMenu)
                            deleteItem = Gtk.MenuItem("Delete")
                            deleteItem.connect('activate',item.delete,self)
                            changeCategoryItem = Gtk.MenuItem("Change Category")
                            changeCategoryItem.connect('activate', item.changeCategory, self, item)
                            subMenu.append(changeCategoryItem)
                            subMenu.append(deleteItem)
                            menuItemList.append(itemListSub)
                        else:
                            #print item
                            if item.category in list(categoryDict.keys()):
                                categoryDict[item.category].append(item)
                            else:
                                categoryDict[item.category]=[item]
                categorySeperator = Gtk.SeparatorMenuItem()
                categoryMenus = []
                if len(categoryDict) >= 1:
                    for catName in list(categoryDict.keys()):
                        categoryMenu = Gtk.MenuItem(catName)
                        catSubMenu = Gtk.Menu()
                        categoryMenu.set_submenu(catSubMenu)
                        for item in categoryDict[catName]:
                            itemListSub=Gtk.MenuItem(item.name)
                            subMenu=Gtk.Menu()
                            itemListSub.set_submenu(subMenu)
                            deleteItem = Gtk.MenuItem("Delete")
                            deleteItem.connect('activate',item.delete,self)
                            changeCategoryItem = Gtk.MenuItem("Change Category")
                            changeCategoryItem.connect('activate', item.changeCategory, self, item)
                            subMenu.append(changeCategoryItem)
                            subMenu.append(deleteItem)
                            catSubMenu.append(itemListSub)
                        categoryMenus.append(categoryMenu)


                        
                itemAdder = Gtk.MenuItem("Add Item")
                itemAdder.connect("activate", lambda x: AddItemPopup()) #We have to use a lambda because... Python.
 
                notifytester = Gtk.MenuItem("Test Notifications")
                notifytester.connect('activate', self.notification)
 
                seperator = Gtk.SeparatorMenuItem()    
    
                exit = Gtk.MenuItem("Exit")
                exit.connect('activate', Gtk.main_quit)
                if len(categoryMenus) >= 1:
                    for categoryMenu in categoryMenus:
                        self.menu.append(categoryMenu)

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

                myItem = Item(myWindow.nameField.get_text(),myWindow.categoryField.get_text())#Create an item
                indicator.itemList.append(myItem)#Add item to local list
                myFile = open(storageLocation, 'a+')#Write to the storage file starting at the end.
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
            self.category = category
            #self.category = category
        #def set_item_id(self):
        #    myFile=open('data.json','a+') #Delete the data, so that we can conveniently rewrite it
        #    self.id = uuid.uuid1()
        #    encodement=jsonpickle.encode(self)
        #    myFile.write(encodement)
        #    myFile.write("\n")       
        #    myFile.close()
        def notify(self):


            response = client.publish(PhoneNumber=number, Message="<InsertMessageHere>")
        def delete(self,connection,indicator):
            myFile = open(storageLocation, 'r')
            lines=myFile.readlines() #Read all the lines from our file
            myFile.close() #Is this necessary?
            myFile=open(storageLocation,'w') #Delete the data, so that we can conveniently rewrite it
            for line in lines: #For each of the lines in the file
                    if self.id.hex not in line: #If the name of our item isn't in the line, don't write
                        if line != '\n': #Don't write extraneous lines. These mainly occur if we delete a line in the middle.
                            myFile.write(line) #But write all the other lines
            indicator.itemList.remove(self) #Remove the item from our local copy
            myFile.close()
            indicator.render() #Re-render the applet, now that we have altered the view
        def changeCategory(self, connection, indicator):
            pass

 
global storageLocation
global theActualPath
global client 
global phoneNumber

client = boto3.client('sns')
theActualPath = os.path.dirname(os.path.realpath(__file__))

settings = open(theActualPath+"/settings")
settingsLines = settings.readlines()
line = settingsLines[0]
pattern = re.compile('"(.*?)"')
phoneNumber = pattern.search(line).group(0).strip("\"")
storageLocation = theActualPath + "/data.json"
indicator = ToDoIndicator()
#thread.start_new_thread #For when I get around to implimenting threading

Gtk.main()
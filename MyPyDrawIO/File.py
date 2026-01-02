import json
import os
import xmltodict

import MyFramework.Informations     as Infos
import MyFramework.DE as DE

import MyPyDrawIO.Page              as Page

class File(dict):
    """
    File represents the whole draw.io file.
    You use it to manage the file and the pages within the file.

    ## manage the file
    Functions to create, open, and save to draw.io files using a MyPyDrawIO : File instance.
    - [File()](./File.html#File.__init__)
    - [open()](./File.html#File.open)
    - [save()](./File.html#File.save)
    - [saveAs()](./File.html#File.saveAs)
    
    ## manage the pages
    Functions to manage the pages of the file.
    - [pages()](./File.html#File.pages)
    - [numOfPages()](./File.html#File.numOfPages)
    - [insertPage()](./File.html#File.insertPage)
    - [movePage()](./File.html#File.movePage)
    - [deletePage()](./File.html#File.deletePage)
    
    The order of the pages returned by [pages()](./File.html#File.pages) is the same order they
    are shown when opening the draw.io file with a draw.io application.
    Therefore moving or inserting the pages to specific positions is crucial.

    ## Code examples
    ### Manage the file

    ```
    import MyPyDrawIO.File              as File

    file = File.File("./MyDrawIOFile.drawio")

    # do some stuff

    file.save() 
    # Saves changes to "./MyDrawIOFile.drawio".
    # If "./MyDrawIOFile.drawio" does not exist yet, it will be created.

    # do some stuff

    file.saveAs("./OtherFile.drawio")
    # Saves changes to "./OtherFile.drawio", leaving "./MyDrawIOFile.drawio" unchanged.
    # If "./OtherFile.drawio" does not exist yet, it will be created.

    # do some stuff

    file.open("./AnotherFile.drawio")
    # Saves changes to "./OtherFile.drawio".

    # do some stuff

    file.save() 
    # Saves changes to "./Anoriginal.drawio". 
    # If "./AnotherFile.drawio" does not exist yet, it will be created.
    ```

    ### Manage the pages

    ```
    import MyPyDrawIO.File              as File

    # New file
    file = File.File("./MyDrawIOFile.drawio")
    print("Pages in new file:")
    for page in file.pages():
        print(" - " + page.name())

    # First changes
    file.insertPage("New Page A")
    file.insertPage("New Page B", 1)
    file.insertPage("New Page C")
    file.deletePage(3)

    print("")
    print("Pages after first changes:")
    for page in file.pages():
        print(" - " + page.name())

    # Second changes
    file.movePage(0, 2)

    print("")
    print("Pages after second changes:")
    for page in file.pages():
        print(" - " + page.name())

    print("")
    print("Number of pages: " + str(file.numOfPages()))
    ```
    """
    ###############################################################################################
    # class variables

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __createFile(self):
        """
        Private function to create a MyPyDrawIO : File with one page.
        """
        newPage = Page.Page("Page - 1")
        self["mxfile"] = {
            "diagram" : []
        }

        self.__pages = list()
        self.__pages.append(
            newPage
        )

    #----------------------------------------------------------------------------------------------
    def __init__(self, filePath):
        """
        Constructor of MyPyDrawIO : File.

        filePath is path to a draw.io file to be opened or created (if not existing yet).
        """
        self.__filePath     = ""
        self.__pages        = list[Page.Page]()
        self.__infos        = Infos.Informations()
        self.__filePath     = ''
        self.__pages        = list()

        self.open(filePath)

    #----------------------------------------------------------------------------------------------
    def __loadFile(self):
        """
        Private function to load an existing draw.io file.
        """
        pages = []
        self.__pages = list[Page.Page]()

        # 1. load file
        try:
            file = open(self.__filePath)
            content = xmltodict.parse(file.read())
            file.close()
            dict.__init__(self, content)
            pages = content["mxfile"]["diagram"]
            self["mxfile"]["diagram"] = []
        except:
            Infos.announceError("Can not load file \"" + self.__filePath + "\".")
            return
        
        # 2. create the pages
        if(type(pages) == dict):
            self.__pages.append(
                Page.Page(pages)
            )
        else:
            for page in pages:
                self.__pages.append(
                    Page.Page(page)
                )
        self["mxfile"]["diagram"] = []

    ###############################################################################################
    # Public functions
    #----------------------------------------------------------------------------------------------
    def deletePage(self, position : int):
        """
        Deletes the page at the given position.

        If the last page will be deleted, an empty page with name "Page - 1" will be inserted.
        """
        page = self.__pages.pop(position)
        if(len(self.__pages) == 0):
            self.insertPage(0, "Page - 1")

    #----------------------------------------------------------------------------------------------
    def insertPage(self, name : str, position : int = 0) -> Page.Page:
        """
        Creates a new page and inserts them at the given position.
        The [page instance](./Page.html) is returned.
        """
        newPage = Page.Page(name)
        self.__pages.insert(position, newPage)
        return newPage

    #----------------------------------------------------------------------------------------------
    def movePage(self, positionOld : int, positionNew : int):
        """
        Moves the page at position positionOld to positionNew.
        """
        page = self.__pages.pop(positionOld)
        self.__pages.insert(positionNew, page)

    #----------------------------------------------------------------------------------------------
    def numOfPages(self):
        """
        Returns the number of pages.
        """
        return len(self.__pages)

    #----------------------------------------------------------------------------------------------
    def open(self, filePath):
        """
        Saves changes to the currently opened draw.io file.

        If filePath represents an existing draw.io file, this file will be opened.
        Otherwise an empty draw.io file will be created, saved and remains open for further manipulation.
        """
        if(self.__filePath):
            self.save()

        self.__filePath = filePath
        if(os.path.exists(filePath) == True):
            self.__loadFile()
        else:
            self.__createFile()
            self.save()
    
    #----------------------------------------------------------------------------------------------
    def pages(self) -> list [Page.Page]:
        """
        List of all pages within this file.
        """
        return self.__pages
            
    #----------------------------------------------------------------------------------------------
    def save(self):
        """
        Saves the current state into the draw.io file set as filePath.
        """
        # List for all the diagrams aka pages
        diagrams = []
        # Retrieve all the pages
        for page in self.__pages:
            diagrams.append(page._content())

        # Assemble the content
        content = self
        content["mxfile"]["diagram"] = diagrams

        # Save the content to the file
        f = open(self.__filePath, "w")
        f.write(xmltodict.unparse(content, pretty = True))
        f.close()

    #----------------------------------------------------------------------------------------------
    def saveAs(self, filePath : str):
        """
        Changes the filePath to the filePath provided and saves the current content into that file.
        """        
        self.__filePath = filePath
        self.save()

###################################################################################################
# Public global functions / Helper functions

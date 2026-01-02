import os

import MyFramework.Informations as Infos
import MyPyDrawIO.Library       as Library
    
class Libraries:
    """
    Singleton-Klasse zum Laden von DrawIO-Bibliotheken (xml-Dateien).
    Jede Bibliothek wird über ein eigenes [Library Objekt](./Library.html#Library) abgebildet. Zu den in den DrawIO Bibliotheken enthaltenen Vertices und Edges werden [ElementDefinition](./ElementDefinition.html#ElementDefinition) erstellt. Diese dienen als Vorlage für die Erstellung von Vertices und Edges, welche den Funktionen [Page.createVertex()](./Page.html#Page.createVertex) und [Page.createEdge()](./Page.html#Page.createEdge) übergeben werden.
    """
    ###############################################################################################
    # class variables
    __infos     = Infos.Informations()
    __libraries = list[Library.Library]()

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __new__(cls):
        """
        Das Libraries Objekt wird als Singleton erstellt, da es als zentrales Objekt den Zugriff auf die Bibliotheken ermöglichen soll.
        """        
        if not hasattr(cls, 'instance'):
            cls.instance = super(Libraries, cls).__new__(cls)
        return cls.instance

    ###############################################################################################
    # public functions
    #----------------------------------------------------------------------------------------------
    def library(self, name) -> Library.Library:
        """
        Gibt das [Library Objekte](./Library.html#Library) mit dem Namen zurück.
        """
        for library in self.__libraries:
            if(library["name"] == name):
                return library
        
        return None
    
    #----------------------------------------------------------------------------------------------
    def libraries(self) -> list[Library.Library]:
        """
        Gibt eine Liste der [Library Objekte](./Library.html#Library) zurück.
        """        
        return self.__libraries
    
    #----------------------------------------------------------------------------------------------
    def loadLibrary(self, filePath : str) -> bool:
        """
        Lädt die DrawIO Library-Datei, wenn diese existiert, erstellt ein [Library Objekte](./Library.html#Library) und fügt dieses der Liste der [libraries()](./Libraries.html#Libraries.libraries) hinzu.

        Gibt True zurück, wenn die Library geladen werden konnte, ansonsten wird False ausgegeben.
        """
        # 1. Check if the file exists, otherwise return with a warning
        if(not os.path.exists(filePath)):
            Infos.announceWarning("Library \"" + filePath + "\"does not exist.")
            return False
            
        # 2. Create the library object
        library = Library.Library()
        successCode = library.load(filePath)
        if(successCode):
            self.__libraries.append(library)
            
        return successCode

###################################################################################################
# Public global functions / Helper functions
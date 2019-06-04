import os
import re

class PRO:

    #===================================================#
    #                   CONSTRUCTEUR                    #
    #===================================================#

    def __init__(self,CC,CA):
        self.__path=None
        self.__CC=CC
        self.__CA=CA
        self.__file=None
        self.__data={}
        self.lower=False
        self.client=None
        self.env="PROD"
        # INITIALIZE CC/CA IF NOT CORRECT
        #################################################
        self.set_CC(CC)
        self.set_CA(CA)

    #===================================================#
    #                   ACESSORS GET                    #
    #===================================================#

    def get_Path(self):
        return self.__path

    def get_CC(self):
        return self.__CC

    # RETURN UPPER OR LOWER FILE EXTENSION
    #####################################################
    def getExt(self):
        if self.lower:
            return "pro"
        else:
            return "PRO"

    def get_CA(self):
        return self.__CA

    def get_File(self):
        return self.__file

    def getClient(self):
        return self.client

    # RETURN ALL KEY FROM DATA DICTIONARY
    #####################################################
    def get_Data_Key(self):
        tab=[]
        for i in self.__data.keys():
            tab.append(i)
        return tab

    # RETURN ALL VALUES FROM DATA DICTIONARY
    #####################################################
    def get_Data_Value(self):
        tab=[]
        for i in self.__data.values():
            tab.append(i)
        return tab

    # RETURN VALUE FOUND AT POSITION FROM DATA DICTIONARY
    #####################################################
    def get_Data_By_Position(self, p):
        try:
            tmp=self.get_Data_Value()
            return tmp[p]
        except IndexError as ie:
            return "NOT FOUND AT ASKED POSITION : {}".format(str(ie))

    # RETURN VALUE FOUND WITH KEY FROM DATA DICTIONARY
    #####################################################
    def get_Data_By_Key(self, key):
        test=False
        p=0
        for i in self.get_Data_Key():
            if i==key:
                return self.get_Data_By_Position(p)
                test=True
            p+=1
        if test!=True:
            return "Not found with this key"

    # RETURN ALL VALUES FOUND WITH REGEX FROM DATA DIC
    #####################################################
    def get_Data_By_RegKey(self,key):
        test=False
        p=0
        fnd=[]
        for i in self.get_Data_Key():
            print(i)
            if re.search(i,key,re.IGNORECASE):
                fnd.append(self.get_Data_By_Position(p))
                test=True
            p+=1
        if test!=True:
            return "Not found at all with this RegKey"

    # RETURN ALL VALUES FROM THE CURRENT INSTANCE
    #####################################################
    def toString(self):
        return print("CC = {} || CA = {} || PRO = {} || Path = {} || lower = {} || client = {} || environment = {}".format(self.get_CC(),self.get_CA(),self.get_File(),self.get_Path(),self.lower,self.client,self.env))

    #===================================================#
    #                   ACESSORS SET                    #
    #===================================================#

    def set_Path(self, data):
        self.__path=data

    def set_CC(self,data):
        tmp=self.Ctrl_CC(data)
        if tmp[0]:
            self.__CC=tmp[1]

    def set_CA(self,data):
        tmp=self.Ctrl_CA(data)
        if tmp[0]:
            self.__CA=tmp[1]

    def set_Data(self,key,value):
        self.__data[key]=value

    def setClient(self):
        self.client=self.get_Data_By_Key("Base_Mysql")

    def set_File(self):
        try:
            self.__file="{}{}.{}".format(self.get_CC(),self.get_CA(),self.getExt())
        except AttributeError as ae:
            print("Mise à jour impossible : il manque le code client ou le code appli")

    # UPDATE CURRENT INSTANCE WITH OLD PATH SETTINGS
    #####################################################
    def setOldPath(self):
        #self.set_Path(r'\\opn-cold01\comcold\PRODUCTION')  #PROD
        self.set_Path(r'E:\Programmation\Nomade\Projets\docaposte\sql\DEV')
        self.set_File()
        self.set_Path(self.get_Path())

    # UPDATE CURRENT INSTANCE WITH NEW PATH SETTINGS
    #####################################################
    def setNewPath(self,env):
        #self.set_Path("\\\\opn-cold01\\comcold\\_ENVIRONNEMENT_\\"+env+"\\"+self.get_CC()+"\\"+self.get_CA()+"\\PRO") #PROD
        self.set_Path(r'E:\Programmation\Nomade\Projets\docaposte\sql\DEV')
        self.set_File()
        self.set_Path(self.get_Path())

    # UPDATE CURRENT INSTANCE DEPENDING ON ENVIRONMENT
    #####################################################
    def setPRO(self,env):
        if env=="PROD" and self.lower==True : # old
            self.setOldPath()
        else:                         # New
            self.setNewPath(env)

    #===================================================#
    #                       TRIGGERS                    #
    #===================================================#

    def Ctrl_CC(self,data):
        test=True
        if data.isalpha() or len(data)!=4:
            test=False
            try:
                while test == False:
                    data=input(print("Entrer le code client :"))
                    if data.isdigit() and len(data)==4:
                        test=True
            except KeyboardInterrupt as e:
                print("Annulation de la saisie")
        return (test,data)

    def Ctrl_CA(self,data):
        test=True
        if 2>=len(data) and len(data)<4:
            test=False
            try:
                while test == False:
                    data=input(print("Entrer le code appli :"))
                    if 3<=len(data)<=4 :
                        test=True
            except KeyboardInterrupt as e:
                print("Annulation de la saisie")
        return (test,data)

    #===================================================#
    #                   SEARCH & FOUND                  #
    #===================================================#

    # DO SEARCH FOREACH LINE DATA
    #####################################################
    def find_data_pro(self,profile):
        # lecture du fichier et stockage dans la variable
        pro=open(profile,"r")
        data_pro=pro.read()
        pro.close()
        # mise au format et recherche ligne
        data_pro=data_pro.splitlines()
        #switch pour les cas voulu
        for k in data_pro:
            self.search_data(k)

    # SEARCH WHICH DATA TO PICK UP
    #####################################################
    def search_data(self,arg):
        wanted=['IP_Serveur_Mysql_P','Table_Mysql','Base_Mysql','FICHIER_CHRONO','login','password','Mysql_Server','Mysql_Login','Mysql_Pass ','Mysql_Database ','URL_OKORO','PASS_OKORO','USER_OKORO']
        for j in wanted:
            if re.search(j,arg,re.IGNORECASE):
                self.extract(arg)

    # UPDATE CURRENT INSTANCE WITH DATA FOUNDED
    #####################################################
    def extract(self,row):
        valu=row.split("=")
        print("value {} found = {}".format(valu[0],valu[1]))
        self.set_Data(valu[0],valu[1])                              # update data
        self.setClient()                                            # update client

    #===================================================#
    #                 MAIN FUNCTIONS                    #
    #===================================================#

    # SEARCH WITH EXTENSION & ENVIRONMENT GIVEN
    #####################################################
    def searchIt(self,bt,env):
        self.lower=bt
        self.setPRO(env)
        tmp=self.get_Path()
        print("tmp = {}".format(tmp))
        try:
            os.chdir(tmp)
            if os.path.isfile(self.get_File()):
                global test
                test=True
                self.env=env
                self.find_data_pro(self.get_File())
        except Exception as e:
            print("Fichier introuvable : "+str(e))

    # SEARCH WITH ALL CASES POSSIBLE
    #####################################################
    def doIt(self):
        # var test trouve
        global test
        test=None

        # test INT
        self.searchIt(False,'INT')
        self.searchIt(True,'INT')
        # test recette
        self.searchIt(False,'REC')
        self.searchIt(True,'REC')
        # test PRP
        self.searchIt(False,'PRP')
        self.searchIt(True,'PRP')
        # test prod
        self.searchIt(False,'PROD')
        self.searchIt(True,'PROD')

        # Not Found or not Exist
        if test == None:
            print("Erreur : le PRO n'existe pas ou n'a pas pu être trouvé.")

#===================================================#
#                   TEST UNITAIRE                   #
#===================================================#

# Test class
if __name__ == '__main__':
    print("CREATION OBJET")
    pt=PRO("","") # a vide
    #pt=PRO("9552","805")
    print("TOSTRING INIT")
    pt.toString()
    print("SET FILE <=== || ===> SET CC/CA")
    #pt.set_CA("123")
    #pt.set_CC("7896")
    print("DO IT + ToString ===>")
    pt.doIt()
    pt.toString()
    print("CHECK DATA LIST KEYS")
    print(pt.get_Data_Value())
    print(pt.get_Data_Key())
    print("CHECK SEARCH INTO DATA")
    print(pt.get_Data_By_Key("Table_Mysql"))
    print(pt.get_Data_By_Position(3))
    print(pt.get_Data_By_RegKey("LoGIn"))

"""
#       HOW TO USE FUNCTIONS =>

##################################################

    p=PRO() =>
    p.doIt() =>
    p.get_Data_By_Key() ;

    $ New Instance PRO
    $ Get all informations needs
    $ Show a data founded

##################################################

"""

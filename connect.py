import mysql.connector
import pickle
import os
import re

class Connexion:

    #===================================================#
    #                   CONSTRUCTEUR                    #
    #===================================================#

    def __init__(self, host, user, passwd, database):
        self.__host=host
        self.__user=user
        self.__passwd=passwd
        self.__database=database
        self.__status=None
        self.ext=".cnx"
        self.autoConnect()

    #===================================================#
    #                   ACESSORS GET                    #
    #===================================================#

    def get_Host(self):
        return(self.__host)

    def get_User(self):
        return(self.__user)

    def get_Passwd(self):
        return(self.__passwd)

    def get_Database(self):
        return(self.__database)

    def get_Status(self):
        return(self.__status)

    # ALIAS FOR USING A MYSQL CONNECTION
    #####################################################
    def useConnect(self):
        return self.get_Status()

    #===================================================#
    #                   ACESSORS SET                    #
    #===================================================#

    def set_Host(self,data):
        self.__host=data

    def set_User(self,data):
        self.__user=data

    def set_Passwd(self,data):
        self.__passwd=data

    def set_Database(self,data):
        self.__database=data

    def set_Status(self,data):
        self.__status=data

    # CASE FOR SETTING ATRTIBUTES
    #####################################################
    def set(self,i,data):
        if i=="Host": self.set_Host(data)
        elif i=="User": self.set_User(data)
        elif i=="Passwd": self.set_Passwd(data)
        elif i=="Database": self.set_Database(data)


    # ASK THE USER ABOUT DATA NEEDED
    #####################################################
    def giveData(self):
        needed=["Host","User","Passwd","Database"]
        for i in needed:
            tmp=input(print(i))
            self.set(i,str(tmp))
        self.doConnect()


    # DO THE MYSQL CONNECTION
    #####################################################
    def autoConnect(self):
        if len(self.get_Host())>0 or len(self.get_User())>0 or len(self.get_Passwd())>0 or len(self.get_Database())>0:
            self.set_Status(mysql.connector.connect(host=self.get_Host(),user=self.get_User(),passwd=self.get_Passwd(),database=self.get_Database()))

    #===================================================#
    #                       TRIGGERS                    #
    #===================================================#

    def isConnected(self):
        # not ok => True if self.get_Status() != None else False
        if self.get_Status() != None:
            return True
        else:
            return False

    def isEstablished(self):
        if self.isConnected():
            tmp="CONNECTED"
        else:
            tmp="FAILED"
        return print("Status connexion : "+tmp)

    def isFileExist(self,target):
        return os.path.exists(target)

    #===================================================#
    #                 MAIN FUNCTIONS                    #
    #===================================================#

    # DO AND RETURN THE CONNECTION TO USE
    #####################################################
    def doConnect(self):
        self.autoConnect()
        return self.useConnect()

    # FREE THE CURRENT CONNEXION
    #####################################################
    def release(self):
        self.get_Status.close()
        self.set_Status(None)

    # PRINT ALL VARIABLES
    #####################################################
    def toString(self):
        return("BASE = {} || USER = {} || PASS = {} || HOST = {} || ETAT = {} || EXTENSION = {}".format(self.get_Database(), self.get_User(), self.get_Passwd(), self.get_Host(), self.get_Status(),self.ext))

    # CONNEXION AS A BINARY FILE
    #####################################################
    def saveConnexion(self):
        data={}
        data["host"]=self.get_Host()
        data["user"]=self.get_User()
        data["passwd"]=self.get_Passwd()
        data["base"]=self.get_Database()

        # REGISTER AS NEW FILE
        #################################################
        mode="ab"
        if self.isFileExist(self.get_Database()+self.ext):

        # OVERWRITE IF EXIST ALREADY
        #################################################
            mode="wb"
        with open(self.get_Database()+self.ext,mode) as file:
            fp=pickle.Pickler(file)
            fp.dump(data)
        if file.closed:
            print("SAVE DONE")


    # DELETE BINARY FILE
    #####################################################
    def deleteConnexion(self):
        if self.isFileExist(self.get_Database()+self.ext):
            os.remove(self.get_Database()+self.ext)
            print("FILE {} DELETED".format(self.get_Database()))
        else:
            print("FILE NOT FOUND")


    # RETURN THE DATA STORED ON THE FILE
    #####################################################
    def readFile(self,target): #
        #print("READ : "+target)
        if os.path.exists(target+self.ext):
            with open(target+self.ext,"rb") as file:
                tmp=pickle.Unpickler(file)
                tmp=tmp.load()
                return tmp
        else:
            print("FILE NOT FOUND")


    # AFFECT TO CURRENT CONNEXION DATA FROM FILE
    #####################################################
    def loadFile(self,target):
        #print("LOAD : "+target)
        tmp=self.readFile(target)
        #print(tmp)
        self.set_Database=tmp["base"]
        self.set_Host=tmp["host"]
        self.set_Passwd=tmp["passwd"]
        self.set_User=tmp["user"]
        print("FILE LOADED")


    # RETURN ALL CONNEXIONS FOUNDED
    #####################################################
    def listConnexions(self):
        repert=os.listdir(".")
        found=[]
        for i in repert:
            if i.endswith("cnx"):   # re.findall("[\Wcnx$]",i): no result with regex
                found.append(i)
        return found


    # LIST ALL FOUNDED CONNEXION FILES
    #####################################################
    def showAllConnexion(self):
        all=self.listConnexions()
        if all!=None:
            for i,j in enumerate(all):
                print(i,j)
        else:
            print("NO CONNEXION FILES FOUNDED")


    # ASK THE USER WHICH CONNEXION FILES HE WANT TO USE
    #####################################################
    def selectConnexion(self):
        print("LISTE DES CONNEXIONS TROUVES :")
        avail=self.listConnexions()
        if len(avail)!=0:
            test=True
            self.showAllConnexion()
            while test:
                tmp=int(input("Quelle connexion voulez-vous utiliser ? "))
                if tmp>=0 and tmp<=len(avail):
                    self.loadFile(avail[tmp].replace(".cnx",""))
                    self.useConnect()
                    print('TEST CONNEXION : '+self.get_Database())
                    self.isEstablished()
                    test=False
                else:
                    print("FILE NOT FOUNDED : TRY AGAIN")
        else:
            print("NO CONNEXION FILES FOUNDED")

#===================================================#
#                   TEST UNITAIRE                   #
#===================================================#

if __name__ == '__main__':
    print("============ TEST CONNEXION ==============")
    c2 = Connexion("127.0.0.1","root","root","test_gegen")
    print(c2.doConnect())
    print(c2.isConnected())
    print(c2.toString())

    mycursor = c2.get_Status().cursor()
    req1="SELECT * FROM indexfiche_calendrier"

    mycursor.execute(req1) #OK #mycursor.execute("SELECT * FROM personnage")  # OK
    myresult = mycursor.fetchall()

    for x in myresult:
      print(x)

    print("========== FILE MANAGEMENT ===============")

    c2.saveConnexion()
    c2.readFile(c2.get_Database())
    c2.loadFile(c2.get_Database())
    print(c2.listConnexions())
    c2.showAllConnexion()
    c2.selectConnexion()
    #c2.deleteConnexion()

"""
#       HOW TO USE FUNCTIONS =>

##################################################

    c=Connexion(args *) =>
    c.listConnexions() ;

    $ New Connexion with settings (auto-connect)
    $ Check all connexion to pick on

##################################################

"""
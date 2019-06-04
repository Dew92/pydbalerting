import requests
import connect

class ExecRequest:
    def __init__(self):
        self.__cursor=None       # cursor from Connexion
        self.__request=None      # request.MakeRequest Object
        self.cmpt=0                   # count number of resultat

    def set_Cursor(self,data):
        self.__cursor=data

    def get_Cursor(self):
        return self.__cursor

    def set_Request(self,data):
        self.__request=data

    def get_Request(self):
        return self.__request

    def configure(self,cu,rq):
        self.set_Cursor(cu)
        self.set_Request(rq)

    def doIt(self):
        try:
            print(self.get_Cursor().execute(self.get_Request().get_it()))
            tmp=self.get_Cursor().execute(self.get_Request().get_it()) #OK
            myresult = tmp.fetchall()

            for x in myresult:
              print(x)# ligne
              print(type(x))#tuple
              print(x[0])
              print(x[1])# 2eme element
        except Exception as e:
            print("Exception {} : {}".format(type(e),e))

    def doItOnce(self):
        try:
            print(self.get_Cursor().execute(self.get_Request().useIt()))
            tmp=self.get_Cursor().execute(self.get_Request().useIt())
            myresult=tmp.fecthone()
            print("{} : {}".format(myresult,tmp))
        except Exception as e:
            print("Exception {} : {}".format(type(e),e))

    def toString(self):
        return ("Cursor : {} || Request : {}".format(self.get_Cursor(),self.get_Request(), ))


if __name__ == '__main__':
    # prepare
    query1=ExecRequest()

    maria_co=connect.Connexion("127.0.0.1","root","root","test")
    rq=requests.MakeRequest("SELECT","personnage")
    rq.set_Elements("*")
    mydb=maria_co.useConnect()
    mycursor = mydb.cursor()

    print("TEST ------- QUERY")
    print(query1.toString())
    print("TEST ========= CONFIG =>")
    query1.configure(maria_co.useConnect().cursor(),rq)
    print("TEST ===> ToString")
    print(query1.toString())
    print("TEST ====> Request")
    print(query1.get_Request().toString())

    # establish

    print(maria_co.toString())
    print("Status connexion : "+str(maria_co.isConnected()))

    print("TEST ====> GET ALL VARS")
    print("{}:{}".format(query1.get_Cursor(),query1.get_Request().get_it()))

    # prepare request
    req1="SELECT * FROM personnage"

    print(query1.get_Cursor().execute(req1))

    print("TEST --- ONCE ---")
    query1.doItOnce()

    print("TEST --- ALL ---")
    query1.doIt()

"""
#       HOW TO USE FUNCTIONS =>

##################################################

    need :
    d
    $

    e=ExecRequest() =>
    e.doIt() => p.get_Data_By_Key()

    $ New Instance PRO
    $ Get all informations needs
    $ Show a data founded

##################################################

"""
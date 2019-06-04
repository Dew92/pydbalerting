import connect

class MakeRequest:

    #===================================================#
    #                   CONSTRUCTEUR                    #
    #===================================================#

    def __init__(self, action, table):
        self.__action=action                    # select, update, delete, describe
        self.__elements=None                    # * or few columns or DISTINCT(ID) // SUM(prix)
        self.__table=table                      # Table SQL
        self.__conditions=None                  # WHERE args *
        self.__it=None                          # Complete request
        self.bind()                             # Do default req

    """

    exemples :

    SELECT * FROM truc WHERE machin="toto"
    PDATE table_cle SET machin="123" WHERE bidul IN ("456","789)"
    DELETE FROM table_aaaa WHERE condition="OK"

    """

    #===================================================#
    #                   ACESSORS GET                    #
    #===================================================#

    def get_Action(self):
        return(self.__action)

    def get_Elements(self):
        return(self.__elements)

    def get_Table(self):
        return(self.__table)

    def get_Conditions(self):
        return(self.__conditions)

    def get_it(self):
        return(self.__it)

    def useIt(self):
        return self.get_it()

    # ALIAS PRINTING REQUEST
    #####################################################
    def show(self):
        print(self.get_it())

    #===================================================#
    #                   ACESSORS SET                    #
    #===================================================#

    def set_Action(self,data):
        data=data.upper()
        allow=["SELECT","EXPLAIN","UPDATE","DESCRIBE","DELETE"]
        for i in allow:
            if data==i:
                self.__action=dat
        self.bind()

    def set_Elements(self,data):
        self.__elements=data
        self.bind()

    def set_Table(self,data):
        self.__table=data
        self.bind()

    def set_Conditions(self,data):
        self.__conditions=" WHERE "+data
        self.bind()

    # BUILD SQL REQUEST WITH DATA GIVEN
    #####################################################
    def set_it(self,action,elements,table,conditions):
        struct=action+" "
        if action=='SELECT':
            if elements != None:
                struct+=elements+" "
            struct+="FROM "+table
            if conditions!=None:
                struct+=conditions
        elif action=='UPDATE':
            struct+=table+" "
            if elements != None and conditions != None:
                struct+=elements
                struct+=conditions
        self.__it=struct
    # update indexfiche_production set etat='49', commentaire='' where enreg=''

    # BUILD SQL REQUEST WITH SPECIFIC NEEDS
    #####################################################
    def setup(self,elem,where):
        self.set_Elements(elem)
        self.set_Conditions(where)
        self.bind()

    #===================================================#
    #                 MAIN FUNCTIONS                    #
    #===================================================#

    # BUILD SQL REQUEST WITH CURRENTE DATA
    #####################################################
    def bind(self): # create full request
        self.set_it(self.get_Action(),self.get_Elements(),self.get_Table(),self.get_Conditions())

    # SHOW ALL VALUES FROM CURRENT INSTANCE
    #####################################################
    def toString(self):
        return("Action = {} || elements = {} || table = {} || conditions = {} || Full = {}".format(self.get_Action(), self.get_Elements(), self.get_Table(), self.get_Conditions(), self.get_it()))

#===================================================#
#                   TEST UNITAIRE                   #
#===================================================#

if __name__ == '__main__':
    # prepare conditions test
    maria_co=connect.Connexion("127.0.0.1","root","root","test_gegen")
    print(maria_co.toString())
    maria_co.isEstablished()
    # current connection
    mydb=maria_co.useConnect()

    # prepare cursor
    mycursor = mydb.cursor()

    # new request object
    rq=MakeRequest("SELECT","indexfiche_calendrier")
    rq.set_Elements("*")
    rq.show()
    print(rq.toString())

    # exec request
    try:
        mycursor.execute(rq.useIt()) #OK
        myresult = mycursor.fetchall()
        for x in myresult:
          print(x[1])# 2eme element
    except Exception as e:
        print("Exception {} : {}".format(type(e),e))


"""
#       HOW TO USE FUNCTIONS =>

##################################################

    need :  Connection Oject c.useConnect()

    $ prepare connexion to use

    mr=MakeRequest() =>
    mr.configure() =>
    data=mr.execute(rm.useIt()) =>
    dataF=data.fetchall() ;

    $ New Instance MakeRequest(argv *)
    $ Give additional info if needed
    $ Do request
    $ Store resultat from request

##################################################

"""
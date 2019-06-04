import connect
import requests
import execReq
import pro

try:
    # TEST
    test=pro.PRO("1464","1354")  #init NULL = CC=7896,CA=123
    test.set_CC("7896")
    test.set_CA("123")
    test.doIt()
    # PRO PRET => MAKE CO
    tc=connect.Connexion(test.get_Data_By_Key("Mysql_Server"),test.get_Data_By_Key("Mysql_Login"),test.get_Data_By_Key("Mysql_Login"),test.get_Data_By_Key("Base_Mysql"))
    tc.isEstablished()
    # CO PRET => CURSOR MAKE
    co=tc.useConnect()
    cur=co.cursor()
    # CURSOR PRET => MAKE REQ
    tr=requests.MakeRequest("SELECT",test.get_Data_By_Key("Table_Mysql"))
    tr.setup("*","")
    q=execReq.ExecRequest()
    q.configure(co,q)
    # ALL READY
    try:
        cur.execute(tr.useIt()) #OK
        myresult = cur.fetchall()
        print("RECORDS = "+str(len(myresult)))
#        z=1
        for x in myresult:
            print(x)
#            print("login nÂ°{}={}".format(z,x[1]))# 2eme element
#            z+=1
    except Exception as e:
        print("Exception {} : {}".format(type(e),e))

except Exception as e:
    print("Exception {} : {}".format(type(e),e))

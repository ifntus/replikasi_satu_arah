import pymysql.cursors
import time

print("Program sedang berjalan...")
while (1):
    try:
        connection_to_toko = 1
        try:
            connToko = pymysql.connect(
                host='localhost', # deklarasi nama host
                user='root', # deklarasi nama user database
                passwd='', # deklarasi password database
                port=3306, # deklarasi port yang digunakan pada database
                db='db_toko')
            curToko = connToko.cursor()
        except:
            continue

        try:
            connBank = pymysql.connect(
                host='localhost', # deklarasi nama host
                user='root', # deklarasi nama user database
                passwd='', # deklarasi password database
                port=3306, # deklarasi port yang digunakan pada database
                db='db_bank')
            curBank = connBank.cursor()
        except:
            continue
            connection_to_toko = 0
            
        sql_select = "SELECT * FROM tb_invoice"
        curBank.execute(sql_select)
        invoice = curBank.fetchall()

        sql_select = "SELECT * FROM tb_integrasi"
        curBank.execute(sql_select)
        integrasi = curBank.fetchall()
        
        #update
        if (invoice != integrasi):
            print("-- UPDATE DETECTED --")
            for data in invoice:
                for dataIntegrasi in integrasi:
                     if (data[0] == dataIntegrasi[0]):
                        if (data != dataIntegrasi):
                            val = (data[2], data[0])
                            update_integrasi_bank = "update tb_integrasi set status = %s where id_invoice = %s"
                            curBank.execute(update_integrasi_bank, val)
                            connBank.commit()
                            if (connection_to_toko == 1):
                                update_integrasi_toko = "update tb_integrasi set status = %s where id_invoice = %s"
                                curToko.execute(update_integrasi_toko, val)
                                connToko.commit()
                                update_transaksi_toko = "update tb_invoice set status = %s where id_invoice = %s"
                                curToko.execute(update_transaksi_toko, val)
                                connToko.commit()
    except (pymysql.Error, pymysql.Warning) as e:
        print(e)
    time.sleep(5)
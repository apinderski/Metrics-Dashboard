from datetime import datetime

def Calculate_Defect_Density(c, conn, LoC, Open_BF):
    if (LoC == 0):
        Defect_Density = 0
    else:
        Defect_Density = Open_BF / LoC
    return Defect_Density

def Main(c, conn, days):
    #First Pull down all of the values and loop through them one day at a time
    
    #Once table exists, pull down data here#

    #Now loop!
    for day in days:
        #print(day)

        Num_Of_Open_BF = "" #Fill this with the total number of open BF on that date
        Num_Of_Open_FR = "" #Fill this with the total number of open FR on that date
        Num_Of_Open_T = "" #Fill this with the total number of open T on that date
        Num_Of_Closed_BF = "" #Fill this with the total number of closed BF on that date
        Num_Of_Closed_FR = "" #Fill this with the total number of closed FR on that date
        Num_Of_Closed_T = "" #Fill this with the total number of closed T on that date
        DeDen_Open_BF = "" #Fill this with defect density of BF
        DeDen_Open_FR = "" #Fill this with defect density of FR
        DeDen_Open_T = "" #Fill this with defect density of T
        IssSpoil_Open_BF = "" #Fill this with issue spoilage of BF
        IssSpoil_Open_FR = "" #Fill this with issue spoilage of FR
        IssSpoil_Open_T = "" #Fill this with issue spoilage of BT
        Lines_Of_Code = "" #Store the lines of code on that specifc date

        day = datetime.strptime(str(day)[:10], "%Y-%m-%d")

        c.execute("SELECT COUNT(*) FROM ISSUES WHERE date(updated_at) <= date('" + str(day) + "');")
        # AND BF = 'True' AND state = 'Open'
        try:
            Num_Of_Open_BF = int(c.fetchall()[0][0])
        except:
            Num_Of_Open_BF = 0
        #print(Num_Of_Open_BF)
        conn.commit()

        c.execute("select total_lines from LINES_OF_CODE_NUM_OF_CHARS where date(date) = (select max(date(date)) from LINES_OF_CODE_NUM_OF_CHARS where date(date) <= date('" + str(day) + "'));")
        try:
            LOC = int(c.fetchall()[0][0])
        except:
            LOC = 0
        #print(LOC)
        conn.commit()

        Defect_Den = Calculate_Defect_Density(c, conn, LOC, Num_Of_Open_BF)
        #print(Defect_Den)

        sql = "INSERT INTO DEFECT_DENSITY (date, DD) VALUES (?,?);"
        c.execute(sql, (str(day), str(Defect_Den)))
        conn.commit()





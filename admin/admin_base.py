import mysql.connector as sql

class AdminBase:

    def __init__(self):
        try:
            self.connection = sql.connect(
                host='localhost',
                user='root',
                password='',
                database='dbfm1'
            )
            self.cursor = self.connection.cursor()
            print("✅ Database Connection Successful")
            return True
        except sql.Error as e:
            print("❌ Failed to connect to database:", e)
            return False


    def select_theatre(self):
        theatre_id = input("\n🔹 Enter Theatre ID to manage: ").upper()
        query = "SELECT Theatre_ID FROM theatre;"
        self.cursor.execute(query)
        theatres = self.cursor.fetchall()# list in tuple format
        
        theatre_ids = [row[0] for row in theatres]# list formate convert
         
        if theatre_id in theatre_ids :
            return theatre_id
        else : raise Exception(f'No theater-id with {theatre_id}')

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
    # print("🔴 Database Connection Closed.")
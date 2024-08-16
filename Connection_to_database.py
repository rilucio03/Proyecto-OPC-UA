import mysql.connector

class Connection:
    def connection_database():
        try:
            connection = mysql.connector.connect(user = 'uutnrfzk8jttqc1i',
                                                password = '7CjSXhgEymyKgfgBD9Ut',
                                                host = 'beoh6nl3c3a07jj7vev9-mysql.services.clever-cloud.com',
                                                database = 'beoh6nl3c3a07jj7vev9',
                                                port = '3306')
            print ("Successful connection")
            
            return connection
        
        except mysql.connector.Error as error:
            print("Error connecting to database {}".format(error))
            
            return connection
    
    connection_database()
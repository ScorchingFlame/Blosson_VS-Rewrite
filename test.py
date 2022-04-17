from datetime import datetime

def run(n: bool, ip, port: int, username, password):
    if n:
        message = f"""                Voting System application By Ritheesh
!!READ THIS BEFORE DOING ANYTHING!!     
        Creating/Inserting Voter:
                    - Remember not a Create/Insert a Voter With a Same Admission ID as Others
                    * Excel Inserting:
                        - If you Get Error When Inserting Excel Sheet, Try These:
                            : Check IF the File Format Is .xlsx
                            : Check If the Coloum Have The Same Text As in Example Sheet 
                            : Check If There is a Alphabet In Admission Number or STD               
                
        No Network Found:
                    - This Error means that no network is found (Not Internet)
                    Things to Do:
                        * Checking The Ethernet Cable Connection or Wifi (Internet is optional, This Application also works without internet)
                        * If You Cant Get A Network, You can also Host This Application in Cloud (Contact Ritheesh)    
        NOTE: 
        - The Application Is Not WSGI or Async, Meaning that This Application Can Only Handel 1 request at a time.  
        - This Application Is Made With Python, Flask and Socket-IO

Admin Login:            
    Username: {username}
    Password: {password}
Links:
    Voting Page: http://{ip}:{port}/
    Admin Page:  http://{ip}:{port}/admin
    Admin Login: http://{ip}:{port}/admin/login 
    Live Feed:   http://{ip}:{port}/admin/live-feed

Webserver Started At {datetime.now().ctime()}"""
        print(message)
    else:
        message = f"""                Voting System application By Ritheesh
!!READ THIS BEFORE DOING ANYTHING!!     
        Creating/Inserting Voter:
                    - Remember not a Create/Insert a Voter With a Same Admission ID as Others
                    * Excel Inserting:
                        - If you Get Error When Inserting Excel Sheet, Try These:
                            : Check IF the File Format Is .xlsx
                            : Check If the Coloum Have The Same Text As in Example Sheet 
                            : Check If There is a Alphabet In Admission Number or STD               
                
        No Network Found:
                    - This Error means that no network is found (Not Internet)
                    Things to Do:
                        * Checking The Ethernet Cable Connection or Wifi (Internet is optional, This Application also works without internet)
                        * If You Cant Get A Network, You can also Host This Application in Cloud (Contact Ritheesh)    
        NOTE: 
        - The Application Is Not WSGI or Async, Meaning that This Application Can Only Handel 1 request at a time.  
        - This Application Is Made With Python, Flask and Socket-IO

!!!!!!!!!!!!!!!!!!!!!!!!
!!! NO NETWORK FOUND !!!
!!!!!!!!!!!!!!!!!!!!!!!!"""
        print(message)

if __name__ == '__main__':
    run(True, '127.0.0.1', 1221, 'idk', 'idk')
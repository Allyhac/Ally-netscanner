import socket
import argparse


def scan(ip,verbose,start_port,end_port,full):
    print('''
        ============================
          🌸Ally Network Scanner🌸
        ============================
          ''')
    print('''-------------------------------------------------''')
    print(f'[+]Scanning {ip} ...')
    print(f'[+]ports:{start_port}-{end_port}')
    print('''-------------------------------------------------
''')

    x=[]
    if full:
        start_port = 1
        end_port = 65535
      
    if end_port > 65535:
        print('[!]The end port cannot be greater than 65535!!!')
        an=input('Do y0u want to set end port to 65535? (y/n):  ')
        if an.lower() == 'y':
            end_port = 65535
        else:
            print('setting the port to default(1024)')
            end_port = 1024

    for port in range(start_port,end_port+1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f" ✨ Trying port: {port} [{port-start_port + 1}/{end_port-start_port + 1}]", end="\r")
            s.settimeout(0.5)
            try:
                result=s.connect_ex((ip,port))
                if result == 0:
                    try:
                        service = socket.getservbyport(port,'tcp')
                    except:
                        service = 'uknown'
                    try:
                        banner = s.recv(1024).decode().strip()
                        banner= banner.replace('\n','').replace('\r','')
                        try:
                            s.send(b"HEAD / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n")
                            data = s.recv(1024)
                            if data:
                                banner=data.decode(errors='ignore').strip()
                                banner = banner.splitlines()[0]
                        except:
                            pass        
                    except:
                        banner = 'No Banner response'           
                    print(f'[OPEN]✅ {port} | service: {service} | Banner: {banner}' )
                    x.append(port)
                elif result != 0 and verbose:
                    print(f'[CLOSED] {port}')
                
                        
            except Exception as e:
                print(e)            
    print(f'''
        ----------------------------
        ✨ Scan Complete!
        Found {len(x)} open ports: {x}
        ============================''')
            
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ally network scanner.. you can scan for open ports and services')
    parser.add_argument('-i','--ip',help='The ip address to scan.The default is localhost',default='127.0.0.1')
    parser.add_argument('-v','--verbose',help='for verbosity use -v(optional)',action='store_true')
    parser.add_argument('-s','--start_port',help="The starting port to scan the network",default=1,type=int)
    parser.add_argument('-e','--end_port',help="The final port to scan the network",default=1024,type=int)
    parser.add_argument('-f','--full',help='for full scan use -f',action='store_true')

    
    
    args = parser.parse_args()
    scan(args.ip,args.verbose,args.start_port,args.end_port,args.full)
#!/bin/python3.6
import re
class Zone(object):
       ''' 
        DNS zone
       '''
       def __init__(self, name, ty, filepath, allowupdate, forwarders, forward):
               self.name=name
               self.ty = ty
               self.filepath = filepath
               self.allowupdate = allowupdate
               self.forwarders = forwarders
               self.forward = forward

class Named(object):
        '''
        named new zone file
        '''
        def __init__(self, name, ttl, ip):
                self.name = name
                self.ttl = ttl
                self.ip = ip

                


def read_zone():
        file = open("/var/named/chroot/etc/named.rfc1912.zones")
        while 1:
                lines = file.readlines(10000)
                if not lines:
                        break
                str = []
                for line in lines:
                        if re.search('//',line):
                                print("注释解析")
                        else:
                                if re.search('.',line):
                                        str.append(line.strip())
                                else:
                                        pass
                zone_list = []
                name=ty=filepath=allowupdate=forwarders=forward= ""
                pattern = re.compile(r'(?<=").*?(?=")',re.I)
                for st in str:
                        if "zone" in st and "IN" in st:
                                name =pattern.findall(st)[0] 
                        elif "type" in st:
                                ty = st
                        elif "file" in st:
                                filepath = st
                        elif "allow-update" in st:
                                allowupdate = st
                        elif "forwarders" in st:
                                forwarders = st
                        elif "forward" in st:
                                forward = st
                        elif "};" in st:
                                zone_list.append(Zone(name,ty,filepath,allowupdate,forwarders,forward))
                                name=ty=filepath=allowupdate=forwarders=forward= ""
                        else:
                                 pass
                

        return zone_list 

def insert_zone(zone):
        seq = ["zone \""+zone.name+"\" IN {\n","        type "+zone.ty+";\n", "        file \""+zone.name+".zone\";\n","};\n" ]
        fo = open("/var/named/chroot/etc/named.rfc1912.zones","a+")
        fo.writelines(seq)
        fo.close()
def delete_zone(zone_name):
        with open("/var/named/chroot/etc/named.rfc1912.zones","r") as f:
                lines = f.readlines()

        with open("/var/named/chroot/etc/named.rfc1912.zones","w") as f_w:
                flag = 1
                for line in lines:
                        if  zone_name in line :
                                flag +=1
                                print(flag)
                        else:
                                if flag ==2 :
                                        flag -= 1
                                        print(flag)
                                else:
                                        f_w.write(line)
        



def create_named(d1bi):
        fo = open("/var/named/chroot/var/named/"+d1bi.name+".fuyoukache.com.zone","w")
        seq = ["$TTL "+d1bi.ttl+"\n", "@ IN SOA  dns."+d1bi.name+".fuyoukache.com.     dnsadmin."+d1bi.name+".fuyoukache.com. (\n", "                                      0       ; serial\n", "                                      1D      ; refresh\n", "                                      1H      ; retry\n", "                                      60      ; expire\n", "                                      3H )    ; minimum\n", "     IN      NS      "+d1bi.name+".fuyoukache.com.\n", "     IN      MX      10      mail\n", d1bi.name+".fuyoukache.com.       A       "+d1bi.ip+"\n"] 
        fo.writelines(seq)

        fo.close()
        




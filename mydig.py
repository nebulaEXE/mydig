import sys
import dns.message
import dns.query
import dns.name
import dns.flags
import time

if len(sys.argv) != 2: #CHECK IF THERE WAS AN ARG GIVEN TO THE PROGRAM
    print("Incorrect usage. Please enter a URL")
    exit()

ROOT_IP = '198.41.0.4' #Root Server IP

TARGET = dns.name.from_text(sys.argv[1]) #Target Website we want to query

time_begin = time.time()
current_time = time.localtime()
root_request = dns.message.make_query(TARGET, 'A') #Make a query to the root server
root_response = dns.query.udp(root_request, ROOT_IP)


print("QUESTION SECTION: \n" + root_request.question[0].to_text(), "\n") #Question Section (which is the query request of the website)

root_response = root_response.additional[0].to_text().split()

TLD_IP = root_response[4] #Grab TLD IP Address from response

tld_request = dns.message.make_query(TARGET, 'A')
tld_response = dns.query.udp(tld_request, TLD_IP)



if tld_response.additional == []: #Additional Resolution, if no response in ANSWER or ADDITIONAL SECTION we 
                                  #requery the IP Address in Authority back to the root
    auth_temp = tld_response.authority[0].to_text().split()
    AUTH_IP = auth_temp[4] #IP OF SERVER IN AUTHORITY SECTION
    authority_root_request = dns.message.make_query(AUTH_IP, 'A')
    authority_root_response = dns.query.udp(authority_root_request, ROOT_IP)

    temp_var = authority_root_response.additional[0].to_text().split()[4] #IP OF THE AUTHORITY ADDRESS
    temp_request = dns.message.make_query(AUTH_IP, 'A')
    temp_response = dns.query.udp(temp_request, temp_var)

    temp_var2 = temp_response.additional[0].to_text().split() #Additional Server Response of previous Querys
    if temp_var2[3] != 'A': #Check if the address given was IPV4, if not grab the next address
        temp_var2 =  temp_response.additional[1].to_text().split()
   
    TEMP_IP = temp_var2[4]
    
    temp2_root_request = dns.message.make_query(TARGET, 'A') #After resolution query the target address with the authoritative name server's address
    temp2_response = dns.query.udp(temp2_root_request, TEMP_IP)

    final_IP = temp2_response.answer[0].to_text() #Final IP given in Answer Section



    print("ANSWER SECTION: \n" + final_IP)
    time_end = time.time()
    print("Query time:", round(time_end - time_begin, 3), "seconds.")
    print("WHEN: ", time.asctime(current_time))
    exit()




tld_response_temp = tld_response.additional[0].to_text().split()


if tld_response_temp[3] != 'A': #Check if IP Address is IPV4
    tld_response_temp = tld_response.additional[1].to_text().split()

NS_IP = tld_response_temp[4]

ns_request = dns.message.make_query(TARGET, 'A')
ns_response = dns.query.udp(ns_request, NS_IP)

print("ANSWER SECTION: \n" + ns_response.answer[0].to_text())
time_end = time.time()
print("Query time:", round(time_end - time_begin, 3), "seconds.")
print("WHEN: ", time.asctime(current_time))
exit()

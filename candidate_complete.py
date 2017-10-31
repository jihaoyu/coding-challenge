## Program Name : Finding Political Donors
## Created On   : 30-10-2017
## Author 	: Jihao Y.  
## Version 	: 1.0

##medianvals_by_zip.txt
    ##Other_ID should be empty
    ##Consider Transaction_DT
    ##Consider only the first 5 chars from the 9 char zip code, ignore if empty or less than 5 chars
    ##Ignore record if CMTE_ID or TRANSACTION_AMT are empty

##medianvals_by_date.txt
    ##Other_ID should be empty
    ##Ignore Malformed Dates
    ##CMTE shouldn't be empty, Transaction Date not empty
   
    


count = 0				
zipcode_count = {}			#Dictionary that holds the count for zip code i.e. how many times a zip code has been seen earlier.
zipcode_sum = {}			#Dictionary to hold the cummulative sum for a repeating zip_code.
names = {}				#Dictionary to hold data for medianvals_by_date.

file = open(".\medianvals_by_zip.txt","w")  
file2 = open(".\medianvals_by_date.txt","w")  


with open('.\itcont.txt') as infile:
    current_sum = 0
    updated_count = 0
    for line in infile:
        line.rstrip("\n")
        count = count + 1
        values = line.split("|")
        
	#Transaction_ID empty check, CMTE_ID not empty check and TRX_AMT not empty check.
        if(values[15] == "" or values[0] != "" or values[14] != ""):           
            #print str(count) + "."
            #print "CMTE_ID: " + values[0]
            #print "ZIP CODE: " + values[10][:5]                            #Stripping to 5 digit
            #print "TRANSACTION_DT: " + values[13]			    #Transaction Date
            #print "TRANSACTION_AMT: " + values[14]			    #Transaction Amount
            
            if(values[10][:5] in zipcode_count.keys()):
                present_count = zipcode_count[values[10][:5]]
                updated_count = present_count + 1
                zipcode_count[values[10][:5]] = updated_count
            else:
                updated_count = 1
                zipcode_count[values[10][:5]] = 1

            if(zipcode_count[values[10][:5]] > 1):
                current_sum = str( int(zipcode_sum[values[10][:5]]) + int(values[14]))
                zipcode_sum[values[10][:5]] =  str( int(zipcode_sum[values[10][:5]]) + int(values[14]))
            else:
                current_sum =values[14]
                zipcode_sum[values[10][:5]] = values[14]
            #Write the data to the file --> medianvals_by_zip.txt 
            file.write(values[0]+"|"+values[10][:5]+"|"+str(int(round(float(current_sum)/float(updated_count))))+"|"+str(updated_count)+"|"+current_sum+'\n')

            #print values[0]+"|"+values[10][:5]+"|"+str(int(round(float(current_sum)/float(updated_count))))+"|"+str(updated_count)+"|"+current_sum
            
        if(values[15] == "" or (values[13] != "" and len(values[13])== 7) or  values[0] != "" or values[14] != ""):    
            
            if(values[0] in names.keys()):
                dates = names[values[0]]
                if (values[13] in dates.keys()):
                    current_list = dates[values[13]];
                    current_list[0]= current_list[0]+1
                    current_list[1]= current_list[1]+int(values[14])
                    dates[values[13]] = current_list
                else:
                    dates[values[13]] = [int(1),int(values[14])]
            else:
                datelist = {values[13]:[int(1),int(values[14])]}
                names[values[0]] = datelist
                
            
                        
    for key in names:
        for key2 in names[key]:
            #Write the data to the file --> medianvals_by_date.txt
            file2.write(key + "|" + key2 + "|" + str(names[key][key2][1]/names[key][key2][0]) + "|" + str(names[key][key2][0]) + "|" + str(names[key][key2][1]) + "\n")
	    #print key + "|" + key2 + "|" + str(names[key][key2][1]/names[key][key2][0]) + "|" + str(names[key][key2][0]) + "|" + str(names[key][key2][1]) + "\n"
            
	    
            

file.close()		    #Close file medianvals_by_zip
file2.close() 		    #Close file medianvals_by_date

print "Processing Complete"

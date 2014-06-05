#script to collect all the filenames in the ESD folder of a run 
#!/bin/bash

clear
filen=''


for i in $(cat periodH)
do
   
    
    filen="$filen""${i}"'/,'

done
echo "$filen" >lochan





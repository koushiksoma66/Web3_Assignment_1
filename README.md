# Web3_Assignment_1

## Extracting all the transaction files in the mempool
For this I imported the os library with which I could list out all the names of the files in the mempool directory using the listdir() function in os.<br>
For getting the path of mempool I first brought the mempool folder to the directory I am working on then, used 'path.abs.path(__file__)' function to get the path of current directory then used path.join(current_directory,'mempool') which gives the path of the file/folder with the name 'mempool' in the current_directory.<br>
As we can't open a file just with its name I had to use the path.join(mempool_path,file_name) function which gives the path of the file in mempool whose name is mempool_path.<br>
Open this files in reading mode using with <b>open(file_path,'r') as file:</b>  This is the best way since it automatically closes the file after exiting from its scope.<br>

## Validating the transaction
Just added all the values in vin and vout and compared them, which gives whether the transaction is valid or not.<br>
Append all the valid transaction ids in a list. As the txid of a file is its file name append the file names in the list after removing the .json extension, which is done using the split() function. It splits at everywhere it finds the splitter and stores all of them in a list. Therefore <b>file_name.split('.')</b> is a list which contains the txid as its 1st element and 'json' as its 2nd element.<br>

## Header components
time_stamp: For getting time stamp I imported time library and used the .time() function. It returns the a value in float but we want it in hex so first convert it to an integer, then apply the hex() function which converts it into hexadecimal.<br>
#### Merkel Root:
First hash all the txids in the list.<br>
Then hash the concatination of every two consecutive elements in the list. For this use 'for i in  range(0,size_of_list,2)' which takes a jump of two steps. And if the list has odd number of elements i would be the last element in the last iteration after which there is no hash to concatinate with it so, in that case i.e, if i is ever equal to the index of last element, concatinate it with itself and then hash.<br>
As we can't save all these in the actual list since we are already looping in the list, save them in a temparory list and save them to the actual list after completion of traversal of the actual list one time. <br>
Keep doing this till the size is decreased to just 1 which is the merkel root.<br>

#### Nonce:
Concatinate all the header components except nonce which is intially set to zero.<br>
Concatinate the nonce inside the loop as the header hash must keep updating along with nonce.<br>
Break the loop after the target is reached

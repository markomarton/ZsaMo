1) Share a folder on the Windoes computer, allow read/write access
   
   Right click on folder -> Properties -> Staring tab -> Click on "Share this folder on network" and "Allow network users to change my files"

2) Set password for the Windows account

3) Create a file (e.g. .detShareCredits )  on linux with username and password. Content of file should be:

~~~
   username=OTDC
   password=pw_for_win_machine
~~~

4) Change acces to .detShareCredits file: 

~~~
   chmod 600 .detShareCredits
~~~
   
5) Modify /etc/fstab (sudo needed). Add a similar line:
   
~~~
   //192.168.88.248/rnd /home/athos/Desktop/tmpMount cifs credentials=/home/athos/.detShareCredits,vers=1.0,noauto,user,rw    0   0
~~~

6) The shared directory can be mounted by: 

~~~
   mount /home/athos/Desktop/tmpMount
~~~
   This shsould not need root privileges and you should have read/write access to the shared folder. 


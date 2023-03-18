# AAA_USERS
get aaa users info from Huawei Router

you pass the routers list (csv file) throught argument in the command line
this is how csv should be:
---------------------
RouterName,IPAddress
R1,192.168.1.15
--------------------

when the script Done, it give two file The Report of aaa users and Routers list that it could not to connect.
this an exmple of the output (csv file is separated by \t):

RouterName  UserName Password	ServiceType	Level
R1	User1	$1c$;'st$,duiR$.`f`@u,J$P&gXTE-7zcObj9^8:j^82^q[{.\WJFU$	telnet ssh	3
R1	user2	%^%#~MCWKH=]gTs`8#T%Ia8ICFg~Hsgc%6,%:T8>L#pS%^%#	none	None
R1	user3	%^%#/Jf$Zr=bL1UMcqBt>vrM"Z%&4SxRM6Kkv-QP<teT%^%#	none	1

from django.test import TestCase

# Create your tests here.

'''

1.register

Blank
Blank
Please input username 

15682871716
Blank
Please input password 

1
1
Wrong username, it is neither phone nor email 

15682871716
123
Wrong password, the length of password must be not less than 6 and not more than 64 

15682871716
123456
Turn Page ...

15682871716
123456
username has existed 

//////

@
1
Wrong username, it is neither phone nor email 

1249591860@qq.com
123
Wrong password, the length of password must be not less than 6 and not more than 64 

1249591860@qq.com
123456
Turn Page ...

1249591860@qq.com
123456
username has existed 

////////////

2.login

Blank
Blank
Please input username 

15682871716
Blank
Please input password 

1
123456
Wrong username, it is neither phone nor email 

15682871719
123456
username or password wrong 

15682871716
123
Wrong password, the length of password must be not less than 6 and not more than 64 

15682871716
1234567
username or password wrong 

15682871716
12345678
Turn Page ...

//////

@
123456 
Wrong username, it is neither phone nor email 

1249591861@qq.com
123456
username or password wrong 

1249591860@qq.com
123
Wrong password, the length of password must be not less than 6 and not more than 64 

1249591860@qq.com
123456
username or password wrong 

1249591860@qq.com
12345678
Turn Page ...

////////////

3.password_forget

Blank
Blank
Please input username 

15682871716
Blank
Please input password 

1
1
Wrong username, it is neither phone nor email 

15682871716
123
Wrong password, the length of password must be not less than 6 and not more than 64 

15682871716
12345678
Turn Page ...

*Login:
15682871716
12345678
Turn Page ...

//////

@
1
Wrong username, it is neither phone nor email 

1249591860@qq.com
123
Wrong password, the length of password must be not less than 6 and not more than 64 

1249591860@qq.com
12345678
Turn Page ...

*Login:
15682871716
12345678
Turn Page ...

4.admin
*Register:
1@qq.com
123456

*Login:
1@qq.com
123456

Turn Page ...
'''


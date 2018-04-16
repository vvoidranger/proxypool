f= open('proxy_list','r+')

a=f.readlines()
print(a)


f=open('proxy_list','r+')
f.truncate()

print('b')
b=a[0]
del a[0]
for item in a:
    f.write(item)
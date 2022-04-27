import csv
from wsgiref import headers
import string
import pandas as pd
import time

class Book:
    def __init__(self,name,author,publish_time,introduce,status='0'):
        self.name=name
        self.author=author
        self.publish_time=publish_time
        self.introduce=introduce
        self.status=status

        status_book='未借出'

        self.book1=[]

        if (self.status == '0'):
            status_book='未借出'

        else:
            status_book='已借出'

        self.book1={'书籍名称':'《{}》'.format(self.name),'作者':'{}'.format(self.author),'出版日期':'{}'.format(self.publish_time),'介绍语':'{}'.format(self.introduce),'借出状态':'{}'.format(status_book)}

class BookManagerSystem:


    bookstore ={}

    global header
    header=['书籍名称','作者','出版日期','介绍语','借出状态']


    def menu(self):

        while (True):
            print('******潘伯奎图书管理系统******\n')
            print ('1.查询所有书籍\n2.添加书籍\n3.借阅书籍\n4.归还书籍\n5.删除库中书籍\n6.查询书籍状态\n7.退出系统')
            choice=input ('请输入相应的数字来选择您的操作。')
            
            if(choice == '1'):
                self.all_book()
            
            elif(choice == '2'):
                self.add_book()

            elif(choice == '3'):
                self.borrow_book()

            elif(choice == '4'):
                self.return_book()

            elif(choice == '5'):
                self.delete_book()
            
            elif(choice == '6'):
                self.inspect_book()

            elif(choice =='7'):
                print('祝您使用愉快！再见！')
                break

            else:
                print('请输入正确的指令！')
                time.sleep(1)
            

    def all_book(self):

        global join_head    
        global new_read
        #csv方法遍历
        ''' with open('bookstore.csv','r',newline='') as r:
            reader=csv.DictReader(r,fieldnames=header)
            head = reader.fieldnames
            join_head=' '.join(head)              
            print(join_head)
            for i in reader:
                print(i['书籍名称'],i['作者'],i['出版日期'],i['介绍语'],i['借出状态'],)
                '''
        #用pandas方法遍历：        
        read=pd.read_csv('bookstore.csv',encoding='gb18030',header=None,names=['书籍名称','作者','出版日期','介绍语','借出状态']) #header=None防止第一行变成头，names增加列头
        new_read=pd.DataFrame(read) #转换成data结构了
        print('潘伯奎图书馆系统书籍目录：\n')
        print(new_read)
        print('\n')

        time.sleep(1)

    def add_book(self):
        global book1
        

        book_name=input('请输入添加书籍的名称：')
        book_author=input('请输入添加书籍的作者：')
        book_publishtime=input('请输入添加书籍的出版日期：')
        book_introduce=input('请输入添加书籍的介绍语（若无可填无）')

        book=Book(book_name,book_author,book_publishtime,book_introduce)

 

        with open('bookstore.csv','r',newline='') as r:
            reader=csv.DictReader(r,fieldnames=header)
            whether_exit=0
            for i in reader:
                if ('《'+book_name+'》'  == i['书籍名称']):
                    print("书库中已经有此书籍。")
                    whether_exit=1
                    break
            
            if (whether_exit==0):      
                with open('bookstore.csv','a',newline='') as f:
                    
                    writer=csv.DictWriter(f,fieldnames=header)
                    writer.writerow(book.book1)
                    print('添加成功！') 

            time.sleep(1)
            self.all_book()



    def check_book(self,name):  #一个检查模块函数
        self.name=name

        with open('bookstore.csv','r',newline='') as r:
            reader=csv.DictReader(r,fieldnames=header)
            for i in reader:
                if (i['书籍名称'] == name):   
                    return i     
            else:
                return None


    def borrow_book(self):
        borrowbook = input('请输入书籍名称：\n')
        brbook = self.check_book(borrowbook)

        if(brbook!= None):
            if (brbook['借出状态'] == '未借出'):

                #读取资料所在的行号：这一步很重要！！！！！！！
                borrowbook_line = -1
                with open('bookstore.csv','r',newline='') as r:
                    reader=csv.DictReader(r,fieldnames=header)
                    for i in reader:
                        borrowbook_line = borrowbook_line+1
                        if (i['书籍名称'] == borrowbook):
                            break

                read=pd.read_csv('bookstore.csv',encoding='gb18030',header=None,names=['书籍名称','作者','出版日期','介绍语','借出状态'])
                #new_read=pd.DataFrame(read) #转换成dataframe结构
                print(read)
                read['借出状态'].loc[borrowbook_line] = '已借出'  #修改指定行列数据
                #new_read.loc[borrowbook_line,'借出状态']='已借出'
                read.to_csv('bookstore.csv', encoding='gb18030',header=False, index=False) #输入（header=False, index=False)可以防止重复出现表头和索引
                
                print('借阅成功！祝您阅读愉快！')
                
                #修改成功！！！！！！！

            else :
                 print ('这本书已经被借走了，抱歉！')

        else:

            print('这本书还未被收录到书库中，抱歉！')

        time.sleep(1)
        self.all_book()

    def return_book(self):
        returnbook = input('请输入书籍名称：\n')
        rebook = self.check_book(returnbook)

        if(rebook!= None):
            if (rebook['借出状态'] == '已借出'):

                #读取资料所在的行号：
                returnbook_line = -1
                with open('bookstore.csv','r',newline='') as r:
                    reader=csv.DictReader(r,fieldnames=header)
                    for i in reader:
                        returnbook_line = returnbook_line+1
                        if (i['书籍名称'] == returnbook):
                            break

                read=pd.read_csv('bookstore.csv',encoding='gb18030',header=None,names=['书籍名称','作者','出版日期','介绍语','借出状态'])
                #new_read=pd.DataFrame(read) #转换成dataframe结构
                print(read)
                read['借出状态'].loc[returnbook_line] = '未借出'  #修改指定行列数据
                read.to_csv('bookstore.csv', encoding='gb18030',header=False, index=False) #输入（header=False, index=False)可以防止重复出现表头和索引
                
                print('成功归还书籍！')
            else:
                print('这本书暂时还未被借阅！')            

        else:
            print('这本书还未被收录到书库中，请检查您的归还信息是否正确！')
            
        time.sleep(1)
        self.all_book()

    
    def delete_book(self):
        self.all_book()
        deletebook = input('请输入需要删除的书籍名称：\n')
        debook = self.check_book(deletebook)
        if(debook!= None):
            if (debook['借出状态'] == '已借出'):
                print('抱歉，你选择的书籍正在被人使用，无法删除出库！\n')

            time.sleep(1)

            if (debook['借出状态'] == '未借出'):
                #读取资料所在的行号：这一步很重要！！！！！！！
                deletebook_line = -1
                with open('bookstore.csv','r',newline='') as r:
                    reader=csv.DictReader(r,fieldnames=header)
                    for i in reader:
                        deletebook_line = deletebook_line+1
                        if (i['书籍名称'] == deletebook):
                            break
                
                read=pd.read_csv('bookstore.csv',encoding='gb18030',header=None,names=['书籍名称','作者','出版日期','介绍语','借出状态'])
                #new_read=pd.DataFrame(read) #转换成dataframe结构
                #print(read)
                read.drop(deletebook_line,inplace=True)#删除指定行
                read.to_csv('bookstore.csv', encoding='gb18030',header=False, index=False) #输入（header=False, index=False)可以防止重复出现表头和索引
                print('书籍删除成功！')
                self.all_book()
                time.sleep(1)

    def inspect_book(self):
        inspect_book=input('请输入你想要查询的书籍名称:\n')
        insbook = self.check_book(inspect_book)
        if(insbook!= None):
            insbook_line = -1
            with open('bookstore.csv','r',newline='') as r:
                reader=csv.DictReader(r,fieldnames=header)
                for i in reader:
                    insbook_line=insbook_line+1
                    if (i['书籍名称'] == inspect_book):
                        break

                read=pd.read_csv('bookstore.csv',encoding='gb18030',header=None,names=['书籍名称','作者','出版日期','介绍语','借出状态'])
                print(read.loc[insbook_line])  #pandas的直接读取，会带有表头输出！

        else:
            time.sleep(1)
            print('抱歉，你查询的书籍不在书库当中！')

        time.sleep(1)
            
    

bookmanagersystem = BookManagerSystem()
bookmanagersystem.menu()
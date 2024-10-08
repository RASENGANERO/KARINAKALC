class Parser:
    def __init__(self, exp):
        self.__exp = '(' + exp + ')'
        self.__prev_token = None

        # Стек операндов (например, числа)
        self.__operands = []

        # Стек операторов (функций, например +, *, и т.п.)
        self.__functions = []

        self.__pos = 0

    __OPERATORS = {
        '+': 2,
        '-': 2,
        '*': 1,
        '/': 1,
        '^': 1,
    }
    

    @staticmethod
    def __is_function(c):
        return c in Parser.__OPERATORS.keys()

    @staticmethod
    def __priority_function(c):
        if not Parser.__is_function(c):
            raise Exception('Не найден оператор "{}"'.format(c))

        return Parser.__OPERATORS[c]

    def __execute_function(self):
        if len(self.__operands) < 2:
            return

        a, b = self.__operands.pop(), self.__operands.pop()
        f = self.__functions.pop()

        if f == '+':
            self.__operands.append(b + a)
        elif f == '-':
            self.__operands.append(b - a)
        elif f == '*':
            self.__operands.append(b * a)
        elif f == '/':
            self.__operands.append(b / a)
        elif f == '^':
            self.__operands.append(b ** a)

    def __can_pop(self, c):
        if not self.__functions:
            return False

        head = self.__functions[-1]
        if not Parser.__is_function(head):
            return False

        p1 = Parser.__priority_function(c)
        p2 = Parser.__priority_function(head)

        # Чем больше значение приоритета, тем меньше он
        # Например: операции * и / имеют больший приоритет, чем + и -
        return p1 >= p2

    @staticmethod
    def __isfloat(number):
        try:
            float(number)
            return True
        except ValueError:
            return False

    def __read_number(self):
        res = ''
        point = 0

        c = self.__exp[self.__pos]

        while c.isdigit() or c == '.':
            if c == '.':
                point += 1
                if point > 1:
                    raise Exception('Выражение не верное -- слишком '
                                    'много точек (pos: %s)' % self.__pos)

            res += c
            self.__pos += 1

            c = self.__exp[self.__pos]

        return res

    def __get_token(self):
        for i in range(self.__pos, len(self.__exp)):
            c = self.__exp[i]

            if c.isdigit():
                return self.__read_number()
            else:
                self.__pos += 1
                return c

        return None

    def calc(self):
        self.__pos = 0

        token = self.__get_token()

        while token:
            if token.isspace():
                pass

            elif token.isdigit():
                self.__operands.append(int(token))

            elif self.__isfloat(token):
                self.__operands.append(float(token))

            elif Parser.__is_function(token):
                # Разруливаем ситуации, когда после первой скобки '(' идет знак + или -
                if self.__prev_token and self.__prev_token == '(' and (token == '+' or token == '-'):
                    self.__operands.append(0)

                # Мы можем вытолкнуть, если оператор c имеет меньший или равный приоритет, чем
                # оператор на вершине стека functions
                # Например, с='+', а head='*', тогда выполнится операция head
                while self.__can_pop(token):
                    self.__execute_function()

                self.__functions.append(token)

            elif token == '(':
                self.__functions.append(token)

            elif token == ')':
                # Выталкиваем все операторы (функции) до открывающей скобки
                while self.__functions and self.__functions[-1] != '(':
                    self.__execute_function()

                # Убираем последнюю скобку '('
                self.__functions.pop()

            # Запоминаем токен как предыдущий
            self.__prev_token = token

            # Получаем новый токен
            token = self.__get_token()

        if self.__functions or len(self.__operands) > 1:
            raise Exception('Неверное выражение: operands={}, functions={}'.format(self.__operands, self.__functions))

        # Единственным значением списка operands будет результат выражения
        return self.__operands[0]


import math
from PyQt5 import QtWidgets, QtGui, QtCore
from name import Ui_MainWindow
import sys
from numpy import arange
from PyQt5.QtWidgets import (QTableWidgetItem,QAbstractItemView,QHeaderView)
from PyQt5.QtGui import (QPalette,QBrush,QPixmap,QImage)
import matplotlib.pyplot as plt
from PyQt5.QtCore import QSize

class mywindow(QtWidgets.QMainWindow):
 
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.label.setText('Введите функцию')
        self.ui.label_2.setText('Введите границы      [')
        self.ui.label_3.setText('              :   ')
        self.ui.label_4.setText('          ]')
        self.ui.label_5.setText('       Введите шаг:                              Δx=')
        self.ui.label_7.setText('                      y0=')
        self.ui.pushButton.setText('Метод Эйлера')
        self.ui.pushButton_2.setText('Метод Эйлера-Коши')
        self.ui.pushButton_3.setText('Метод Рунге-Кутты')
        self.ui.pushButton.clicked.connect(self.eiler)
        self.ui.pushButton_2.clicked.connect(self.eiler_koshi)
        self.ui.pushButton_3.clicked.connect(self.runge_cuta)
        self.create_table(5,["i","x","y","f(x,y)","Δx * f(x,y)"])
        self.ui.lineEdit.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.ui.lineEdit_2.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.ui.lineEdit_3.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.ui.lineEdit_4.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.ui.lineEdit_5.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.spx=list()
        self.formula=str()#ПРЕОБРАЗОВАНИЕ БУКВ
        self.y0=int(0)
        self.shag=float(0)
        self.ui.lineEdit.setText('x^2-2*y')
        self.ui.lineEdit_2.setText('0')
        self.ui.lineEdit_3.setText('1')
        self.ui.lineEdit_4.setText('0.1')
        self.ui.lineEdit_5.setText('1')
        self.k=int(0)
        
    def create_table(self,k,s):
        self.ui.tableWidget.setColumnCount(k)
        self.ui.tableWidget.setHorizontalHeaderLabels(s)
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)        
        


    def set_i_x(self):
        x1=float(self.ui.lineEdit_2.text().format('{:.1f}'))
        x2=float(self.ui.lineEdit_3.text().format('{:.1f}'))+0.1
        self.shag=float(self.ui.lineEdit_4.text().format('{:.1f}'))
        self.y0=float(self.ui.lineEdit_5.text())
        self.formula=self.ui.lineEdit.text()


        self.spx.clear()
        self.ui.tableWidget.setRowCount(0)
        for v in arange(x1,x2,self.shag):
            x=float('{:.1f}'.format(v))
            self.spx.append(x)
        self.spx[0]=int(0)
        for v in range(len(self.spx)):
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            it1 = QTableWidgetItem(str(v+1))
            it1.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            it2 = QTableWidgetItem(str(self.spx[v]))
            it2.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,0,it1)
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,1,it2)
        
    def change_scob(self,k):
        if k.count('(')>k.count(')'):k=k+self.set_scob(')',int(k.count('(')-k.count(')')))
        if k.count('(')<k.count(')'):k=self.set_scob('(',k.count(')')-k.count('('))+k
        return k


    def set_scob(self,s,x):
        su=str(' ')
        i=int(0)
        while i<x:
            su+=s
            i+=1
        return su.strip()


    def set_formulas(self,s,h):
        #if h.find('q')!=-1:s=int(form.find('q'))#,int(form.find(')'))]
        lk=[]
        for v in range(s,len(h)-1):
            if h[v]==')':
                lk.append(v)
        print(h)
        sk=[]
        if h.count('(')!=1:
            sk=h[s:lk[-1]]
        else:
            sk=h
        sk=self.change_scob(sk)    
        return sk     



    def settes_form(self,form,x,y):#ДОБАВИТЬ ПРОВЕРКУ НА Pi sin cos e
        #p=Parser(form.replace('x',str(x)).replace('y',str(y))).calc()
        #return p
        form=form.lower().strip()
        
        lkst=[['sqrt','x','y','cos','sin',' ','\n','pi','e'],['q',x,y,'c','s','','',math.pi,math.e]]
        for v in range(len(lkst[0])):
            form=form.replace(str(lkst[0][v]),str(lkst[1][v]))

        ind=int(0)
        if form.find('q')!=-1:
            #print(form)
            if form.find('q')!=-1:ind=int(form.find('q'))#,int(form.find(')'))]
            sk=self.set_formulas(ind,form)
            if sk.startswith('q')==True:form=form.replace(str(sk),str(math.sqrt(Parser(sk.replace('q','')).calc())))
            


        if form.find('c')!=-1 or form.find('s')!=-1:
            
            if form.find('c')!=-1:ind=int(form.find('c'))#,int(form.find(')'))]
            if form.find('s')!=-1:ind=int(form.find('s'))#,int(form.find(')'))]
            
            sk=self.set_formulas(ind,form)
            
            if sk.startswith('c')==True:form=form.replace(str(sk),str(math.cos(Parser(sk.replace('c','')).calc())))
            if sk.startswith('s')==True:form=form.replace(str(sk),str(math.sin(Parser(sk.replace('s','')).calc())))
            p=Parser(form).calc()
            return p
        else:
            p=Parser(form).calc()
            return p
        #print(form)
        #print(ind)
        #print(lk)
        #print(sk)
        #print(s)
        #return form


    def get_column_value(self,column,k):
        if k==1:
            col_value=float([self.ui.tableWidget.item(row,column).text() for row in range(self.ui.tableWidget.rowCount()) if self.ui.tableWidget.item(row,column) is not None][-1])
        else:
            col_value=[self.ui.tableWidget.item(row,column).text() for row in range(self.ui.tableWidget.rowCount()) if self.ui.tableWidget.item(row,column) is not None]
            col_value=[float(a) for a in col_value]
        return col_value
    

    def eiler(self):
        self.create_table(5,["i","x","y","f(x,y)","Δx * f(x,y)"])
        self.set_i_x()
        y=None
        f_x=None
        x_fx=None
        for v in range(len(self.spx)):
            if int(v)==0:
                y=self.y0
                f_x=self.settes_form(self.formula,'('+str(self.spx[v])+')','('+str(y)+')')
                x_fx=f_x*self.shag
            else:
                y=float(self.get_column_value(2,1))+float(self.get_column_value(4,1))
                f_x=self.settes_form(self.formula,'('+str(self.spx[v])+')','('+str(y)+')')
                x_fx=f_x*self.shag
            it3 = QTableWidgetItem(('%.8f' % y).rstrip('0').rstrip('.'))
            it3.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            it4 = QTableWidgetItem(('%.8f' % f_x).rstrip('0').rstrip('.'))
            it4.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            it5 = QTableWidgetItem(('%.8f' % x_fx).rstrip('0').rstrip('.'))
            it5.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.ui.tableWidget.setItem(v,2,it3)
            self.ui.tableWidget.setItem(v,3,it4)
            self.ui.tableWidget.setItem(v,4,it5)
        y=self.get_column_value(2,2)
        self.create_graph(self.spx,y,'Метод Эйлера','blue')




    def eiler_koshi(self):
        self.create_table(5,["i","x","y","f(x,y)","Δx * f(x,y)"])
        self.set_i_x()
        y=None
        f_x=None
        x_fx=None
        for v in range(len(self.spx)):
            if int(v)==0:
                y=self.y0
                f_x=self.settes_form(self.formula,self.spx[v],y)
                x_fx=f_x*self.shag
            else:
                x1=float(self.spx[v-1])
                y1=float(self.get_column_value(2,1))
                shag1=self.shag/2
                f2=x1+shag1
                f1=y1+shag1*(self.settes_form(self.formula,'('+str(x1)+')','('+str(y1)+')'))
                delta_y=self.shag*(self.settes_form(self.formula,'('+str(f2)+')','('+str(f1)+')'))
                y=y1+delta_y
                f_x=(self.settes_form(self.formula,'('+str(self.spx[v])+')','('+str(y)+')'))
                x_fx=f_x*self.shag
            it3 = QTableWidgetItem(('%.8f' % y).rstrip('0').rstrip('.'))
            it3.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            it4 = QTableWidgetItem(('%.8f' % f_x).rstrip('0').rstrip('.'))
            it4.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            it5 = QTableWidgetItem(('%.8f' % x_fx).rstrip('0').rstrip('.'))
            it5.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.ui.tableWidget.setItem(v,2,it3)
            self.ui.tableWidget.setItem(v,3,it4)
            self.ui.tableWidget.setItem(v,4,it5)
        y=self.get_column_value(2,2)
        self.create_graph(self.spx,y,'Метод Эйлера-Коши','red')




    def runge_cuta(self):
        self.create_table(8,["i","x","y","k1","k2","k3","k4","Δy"])
        self.set_i_x()
        y=None
        k1=None
        k2=None
        k3=None
        k4=None
        delta_y=None
        for v in range(len(self.spx)):
            if int(v)==0:
                y=self.y0
            else:
                y=float(self.get_column_value(2,1))+float(self.get_column_value(7,1))
            k1=self.settes_form(self.formula,'('+str(self.spx[v])+')','('+str(y)+')')
            k2=self.settes_form(self.formula,'('+str(((self.shag/2)+self.spx[v]))+')','('+str((y+((self.shag*k1)/2)))+')')
            k3=self.settes_form(self.formula,'('+str(((self.shag/2)+self.spx[v]))+')','('+str((y+((self.shag*k2)/2)))+')')
            k4=self.settes_form(self.formula,'('+str((self.shag+self.spx[v]))+')','('+str((y+((self.shag*k3))))+')')
            delta_y=(self.shag/6)*(k1+(2*k2)+(2*k3)+k4)
            it3 = QTableWidgetItem(('%.8f' % y).rstrip('0').rstrip('.'))
            it3.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            it4 = QTableWidgetItem(('%.8f' % k1).rstrip('0').rstrip('.'))
            it4.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            it5 = QTableWidgetItem(('%.8f' % k2).rstrip('0').rstrip('.'))
            it5.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            it6 = QTableWidgetItem(('%.8f' % k3).rstrip('0').rstrip('.'))
            it6.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            it7 = QTableWidgetItem(('%.8f' % k4).rstrip('0').rstrip('.'))
            it7.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            it8 = QTableWidgetItem(('%.8f' % delta_y).rstrip('0').rstrip('.'))
            it8.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.ui.tableWidget.setItem(v,2,it3)
            self.ui.tableWidget.setItem(v,3,it4)
            self.ui.tableWidget.setItem(v,4,it5)
            self.ui.tableWidget.setItem(v,5,it6)
            self.ui.tableWidget.setItem(v,6,it7)
            self.ui.tableWidget.setItem(v,7,it8)
        y=self.get_column_value(2,2)
        self.create_graph(self.spx,y,'Метод Рунге-Кутта','green')


    def create_graph(self,s1,s2,k,col):
        plt.plot(s1,s2,label=k,color = col)
        s1[0]=float(self.ui.lineEdit_2.text())
        s1[-1]=float(self.ui.lineEdit_3.text())
        plt.legend(shadow=True)
        plt.grid(True)
        plt.yticks(s1)
        plt.xticks(s1)
        plt.xlim([float(self.ui.lineEdit_2.text()),float(self.ui.lineEdit_3.text())])
        plt.savefig('D:/1.jpg')
        pixmap = QPixmap('D:/1.jpg')
        self.ui.label_6.setPixmap(pixmap)
        self.ui.label_6.setAutoFillBackground(True)
        self.k+=1
        if self.k==3:
            self.k=0
            plt.close()
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())
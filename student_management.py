from tkinter import *
import mysql.connector
from tkinter import ttk
from tkinter import messagebox
class StudentMgmt:
    def __init__(self,root):
        try:
            self.con=mysql.connector.connect(host='localhost',user='root',passwd='Softwarica@123',database='database_0x2316541')
            self.cur= self.con.cursor()
        except mysql.connector.Error as e:
            print(e)
        self.root = root
        self.root.configure(background ="#70adda")
        self.root.geometry("1200x650+0+30")
        self.root.title("Student Management System")
        self.root.iconbitmap("icon.ico")
        self.img1 = PhotoImage(file = "Student-Health-Management.png")
        self.title = Label(self.root, image = self.img1, font=('Arial Black', 25), bg='#70adda')
        self.student_id = Label(self.root, text='Id:', bg='#70adda', font=('Arial Black', 12, 'bold'))
        self.first_name = Label(self.root, text='First Name:', bg='#70adda', font=('Arial Black', 12, 'bold'))
        self.last_name = Label(self.root, text='Last Name:', bg='#70adda', font=('Arial Black', 12, 'bold'))
        self.degree = Label(self.root, text='Degree:', bg='#70adda', font=('Arial Black', 12, 'bold'))
        self.address = Label(self.root, text='Address:', bg='#70adda', font=('Arial Black', 12, 'bold'))
        self.contact_no = Label(self.root, text='Contact Number:', bg='#70adda', font=('Arial Black', 12, 'bold'))

        self.title.place(x=0, y=0)
        self.student_id.place(x=20, y=250)
        self.first_name.place(x=20, y=300)
        self.last_name.place(x=20, y=350)
        self.degree.place(x=20, y=400)
        self.address.place(x=20, y=450)
        self.contact_no.place(x=20, y=500)

        # Text Variables
        self.stid = StringVar()
        self.cont = StringVar()
        # ENTRY
        self.entrystudent_id = Entry(self.root, width=23,textvariable = self.stid)
        self.entryfirst_name = Entry(self.root, width=23)
        self.entrylast_name = Entry(self.root, width=23)
        self.entrydegree = ttk.Combobox(self.root, values=['Bsc(Hons)computing', 'Ethical Hacking'], state="readonly")
        self.entrydegree.set("Ethical Hacking")
        self.entryaddress = Entry(self.root, width=23)
        self.entrycontact_no = Entry(self.root, width=23,textvariable =self.cont)

        #Input limit
        self.stid.trace_variable("w",self.InputLim)
        self.cont.trace_variable("w",self.InputLim1)


        self.entrystudent_id.place(x=200, y=250)
        self.entryfirst_name.place(x=200, y=300)
        self.entrylast_name.place(x=200, y=350)
        self.entrydegree.place(x=200, y=400)
        self.entryaddress.place(x=200, y=450)
        self.entrycontact_no.place(x=200, y=500)

        # FRAMES
        self.btn_frame = Frame(self.root, bd=4, relief=RIDGE, bg='#70adda')
        self.btn_frame.place(x=20, y=550, width=355, height=40)

        self.table_frame = Frame(self.root, bd=4, relief=RIDGE, bg='gray')
        self.table_frame.place(x=400, y=240, width=780, height=400)

        self.scroll_x = Scrollbar(self.table_frame, orient=HORIZONTAL)
        self.scroll_y = Scrollbar(self.table_frame, orient=VERTICAL)

        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.scroll_y.pack(side=RIGHT, fill=Y)

        self.student_table = ttk.Treeview(self.table_frame, column=(
        'student_id', 'first_name', 'last_name', 'degree', 'address', 'contact_no'),
                                    xscrollcommand=self.scroll_x.set,
                                    yscrollcommand=self.scroll_y.set)
        self.student_table.heading('student_id', text="Id")
        self.student_table.heading('first_name', text="First Name")
        self.student_table.heading('last_name', text="Last Name")
        self.student_table.heading('degree', text="Degree")
        self.student_table.heading('address', text="Address")
        self.student_table.heading('contact_no', text="Contact Number")
        self.student_table['show'] = 'headings'

        self.student_table.column('student_id', width=120)
        self.student_table.column('first_name', width=120)
        self.student_table.column('last_name', width=120)
        self.student_table.column('degree', width=120)
        self.student_table.column('address', width=120)
        self.student_table.column('contact_no', width=120)

        self.scroll_x.config(command=self.student_table.xview)
        self.scroll_y.config(command=self.student_table.yview)

        self.student_table.bind(('<ButtonRelease-1>'), self.pointer)
        self.student_table.pack(fill=BOTH, expand=True)

        # BUTTONS
        self.addbutton = ttk.Button(self.btn_frame,text='Add',command=self.add_info)
        self.addbutton.place(relx=0.015, rely=0.004)

        self.btn_update = ttk.Button(self.btn_frame,command=self.update,text = "update")
        self.btn_update.place(relx=0.25, rely=0.004)

        self.delete = ttk.Button(self.btn_frame,text='Delete',command=self.delete_data)
        self.delete.place(relx=0.50,rely=0.004)

        self.btn_clear = ttk.Button(self.btn_frame,text='Clear',command=self.clear)
        self.btn_clear.place(relx = 0.75,rely= 0.002)

        # SEARCH LABEL
        self.lbl_search = Label(self.root, text='Search / Sort by:', bg='#70adda', font=('Arial Black', 12, 'bold'))
        self.lbl_search.place(x=400, y=200)

        #Combo LABEL
        self.combo_search = ttk.Combobox(self.root, font=('Arial Black', 12), state='readonly', width=12)
        self.combo_search['values'] = ('student_id', 'first_name', 'last_name', 'degree', 'address', 'contact_no')
        self.combo_search.set('student_id')
        self.combo_search.place(x=558, y=200)

        # SEARCH ENTRY
        self.Esearch = Entry(self.root, font=('Arial Black', 12, 'bold'), width=20)
        self.Esearch.place(x=735, y=200)

        # SEARCH BUTTON
        self.btn_search = ttk.Button(self.root, text='search', command=self.search_fetch)
        self.btn_search.place(x=1050, y=200)

        # SORT BUTTON
        self.sort_btn = ttk.Button(self.root, text='Sort', command=self.sort)
        self.sort_btn.place(x=970, y=200)

        self.title1 = Label(self.root,text = "Student Management System",font = "Algerian 35", bg = "#70adda")
        self.title1.place(x=450,y=30)
        self.title2 = Label(self.root,text = "Copyright © 2019", font = "Arial 15" , bg = "#70adda")
        self.title2.place(x=700,y = 90)
        self.show()
        self.root.mainloop()


#FUNCTIONS
    def add_info(self):
        student_id=int(self.entrystudent_id.get())
        first_name=self.entryfirst_name.get()
        last_name=self.entrylast_name.get()
        degree = self.entrydegree.get()
        address=  self.entryaddress.get()
        contact_no=int(self.entrycontact_no.get())

        query='insert into form values(%s,%s,%s,%s,%s,%s)'
        values=(student_id,first_name,last_name,degree,address,contact_no)
        self.cur.execute(query,values)
        print('Data saved successfully')
        self.con.commit()
        self.show()
        self.clear()

    def InputLim(self,*args):
        """
        This method limits the input in Entry box to integer.

        :param args: args could be anything pressed by the user to Entrybox.
        :return: None

        """
        a = str(self.stid.get())
        try:
            b = int(self.stid.get())
        except Exception:
            self.stid.set(a[:-1])

    def InputLim1(self,*args):
        """
        This method limits the input in Entry box to integer.

        :param args: args could be anything pressed by the user to Entrybox.
        :return: None

        """
        a = str(self.cont.get())
        try:
            b = int(self.cont.get())
        except Exception:
            self.cont.set(a[:-1])

    def show(self):
        query='select * from form'
        self.cur.execute(query)
        result= self.cur.fetchall()
        if len(result)!=0:
            self.student_table.delete(*self.student_table.get_children())
        for row in result:
            self.student_table.insert('',END,values=row)
            self.con.commit()

    def delete_data(self):
        student_id=int(self.entrystudent_id.get())
        query='delete from form where student_id=%s'
        values=(student_id,)
        self.cur.execute(query,values)
        print('data deleted successfully')
        self.con.commit()
        self.show()

    def clear(self):
        self.entrystudent_id.delete(0,END)
        self.entryfirst_name.delete(0,END)
        self.entrylast_name.delete(0,END)
        self.entrydegree.delete(0,END)
        self.entryaddress.delete(0,END)
        self.entrycontact_no.delete(0,END)

    def pointer(self,event):
        point= self.student_table.focus()
        content= self.student_table.item(point)
        row=content['values']
        self.clear()
        print(row)
        if len(row) != 0:
            self.entrystudent_id.insert(0,row[0])
            self.entryfirst_name.insert(0,row[1])
            self.entrylast_name.insert(0,row[2])
            self.entrydegree.insert(0,row[3])
            self.entryaddress.insert(0,row[4])
            self.entrycontact_no.insert(0,row[5])


    def update(self):
        self.cur.execute('select * from form')
        result = self.cur.fetchall()
        test = []
        student_id= self.entrystudent_id.get()
        for i in result:
            test.append(i[0])
        if student_id == "":
            messagebox.showinfo("Error","You can't left id Empty")
        elif student_id not in test:
            messagebox.showinfo("Error","No Such Data in Database")
        else:
            query = 'update form set first_name=%s,last_name=%s,degree=%s,address=%s,contact_no=%s where student_id=%s'
            first_name= self.entryfirst_name.get()
            last_name=  self.entrylast_name.get()
            degree= self.entrydegree.get()
            address=self.entryaddress.get()
            contact_no= int(self.entrycontact_no.get())
            values=(first_name,last_name,degree,address,contact_no,student_id)
            self.cur.execute(query,values)
            self.con.commit()
            self.show()
            self.clear()
    @staticmethod
    def bubble_sort(result, sort_by):
        for i in range(0, len(result) - 1):
            for j in range(0, len(result) - 1 - i):
                if result[j][sort_by] > result[j + 1][sort_by]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result

    def sort(self):
        self.thelist = 'select * from form'
        self.cur.execute(self.thelist)
        result = self.cur.fetchall()
        a = self.combo_search.get()
        tri = ('student_id', 'first_name', 'last_name', 'degree', 'address', 'contact_no')
        sort_by = int()
        for i in tri:
            if i == a:
                sort_by = tri.index(i)
                break
        self.bubble_sort(result, sort_by)
        if len(result) != 0:
            self.student_table.delete(*self.student_table.get_children())
            for row in result:
                self.student_table.insert('', END, values=row)
                self.con.commit()
    @staticmethod
    def search(data, search_index, search_for):
        global search_results
        search_results = []
        for i in data:
            if str(search_for) in str(i[search_index]):
                search_results.append(i)
                return search_results

    def search_fetch(self):
        query = "select * from form"
        self.cur.execute(query)
        data = self.cur.fetchall()
        test = self.combo_search.get()
        searching = self.Esearch.get()
        tri = ('student_id', 'first_name', 'last_name', 'degree', 'address', 'contact_no')
        search_index = int()
        for i in tri:
            if i == test:
                search_index = tri.index(i)

        self.search(data, search_index, searching)
        self.student_table.delete(*self.student_table.get_children())
        if len(search_results) != 0:
            for i in search_results:
                self.student_table.insert('', END, values=i)
                self.con.commit()


root = Tk()
a = StudentMgmt(root)
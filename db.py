from sqlite3.dbapi2 import Row
from tkinter import *
import sqlite3

root = Tk()
root.title('Todo List')
root.geometry('400x500')

conn = sqlite3.connect('todo.db')
c = conn.cursor()
c.execute(
        """
        create table if not exists todo (
            id integer primary key autoincrement,
            created_at timestamp not null default current_timestamp,
            description text not null,
            completed boolean not null
        );
        """
    )
conn.commit()

# Currying
def completar(id):
    def _completar():
        todo = c.execute('select * from todo where id = ?',
        (id, )
        ).fetchone()
        c.execute('update todo set completed = ? where id = ?',
        (not todo[3], id)
        )
        conn.commit()
        render_todo()
    return _completar

def remover(id):
    def _remover():
        c.execute('delete from todo where id = ?',
        (id, )
        )
        conn.commit()
        render_todo()
    return _remover

def render_todo():
    rows = c.execute('select * from todo').fetchall()
    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = '#999' if completed else '#000'
        ch = Checkbutton(frame, text=description, fg=color, width=42, anchor='w', command=completar(id))
        ch.grid(row=i, column=0, sticky='w')
        bot = Button(frame, text='Eliminar', command=remover(id))
        bot.grid(row=i, column=1)
        ch.select() if completed else ch.deselect()

def add_todo():
    todo = e.get()
    if todo:
        c.execute(
            """
            insert into todo (description, completed) values (?, ?)
            """,
            (todo, False)
        )
        conn.commit()
        e.delete(0, END)
        render_todo()
    else:
        pass

l = Label(root, text='Tarea')
l.grid(row=0, column=0)

e = Entry(root, width=40)
e.grid(row=0, column=1)

btn = Button(root, text='Agregar', command=add_todo)
btn.grid(row=0,column=2)

frame = LabelFrame(root, text='Mis Tareas', padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nswe', padx=5)
e.focus()

root.bind('<Return>', lambda x: add_todo())
render_todo()
root.mainloop()
import tkinter
from tkframes import MyWindow


def main():
    root = tkinter.Tk()
    root.title("Grapher")
    window = MyWindow(master=root)
    window.pack()
    root.mainloop()


if __name__ == '__main__':
    main()

import tkinter
from math import *


class CoordinatePlane(tkinter.Frame):
    """
    class that creates gridlines and graphs lines
    """

    def __init__(self, master, manager, width=700, height=700):
        self.master = master
        self.width = width
        self.height = height
        tkinter.Frame.__init__(self, master, width=self.width, height=self.height, borderwidth=0,
                               highlightthickness=0)
        self.canvas = tkinter.Canvas(self, width=self.width, height=self.height, borderwidth=0,
                                     highlightthickness=0)

        self.equations = []

        # store the manager class #
        self.manager = manager

        self.canvas.grid()

    def draw_graph_paper(self, seperator=True):
        zoom = self.manager.graph_zoom
        """
        Draws gridlines on canvas with a certain zoom (default is 25)
        Also draws the x and y axes and if seperator is true, draws
        lines surrounding the graph
        """
        for x_pos in range(int((self.width / zoom) / 2) + 1):
            color = "blue"
            # Draw vertical lines starting at the middle #

            # first, check if you are on the first iteration #
            if x_pos == 0:
                color = "black"

            # going to the right #
            self.canvas.create_line((self.width / 2 + x_pos * zoom), 0,
                                    (self.width / 2 + x_pos * zoom), self.height, fill=color)

            # going to the right #
            self.canvas.create_line((self.width / 2 + (-x_pos) * zoom), 0,
                                    (self.width / 2 + (-x_pos) * zoom), self.height, fill=color)

        for y_pos in range(int(self.height / zoom / 2) + 1):
            color = "blue"
            # Draw horizontal lines starting at the middle #

            # check if you are on the first iteration #
            if y_pos == 0:
                color = "black"

            # going up #
            self.canvas.create_line(0, (self.height / 2 + (-y_pos) * zoom),
                                    self.width, (self.height / 2 + (-y_pos) * zoom), fill=color)

            # going down #
            self.canvas.create_line((0, (self.height / 2 + y_pos * zoom)),
                                    self.width, (self.height / 2 + y_pos * zoom), fill=color)

        # Draw X-axis #
        self.canvas.create_line(0, int(self.height / 2),
                                self.width, int(self.height / 2), fill="black", width=3)

        # Draw Y-axis #
        self.canvas.create_line(int(self.width / 2), 0,
                                int(self.width / 2), self.height, fill="black", width=3)

        if seperator:
            # Draw lines around graph #
            self.canvas.create_line(self.width, 0, self.width, self.height, fill="black", width=2)
            self.canvas.create_line(0, self.height, self.width, self.height, fill="black", width=2)
            self.canvas.create_line(0, 0, 0, self.height, fill="black", width=2)
            self.canvas.create_line(0, 0, self.width, 0, fill="black", width=2)

    def graph(self, equation):
        zoom = self.manager.graph_zoom
        equation = equation.replace(" ", "")
        """
        graphs an equation with a certain zoom
        and returns a list of all lines drawn to plot the equation
        """
        # create a list of lines drawn, so they can be deleted #
        line_list = []

        j = self.width/2
        while j > -(self.width/2):
            try:
                # set initial x and y #
                x = j/zoom
                y = eval(equation)

                if not (equation in self.equations):
                    self.equations.append(equation)
                x, y = x * zoom, y * zoom

                # convert into tk coordinates #
                last_x = x + int(self.width / 2)
                last_y = -y + int(self.height / 2)
                break

            except:
                j -= 1

        # set i to the x value calculated above #
        i = int(last_x)
        while i > int(-(self.width / 2)):
            # graph the line from left to right to avoid errors with #
            # equations that cant use negative values (sqrt, log...) #
            try:
                # set the first x value to account for the zoom (makes a smoother line) #
                x = i / zoom
                y = eval(equation)
                x, y = x * zoom, y * zoom

                # convert coordinates into tk coordinates #
                real_x = (x + int(self.width / 2))
                real_y = (-y + int(self.height / 2))

                # create line and add it to the line list #
                line = self.canvas.create_line(last_x, last_y, real_x, real_y, fill="red")
                line_list.append(line)

                last_x = real_x
                last_y = real_y

            except:
                pass

            i -= 1
        return line_list

    def remove_equation(self, equation):
        self.equations.remove(str(equation))

    def redraw(self):
        self.canvas.delete(tkinter.ALL)
        self.draw_graph_paper()
        for line in self.equations:
            self.graph(line)

    def clear_equations(self):
        self.canvas.delete(tkinter.ALL)
        self.equations = []
        self.draw_graph_paper()


class CmdFrame(tkinter.Frame):
    """
    frame you type commands into
    """
    def __init__(self, master, manager, width=700, height=700):
        self.master = master
        self.width = width
        self.height = height

        tkinter.Frame.__init__(self, self.master, width=self.width, height=self.height)

        self.manager = manager

        self.cmd_entry = tkinter.Text(self, width=20, height=46)
        self.cmd_entry.bind("<Return>", self.on_enter)

        self.cmd_entry.grid(row=0, sticky=tkinter.W)

        

    def on_enter(self, event):
        """
        give the log window the command to process
        and delete text from text widget
        returns "break"
        """

        self.manager.log_frame.process(str(self.cmd_entry.get(0.0, "1.end")))

        self.cmd_entry.delete(0.0, tkinter.END)
        return "break"


class LogFrame(tkinter.Frame):
    """
    responsible for processing commands
    """
    def __init__(self, master, manager, width=1400, height=200):
        self.master = master
        self.width = width
        self.height = height
        tkinter.Frame.__init__(self, self.master, width=self.width, height=self.height)

        self.manager = manager

        self.curr_cmd = tkinter.StringVar()

        # store all equations #
        self.equations = []

        self.cmd_text = tkinter.Label(master=self, textvariable=self.curr_cmd)
        self.cmd_text.grid()

        self.zoomed_out = False

    def process(self, command):
        
        """
        processes commands and applies them to the graph
        """
        if not isinstance(command, str):
            raise RuntimeError("command must be a string")

        if command == "+" or command == "zoom+" or command == "zoom +":
            self.manager.graph_zoom += 10
            self.manager.coordinate_plane.redraw()
            self.curr_cmd.set("Zoomed in")
            self.zoomed_out = False

        elif command == "-" or command == "zoom-" or command == "zoom -":
            if self.manager.graph_zoom > 10:
                self.manager.graph_zoom -= 10
                self.manager.coordinate_plane.redraw()
                self.curr_cmd.set("Zoomed out")

            else:
                if self.zoomed_out == True:
                    self.curr_cmd.set("who do you think you are? I said max zoom reached you bastard.")
                else:
                    self.zoomed_out = True
                    self.curr_cmd.set("max zoom out reached")

        elif command == "clear":
            self.manager.coordinate_plane.clear_equations()
            self.curr_cmd.set("Cleared coordinate plane")

        elif command[0:6].upper() == "DELETE":
            command = command[6:]
            command = command.replace(" ", "")

            try:
                self.manager.coordinate_plane.remove_equation(command)
                self.manager.coordinate_plane.redraw()
                self.curr_cmd.set("deleted " + command)

            except:
                self.curr_cmd.set("\"" + command + "\" is not a graphed equation")

        elif command[0:5].upper() == "GRAPH":
            command = command[5:]
            command = command.replace(" ", "")
            try:

                self.manager.coordinate_plane.graph(command)
                self.curr_cmd.set("Successfully graphed: " + command)
                # self.equations.append(command) # now stored in coordinate plane class
            except:
                self.curr_cmd.set("invalid function: \"" + command + "\"")

        else:
            self.curr_cmd.set("Unknown command: \"" + command + "\"")



class MyWindow(tkinter.Frame):
    def __init__(self, master):
        self.master = master
        tkinter.Frame.__init__(self, self.master)

        self.width = 700
        self.height = 700
        self.extra_width = 700
        self.extra_height = 200

        self.graph_zoom = 25

        self.top_frame = tkinter.Frame(master=self)
        self.bottom_frame = tkinter.Frame(master=self)

        self.coordinate_plane = CoordinatePlane(master=self.top_frame, manager=self)
        self.log_frame = LogFrame(master=self.bottom_frame, manager=self)
        self.cmd_frame = CmdFrame(master=self.top_frame, manager=self)

        self.top_frame.pack(side="top")
        self.bottom_frame.pack(side="bottom")

        self.coordinate_plane.pack(side="left")
        self.cmd_frame.pack(side="right", fill="x")
        self.log_frame.pack(side="left", fill="both")

        self.coordinate_plane.draw_graph_paper()


def main():
    try:
        root = tkinter.Tk()
        w1 = MyWindow(root)
        print("successfully loaded main class")

    except Exception as exception:
        print(exception)


if __name__ == '__main__':
    main()

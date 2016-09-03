import tkinter
import math


class TwoDimentionalPlane(tkinter.Canvas):
    """
    A class that can be used to to many things related to 2D coordinate planes
    extends tkinter.Canvas class
    """

    def __init__(self, width=700, height=700):

        tkinter.Canvas.__init__(self)
        self.master.title("2D Plane")
        self.config(width=width, height=height, borderwidth=0, highlightthickness=0)
        self.pack(fill=tkinter.BOTH, expand=tkinter.YES)

        self.update()

        self.zoom = 25

        self.equations = []

        self.bind("<Configure>", self.redraw)

    def draw_graph_paper(self, draw_borders=True):
        """
        Draws gridlines on canvas with a certain zoom (default is 25)
        Also draws the x and y axes and if seperator is true, draws
        lines surrounding the graph
        :param zoom: the magnification of the graph paper
        :type zoom: int
        :param draw_borders: wether or not to draw borders around edges of graph
        :type draw_borders: bool
        """
        for x_pos in range(int((self.winfo_width() / self.zoom) / 2) + 1):
            color = "blue"
            # Draw vertical lines starting at the middle #

            # first, check if you are on the first iteration #
            if x_pos == 0:
                color = "black"

            # going to the right #
            self.create_line((self.winfo_width() / 2 + x_pos * self.zoom), 0,
                             (self.winfo_width() / 2 + x_pos * self.zoom), self.winfo_height(), fill=color)

            # going to the right #
            self.create_line((self.winfo_width() / 2 + (-x_pos) * self.zoom), 0,
                             (self.winfo_width() / 2 + (-x_pos) * self.zoom), self.winfo_height(), fill=color)

        for y_pos in range(int(self.winfo_height() / self.zoom / 2) + 1):
            color = "blue"
            # Draw horizontal lines starting at the middle #

            # check if you are on the first iteration, doesn't really matter, it is re written #
            if y_pos == 0:
                color = "black"

            # going up #
            self.create_line(0, (self.winfo_height() / 2 + (-y_pos) * self.zoom),
                             self.winfo_width(), (self.winfo_height() / 2 + (-y_pos) * self.zoom), fill=color)

            # going down #
            self.create_line((0, (self.winfo_height() / 2 + y_pos * self.zoom)),
                             self.winfo_width(), (self.winfo_height() / 2 + y_pos * self.zoom), fill=color)

        # Draw X-axis #
        self.create_line(0, int(self.winfo_height() / 2),
                         self.winfo_width(), int(self.winfo_height() / 2), fill="black", width=3)

        # Draw Y-axis #
        self.create_line(int(self.winfo_width() / 2), 0,
                         int(self.winfo_width() / 2), self.winfo_height(), fill="black", width=3)

        if draw_borders:
            # Draw lines around graph #
            self.create_line(self.winfo_width(), 0, self.winfo_width(), self.winfo_height(), fill="black", width=2)
            self.create_line(0, self.winfo_height(), self.winfo_width(), self.winfo_height(), fill="black", width=2)
            self.create_line(0, 0, 0, self.winfo_height(), fill="black", width=2)
            self.create_line(0, 0, self.winfo_width(), 0, fill="black", width=2)


    def __graph_of_x(self, equation):

        # create a list of lines drawn, so they can be deleted #
        line_list = []

        j = self.winfo_width() / 2
        while j > -(self.winfo_width() / 2):
            try:
                # set initial x and y #

                x = j / self.zoom
                y = equation(x)



                x, y = x * self.zoom, y * self.zoom

                # convert into tk coordinates #
                last_x = x + int(self.winfo_width() / 2)
                last_y = -y + int(self.winfo_height() / 2)
                break

            except:
                j -= 1

        # set i to the x value calculated above #
        i = int(last_x)
        while i > int(-(self.winfo_width() / 2)):
            # graph the line from left to right to avoid errors with #
            # equations that cant use negative values (sqrt, log...) #
            try:
                # set the first x value to account for the zoom (makes a smoother line) #

                x = i / self.zoom
                y = equation(x)

                x, y = x * self.zoom, y * self.zoom

                # convert coordinates into tk coordinates #
                real_x = (x + int(self.winfo_width() / 2))
                real_y = (-y + int(self.winfo_height() / 2))

                # create line and add it to the line list #
                line = self.create_line(last_x, last_y, real_x, real_y, fill="red")
                line_list.append(line)

                last_x = real_x
                last_y = real_y

            except:  # It is fine if it doesn't work, and is expected sometimes, so no need to do anything
                pass

            i -= 1
        if not ([equation, "x"] in self.equations):
                    self.equations.append([equation, "x"])
        return line_list


    def __graph_of_y(self, equation):

        # create a list of lines drawn, so they can be deleted #
        line_list = []

        j = self.winfo_width() / 2
        while j > -(self.winfo_width() / 2):
            try:
                # set initial x and y #

                y = j / self.zoom
                x = equation(y)


                x, y = x * self.zoom, y * self.zoom

                # convert into tk coordinates #
                last_x = x + int(self.winfo_width() / 2)
                last_y = -y + int(self.winfo_height() / 2)
                break

            except:
                j -= 1

        # set i to the x value calculated above #
        i = int(last_x)
        while i > int(-(self.winfo_width() / 2)):
            # graph the line from top to bottom to avoid errors with #
            # equations that cant use negative values (sqrt, log...) #
            try:
                # set the first y value to account for the zoom (makes a smoother line) #

                y = i / self.zoom
                x = equation(y)
                x, y = x * self.zoom, y * self.zoom

                # convert coordinates into tk coordinates #
                real_x = (x + int(self.winfo_width() / 2))
                real_y = (-y + int(self.winfo_height() / 2))

                # create line and add it to the line list #
                line = self.create_line(last_x, last_y, real_x, real_y, fill="red")
                line_list.append(line)

                last_x = real_x
                last_y = real_y

            except:  # It is fine if it doesn't work, and is expected sometimes, so no need to do anything
                pass

            i -= 1

        if not ([equation, "y"] in self.equations):
                    self.equations.append([equation, "y"])

        return line_list
    
    
    def graph(self, equation, give_equation="x"):
        """
        graphs an equation of x or y with a certain zoom
        and returns a list of all lines drawn to plot the equation
        :param equation: a function that take an x and returns a y or vice versa
        :type equation: function
        :param give_equation: wether to pass the x or the y values to equation
        :type give_equation: str
        :returns list: a list of lines that make up the graphed line
        """

        if give_equation == "x":
            line_list = self.__graph_of_x(equation)

        elif give_equation == "y":
            line_list = self.__graph_of_y(equation)

        else:
            raise ValueError("give_equation must be \"x\" or \"y\", not: " + str(give_equation))

        return line_list


    def redraw(self, event=None):
        self.delete("all")
        self.update()
        self.draw_graph_paper()
        for eq in self.equations:  # redraw each equation with the correct values passed to it (x or y)
            self.graph(eq[0], eq[1])


    def new_width(self, new):
        self.config(width=new)
        self.update()
        self.redraw()

    def new_height(self, new):
        self.config(height=new)
        self.update()
        self.redraw()

    def new_dimentions(self, new_width, new_height):
        self.new_width(new_width)
        self.new_height(new_height)

    def __delete_single_equation(self, equation, x_or_y, redraw=True):
        if [equation, x_or_y] in self.equations:
            self.equations = [eq for eq in self.equations if eq != [equation, x_or_y]]
            print(self.equations)
            if redraw:
                self.redraw()
        else:
            print(str([equation, x_or_y]) + " is not in the list of graphed functions")


    def delete_equation(self, equation, x_or_y="x"):
        if isinstance(equation, list):
            for eq in equation:
                self.__delete_single_equation(eq[0], eq[1])

        elif equation == "all":
            self.equations = []
            self.redraw()

        else:
            self.__delete_single_equation(equation, x_or_y)


    def zoom_in(self, amount=5):
        self.zoom += amount
        self.redraw()


def f(x):
    return x * 2


if __name__ == "__main__":
    a = TwoDimentionalPlane()
    a.draw_graph_paper()
    a.graph(f, "y")
    a.graph(math.cos, "x")
    a.zoom_in(25)
    a.redraw()
    a.new_dimentions(700, 700)
    a.mainloop()

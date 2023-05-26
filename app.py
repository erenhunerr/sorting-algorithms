# Sorting Algorithms Solver Class
from time import sleep

class Solver:

    def __init__(self, unsorted, n, solve_mode, subscriber):
        self.subscriber = subscriber
        if solve_mode == 0:
            self.selection_sort(unsorted, n)
        elif solve_mode == 1:
            self.insertion_sort(unsorted, n)
        elif solve_mode == 2:
            self.bubble_sort(unsorted, n)
        elif solve_mode == 3:
            self.divide(unsorted, 0, n - 1)  # merge sort
        elif solve_mode == 4:
            self.quick_sort(unsorted, 0, n)

    ########################################################################

    def selection_sort(self, unsorted, n):
        """ selection sort algorithm inplace """
        for i in range(0, n):
            # current_min = min(unsorted[i:], key=lambda x: x.value)
            # a_index = unsorted.index(a)
            current_min = unsorted[i]
            min_index = i
            for j in range(i, n):
                if unsorted[j] < current_min:
                    current_min = unsorted[j]
                    min_index = j
            self.swap(unsorted, i, min_index)

    ########################################################################

    @staticmethod
    def insertion_sort(unsorted, n):
        """ insertion sort algorithm """
        for i in range(1, n):
            val = unsorted[i].value
            hole = i
            while hole > 0 and unsorted[hole - 1].value > val:
                unsorted[hole].value = unsorted[hole - 1].value
                unsorted[hole].index = hole  # set index to trigger dispatch
                hole -= 1
            unsorted[hole].value = val
            unsorted[hole].index = hole  # set index to trigger dispatch

    ########################################################################

    def bubble_sort(self, unsorted, n):
        """ bubble sort algorithm """
        for i in range(0, n - 1):
            swapped = False
            for j in range(0, n - 1 - i):
                if unsorted[j].value > unsorted[j + 1].value:
                    self.swap(unsorted, j, j + 1)
                    swapped = True
            if not swapped:
                break

    # ==============================================================
    # Merge Sort Algorithm

    def divide(self, unsorted, lower, upper):
        """ recrusive function to divide array into 2 sub arrays for sorting """
        if upper <= lower:
            return
        mid = (lower + upper) // 2
        self.divide(unsorted, lower, mid)
        self.divide(unsorted, mid + 1, upper)
        self.merge(unsorted, lower, mid, mid + 1, upper)

    @staticmethod
    def merge(unsorted, l_lower, l_upper, r_lower, r_upper):
        """ merging two sorted arrays to one sorted array """
        i, j = l_lower, r_lower
        temp = []
        while i <= l_upper and j <= r_upper:
            if unsorted[i].value <= unsorted[j].value:
                temp.append(unsorted[i])
                i += 1
            else:
                temp.append(unsorted[j])
                j += 1
        while i <= l_upper:
            temp.append(unsorted[i])
            i += 1
        while j <= r_upper:
            temp.append(unsorted[j])
            j += 1

        for y, k in enumerate(range(l_lower, r_upper + 1)):
            unsorted[k] = temp[y]
            unsorted[k].index = k  # set index to trigger dispatch

    # ==============================================================
    # Quick Sort Algorithm

    def quick_sort(self, unsorted, start, end):
        """ quick sort recursive algorithm """
        if start >= end:
            return
        i_pivot = self.partition(unsorted, start, end - 1)
        self.quick_sort(unsorted, start, i_pivot)
        self.quick_sort(unsorted, i_pivot + 1, end)

    def partition(self, unsorted, start, end):
        """ arrange (left array < pivot) and (right array > pivot) """
        pivot = unsorted[end]
        i_pivot = start
        for i in range(start, end):
            if unsorted[i].value <= pivot.value:
                self.swap(unsorted, i, i_pivot)
                i_pivot += 1
        self.swap(unsorted, i_pivot, end)
        return i_pivot

    ########################################################################

    @staticmethod
    def swap(arr, a, b, self):
        """ helper function to swap elements a and b in an array """
        arr[a].index = b  # set index to trigger dispatch
        arr[b].index = a  # set index to trigger dispatch
        temp = arr[a]
        arr[a] = arr[b]
        arr[b] = temp
        


# Sorting Algorithm Visualiser

from bar import Bar
import tkinter as tk
import random
from ttkthemes import themed_tk as theme
from tkinter import ttk as ttk
from tkinter import messagebox
from solver import Solver
from time import sleep

class SortVisualiser:
    anim_speed = 0
    def __init__(self):
        """ initialise sorting algorithm visualiser """
        self.algorithms = ['Selection Sort', 'Insertion Sort', 'Bubble Sort', 'Merge Sort', 'Quick Sort']  # list of sorting algorithms implemented
        self.graph_width, self.graph_height = 1430, 810  # ui window width and height
        self.root = theme.ThemedTk()  # define themed root
        self.menu_frame = ttk.Frame(self.root, width=self.graph_width / 2)  # create menu frame
        self.canvas = tk.Canvas(self.root, height=self.graph_height, width=self.graph_width, bg='#222222')  # create tkinter canvas
        self.n_bars = 100  # starting number of items to sort
        self.bars = []  # initialise empty list to store bar objects
        self.bar_width = 0  # bar width -> calculated later depending on width and n_bars
        self.y_scale = 0  # scaling factor to fit heights on screen
        self.solve_mode = 0  # initially select selection sort, algorithms[0]
        self.colours = ['#FFE45C', '#2ECBE9', '#2F7AE5', '#797EF6', '#4ADEDE', '#1AA7EC']
        self.colour = random.sample(self.colours, k=1)
        self.v1 = tk.DoubleVar()
        self.v2 = tk.StringVar()
        self._custom_trigger = False
        self.barvals = [100,33,88,99,11]
        self.graphs = ['Bar Graph','Scatter Graph']
        self.graph_mode = 0
        self.update_counter = 0
        self.pause_var = tk.StringVar()

        # progress monitoring variables
        self.is_solving = False
        self.is_rendering = False

        # configure tkinter visual properties
        self.config_root()
        self.config_menu()
        self.config_canvas()

        self.root.bind('<F1>', self.function_call)
        # press <F9> to update the tkinter variable
        self.root.bind('<F9>', lambda e: self.pause_var.set(1))
        # run ui visualisation loop
        self.root.mainloop()


    def function_call(self,event=None):
        print('pause')
        self.root.wait_variable(self.pause_var)
        print('continue')
        
    def config_root(self):
        """ configure tkinter root object """
        self.root.title('Sorting Algorithm Visualisation')  # set window title
        self.root.resizable(True, True)  # non-responsive window
        self.root.set_theme('radiance')  # set window style theme

    def config_menu(self):
        """ menu - user configurable settings for visualisation"""

        # create menu frame on top of screen
        self.menu_frame.grid(row=0, column=0, sticky='new')

        # create run button and reset buttons
        start_button = ttk.Button(self.menu_frame, text='Start', command=self.validate_setup)
        regenerate_button = ttk.Button(self.menu_frame, text='Create/Regenerate', command=self.clean_canvas)
        pause_button = ttk.Button(self.menu_frame, text='Pause', command=self.function_call)
        continue_button = ttk.Button(self.menu_frame, text='Continue', command=lambda : self.pause_var.set(1))
        
        

        # track currently selected algorithm
        current_algo = tk.StringVar()
        current_algo.set(self.algorithms[self.solve_mode])

        # add algorithms option menu
        algorithms_menu = ttk.OptionMenu(self.menu_frame, current_algo, self.algorithms[0], *self.algorithms, command=self.algorithm_change)
        algorithms_menu.config(width=15)
        
        current_plot = tk.StringVar()
        current_plot.set(self.graphs[self.graph_mode])
        
        plot_menu = ttk.OptionMenu(self.menu_frame, current_plot, self.graphs[0], *self.graphs, command=self.plot_change)
        plot_menu.config(width=15)

        # allow user to define unsorted array size - only accept numeric input
        ttk.Label(self.menu_frame, text='Array Size', anchor='e')
        callback = self.menu_frame.register(self.only_numeric_input)
        ttk.Entry(self.menu_frame, validate="key", validatecommand=(callback, "%P")).insert(0, str(self.n_bars))

        #speed deneme
        dynamic_label = ttk.Label(self.menu_frame, text='Animation Speed:', anchor='e')
        callback2 = self.menu_frame.register(self.change_anim_speed)
        tk.Scale(self.menu_frame, showvalue=1, orient=tk.HORIZONTAL, command=(callback2))
        
        ttk.Label(self.menu_frame, text='Custom Array', anchor='e')
        callback3 = self.menu_frame.register(self.only_list_input)
        ent1 = ttk.Entry(self.menu_frame, validate="focusout", validatecommand=(callback3, "%P")).insert(0, str(','.join([str(i) for i in self.barvals])))
        self.root.bind('<Return>',print(callback3))
        
        
        
        ttk.Label(self.menu_frame,justify='center', textvariable=self.v2, anchor='e')

        # iterate over menu children and assign it a position in the grid
        for c, child in enumerate(self.menu_frame.winfo_children()):
            pad = 0 if isinstance(child, tk.Button) else 5
            child.grid_configure(row=c+2, column=0, sticky='ew', padx=pad, pady=pad)
            
        pause_button.grid_configure(row=1, column=0, sticky='ew', padx=0, pady=0)
        continue_button.grid_configure(row=2, column=0, sticky='ew', padx=0, pady=0)
        start_button.grid_configure(row=0, column=0, sticky='ew', padx=0, pady=0)
        regenerate_button.grid_configure(row=3, column=0, sticky='ew', padx=0, pady=0)


    def config_canvas(self):
        """ pack canvas on root and bind mouse event methods """
        # once canvas is configured, configure bars
        self.canvas.bind('<Configure>', self.config_bars)
        self.canvas.grid(row=0, column=1)

    # event param is not used but it is required
    def config_bars(self, event=None):
        """ configure array of bars to sort """
        # check if program is running or bars is less than 2
        if self.is_solving or self.n_bars < 2:
            self.is_rendering = False  # stop rendering and end configuration
            return

        
        self.bars = []  # initialise list of bars
        self.bar_width = self.graph_width / self.n_bars  # calcualte bar width based on graph width and number of bars
        values = random.sample(range(0, self.n_bars), self.n_bars)  # create random sample of values - values from zero to the number of bars
        
        if self._custom_trigger:
            values = self._custom_bar_values
            print(values)
            self.y_scale = self.graph_height / max(values)
            self._custom_trigger= False
        
        self.y_scale = self.graph_height / max(values)  # determine scaling factor to fit bars inside available height

        # iterate over the bars
        for i, value in enumerate(values):
            bar = Bar(self.bar_width, i, value * self.y_scale, self)
            self.bars.append(bar)
            self.render_bar(bar)

        # bar initial rendering complete
        self.is_rendering = False
        self.barvals = values

    def clean_canvas(self):
        self.pause_var.set(1)
        """ delete all bars from the canvas and redraw """
        # check if screen is already rendering or solving
        if self.is_rendering or self.is_solving:
            return
        self.is_rendering = True
        # delete all bars on canvas
        for bar in self.bars:
            self.canvas.delete(bar.shape)

        self.colour = random.sample(self.colours, k=1)

        # reconfigure bars
        self.config_bars()
        self.update_counter = 0
        self.pause_var.set(1)

    def change_array_size(self, value):
        """ change graph size """
        if self.is_rendering or self.is_solving:
            return

        # clean canvas and render updated array size
        self.n_bars = int(float(value))
        self.clean_canvas()
        
    def change_anim_speed(self, value):
        if self.is_rendering or self.is_solving:
            return

        # update animation speed
        self.anim_speed = (100-(float(value)))/2500
        print(self.anim_speed)
        

    def algorithm_change(self, *args):
        """ change solve mode """
        self.solve_mode = self.algorithms.index(args[0])
        
    def plot_change(self, *args):
        """ change solve mode """
        self.graph_mode = self.graphs.index(args[0])
        self.clean_canvas()

    def validate_setup(self):
        """ validate inputs to avoid unitialised errors """
        if self.bars is None or self.is_solving or self.is_rendering:
            return

        self.is_solving = True

        # create sorting solver object
        Solver(self.bars, self.n_bars, self.solve_mode, self)

        self.is_solving = False

    def render_bar(self, bar):
        """ draw bar on canvas """
        # render bar shape blue rectangle
        if self.graph_mode == 1:
            bar.shape = self.canvas.create_oval(bar.x1, self.graph_height-bar.value, bar.x2, self.graph_height-bar.value+(bar.x2-bar.x1), fill=self.colour)
            
        elif self.graph_mode == 0:
            bar.shape = self.canvas.create_rectangle(bar.x1, self.graph_height, bar.x2, self.graph_height-bar.value, fill=self.colour)
            
        else:
            bar.shape = self.canvas.create_rectangle(bar.x1, self.graph_height, bar.x2, self.graph_height-bar.value, fill=self.colour)
        self.root.update()
        print(self.graph_mode)

    def update_bar(self, bar, fill):
        """ update bar coordinates """
        self.update_counter += 1
        # update bar is called from bar object when coordinates change
        if self.graph_mode == 1:
            self.canvas.coords(bar.shape, bar.x1, self.graph_height-bar.value, bar.x2, self.graph_height-bar.value+(bar.x2-bar.x1))
        
        elif self.graph_mode == 0:
            self.canvas.coords(bar.shape, bar.x1, self.graph_height, bar.x2, self.graph_height-bar.value)
        
        else:
            self.canvas.coords(bar.shape, bar.x1, self.graph_height, bar.x2, self.graph_height-bar.value)
        # show updating bar as red
        self.canvas.itemconfig(bar.shape, fill=fill)
        self.root.update()
        self.v2.set('Karşılaştırma Sayısı: '+str(self.update_counter))
        print(self.v2.get())

        # after move complete, change colour back to blue
        self.canvas.itemconfig(bar.shape, fill='green')
        sleep(self.anim_speed)
        

    def only_numeric_input(self, i):
        try:
            if i == '' or i == '100':
                self.n_bars = 100
            else:
                self.n_bars = int(i)
            return True
        except Exception as e:
            tk.messagebox.showerror('Array Size Error', 'Please enter a positive integer for the array size or leave blank 100')
            print(e)
            return False
        
    def only_list_input(self, i):
        try:
            if i == '' or i == ",":
                self.n_bars = 100
            else:
                #self.n_bars = "100,50,99"
                temp_count = 0
                split = list(i.split(','))
                self.n_bars = int(len(split))
                for val in split:
                    split[temp_count] = int(val)
                    temp_count += 1
                print(f'self.n_bars:{self.n_bars}')
                self._custom_bar_values = split
                self._custom_trigger = True
            return True
        except Exception as e:
            return False


# Program Driver for sorting visualisation
if __name__ == '__main__':
    visualiser = SortVisualiser()

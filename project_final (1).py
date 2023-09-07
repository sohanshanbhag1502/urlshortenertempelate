'''Jai Shree ram'''

# Importing required modules
import csv
import socket
from os.path import basename, exists
from random import randint, choice
from subprocess import run, Popen, PIPE
from threading import Thread
from tkinter import *
from tkinter import messagebox, ttk

# For add-on modules
try:
    import  pyperclip, requests
    from PIL import Image, ImageTk
    from plyer import notification
    modules_notfound = False
except ModuleNotFoundError:
    modules_notfound = True




# Checking the existence of all data files

# Create urlbase.csv if not found
if not exists(r'.\urlbase.csv'):
    open('urlbase.csv', 'w').close()

# Check for existance of swatik logo
if not exists('logo.png'):
    messagebox.showerror('Data file missing',
                         'File logo.png is missing.')
    exit(1)

# Check for the existance of icon file
if not exists('logo.ico'):
    messagebox.showerror('Data file missing',
                         'File logo.ico is missing.')
    exit(1)
if not exists('Bell.ico'):
    messagebox.showerror('Data file missing',
                         'File Bell.ico is missing.')
    exit(1)


#Checking for the internet connection


# Installer window class
class modules_installer(Tk):
    # Automatic installation of non-existing modules
    def __init__(self):
        # First checking the existance of pip before running the installer
        pip_exists = Popen('cmd.exe /C pip.exe', stdout=PIPE, stderr=PIPE)
        if "'pip.exe' is not recognized as an" in str(pip_exists.communicate()[1], encoding='UTF-8').strip():
            messagebox.showerror(
                'Pip not found', 'Install pip bootstrap before running this.')
            exit(1)

        IPaddress=socket.gethostbyname(socket.gethostname())
        if IPaddress=="127.0.0.1":
            messagebox.showerror(
                'No internet connection', 'Ensure a proper internet connection to install modules.')
            exit(1)
        
        # The installer window
        Tk.__init__(self)
        self.attributes('-topmost', True)
        self.geometry('500x300+{}+{}'.format(self.winfo_screenwidth() //2+1-250,
                     self.winfo_screenheight()//2+1-150))
        self.overrideredirect(1)
        self.update()
        self.create_install_widgets()

    def module_install(self):
        # Checking for existance of external modules
        module_list = str(run(['pip', 'list'], capture_output=True,
                          universal_newlines=True)).replace('\n', '')
        self.update()

        # Installation of required modules
        # pyperclip
        self.module_name.configure(text='Installing pyperclip...')
        self.update()
        run(['pip', 'install', 'pyperclip'])
        self.pro_bar.config(value=25)
        self.comp.config(text='25.0%')
        self.update()

        # requests
        self.module_name.configure(text='Installing requests...')
        self.update()
        run(['pip', 'install', 'requests'])
        self.pro_bar.config(value=50)
        self.comp.config(text='50.0%')
        self.update()

        # python imaging library
        self.module_name.configure(text='Installing pillow (PIL)...')
        self.update()
        run(['pip', 'install', 'pillow'])
        self.pro_bar.config(value=75)
        self.comp.config(text='75.0%')
        self.update()
        
        # plyer
        self.module_name.configure(text='Installing plyer...')
        self.update()
        run(['pip', 'install', 'plyer'])
        self.pro_bar.config(value=100)
        self.comp.config(text='100.0%')
        self.update()

        # Notifying the success of installation of modules
        from plyer import notification
        notification.notify(
            app_name='Module installer',
            title='Installation Success',
            message='All external modules were installed successfully',
            timeout=10,
            app_icon='Bell.ico'
        )

        # Restarting the app after installation of modules
        self.module_name.configure(text='Restarting the app...')
        self.update()
        self.after(10000, self.destroy)

    def create_install_widgets(self):
        # Creating installer widgets
        Label(
            self, text='SOS URL Shortener', font='Haettenschweiler 30').pack(side=TOP, fill=X)
        Label(
            self, text='Be patient! Installing pre\nrequisite modules using pip bootstrap!', font='Arial 20 italic').pack(pady=25)
        self.module_name = Label(
            self, text='Checking for existence of modules...', font='Arial 18')
        self.comp = Label(
            self, text='0.0%', font='Arial 18')
        self.pro_bar = ttk.Progressbar(
            self, length=496, mode='determinate', orient='horizontal', maximum=100, value=0)

        # Placement of widgets in window
        self.module_name.place(x=0, y=210)
        self.comp.place(x=415, y=210)
        self.pro_bar.place(x=2, y=255)
        self.update()

        # Starting installation process thread
        Thread(target=self.module_install).start()




# Main window class
class Mainwin(Tk):
    def __init__(self):
        # Main window
        Tk.__init__(self)
        self.resizable(0, 0)
        self.config(background='#1e1f1c')
        self.HEIGHT = 600
        self.BREADTH = 600
        self.geometry('{}x{}+400+50'.format(self.HEIGHT, self.BREADTH))
        self.title('SOS URL Shortener')
        self.iconbitmap('logo.ico')
        self.config(background='#1e1f1c')

    def create_mainwidgets(self):
        # Main header label
        Label(self, text='SOS URL Shortener', font='Haettenschweiler 30',
              bg='#1e1f1c', fg='#ffffff').pack()

        # Configuring the appearance of notebook widget
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("TNotebook", background='#1e1f1c')
        self.style.map("TNotebook.Tab", background=[("selected", "#262823")])
        self.style.configure(
            "TNotebook.Tab", background='#34352f', foreground='#ffffff')

        # The notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=BOTH, expand=1)

        # Tabs
        self.quick_shortner_frame_widget()
        self.history_frame_widget()

    def quick_shortner_frame_widget(self):
        # The main Quick response frame
        self.Qsframe = Frame(self.notebook, background='#262823')

        # The functions
        call = lambda _:(self.quickshorten.event_generate('<1>'),
                         self.quickshorten.update(), self.quick_shorten())

        def copy_to_clipboard():
            if self.output.get(1.0, END).strip().replace('\n', '') == 'The Shortened url comes here...':
                pyperclip.copy(self.text1.get(0.0, END) +
                               self.text2.get(0.0, END))
            else:
                pyperclip.copy(self.text1.get(0.0, END) +
                               self.text2.get(0.0, END))
            notification.notify(
                app_name='URL Shortner',
                title='Copied to clipboard.',
                message='Copied url to clipboard successfully',
                timeout=10,
                app_icon='Bell.ico'
            )


        # Function executed when user clicks on the input entry box
        focusin = lambda _:((self.link.config(fg='black'), self.link.delete(0, END), self.link.insert(0, "https://"))
                            if self.link.get() == 'https://example.com/xyz' else False)

        focusout = lambda _:((self.link.config(fg='#7c787c'), self.link.delete(0, END), self.link.insert(0, 'https://example.com/xyz'))
                            if self.link.get().isspace() or not self.link.get() or self.link.get() == 'https://' else False)

        # The Threads
        thread = lambda _=None:Thread(
            target=self.quick_shorten, daemon=True).start()
        thread1 = lambda _:(Thread(target=self.isvalid, args=(self.link.get(
        ),), daemon=True).start() if self.link.get() != 'https://example.com/xyz' else False)
        thread2 = lambda _:Thread(
            target=copy_to_clipboard, daemon=True).start()

        # The quick shortener tab widgets
        # Link entry box
        Label(self.Qsframe, text='Enter link:', foreground='#ffffff',
              font='Calibri 20', background='#262823').pack(anchor=NW, pady=8, padx=3)
        self.link = Entry(self.Qsframe, font='Helvetica 18',
                          width=45, fg='#7c787c')
        self.link.insert(0, 'https://example.com/xyz')

        # The Quick shortner button
        self.quickshorten = Button(
            self.Qsframe, text='Shorten',  bg='#1e1f1c', fg='white', cursor='hand2', command=thread, font="Helvetica 18"
            , relief=RIDGE, activeforeground='grey', activebackground='#34352f')

        # The Shortened url output
        self.output = Text(
            self.Qsframe, height=1, font='Helvetica 18 italic', fg='grey', width=44)
        self.output.insert(1.0, 'The shortened url comes here...')
        self.output.configure(state=DISABLED)

        # The Copy to clipboard label
        self.clip = Label(
            self.Qsframe, text='Copy to clipboard', fg='lightblue', bg='#262823', font='helvetica 18', cursor='hand2')
        self.clip.bind('<Enter>', lambda _: self.clip.config(
            font='helvetica 18 underline'))
        self.clip.bind(
            '<Leave>', lambda _: self.clip.config(font='helvetica 18'))

        # The swastik logo inclusion
        self.logo = Image.open('logo.png')
        self.logo = ImageTk.PhotoImage(self.logo)
        self.canvas = Canvas(
            self, bg='#222420', width=68, height=68, highlightthickness=0)
        self.canvas.create_image(35, 35, image=self.logo)

        # The placement of widgets
        self.link.pack(anchor=NW, padx=6)
        self.quickshorten.place(x=250, y=380)
        self.output.place(x=9, y=450)
        self.clip.place(x=9, y=490)
        self.canvas.place(x=500, y=0)

        # Event Bindings
        self.link.bind('<Enter>', thread1)
        self.link.bind('<Return>', call)
        self.link.bind('<Return>', thread)
        self.link.bind('<BackSpace>', lambda _: self.link.config(fg='black'))
        self.link.bind("<FocusIn>", focusin)
        self.link.bind("<FocusOut>", focusout)
        self.quickshorten.bind('<Enter>',
                               lambda _: (self.quickshorten.config(foreground='lightgrey', bg='#181818', relief='raised'),
                               self.quickshorten.place(x=250, y=375)))
        self.quickshorten.bind('<Leave>',
                               lambda _: (self.quickshorten.config(foreground='white', bg='#1e1f1c', relief='ridge'),
                               self.quickshorten.place(x=250, y=380)))
        self.clip.bind('<1>', thread2)

        # Adding Customizations Labelframe
        self.customizations_frame()

        # Adding Suggestions LabelFrame
        self.suggestions_frame()

        # Adding the entire frame to the notebook
        self.notebook.add(self.Qsframe, text='Quick Shortener')

    def quick_shorten(self):
        # Used to generate random shortened URL
        url = self.link.get()

        # Accessing the Shortened URL from csv file
        with open("urlbase.csv", "r", newline="") as file:
            r = list(csv.reader(file))
            for i in r:
                # If the url already exists in csv file4 
                if i[0] == url:
                    output_url = i[1]
                    self.output.config(state=NORMAL)
                    self.output.delete(1.0, END)
                    self.output.insert(1.0, output_url)
                    self.output.configure(
                        state=DISABLED, fg='black', font='helvetica 18')
                    return

        # If url is not correct and not in csv file
        # Checking for internet connection
        IPaddress=socket.gethostbyname(socket.gethostname())
        if IPaddress=="127.0.0.1":
            messagebox.showerror(
                    'No internet connection', 'Ensure a proper internet connection to shorten the url.')
            exit(1)
        # If user doesnt provide the URL
        if url == 'https://example.com/xyz':
            messagebox.showerror(
                'Syntax Error', 'Please enter a valid URL')
            return
        # Checking validity of the url using requests
        validity = self.isvalid(url)
        if not validity:  # Invalid URL
            if validity == -1:
                return
            messagebox.showerror(
                'Syntax Error', 'Please enter a valid URL')
            return

        # The provided url has successfully passed all integrity checks
        # Generating the shortened URL
        shorturl = "https://b.in/" + \
            chr(randint(97, 122)) + \
            chr(randint(97, 122)) + chr(randint(97, 122))
        urldata = (url, shorturl)

        # Adding new contents to the file
        with open("urlbase.csv", 'a+', newline="") as file:
            w = csv.writer(file)
            w.writerow(urldata)
        output_url = shorturl

        # Configuring the output entry box
        self.output.config(state=NORMAL)
        self.output.delete(1.0, END)
        self.output.insert(1.0, output_url)
        self.output.configure(
            state=DISABLED, fg='black', font='helvetica 18')
        self.update_history()

    def isvalid(self, url):
        # Checking the existance of URL on the Internet
        try:  # Checking validity of the url using requests
            request = requests.get(url)
            if request.status_code == 200:
                self.link.config(fg='green')
                return True
            else:
                self.link.config(fg='red')
                return False
        except:
            self.link.config(fg='red')
            return False
            

    # The Customizations frame
    def customizations_frame(self):
        # The Functions
        on_click = lambda _:((self.text2.delete(0.0, END), self.text2.config(fg='black'))
                              if 'Type custom suffix here...' in self.text2.get(0.0, END) else False)

        off_click = lambda _:((self.text2.insert(0.0, 'Type custom suffix here...'), self.text2.config(fg='#7c787c'))
                               if self.text2.get(0.0, END).isspace() or self.text2.get(0.0, END) == "" else False)

        def command():
            # Function to switch between Custom and prog generated URL
            if self.output.get(0.0, END).strip().strip('\n') == 'The shortened url comes here...' or self.output.get(0.0, END).strip().strip('\n'):
                # Switching to custom URL
                self.text2.config(fg='#7c787c')
                self.output.config(state=NORMAL)
                self.output.delete(0.0, END)
                self.output.config(state=DISABLED)
                self.text2.config(state=NORMAL)
                self.text2.insert(0.0, 'Type custom suffix here...')
                self.text2.config(fg='grey')
                self.conflict.config(text='')
                self.conflict.place(x=20, y=70)
                self.quickshorten.config(command=self.shoten_custom)

            else:
                # Switching to program generated URL
                self.output.config(state=NORMAL, fg='gray', font='Arial 18 italic')
                self.output.delete(0.0, END)
                self.output.insert(0.0, 'The shortened url comes here...')
                self.text2.config(font='Arial 18', fg='black')
                self.output.config(state=DISABLED)
                self.text2.config(state=NORMAL)
                self.text2.delete(0.0, END)
                self.conflict.place_forget()
                self.text2.config(state=DISABLED)
                self.quickshorten.config(command=self.quick_shorten)

        # The customizations label frame
        self.customization_frame = LabelFrame(
            self.Qsframe, text='Customizations', fg='white', bg='#262823', font='Arial 18', height=150, width=580)
        self.customization_frame.place(x=10, y=100)

        # The customizations frame widgets

        # The checkbutton
        self.check = Checkbutton(self.customization_frame, bg='#262823', font='helvetica 15', activeforeground='gray',
                                 activebackground='#262823', command=command, indicatoron=True, onvalue=1, offvalue=0)
        
        Label(self.customization_frame, text='Customize', fg='white',
              bg='#262823', font='Arial 18').place(x=20, y=0)

        # The 1st text widget(Domain prefix)
        self.text1 = Text(self.customization_frame, height=1,
                          width=10, font='Arial 18', fg='#7c787c')
        self.text1.insert(0.0, 'https://b.in/')
        self.text1.config(state=DISABLED)

        # The 2nd text widget(Suffix)
        self.text2 = Text(self.customization_frame, height=1,
                          width=30, font='Arial 18', fg='#7c787c')
        self.text2.config(state=DISABLED)

        # The status display label widget
        self.conflict = Label(self.customization_frame,
                              font='Arial 18', bg='#262823')

        # The placement of widgets
        self.check.place(x=0, y=0)
        self.text1.place(x=20, y=30)
        self.text2.place(x=154, y=30)

        # The event bindings
        self.text2.bind('<FocusIn>', on_click)
        self.text2.bind('<FocusOut>', off_click)
        self.text2.bind('<Return>', self.shoten_custom)


    #The suggestions label frame
    def suggestions_frame(self):
        # The Suggestions Frame
        self.suggestions = LabelFrame(self.Qsframe, text='Suggestions', fg='white', bg='#262823', font='Arial 18',
                                      height=100, width=580)

        # The Suggestions output boxes
        self.sugg1 = Text(self.suggestions, height=1, width=5,
                          font='Arial 18', state=DISABLED)

        self.sugg2 = Text(self.suggestions, height=1, width=5,
                          font='Arial 18', state=DISABLED)

        self.sugg3 = Text(self.suggestions, height=1, width=5,
                          font='Arial 18', state=DISABLED)

        self.sugg4 = Text(self.suggestions, height=1, width=5,
                          font='Arial 18', state=DISABLED)

        # The placement of widgets
        self.sugg1.place(x=75, y=10)
        self.sugg2.place(x=195, y=10)
        self.sugg3.place(x=315, y=10)
        self.sugg4.place(x=435, y=10)
        self.suggestions.place(x=10, y=270)

    def give_suggestions(self, domain):
        # Function to generate 4 suggestions for a given domain
        with open("urlbase.csv") as file:
            r = csv.reader(file)
            data = []
            for i in list(r):
                if domain in i[1]:
                    data.append(i[1])

            suggestions = []
            s = 0
            characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "_",
                          "-", ".", "!", "@", "#", "$", "%", "&", "*"]
            while s < 4:
                d = domain + choice(characters)
                if d in data or d in suggestions:
                    continue
                else:
                    suggestions.append(d)
                    s += 1
        return suggestions

    def show_suggestions(self, domain):
        # Function to dispaly the generated 4 suggestions
        suggs = self.give_suggestions(domain)
        self.sugg1['state'] = NORMAL
        self.sugg2['state'] = NORMAL
        self.sugg3['state'] = NORMAL
        self.sugg4['state'] = NORMAL
        self.sugg1.insert(0.0, suggs[0])
        self.sugg1['state'] = DISABLED
        self.sugg2.insert(0.0, suggs[1])
        self.sugg2['state'] = DISABLED
        self.sugg3.insert(0.0, suggs[2])
        self.sugg3['state'] = DISABLED
        self.sugg4.insert(0.0, suggs[3])
        self.sugg4['state'] = DISABLED

    def shoten_custom(self, _=None):
        # Function to store custom shortened URL provided by the user
        custom_url = self.text1.get(0.0, END).strip(
            '\n')+self.text2.get(0.0, END).strip('\n')
        with open('urlbase.csv', 'r', newline="") as csv_:
            content = list(csv.reader(csv_))

        url = self.link.get()

        # Checking validity of the provided custom url
        if 'Type custom suffix here...' in custom_url:
            messagebox.showerror(
                'Error', 'Please enter a valid suffix.')
            return
        if url == 'https://www.example.com/xyz':
            messagebox.showerror(
                'Syntax Error', 'Please enter a valid URL.')
            return
        validity = self.isvalid(url)
        if not validity or validity == -1:
            if validity == -1:
                return
            messagebox.showerror(
                'Syntax Error', 'Please enter a valid URL.')
            return

        for i in content:
            if url == i[0] and custom_url == i[1]:
                # Both custom and input URL match
                self.conflict.config(
                    text='The given url and custom url is already in use.', fg='#ffa500')
                break
            elif url != i[0] and custom_url == i[1]:
                # If Custom URL doesnt match the input URL
                self.conflict.config(
                    text='ERROR:The given custom url is already in use.', fg='#ffa500')
                self.show_suggestions(custom_url[13:])
                break
            elif url == i[0] and custom_url != i[1]:
                # If input URL doesnt match the custom URL
                content[content.index(i)][1] = custom_url
                self.conflict.config(
                    text='The given custom url was successfully replaced.', fg='green')
                break

        else:
            # Storing the new custom URL in the csv file
            content.append([url, custom_url])
            self.conflict.config(
                text='The given url was shortened.', fg='green')

        # Updating the history tab with new contents
        with open("urlbase.csv", 'w', newline="") as file:
            w = csv.writer(file)
            w.writerows(content)
        self.update_history()



    # The History Tab
    def history_frame_widget(self):
        # The frame with History tab
        self.hist_frame = Frame(self.notebook)

        # The scrollbars
        self.XScroll = Scrollbar(self.hist_frame,  orient='horizontal')
        self.YScroll = Scrollbar(self.hist_frame, orient='vertical')

        # The Text Widget
        self.hist_frame.text = Text(
            self.hist_frame, font=('Cascadia Code SemiLight', '15'), wrap='none',
            xscrollcommand=self.XScroll.set, yscrollcommand=self.YScroll.set)
        self.XScroll.config(command=self.hist_frame.text.xview)
        self.YScroll.config(command=self.hist_frame.text.yview)

        self.update_history()  # To update the contents of Text widget

        # The placement of widgets
        self.XScroll.pack(side=BOTTOM, fill=X)
        self.YScroll.pack(side=RIGHT, fill=Y, anchor=E)
        self.hist_frame.text.pack(fill=BOTH, expand=1)

        # Adding history tab to notebook
        self.notebook.add(self.hist_frame, text='  History\t')


    def update_history(self):
        # The function to update the contents of Text widget
        self.hist_frame.text.config(state=NORMAL)
        self.hist_frame.text.delete(0.0, END)
        self.hist_frame.text.insert(0.0, 'User history:\n\n')

        # Copy contents of csv to text widget
        with open('urlbase.csv', newline="") as cs:
            content = list(csv.reader(cs))
            for index, val in enumerate(content):
                self.hist_frame.text.insert(INSERT, f'URL-{index+1}:\n')
                self.hist_frame.text.insert(
                    INSERT, f'   Original:  {val[0]}  \n')
                self.hist_frame.text.insert(
                    INSERT, f'   Shortened: {val[1]}  \n\n')
            else:
                self.hist_frame.text.config(state=DISABLED)

        # If csv file is empty
        if not list(content):
            self.hist_frame.text.config(state=NORMAL)
            self.hist_frame.text.insert(
                END, 'The shortened url\'s will be shown here.')
            self.hist_frame.text.config(state=DISABLED)




# If this file is executed individually
if __name__ == '__main__':
    if modules_notfound:
        #  For installation of modules
        modules_installer().mainloop()
        run(['python', str(basename(__file__))])
        exit(1)

    else:
        # Execution of main code
        main_app = Mainwin()
        main_app.create_mainwidgets()
        main_app.mainloop()

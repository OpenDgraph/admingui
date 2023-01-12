import customtkinter
from PIL import Image
import os
import calls
import re
import arguments as _args
from utils import separators_constructor

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Dgraph Admin GUI")
        self.addr = 'http://localhost:8080/admin' if _args.arguments.hostname == None else _args.arguments.hostname
        self.geometry('1115x900')
        self.resizable(True, True)

        # self.grid_columnconfigure((2, 3), weight=0)
        # self.grid_rowconfigure((0, 1, 2), weight=1)

        # create textbox
        Font_tuple = ('Consolas', 18, "bold")
        self.textbox = customtkinter.CTkTextbox(self, width=800, height=750)
        self.textbox.configure(font=Font_tuple)
        self.textbox.grid(row=1, column=0, padx=(
            10, 0), pady=(20, 0), sticky="nsew")

        self.textbox_button = customtkinter.CTkButton(self.textbox, text="Clean logs",
                                                      command=self.clean_text_event)
        self.textbox_button.grid(row=3, column=0, padx=20, pady=(10, 10))

        # create url entry
        self.url_entry = customtkinter.CTkEntry(
            self, placeholder_text=self.addr)
        self.url_entry.grid(row=0, column=0, sticky="new",
                            padx=18, pady=(30, 15))
        self.addr_button = customtkinter.CTkButton(
            master=self.url_entry, text="change", command=self.change_addr_event, width=50)
        self.addr_button.grid(row=0, column=1, padx=0)
        self.url_entry.insert(0, str(self.addr))

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=280, height=150)
        self.tabview.grid(row=1, column=2, padx=(9, 0),
                          pady=(2, 0), sticky="nsew")
        # Tabs
        self.tabview.add("Info")
        self.tabview.add("Operations")
        self.tabview.add("Configs")
        self.tabview.add("Login")

        # configure grid of individual tabs
        self.tabview.tab("Info").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Operations").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Login")

        self.dqlLog = customtkinter.CTkButton(self.tabview.tab("Info"), text="Activate DQL Logs",
                                              command=self.logRequest)

        self.dqlLog.grid(row=2, column=0, padx=20, pady=(10, 10))

        self.stateLog = customtkinter.CTkButton(self.tabview.tab("Info"), text="Show state",
                                                command=self.stateRequest)
        self.stateLog.grid(row=3, column=0, padx=20, pady=(10, 10))

        self.queryGroup = customtkinter.CTkButton(self.tabview.tab("Info"), text="Show users in groups",
                                                  command=self.groupRequest)
        self.queryGroup.grid(row=4, column=0, padx=20, pady=(10, 10))

        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab(
            "Operations"), text="CTkLabel on Tab Operations")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # create login
        self.login_frame = customtkinter.CTkFrame(
            self.tabview.tab("Login"), corner_radius=0)
        self.login_frame.pack(expand=True, fill="both", padx=0, pady=0)
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Dgraph ACL Login",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 15))

        self.username_entry = customtkinter.CTkEntry(
            self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.password_entry = customtkinter.CTkEntry(
            self.login_frame, width=200, show="*", placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.group_entry = customtkinter.CTkEntry(
            self.login_frame, width=200, placeholder_text="group (Optional: 'default')")
        self.group_entry.grid(row=3, column=0, padx=30, pady=(0, 15))

        self.login_button = customtkinter.CTkButton(
            self.login_frame, text="Login", command=self.login_request, width=200)
        self.login_button.grid(row=4, column=0, padx=30,  pady=(15, 5))

        self.create_logout_button = customtkinter.CTkButton(
            self.login_frame, text="Log out", command=self.log_out, width=200)
        self.create_logout_button.grid(row=5, column=0, padx=30, pady=(5, 15))

        self.create_groot_button = customtkinter.CTkButton(
            self.login_frame, text="Use Default groot", command=self.set_groot, width=200)
        self.create_groot_button.grid(row=6, column=0, padx=30, pady=(15, 5))

        self.create_user_button = customtkinter.CTkButton(
            self.login_frame, text="Create", command=self.create_event, width=200)
        self.create_user_button.grid(row=7, column=0, padx=30, pady=(5, 15))

        if _args.arguments.username != None:
            self.username_entry.insert(0, str(_args.arguments.username))
        if _args.arguments.password != None:
            self.password_entry.insert(0, str(_args.arguments.password))

    def log_out(self):
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        _args.arguments.token = None

    def set_groot(self):
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.username_entry.insert(0, "groot")
        self.password_entry.insert(0, "password")
        self.login_request()

    def login_request(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.username_entry.insert(0, str(username))
        self.password_entry.insert(0, str(password))

        _args.arguments.username = username
        _args.arguments.password = password

        request = calls.MakeCall(
            path="login/login", addr=self.addr).make_call()
        if "errors" not in request[0]:
            _args.arguments.token = str(request[0]["data"]
                                        ["login"]["response"]["accessJWT"])

        self.insert_text_event(request)

    def clean_text_event(self):
        self.textbox.delete(1.0, "end")

    def change_addr_event(self):
        self.addr = self.url_entry.get()

    def line_break(self, _insert):
        self.textbox.insert("end", _insert)
        self.textbox.yview_moveto(10000)

    def insert_text_event(self, payload=""):
        if "errors" in payload[0]:
            _response = separators_constructor(payload[0])
            self.line_break(_response)
            return
        elif "wrong" in payload:  # payload != [] and

            _response = separators_constructor(payload)
            self.line_break(_response)
            return

        myList = payload[1]

        response = ""

        for ii in range(len(myList)):
            pattern = r"\'{}\': (.*?),".format(myList[ii])
            matches = re.findall(pattern, str(payload[0]))
            response += "---\n"
            print("matches", matches)
            if len(matches) > 0:
                for i in range(len(matches)):
                    response += f"{myList[ii]}: {matches[i].replace('}','').replace('{','').replace('[','').replace(']','')}\n"
                    print("(matches)", matches[i])
                    continue
                print("response insert_text_event", response)

        _response = separators_constructor(payload, response)

        self.line_break(_response)

    def create_event(self):
        group = self.group_entry.get() if self.group_entry.get() != "" else "default"
        try:
            variables = {
                "input": [{"name": self.username_entry.get(), "password": self.password_entry.get(), "groups": {"name": group}}]
            }
            request = calls.MakeCall(
                path="add/addUser", variables=variables, addr=self.addr).make_call()
            self.insert_text_event(request)
        except NameError:
            error = f"Something else went wrong: {NameError}"
            self.insert_text_event(error)
        except Exception as e:
            error = f"Something else went wrong: {e}"
            self.insert_text_event(error)

    def logRequest(self):
        try:
            variables = {
                "input": {"logRequest": True}
            }
            request = calls.MakeCall(
                path="config/log", variables=variables, addr=self.addr).make_call()
            self.insert_text_event(request)
        except NameError:
            error = f"Something else went wrong: {NameError}"
            self.insert_text_event(error)
        except Exception as e:
            error = f"Something else went wrong: {e}"
            self.insert_text_event(error)

    def stateRequest(self):
        try:
            request = calls.MakeCall(
                path="information/state", addr=self.addr).make_call()
            self.insert_text_event(request)

        except NameError:
            error = f"Something else went wrong: {NameError}"
            self.insert_text_event(error)
        except Exception as e:
            error = f"Something else went wrong: {e}"
            self.insert_text_event(error)

    def groupRequest(self):
        try:
            request = calls.MakeCall(
                path="information/group", addr=self.addr).make_call()
            self.insert_text_event(request)

        except NameError:
            error = f"Something else went wrong: {NameError}"
            self.insert_text_event(error)
        except Exception as e:
            error = f"Something else went wrong: {e}"
            self.insert_text_event(error)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

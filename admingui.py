#
#  Copyright 2023 Dgraph Labs, Inc. and Contributors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import customtkinter
from PIL import Image
import calls
import re
import arguments as _args
from utils import separators_constructor, copy_to_clipboard

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Dgraph Admin GUI")
        self.addr = 'http://localhost:8080/admin' if _args.arguments.hostname == None else _args.arguments.hostname
        self.geometry('1115x900')
        self.resizable(True, True)
        _args.arguments.JSON = False

        # self.grid_columnconfigure((2, 3), weight=0)
        # self.grid_rowconfigure((0, 1, 2), weight=1)

        # create textbox
        Font_tuple = ('Courier', 16)
        self.textbox = customtkinter.CTkTextbox(self, width=800, height=750)
        self.textbox.configure(font=Font_tuple)
        self.textbox.grid(row=1, column=0, padx=(
            10, 0), pady=(20, 0), sticky="nsew")

        self.clean_button = customtkinter.CTkButton(self.textbox, text="Clean logs",
                                                    command=self.clean_text_event)
        self.clean_button.grid(row=3, column=0, padx=20, pady=(10, 10))

        self.JWT_button = customtkinter.CTkButton(self.textbox, text="JWT to Clipboard",
                                                  command=copy_to_clipboard)
        self.JWT_button.grid(row=3, column=0, padx=5, pady=(5, 5), sticky="e")
        self.JWT_button.configure(state="disabled")

        self.asjsonformat = customtkinter.CTkSwitch(
            self.textbox, text="Response as JSON", command=lambda: self.toggle_JSON())
        self.asjsonformat.grid(row=3, column=0, pady=10, padx=10, sticky="w")
        self.asjsonformat.configure(bg_color="#242424")

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
        self.tabview.add("ACL")

        # configure grid of individual tabs
        self.tabview.tab("Info").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Operations").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Configs").grid_columnconfigure(0, weight=1)
        self.tabview.tab("ACL").grid_columnconfigure(0, weight=1)

        # create tabview for ACL
        self.tabviewACL = customtkinter.CTkTabview(
            self.tabview.tab("ACL"), width=250, height=650)
        self.tabviewACL.grid(row=0, column=0, padx=(0, 0),
                             pady=(0, 0), sticky="nsew")

        self.tabviewACL.add("Login")
        self.tabviewACL.add("Namespaces/others")

        self.tabviewACL.tab(
            "Namespaces/others").grid_columnconfigure(0, weight=1)
        self.tabviewACL.tab("Login").grid_columnconfigure(0, weight=1)

        # Namespaces tab

        self.CreateNamespace = customtkinter.CTkButton(self.tabviewACL.tab("Namespaces/others"), text="Create Namespace",
                                                       command=self.open_input_CreateNamespace)
        self.CreateNamespace.grid(row=0, column=0, padx=20, pady=(30, 10))

        self.DeleteNamespace = customtkinter.CTkButton(self.tabviewACL.tab("Namespaces/others"), text="Delete Namespace",
                                                       command=self.open_input_DeleteNamespace)
        self.DeleteNamespace.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.addGroup = customtkinter.CTkButton(self.tabviewACL.tab("Namespaces/others"), text="Add Group",
                                                command=self.open_input_addGroup)
        self.addGroup.grid(row=2, column=0, padx=20, pady=(10, 10))

        self.deleteGroup = customtkinter.CTkButton(self.tabviewACL.tab("Namespaces/others"), text="Delete Group",
                                                   command=self.open_input_dialog_deleteGroup)
        self.deleteGroup.grid(row=3, column=0, padx=20, pady=(10, 10))

        self.deleteUser = customtkinter.CTkButton(self.tabviewACL.tab("Namespaces/others"), text="Delete User",
                                                  command=self.open_input_deleteUser)
        self.deleteUser.grid(row=4, column=0, padx=20, pady=(10, 10))

        # End of Namespaces tab

        self.dqlLog = customtkinter.CTkButton(self.tabview.tab("Configs"), text="Activate DQL Logs",
                                              command=self.logRequest)
        self.dqlLog.grid(row=0, column=0, padx=20, pady=(10, 10))

        self.label_tab_Info = customtkinter.CTkLabel(self.tabview.tab(
            "Info"), text="General Cluster information")
        self.label_tab_Info.grid(row=0, column=0, padx=20, pady=20)

        self.stateLog = customtkinter.CTkButton(self.tabview.tab("Info"), text="Show state",
                                                command=self.stateRequest)
        self.stateLog.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.queryGroup = customtkinter.CTkButton(self.tabview.tab("Info"), text="Show users in groups",
                                                  command=self.groupRequest)
        self.queryGroup.grid(row=2, column=0, padx=20, pady=(10, 10))

        self.config = customtkinter.CTkButton(self.tabview.tab("Info"), text="Show config",
                                              command=self.configRequest)
        self.config.grid(row=3, column=0, padx=20, pady=(10, 10))

        self.getCurrentUser = customtkinter.CTkButton(self.tabview.tab("Info"), text="Current User",
                                                      command=self.getCurrentUserRequest)
        self.getCurrentUser.grid(row=4, column=0, padx=20, pady=(10, 10))

        self.health = customtkinter.CTkButton(self.tabview.tab("Info"), text="Health",
                                              command=self.healthRequest)
        self.health.grid(row=5, column=0, padx=20, pady=(10, 10))

        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab(
            "Operations"), text="Cluster Operations")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        self.draining = customtkinter.CTkButton(self.tabview.tab("Operations"), text="Set Draining",
                                                command=self.drainingRequest)

        self.draining.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.shutdown = customtkinter.CTkButton(self.tabview.tab("Operations"), text="Shutdown",
                                                command=self.shutdownRequest)

        self.shutdown.grid(row=2, column=0, padx=20, pady=(10, 10))

        # create login
        self.login_frame = customtkinter.CTkFrame(
            self.tabviewACL.tab("Login"), corner_radius=0)
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

    def toggle_JSON(self):
        if _args.arguments.JSON != True:
            _args.arguments.JSON = True
        else:
            _args.arguments.JSON = False

    def log_out(self):
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        _args.arguments.token = None
        self.JWT_button.configure(state="disabled")
        self.JWT_button.configure(fg_color="grey")

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
            self.JWT_button.configure(state="normal")
            self.JWT_button.configure(fg_color="green")

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
        elif "wrong" in payload:
            _response = separators_constructor(payload)
            self.line_break(_response)
            return

        myList = payload[1]

        response = ""

        if _args.arguments.JSON != True:
            for ii in range(len(myList)):
                pattern = r"\'{}\': (.*?),".format(myList[ii])
                matches = re.findall(pattern, str(payload[0]))
                response += "——————————————\n"
                if len(matches) > 0:
                    for i in range(len(matches)):
                        response += f"{myList[ii]}: {matches[i].replace('}','').replace('{','').replace('[','').replace(']','')}\n"
                        continue
            _response = separators_constructor(payload, response, JSON=False)
            self.line_break(_response)
        else:
            _response = separators_constructor(payload[0], JSON=True)
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

    def drainingRequest(self):
        try:
            request = calls.MakeCall(
                path="operations/draining", addr=self.addr).make_call()
            self.insert_text_event(request)
        except NameError:
            error = f"Something else went wrong: {NameError}"
            self.insert_text_event(error)
        except Exception as e:
            error = f"Something else went wrong: {e}"
            self.insert_text_event(error)

    def shutdownRequest(self):
        try:
            request = calls.MakeCall(
                path="operations/shutdown", addr=self.addr).make_call()
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

    def configRequest(self):
        try:
            request = calls.MakeCall(
                path="information/config", addr=self.addr).make_call()
            self.insert_text_event(request)

        except NameError:
            error = f"Something else went wrong: {NameError}"
            self.insert_text_event(error)
        except Exception as e:
            error = f"Something else went wrong: {e}"
            self.insert_text_event(error)

    def getCurrentUserRequest(self):
        try:
            request = calls.MakeCall(
                path="information/currentUser", addr=self.addr).make_call()
            self.insert_text_event(request)

        except NameError:
            error = f"Something else went wrong: {NameError}"
            self.insert_text_event(error)
        except Exception as e:
            error = f"Something else went wrong: {e}"
            self.insert_text_event(error)

    def healthRequest(self):
        try:
            request = calls.MakeCall(
                path="information/health", addr=self.addr).make_call()
            self.insert_text_event(request)

        except NameError:
            error = f"Something else went wrong: {NameError}"
            self.insert_text_event(error)
        except Exception as e:
            error = f"Something else went wrong: {e}"
            self.insert_text_event(error)

    def CreateNamespace(self, password=None):
        try:
            variables = {
                "input": {"password": password}
            }
            request = calls.MakeCall(
                path="add/addNamespace", variables=variables, addr=self.addr).make_call()
            self.insert_text_event(request)
        except NameError:
            error = f"Something else went wrong: {NameError}"
            self.insert_text_event(error)
        except Exception as e:
            error = f"Something else went wrong: {e}"
            self.insert_text_event(error)

    def open_input_CreateNamespace(self):
        dialogNP = customtkinter.CTkInputDialog(
            text="The PASSWORD of your new Namespace", title="Create a namespace")
        password = dialogNP.get_input()
        if password == None or password == "":
            return
        try:
            variables = {
                "input": {"password": password}
            }
            request = calls.MakeCall(
                path="add/addNamespace", variables=variables, addr=self.addr).make_call()
            self.insert_text_event(request)
        except NameError:
            error = f"Something else went wrong: {NameError}"
            self.insert_text_event(error)
        except Exception as e:
            error = f"Something else went wrong: {e}"
            self.insert_text_event(error)

    def open_input_DeleteNamespace(self):
        dialogDNP = customtkinter.CTkInputDialog(
            text="Type the namespace ID", title="Delete namespace")
        ID = dialogDNP.get_input()
        if ID == None or ID == "":
            return
        try:
            variables = {
                "input": {"namespaceId": int(ID)}
            }
            request = calls.MakeCall(
                path="delete/deleteNamespace", variables=variables, addr=self.addr).make_call()
            self.insert_text_event(request)
        except NameError:
            error = f"Something else went wrong: {NameError}"
            self.insert_text_event(error)
        except Exception as e:
            error = f"Something else went wrong: {e}"
            self.insert_text_event(error)

    def open_input_addGroup(self):
        dialogaddGroup = customtkinter.CTkInputDialog(
            text="Type the name of the Group", title="Create a Group")
        name = dialogaddGroup.get_input()
        if name == None or name == "":
            return
        try:
            variables = {
                "input": {"name": str(name)}
            }
            request = calls.MakeCall(
                path="add/addGroup", variables=variables, addr=self.addr).make_call()
            self.insert_text_event(request)
        except NameError:
            error = f"Something else went wrong: {NameError}"
            self.insert_text_event(error)
        except Exception as e:
            error = f"Something else went wrong: {e}"
            self.insert_text_event(error)

    def open_input_dialog_deleteGroup(self):
        dialogdeleteGroup = customtkinter.CTkInputDialog(
            text="Type the name of the Group", title="Delete Group")
        name = dialogdeleteGroup.get_input()
        if name == None or name == "":
            return
        try:
            variables = {
                "name": str(name)
            }
            request = calls.MakeCall(
                path="delete/deleteGroup", variables=variables, addr=self.addr).make_call()
            self.insert_text_event(request)
        except NameError:
            error = f"Something else went wrong: {NameError}"
            self.insert_text_event(error)
        except Exception as e:
            error = f"Something else went wrong: {e}"
            self.insert_text_event(error)

    def open_input_deleteUser(self):
        dialogdeleteUser = customtkinter.CTkInputDialog(
            text="Type the User name to delete", title="Delete User")
        name = dialogdeleteUser.get_input()
        if name == None or name == "":
            return
        try:
            variables = {
                "name": str(name)
            }
            request = calls.MakeCall(
                path="delete/deleteUser", variables=variables, addr=self.addr).make_call()
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

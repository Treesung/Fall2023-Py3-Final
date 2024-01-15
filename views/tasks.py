import ttkbootstrap as tb
import requests as req
from K import *
from views.helper import View
from json import dumps

class SalariesView(View):
    def __init__(self, app):
        super().__init__(app)
        self.tree_columns = ("title", "id", "complete", "priority", "description")
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self.frame, text="Welcome to Teacher Salary Checker", bootstyle="info", font=(FONT_FAMILY, 25)).pack(side=TOP, pady=60)

        self.salaries_tree = tb.Treeview(self.frame, bootstyle=SUCCESS, columns=self.tree_columns, show=HEADINGS)
        self.salaries_tree.pack(expand=TRUE, fill=X, padx=PL, pady=PL)
        self.salaries_tree.heading('title', text="Month")
        self.salaries_tree.heading('id', text="Teacher ID")
        self.salaries_tree.heading('complete', text="Approval")
        self.salaries_tree.heading('priority', text="Salary Ranking")
        self.salaries_tree.heading('description', text="Description")

        tb.Button(self.frame, text="Get Salary List", command=self.get_salaries, bootstyle=DARK).pack(side=LEFT, padx=10, pady=10)
        tb.Button(self.frame, text="Create Salary", command=self.app.show_create_task_view, bootstyle="outline success").pack(side=RIGHT, padx=10, pady=10)
        tb.Button(self.frame, text="Update Salary", command=self.app.show_update_task_view, bootstyle="outline info").pack(side=RIGHT, padx=10, pady=10)

    def get_salaries(self):
        self.salaries_tree.delete(*self.salaries_tree.get_children())
        headers = {'Content-Type': "application/json", "Authorization": f"Bearer {self.app.token['access_token']}"}
        salaries = req.get(f"{self.app.url}salaries", headers=headers)
        salary_list = []
        for salary in salaries.json():
            salary_list.append(
                (salary["title"], str(salary["id"]), str(salary["complete"]), str(salary["priority"]), salary["description"]))
        for salary_data in salary_list:
            self.salaries_tree.insert('', END, values=salary_data)


class CreateSalaryView(View):
    def __init__(self, app):
        super().__init__(app)
        self.salary_month_var = tb.StringVar()
        self.teacher_id_var = tb.StringVar()
        self.salary_description_var = tb.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self.frame, text="Month:", font=(FONT_FAMILY, 25), bootstyle=PRIMARY).pack(padx=PM, pady=PM)
        tb.Entry(self.frame, textvariable=self.salary_month_var, width=40).pack(padx=PM, pady=PM)
        tb.Label(self.frame, text="Teacher ID:", font=(FONT_FAMILY, 25), bootstyle=PRIMARY).pack(padx=PM, pady=PM)
        tb.Entry(self.frame, textvariable=self.teacher_id_var, width=40).pack(padx=PM, pady=PM)
        tb.Label(self.frame, text="Salary Description:", font=(FONT_FAMILY, 25), bootstyle=PRIMARY).pack(padx=PM, pady=PM)
        tb.Entry(self.frame, textvariable=self.salary_description_var, width=40).pack(padx=PM, pady=PM)

        tb.Button(self.frame, text="Create Salary", command=self.create_salary, bootstyle=SUCCESS).pack(padx=PS, pady=PS)
        tb.Button(self.frame, text="Back", command=self.app.show_tasks_view, bootstyle="outline dark").pack(padx=PS, pady=PS)

    def create_salary(self):
        salary_month = self.salary_month_var.get()
        teacher_id = self.teacher_id_var.get()
        salary_description = self.salary_description_var.get()
        headers = {'Content-Type': "application/json", "Authorization": f"Bearer {self.app.token['access_token']}"}
        data = {
            "complete": False,
            "description": salary_description,
            "priority": 1,
            "title": salary_month,
            "id": teacher_id  # Assuming the 'id' field represents Teacher ID
        }
        response = req.post(f"{self.app.url}salaries", data=dumps(data), headers=headers)

        if response.status_code == 201:
            self.create_toast("Salary Created", f"Salary for {salary_month} created successfully")
        else:
            self.create_toast("Error", f"Request failed with status code {response.status_code}")

        # After creating the salary, show the salary page
        self.app.show_tasks_view()


class UpdateSalaryView(View):
    def __init__(self, app):
        super().__init__(app)
        self.salary_id_var = tb.StringVar()
        self.updated_month_var = tb.StringVar()
        self.updated_teacher_id_var = tb.StringVar()
        self.updated_description_var = tb.StringVar()
        self.updated_approval_var = tb.BooleanVar()
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self.frame, text="Salary ID:", font=(FONT_FAMILY, 15), bootstyle=PRIMARY).pack(padx=PM, pady=PS)
        tb.Entry(self.frame, textvariable=self.salary_id_var, width=40).pack(padx=PM, pady=PM)
        tb.Label(self.frame, text="Updated Month:", font=(FONT_FAMILY, 15), bootstyle=PRIMARY).pack(padx=PM, pady=PS)
        tb.Entry(self.frame, textvariable=self.updated_month_var, width=40).pack(padx=PM, pady=PM)
        tb.Label(self.frame, text="Updated Teacher ID:", font=(FONT_FAMILY, 15), bootstyle=PRIMARY).pack(padx=PM, pady=PS)
        tb.Entry(self.frame, textvariable=self.updated_teacher_id_var, width=40).pack(padx=PM, pady=PM)
        tb.Label(self.frame, text="Updated Description:", font=(FONT_FAMILY, 15), bootstyle=PRIMARY).pack(padx=PM, pady=PS)
        tb.Entry(self.frame, textvariable=self.updated_description_var, width=40).pack(padx=PM, pady=PM)
        tb.Label(self.frame, text="Updated Approval:", font=(FONT_FAMILY, 15), bootstyle=PRIMARY).pack(padx=PM, pady=PS)
        tb.Entry(self.frame, textvariable=self.updated_approval_var, width=40).pack(padx=PM, pady=PM)

        tb.Button(self.frame, text="Update Salary", command=self.update_salary, bootstyle=SUCCESS).pack(padx=PS, pady=PXS)
        tb.Button(self.frame, text="Back", command=self.app.show_tasks_view, bootstyle="outline dark").pack(padx=PS, pady=PXS)

    def update_salary(self):
        salary_id = int(self.salary_id_var.get())
        updated_month = self.updated_month_var.get()
        updated_teacher_id = self.updated_teacher_id_var.get()
        updated_description = self.updated_description_var.get()
        updated_approval_status = bool(self.updated_approval_var.get())
        headers = {'Content-Type': "application/json", "Authorization": f"Bearer {self.app.token['access_token']}"}
        data = {
            "complete": updated_approval_status,
            "description": updated_description,
            "priority": 1,
            "title": updated_month,
            "id": updated_teacher_id
        }
        response = req.put(f"{self.app.url}salaries/{salary_id}", data=dumps(data), headers=headers)

        if response.status_code == 204:
            self.create_toast("Salary Updated", f"Salary for {updated_month} updated successfully")
        else:
            self.create_toast("Error", f"Request failed with status code {response.status_code}")

        # After updating the salary, show the salary page
        self.app.show_tasks_view()

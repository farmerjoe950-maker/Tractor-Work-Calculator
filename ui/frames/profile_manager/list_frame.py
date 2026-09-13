import customtkinter as ctk
from ui.dialogs.profile_dialog import ProfilesDetailsDialog
from ui.dialogs.add_equipment import AddEquipmentProfiles
from ui.dialogs.delete_equipment import DeleteEquipmentDialog

class ProfileManagerFrame(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        profile_manager_module= None,
        **kwargs
    ):
        
        super().__init__(parent, **kwargs)
        self.pm = profile_manager_module

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.grid(
            row=0,
            column=0,
            pady=15,
            sticky="ew"
        )
        self.top_bar.grid_columnconfigure(0, weight=1)

        self.category_switch = ctk.CTkSegmentedButton(
            self.top_bar,
            values=["Tractors", "Implements"],
            command=self.on_category_changed
        )
        self.category_switch.set("Tractors")
        self.category_switch.grid(row=0, column=0)

        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0,15)
        )

        self.content_area.grid_columnconfigure(0, weight=2)
        self.content_area.grid_columnconfigure(1,weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        # LIST FRAME #

        self.list_frame = ctk.CTkScrollableFrame(
            self.content_area,
            label_text="Equipment Inventory"
        )
        self.list_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10),
            pady=0
        )
        self.list_frame.grid_columnconfigure(0, weight=1)

        # ACTION FRAME #

        self.action_frame = ctk.CTkFrame(
            self.content_area
        )
        self.action_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(0, 10),
            pady=0
        )
        self.action_frame.grid_columnconfigure(0, weight=1)

        self._build_action_panel()
        self.refresh_list()



    def _build_action_panel(self):
        title = ctk.CTkLabel(
            self.action_frame,
            text="Manage Equipment",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(padx=10, pady=15)

        self.add_button = ctk.CTkButton(
            self.action_frame,
            text="+ Add Profile",
            command=self.open_add_dialog,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.add_button.pack(padx=20, pady=10, fill="x")

        self.del_button = ctk.CTkButton(
            self.action_frame,
            text="- Delete Profile",
            command=self.delete_selected_equipment,
            fg_color="red",
            hover_color="darkred"
        )
        self.del_button.pack(padx=20, pady= 10, fill="x")

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        category = self.category_switch.get()

        if category == "Tractors":
            items = self.pm.load_tractors()
        else:
            items = self.pm.load_implements()

        for idx, (name, data) in enumerate(items.items()):
            card = ctk.CTkFrame(self.list_frame)
            card.grid(
                row=idx,
                column=0,
                sticky="ew",
                padx=5,
                pady=5
            )
            card.grid_columnconfigure(0, weight=1)

            name_button = ctk.CTkButton(
                card,
                text=name,
                anchor="w",
                fg_color="transparent",
                text_color=("black", "white"),
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda n=name, d=data: self.open_details_window(
                    n, d, category
                )
            )
            name_button.grid(
                row=0,
                column=0,
                sticky="w",
                padx=10,
                pady=(5, 0)
            )

            details_button = ctk.CTkButton(
                card,
                text="View Details",
                width=80,
                height=24,
                font=ctk.CTkFont(size=11),
                command=lambda n=name, d=data: self.open_details_window(
                    n, d, category
                )
            )
            details_button.grid(
                row=1,
                column=0,
                sticky="w",
                padx=10,
                pady=(2, 8)
            )

    def open_details_window(self, name, data, category):
        ProfilesDetailsDialog(
            parent=self,
            name=name,
            data=data,
            category=category
        )

    def open_add_dialog(self):
        category = self.category_switch.get()
        AddEquipmentProfiles(
            parent=self,
            category=category,
            profile_manager=self.pm,
            on_success_callback=self._on_data_updated
        )

    def delete_selected_equipment(self):
        category = self.category_switch.get()
        DeleteEquipmentDialog(
            parent=self,
            category=category,
            profile_manager=self.pm,
            on_success_callback=self._on_data_updated
        )

    def _on_data_updated(self):
        self.refresh_list()
        self._notify_app_refresh()

    def on_category_changed(self, value):
        self.refresh_list()

    def _notify_app_refresh(self):
        app_window = self.winfo_toplevel()
        if hasattr(app_window, "refresh_data"):
            app_window.refresh_data()
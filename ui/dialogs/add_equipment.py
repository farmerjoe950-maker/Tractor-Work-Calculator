import customtkinter as ctk

class AddEquipmentProfiles(ctk.CTkToplevel):
    def __init__(
            self,
            parent,
            category: str,
            profile_manager,
            on_success_callback=None,
            **kwargs
    ):
        super().__init__(parent, **kwargs)

        self.category = category
        self.pm = profile_manager
        self.on_success = on_success_callback

        item_type = category[:-1] if category.endswith("s") else category

        self.title(f"Add New {item_type}")
        self.geometry("300x520")
        self.attributes("-topmost", True)
        self.resizable(False, True)

        title_label = ctk.CTkLabel(
            self,
            text=f"New {item_type} Profile",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(15, 10))

        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.entries = {}
        self._build_fields()

        self.error_label = ctk.CTkLabel(
            self,
            text="",
            text_color="red"
        )
        self.error_label.pack(pady=(0, 5))

        save_button = ctk.CTkButton(
            self,
            text="Save Equipment",
            command=self._save_profile,
            fg_color="green",
            hover_color="darkgreen",
        )
        save_button.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

    def _build_fields(self):
        if self.category == "Tractors":
            fields = [
                ("name", "Name / Model:"),
                ("HP", "Horsepower (HP):"),
                ("fuel_burn_hour", "Fuel Burn (Gal/Hr):"),
                ("wear_cost", "Wear Cost ($/Hr):")
            ]
        else:
            fields = [
                ("name", "Name / Model:"),
                ("category", "Category (Mowing, Grading...):"),
                ("width", "Working Width (ft):"),
                ("speed", "Working Speed (mph):"),
                ("pto_speed", "PTO Speed (540/1000, 0 if N/A):"),
                ("min_hp", "Minimum Required HP:"),
                ("max_hp", "Maximum Allowed HP:"),
            ]

        for i, (key, label_text) in enumerate(fields):
            lbl = ctk.CTkLabel(
                self.form_frame,
                text=label_text,
                anchor="w",
                font=ctk.CTkFont(weight="bold")
            )
            lbl.pack(
                fill="x",
                padx=10,
                pady=(8, 2)
            )

            entry = ctk.CTkEntry(
                self.form_frame,
                placeholder_text=label_text
            )
            entry.pack(
                fill="x",
                padx=10,
                pady=(0, 5)
            )

            self.entries[key] = entry

    def _save_profile(self):
        self.error_label.configure(text="")

        name_val = self.entries["name"].get().strip()
        if not name_val:
            self.error_label.configure(text="Equipment Name is Required!")
            return

        try:
            if self.category == "Tractors":
                hp = float(self.entries["HP"].get() or 0)
                fuel = float(self.entries["fuel_burn_hour"].get() or 0)
                wear = float(self.entries["wear_cost"].get() or 0)

                self.pm.add_tractor_profile(
                    name=name_val,
                    HP=hp,
                    fuel_burn_hour=fuel,
                    wear_cost=wear
                )
            else:
                cat = self.entries["category"].get().strip() or "General"
                width = float(self.entries["width"].get() or 5)
                speed = float(self.entries["speed"].get() or 3.0)
                pto = float(self.entries["pto_speed"].get() or 0)
                min_hp = float(self.entries["min_hp"].get() or 0)
                max_hp = float(self.entries["max_hp"].get() or 0)

                self.pm.add_implement_profile(
                    name=name_val,
                    category=cat,
                    width=width,
                    speed=speed,
                    pto_speed=pto,
                    min_hp=min_hp,
                    max_hp=max_hp
                )

            if self.on_success:
                self.on_success()
                self.destroy()

        except ValueError:
            self.error_label.configure(text="Specs must be valid numbers!")

            

        
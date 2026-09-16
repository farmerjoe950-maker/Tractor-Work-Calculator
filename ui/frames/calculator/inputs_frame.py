import customtkinter as ctk
from modules.calculator import calculate_job_quote

class InputsFrame(ctk.CTkFrame):
    def __init__(
            self,
            parent,
            profile_manager= None,
            implements= None,
            tractors= None,
            on_calculate_callback= None,
            on_add_profile_callback= None,
            **kwargs
    ):
        super().__init__(parent, **kwargs)

        self.profile_manager = profile_manager
        self.implements = implements if implements is not None else {}
        self.tractors = tractors if tractors is not None else {}
        self.on_calculate_callback = on_calculate_callback
        self.on_add_profile_callback = on_add_profile_callback

        self._build_ui()

    def _build_ui(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(
            fill="x",
            padx= 20,
            pady= (10, 5)
        )

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Job Details",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.pack(side="left", anchor="w")

        self.help_button = ctk.CTkButton(
            self.header_frame,
            text= "?",
            width=28,
            height=28,
            corner_radius=14,
            font=ctk.CTkFont(size=14, weight="bold"),
            command= self._show_help_dialog
        )
        self.help_button.pack(side="right", anchor= "e")

        # JOB CATEGORY SELECTION #

        self.job_categories = self._extract_categories()

        self.job_frame = ctk.CTkFrame(self)
        self.job_frame.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        self.job_label = ctk.CTkLabel(
            self.job_frame,
            text="Select Job Category:",
            font=ctk.CTkFont(weight="bold")
        )
        self.job_label.pack(
            anchor="w",
            padx=15,
            pady=(10, 0)
        )

        self.job_dropdown = ctk.CTkOptionMenu(
            self.job_frame,
            values= self.job_categories if self.job_categories else ["No Categories"],
            command= self.on_category_change
        )
        self.job_dropdown.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        # TRACTOR SELECTION # 

        self.tractor_frame = ctk.CTkFrame(self)
        self.tractor_frame.pack(
            padx= 20,
            pady=5,
            fill="x"
        )

        self.tractor_label = ctk.CTkLabel(
            self.tractor_frame,
            text="Select Tractor:",
            font=ctk.CTkFont(weight="bold")
        )
        self.tractor_label.pack(
            anchor= "w",
            padx=15,
            pady=(10,0)
        )

        tractor_names = list(self.tractors.keys()) if self.tractors else ["No Tractors Found"]
        self.tractor_dropdown = ctk.CTkOptionMenu(
            self.tractor_frame,
            values=tractor_names
        )
        self.tractor_dropdown.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        # IMPLEMENT SELECTION #

        self.implement_frame = ctk.CTkFrame(self)
        self.implement_frame.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        self.implement_label = ctk.CTkLabel(
            self.implement_frame,
            text="Select Implement:",
            font=ctk.CTkFont(weight="bold")
        )
        self.implement_label.pack(
            anchor="w",
            padx=15,
            pady= (10, 0)
        )

        initial_category = self.job_dropdown.get()
        initial_implements = self._get_implements_for_category(initial_category)

        self.implement_dropdown = ctk.CTkOptionMenu(
            self.implement_frame,
            values=initial_implements
        )
        self.implement_dropdown.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        # JOB PARAMETERS #

        self.job_details_frame = ctk.CTkFrame(self)
        self.job_details_frame.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        self.job_details_frame.grid_columnconfigure((0, 1), weight=1)

        #ACRES#

        self.job_size_label = ctk.CTkLabel(
            self.job_details_frame,
            text="Job Size (Acres):",
            font=ctk.CTkFont(weight="bold")
        )
        self.job_size_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=(8, 0),
            sticky="w"
        )

        self.acres_entry = ctk.CTkEntry(
            self.job_details_frame,
            placeholder_text="5"
        )
        self.acres_entry.grid(
            row=1,
            column=0,
            padx=10,
            pady=(0, 8),
            sticky="ew"
        )

        #FUEl PRICE#

        self.fuel_price_label = ctk.CTkLabel(
            self.job_details_frame,
            text="Fuel Price ($/gal):",
            font=ctk.CTkFont(weight="bold")
        )
        self.fuel_price_label.grid(
            row=2,
            column=0,
            padx=10,
            pady=(8,0),
            sticky="w"
        )

        self.fuel_price_entry = ctk.CTkEntry(
            self.job_details_frame,
            placeholder_text="5"
        )
        self.fuel_price_entry.grid(
            row=3,
            column=0,
            padx=10,
            pady=(0, 8),
            sticky="ew"
        )

        #HOURLY RATE#

        self.hourly_rate_label = ctk.CTkLabel(
            self.job_details_frame,
            text="Hourly/Labor Rate ($/hr)",
            font=ctk.CTkFont(weight="bold")
        )
        self.hourly_rate_label.grid(
            row=4,
            column=0,
            padx=10,
            pady=(8, 0),
            sticky="w"
        )

        self.hourly_rate_entry = ctk.CTkEntry(
            self.job_details_frame,
            placeholder_text="30"
        )
        self.hourly_rate_entry.grid(
            row=5,
            column=0,
            padx=10,
            pady=(0, 8),
            sticky="ew"
        )

        #SPEED ENTRY#

        self.speed_label = ctk.CTkLabel(
            self.job_details_frame,
            text="Working Speed (MPH):",
            font=ctk.CTkFont(weight="bold")
        )
        self.speed_label.grid(
            row=0,
            column=1,
            padx=10,
            pady=(8, 0),
            sticky="w"
        )

        

        self.speed_entry = ctk.CTkEntry(
            self.job_details_frame,
            placeholder_text="5.0",
        )
        self.speed_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=(0, 8),
            sticky="ew"
        )

        #LOADING FEE#

        self.loading_fee_label = ctk.CTkLabel(
            self.job_details_frame,
            text="Loading Fee ($):",
            font=ctk.CTkFont(weight="bold")
        )
        self.loading_fee_label.grid(
            row=2,
            column=1,
            padx=10,
            pady=(8, 0),
            sticky="w"
        )

        self.loading_fee_entry = ctk.CTkEntry(
            self.job_details_frame,
            placeholder_text="50",
        )
        self.loading_fee_entry.grid(
            row=3,
            column=1,
            padx=10,
            pady=(0, 8),
            sticky="ew"
        )

        #MILEAGE#

        self.mileage_label = ctk.CTkLabel(
            self.job_details_frame,
            text="Round Trip Mileage (mi):",
            font=ctk.CTkFont(weight="bold")
        )
        self.mileage_label.grid(
            row=4,
            column=1,
            padx=10,
            pady=(8, 0),
            sticky="w"
        )

        self.mileage_entry = ctk.CTkEntry(
            self.job_details_frame,
            placeholder_text="10"
        )
        self.mileage_entry.grid(
            row=5,
            column=1,
            padx=10,
            pady=(0, 8),
            sticky="ew"
        )

        #MILEAGE RATE#

        self.mileage_rate_label = ctk.CTkLabel(
            self.job_details_frame,
            text="Mileage Rate ($/mi):",
            font=ctk.CTkFont(weight="bold")
        )
        self.mileage_rate_label.grid(
            row=6,
            column=1,
            padx=10,
            pady=(8, 0),
            sticky="w"
        )

        self.mileage_rate_entry = ctk.CTkEntry(
            self.job_details_frame,
            placeholder_text="0.76"
        )
        self.mileage_rate_entry.grid(
            row=7,
            column=1,
            padx=10,
            pady=(0, 8),
            sticky="ew"
        )

        # CALCULATE BUTTON # 

        self.calc_button = ctk.CTkButton(
            self,
            text="Calculate Quote",
            font=ctk.CTkFont(weight="bold", size=14),
            command=self.on_calculate_click
        )
        self.calc_button.pack(padx=20, pady= 15, fill="x")

        # HELPER AND REFRESH METHODS #

    def _extract_categories(self) -> list:
        implements_dict = self._get_implements_dict() if callable(self.implements) else self.implements
        if not implements_dict:
            return []
        categories = set()
        for impl in implements_dict.values():
            if isinstance(impl, dict):
                categories.add(impl.get("category", "Uncategorized"))
        return sorted(list(categories))

    def _get_implements_dict(self) -> dict:
        if callable(self.implements):
            res = self.implements()
            return res if isinstance(res, dict) else {}
        return self.implements if isinstance(self.implements, dict) else {}

    def _get_implements_for_category(self, category: str) -> list:
        implements_dict = self._get_implements_dict()
        matching = [
            name for name, data in implements_dict.items()
            if data.get("category", "Uncategorized") == category
        ]
        return matching if matching else (list(implements_dict.keys())or ["No Implements Found"])

    def _get_implement_speed(self, implement_name: str) -> float:
        implements_dict = self._get_implements_dict()
        implement_data = implements_dict.get(implement_name, {})
        return implement_data.get("speed", 5.0)

    def _sync_speed_entry(self, implement_name: str):
        speed = self._get_implement_speed(implement_name)
        self._set_entry_value(self.speed_entry, speed)

    def update_profiles(self, new_tractors: dict, new_implements: dict):
        self.tractors = new_tractors
        self. implements = new_implements

        self.job_categories = self._extract_categories()
        cat_values = self.job_categories if self.job_categories else ["No Categories"]
        self.job_dropdown.configure(values=cat_values)
        if cat_values:
            self.job_dropdown.set(cat_values[0])

        trac_values = list(self.tractors.keys()if self.tractors else ["No Tractors Found"])
        self.tractor_dropdown.configure(values=trac_values)
        if trac_values:
            self.tractor_dropdown.set(trac_values[0])

        self.on_category_change(self.job_dropdown.get())

    def _show_help_dialog(self):
        help_window = ctk.CTkToplevel(self)
        help_window.title("How to Use Calculator")
        help_window.geometry("400x320")
        help_window.transient(self.winfo_toplevel())
        help_window.grab_set()

        label = ctk.CTkLabel(
            help_window,
            text= "User Guide",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        label.pack(pady=(15, 10))

        instructions = (
            "1. Select Job Category.\n\n"
            "2. Choose your Tractor and Implement. \n\n"
            "3. Enter Job Size, Fuel Cost, and your Hourly Rate. \n\n"
            "4. Click 'Calculate Quote to generate the total estimate.\n\n"
            "The app pulls all the numbers from your tractor and implement profiles"
            "and calculates the estimated price to do the job."
        )

        text_msg = ctk.CTkLabel(
            help_window,
            text= instructions,
            justify="left",
            wraplength=350
        )
        text_msg.pack(padx=20, pady=10)

        close_btn = ctk.CTkButton(
            help_window,
            text="Got It",
            width=100,
            command=help_window.destroy
        )
        close_btn.pack(pady=(10, 15))

        # SET ENTRY VALUE FUNCTION

    def _set_entry_value(
            self, entry_widget: ctk.CTkEntry,
            value
    ):
        entry_widget.delete(0, "end")
        entry_widget.insert(0, str(value))

        # UPDATE IMPLEMENT SPEED #

        # CATEGORY CHANGE FUNTION #

    def on_category_change(self, selected_category: str):
        matching_implements = self._get_implements_for_category(selected_category)
        self.implement_dropdown.configure(values=matching_implements)
        if matching_implements:
            self.implement_dropdown.set(matching_implements[0])
            self._sync_speed_entry(matching_implements[0])

    def on_implement_change(self, selected_implement: str):
        self._sync_speed_entry(selected_implement)        

        # CALL CALCULATE FUNCTION # 

    def on_calculate_click(self):
        try:
            acres = float(self.acres_entry.get())
            fuel_price = float(self.fuel_price_entry.get())
            hourly_rate = float(self.hourly_rate_entry.get())
            speed = float(self.speed_entry.get())
            loading_fee = float(self.loading_fee_entry.get())
            round_trip_miles = float(self.mileage_entry.get())
            if acres <= 0:
                if self.on_calculate_callback:
                    self.on_calculate_callback({
                        "status": "error",
                        "message": "Error: Job size (acres) must be greater that 0."
                    })
                return
        except ValueError:
            if self.on_calculate_callback:
                self.on_calculate_callback({
                    "status": "error",
                    "message": "Error: Please enter valid numbers for Acres, Fuel Price, and Hourly Rate"
                })
            return

        selected_implement_name = self.implement_dropdown.get()
        selected_tractor_name = self.tractor_dropdown.get()

        implement_data = self.implements.get(selected_implement_name, {})
        tractor_data = self.tractors.get(selected_tractor_name, {})

        speed = implement_data.get("speed", implement_data.get("speed", 5.0))
        width = implement_data.get("width", 10.0)
        try:
            res = calculate_job_quote(
                acres=acres,
                fuel_price=fuel_price,
                hourly_rate=hourly_rate,
                speed=speed,
                width=width,
                implement_data=implement_data,
                tractor_data=tractor_data,
                loading_fee=loading_fee,
                round_trip_miles=round_trip_miles
            )

        except Exception as e:
            if self.on_calculate_callback:
                self.on_calculate_callback({
                    "status": "error",
                    "message": f"Calculation Error: {e}"
                })
            return

        report = []
        if res["hp_warning_low"]:
            report.append(
                f" WARNING: Selected tractor ({res['tractor_hp']} PTO HP) is"
                f" underpowered for {selected_implement_name} (Requires {res['min_hp']} HP)!\n"
            )
        if res["hp_warning_high"]:
            report.append(
                f" WARNING: Selected tractor ({res['tractor_hp']} PTO HP) is"
                f" overpowered for {selected_implement_name} (Requires {res['max_hp']} HP)!\n"
            )
        if res.get("implement_pto_speed"):
            report.append(
                f" REMINDER: This implement is set up for"
                f" {res['implement_pto_speed']} RPM! Please verify PTO speed before operation\n"
            )

        report.extend([
           "JOB QUOTE REPORT",
           f" GRAND TOTAL: $ {res.get('total_quote', 0): .2f} "
        ])

        if self.on_calculate_callback:
            self.on_calculate_callback({
                "status": "success",
                "message": "\n".join(report),
                "results": res
        })                    

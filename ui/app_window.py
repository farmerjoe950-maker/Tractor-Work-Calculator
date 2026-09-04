import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
import customtkinter as ctk
from modules.calculator import calculate_job_quote

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class TractorCalculatorApp(ctk.CTk): 
    def __init__(self, tractors= None, implements= None, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.title("Tractor Work Calculator & Estimator")
        self.geometry("600x1000")
        self.resizable(False, False)
        self.tractors = tractors if tractors is not None else {}
        self.implements = implements if implements is not None else {}
        self.header_label = ctk.CTkLabel(
            self,
            text= "Tractor Work Calculator",
            font= ctk.CTkFont(size= 24, weight= "bold"),
        )
        self.header_label.pack(pady= (20, 10))

        # Job Selection Frame

        self.job_categories = list(
            set(
                impl.get("specs", {}).get("category", "Uncategorized") 
                for impl in self.implements.values()
            )
        )
        self.job_frame = ctk.CTkFrame(self)
        self.job_frame.pack(
            padx= 20,
            pady= (10),
            fill= "x"
        )
        self.job_label = ctk.CTkLabel(
           self.job_frame,
           text= "Select Job",
           font= ctk.CTkFont(weight= "bold")
        )
        self.job_label.pack(anchor= "w", padx= 15, pady= (10,0))
        
        self.job_dropdown = ctk.CTkOptionMenu(
           self.job_frame, 
           values= self.job_categories, 
           command= self.on_category_change
        )
        self.job_dropdown.pack(fill= "x", padx= 15, pady= (0,10))

        # Tractor Selection Frame

        self.equip_frame = ctk.CTkFrame(self)
        self.equip_frame.pack(
            padx= 20,
            pady= 10,
            fill= "x"
        )
        self.tractor_label = ctk.CTkLabel(
            self.equip_frame,
            text= "Select Tractor:",
            font= ctk.CTkFont(weight= "bold")
        )
        self.tractor_label.pack(anchor= "w", padx=15, pady=(10,0))
        tractor_names = list(self.tractors.keys())
        self.tractor_dropdown = ctk.CTkOptionMenu(
            self.equip_frame, values = tractor_names
        )
        self.tractor_dropdown.pack(fill="x", padx= 15, pady=(0,10))

        # Implement Selection Frame

        self.equip_frame = ctk.CTkFrame(self)
        self.equip_frame.pack(
            padx= 20,
            pady= 10,
            fill= "x"
        )
        initial_category = self.job_categories[0] if self.job_categories else ""
        initial_implements = [
            name 
            for name, data in self.implements.items()
            if data.get("specs", {}).get("category", "Uncategorized") 
            == initial_category
        ]
        self.implement_label = ctk.CTkLabel(
            self.equip_frame,
            text= "Select Implement:",
            font= ctk.CTkFont(weight= "bold")
        )
        self.implement_label.pack(anchor= "w", padx= 15, pady=(10,0))
        
        self.implement_dropdown = ctk.CTkOptionMenu(
            self.equip_frame, values = initial_implements
        )
        self.implement_dropdown.pack(fill= "x", padx= 15, pady=(0,10))

        #Job Details Frame

        self.job_details_frame = ctk.CTkFrame(self)
        self.job_details_frame.pack(
            padx= 20,
            pady= 10,
            fill= "x"
        )
        self.job_size_label = ctk.CTkLabel(
            self.job_details_frame,
            text= "Job Size (Acres):",
            font= ctk.CTkFont(weight= "bold")
        )
        self.job_size_label.pack(
            anchor= "w",
            padx= 15,
            pady= (0,10)
        )
        self.acres_entry = ctk.CTkEntry(
            self.job_details_frame,
            placeholder_text= "5"
        )
        self.acres_entry.pack(
            fill= "x",
            padx= 15,
            pady= (0,10)
        )
        self.fuel_price_label = ctk.CTkLabel(
            self.job_details_frame,
            text= "Fuel Price ($/gal):",
            font= ctk.CTkFont(weight= "bold")
        )
        self.fuel_price_label.pack(
            anchor= "w",
            padx= 15,
            pady= (5,0)
        )
        self.fuel_entry = ctk.CTkEntry(
            self.job_details_frame,
            placeholder_text= "4.50"
        )
        self.fuel_entry.pack(
           fill= "x",
           padx= 15,
           pady= (0,5) 
        )
        self.hourly_rate_label = ctk.CTkLabel(
            self.job_details_frame,
            text= "Hourly Rate ($/hr):",
            font= ctk.CTkFont(weight= "bold")
        )
        self.hourly_rate_label.pack(
            anchor= "w",
            padx= 15,
            pady= (5,0)
        )
        self.hourly_entry = ctk.CTkEntry(self.job_details_frame)
        self.hourly_entry.insert(0, "45")
        self.hourly_entry.pack(
            fill= "x",
            padx= 15,
            pady= (5,0)
        )

        # Calculate button

        self.calc_button = ctk.CTkButton(
            self,
            text= "Calculate Quote",
            font= ctk.CTkFont(weight= "bold", size= 14),
            command=self.on_calculate_click
        )
        self.calc_button.pack(
            padx= 20,
            pady= 15,
            fill= "x"
        )

        # Results Box

        self.results_box = ctk.CTkTextbox(
            self,
            height= 450,
            font= ctk.CTkFont(size= 14)
        )
        self.results_box.pack(
            padx= 20,
            pady= (0,20),
            fill= "both",
            expand= True
        )
        self.results_box.insert(
           "1.0", "Please select your equipment, enter job specs, and click Calculate."
        )

    # Category Chanege

    def on_category_change(self, selected_category):
        matching_implements = [
            name 
            for name, data in self.implements.items()
            if data.get("specs", {}).get("category", "Uncategorized") 
            == selected_category
        ]
        self. implement_dropdown.configure(values= matching_implements)
        if matching_implements:
            self.implement_dropdown.set(matching_implements[0])

    # Results #

    def on_calculate_click(self):
        self.results_box.delete("1.0", "end")
        try:
            acres = float(self.acres_entry.get())
            fuel_price = float(self.fuel_entry.get())
            hourly_rate = float(self.hourly_entry.get())
            print(f"Inputs Parsed: acres={acres}, fuel={fuel_price}, rate= {hourly_rate}")
            if acres <= 0:
                self.results_box.insert(
                    "1.0", "Error: Job size (acres) must be greater that 0."
                )
                return
        except ValueError:
            print(f"parsing failed {e}")
            self.results_box.insert(
                "1.0",
                "Error: Please enter valid numbers for Acres, Fuel Price, and Hourly Rate"
            )
            return

        selected_implement_name = self.implement_dropdown.get()
        selected_tractor_name = self.tractor_dropdown.get()
        print(f"selected Dropdowns: tractors= '{selected_tractor_name}', implements = '{selected_implement_name}'")

        print(f"Available implement keys: {list(self.implements.keys())}")
        print(f"Available Tracotr keys: {list(self.tractors.keys())}")

        implement_data = self.implements.get(selected_implement_name, {}).get("specs", {})
        tractor_data = self.tractors.get(selected_tractor_name, {}).get("specs", {})
        print(f" Retrieved implement_data: {implement_data}")
        print(f"Retrieved tractor_data: {tractor_data}")
        speed = implement_data.get("working_speed_mph", implement_data.get("speed", 5.0))
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
            )

            print(f"Calculation Result: {res}")
        except Exception as e:
            print(f"CRASH inside calculate_job_quote: {e}")
            self.results_box.insert("1.0", f"Calculation Error: {e}")
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

        self.results_box.insert("1.0", "\n" .join(report))


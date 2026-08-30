import customtkinter as ctk
from modules.profile_manager import(
    load_implements,
    load_tractors
)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class TractorCalculatorApp(ctk.CTk): 
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.title("Tractor Work Calculator & Estimator")
        self.geometry("600x700")
        self.resizable(False, False)
        self.tractors = load_tractors()
        self.implements = load_implements()
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

    def on_calculate_click(self):
        ## button handler ##
        pass

if __name__ == "__main__":
    app = TractorCalculatorApp()
    app.mainloop()

#implement_names = list(self.implements.keys())

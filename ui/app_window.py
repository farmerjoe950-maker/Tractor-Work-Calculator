import customtkinter as ctk
from modules import profile_manager
from ui.frames.calculator.inputs_frame import InputsFrame
from ui.frames.calculator.results_frame import ResultsFrame
from ui.frames.profile_manager.list_frame import ProfileManagerFrame

class TractorCalculatorApp(ctk.CTk):
    def __init__(self, fg_color= None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.title("Tractor Work Calculator & Estimator")
        self.geometry("650x950")
        self.resizable(True, True)

        self.tractors = profile_manager.load_tractors()
        self.implements = profile_manager.load_implements()

        self.header_label = ctk.CTkLabel(
            self, 
            text= "Tractor Work Calculator",
            font= ctk.CTkFont(size= 24, weight= "bold")
        )
        self.header_label.pack(pady= (20, 10))

        # NAVIGATION TAB

        self.tab_view= ctk.CTkTabview(self)
        self.tab_view.pack(
            fill="both", 
            expand=True,
            padx=15,
            pady=10
        )
        self.tab_calculator = self.tab_view.add("Calculator")
        self.tab_profiles = self.tab_view.add("Equipment Manager")
        #self.tab_settings = self.tab_view.add("Settings")

        # SCROLL FRAME # 

        self.calculator_scroll = ctk.CTkScrollableFrame(self.tab_calculator)
        self.calculator_scroll.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # INPUTS FRAME #

        self.inputs_frame = InputsFrame(
            parent=self.calculator_scroll,
            profile_manager= profile_manager,
            implements= self.implements,
            tractors= self.tractors,
            on_calculate_callback= self.handle_calculation_results
        )
        self.inputs_frame.pack(
            side="top",
            fill= "both",
            padx= 10,
            pady= 10
        )

        self.results_frame = ResultsFrame(
            parent= self.calculator_scroll
        )
        self.results_frame.pack(
            side="top",
            fill="both",
            expand=True,
            padx=10,
            pady=(5, 10)
        )


        # PROFILE MANAGER #

        self.profile_manager = ProfileManagerFrame(
            parent=self.tab_profiles,
            profile_manager_module=profile_manager
        )
        self.profile_manager.pack(fill="both", expand= True)

        # SETTINGS TAB #

        #self.settings_placeholder = ctk.CTkLabel(
        #   self.tab_settings,
         #   text="Settings",
        #    font=ctk.CTkFont(size=16)
        #)
        #self.settings_placeholder.pack(expand= True)

    def refresh_data(self):
        self.tractors = profile_manager.load_tractors()
        self.implements = profile_manager.load_implements()

        if hasattr(self.inputs_frame, "update_profiles"):
            self.inputs_frame.update_profiles(self.tractors, self.implements)

    def handle_calculation_results(self, payload: dict):
        self.results_frame.display_results(payload)
        print("Calculation Results Recieved in AppWindow:")

    





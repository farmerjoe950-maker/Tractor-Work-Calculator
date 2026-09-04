import customtkinter as ctk

class InputsFrame(ctk.CTkFrame):
    def __init__(
            self,
            parent,
            data_manager,
            on_calculate_callback, 
            on_add_profile_callback= None
    ):
        super().__init__(parent)
        self.data_manager = data_manager 
        self.on_calculate_callback= on_calculate_callback
        self.on_add_profile_callback= on_add_profile_callback

         

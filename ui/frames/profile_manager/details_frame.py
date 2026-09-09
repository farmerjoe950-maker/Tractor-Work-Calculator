import customtkinter as ctk
from modules import profile_manager as pm

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
        self.grid_rowconfigure(0, weight=1)

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_selector()
        self._build_content_area()

        self.refresh_ui()

    def _build_header(self):
        title =  ctk.CTkLabel(
            self.scroll_frame,
            text="Equipment Manager",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(
            row=0,
            column=0,
            pady=(0,10), 
            sticky="w"
        )

    def _build_selector(self):
        self.category_switch = ctk.CTkSegmentedButton(
            self.scroll_frame,
            values=["Tractors", "Implements"],
            command=self.on_category_changed
        )
        self.category_switch.set("Tractors")
        self.category_switch.grid(
            row=1,
            column=0,
            pady=(0, 15),
            sticky="ew"
        )

    def _build_content_area(self):
        self.content_container = ctk.CTkFrame(self.scroll_frame)
        self.content_container.grid(
            row=2
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )
        self.content_container.grid_columnconfigure(0, weight=1)

    def on_category_changed(self, value):
        print(f"Switched category to: {value}")
        self.refresh_ui

    def refresh_ui(self):

        pass
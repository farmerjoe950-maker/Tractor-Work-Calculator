import customtkinter as ctk

class ProfilesDetailsDialog(ctk.CTkToplevel):
    def __init__(
            self,
            parent,
            name: str,
            data: dict,
            category: str,
            **kwargs
    ):
        super().__init__(parent, **kwargs)

        self.title (f"{category} Details - {name}")
        self.geometry("350x320")
        self.attributes("-topmost", True)
        self.resizable(False, False)

        title_label = ctk.CTkLabel(
            self,
            text=name,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 15), padx=20)

        specs_frame = ctk.CTkFrame(self)
        specs_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        for key, value in data.items():
            formatted_key = key.replace("_", "").title()
            spec_label = ctk.CTkLabel(
                specs_frame,
                text=f"{formatted_key}: {value}",
                font=ctk.CTkFont(size=13),
                anchor="w"
            )
            spec_label.pack(pady=4, padx=15, fill="x")

        close_button = ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy,
            width=100
        )
        close_button.pack(pady=(0, 15))

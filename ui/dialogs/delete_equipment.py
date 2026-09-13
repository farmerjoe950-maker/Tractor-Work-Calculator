import customtkinter as ctk

class DeleteEquipmentDialog(ctk.CTkToplevel):
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
        self.on_success_callback = on_success_callback

        item_type = category[:-1] if category.endswith("s") else category

        self.title(f"Delete {item_type}")
        self.geometry("360x240")
        self.attributes("-topmost", True)
        self.resizable(False, False)

        items_dict = (
            self.pm.load_tractors()
            if category == "Tractors"
            else self.pm.load_implements()
        )
        self.item_names = list(items_dict.keys())

        title_label = ctk.CTkLabel(
            self,
            text=f"Remove a {item_type}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 10))

        if not self.item_names:
            empty_label = ctk.CTkLabel(
                self,
                text=f"No {category.lower()} available to delete."
            )
            empty_label.pack(pady=20)

            close_button = ctk.CTkButton(
                self,
                text="Close",
                command=self.destroy,
                width=100
            )
            close_button.pack(pady=10)
            return

        subtitle_label = ctk.CTkLabel(
            self,
            text="Select equipment profile to permanently delete:"
        )
        subtitle_label.pack(pady=(0, 10))

        self.dropdown = ctk.CTkOptionMenu(
            self,
            values=self.item_names
        )
        self.dropdown.pack(
            fill="x",
            padx=20,
            pady=10
        )

        delete_button = ctk.CTkButton(
            self,
            text=f"Delete {item_type}",
            command=self._delete_profile,
            fg_color="red",
            hover_color="darkred"
        )
        delete_button.pack(
            fill="x",
            padx=20,
            pady=(15, 20)
        )

    def _delete_profile(self):
        selected_name = self.dropdown.get()

        if selected_name:
            if self.category == "Tractors":
                self.pm.delete_tractor_profile(selected_name)
            else:
                self.pm.delete_implements_profiles(selected_name)

            if self.on_success_callback:
                self.on_success_callback()
            self.destroy()
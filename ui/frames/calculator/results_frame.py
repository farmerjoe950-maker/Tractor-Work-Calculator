import customtkinter as ctk

class ResultsFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self._build_ui()

    def _build_ui(self):
       self.header_label = ctk.CTkLabel(
           self,
           text="Results Breakdown",
           font=ctk.CTkFont(size=16, weight="bold")
       )
       self.header_label.pack(anchor="w", padx=15, pady=(10, 5))

       self.table_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray15"))
       self.table_frame.pack(
           fill="both",
           expand=True,
           padx=15,
           pady=10
       )

       self.table_frame.grid_columnconfigure(0, weight=1)
       self.table_frame.grid_columnconfigure(1, weight=1)

       self.display_placeholder()

    def display_placeholder(self):
        for child in self.table_frame.winfo_children():
            child.destroy()

        placeholder = ctk.CTkLabel(
            self.table_frame,
            text="Enter Job Details and click 'Calculate Quote' to generate quote brakdown.",
            font=(ctk.CTkFont(slant="italic"))
        )
        placeholder.grid(
            row=0,
            column= 0,
            columnspan=2,
            padx=20,
            pady=30
        )

    def display_results(self, payload: dict):
        for child in self.table_frame.winfo_children():
            child.destroy()

        if payload.get("status") == "error":
            err_label = ctk.CTkLabel(
                self.table_frame,
                text=f"!!! {payload.get('massage', 'An error occurred')}",
                text_color="#E74C3C",
                wraplength=350,
                justify="left"
            )
            err_label.grid(
                row=0,
                column=0,
                columnspan=2,
                padx=15,
                pady=20
            )
            return

        res = payload.get("results", {})
        row_idx = 0

        report_message = payload.get("message", "")
        if "WARNING" in report_message or "REMINDER" in report_message:
            warning_box = ctk.CTkFrame(
                self.table_frame,
                fg_color=("gray80", "gray25")
            )
            warning_box.grid(
                row=row_idx,
                column=0,
                columnspan=2,
                padx=10,
                pady=(10, 5),
                sticky= "ew"
            )

            warning_lines = [line for line in report_message.split("\n") if "WARNING" in line or "REMINDER" in line]
            for line in warning_lines:
                w_lbl = ctk.CTkLabel(
                    warning_box,
                    text=line.strip(),
                    text_color="#E67E22" if "WARNING" in line else "#3498DB",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    wraplength=350,
                    justify="left"
                )
                w_lbl.pack(anchor="w", padx=10, pady= 3)

            row_idx += 1

        items = [
            ("Fuel Cost", f"${res.get('fuel_cost', 0):,.2f}"),
            ("Hourly/Labor Cost", f"${res.get('labor_cost', 0):,.2f}"),
            ("Equipment Wear", f"${res.get('wear_cost', 0):,.2f}"),
            ("Estimated Time", f"{res.get('total_hours', 0):.2f} hrs"),
        ]

        for label_text, val_text in items:
            lbl = ctk.CTkLabel(
                self.table_frame,
                text=label_text,
                font=ctk.CTkFont(weight="bold")
            )
            lbl.grid(
                row=row_idx,
                column=0,
                padx= 15,
                pady=6,
                sticky="w"
            )

            val = ctk.CTkLabel(
                self.table_frame,
                text=val_text
            )
            val.grid(
                row=row_idx,
                column=1,
                padx=15,
                pady=6,
                sticky="e"
            )
            row_idx +=1

        divider = ctk.CTkFrame(
            self.table_frame,
            height=2,
            fg_color="gray50"
        )
        divider.grid(
            row=row_idx,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=5
        )
        row_idx += 1

        total_label = ctk.CTkLabel(
            self.table_frame,
            text="Grand Total:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        total_label.grid(
            row=row_idx,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        grand_total = res.get("total_quote", 0.0)
        total_val = ctk.CTkLabel(
            self.table_frame,
            text=f"${grand_total:,.2f}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2FA572"
        )
        total_val.grid(
            row=row_idx,
            column=1,
            padx=15,
            pady=10,
            sticky="e"
        )


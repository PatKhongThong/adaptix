import customtkinter as ctk
import threading
import time
from collector import AdaptixCollector

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AdaptixApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Adaptix AI")
        self.geometry("800x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ADAPTIX", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.status_label = ctk.CTkLabel(self.sidebar_frame, text="Status: IDLE", text_color="gray")
        self.status_label.grid(row=1, column=0, padx=20, pady=10)

        # Provider Selection
        self.provider_label = ctk.CTkLabel(self.sidebar_frame, text="AI Provider:", font=ctk.CTkFont(size=12))
        self.provider_label.grid(row=2, column=0, padx=20, pady=(10, 0))

        self.provider_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Gemini", "OpenAI"])
        self.provider_menu.grid(row=3, column=0, padx=20, pady=(0, 10))

        self.api_key_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="API Key", show="*")
        self.api_key_entry.grid(row=4, column=0, padx=20, pady=10)

        self.start_button = ctk.CTkButton(self.sidebar_frame, text="Start Observing", command=self.toggle_observing)
        self.start_button.grid(row=5, column=0, padx=20, pady=10)

        self.summary_button = ctk.CTkButton(self.sidebar_frame, text="Summarize Session", command=self.generate_summary, state="disabled")
        self.summary_button.grid(row=6, column=0, padx=20, pady=10)

        # Main Content
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.header_label = ctk.CTkLabel(self.main_frame, text="Behavior Timeline (2s interval)", font=ctk.CTkFont(size=20, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=(10, 20), sticky="w")

        self.log_textbox = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(size=14))
        self.log_textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.is_observing = False
        self.collector = None
        self.session_insights = []

    def toggle_observing(self):
        if not self.is_observing:
            api_key = self.api_key_entry.get()
            provider = self.provider_menu.get().lower()
            if not api_key:
                self.log_msg("System: Please enter an API key.")
                return

            self.collector = AdaptixCollector(api_key=api_key, provider=provider)
            self.is_observing = True
            self.session_insights = []
            self.start_button.configure(text="Stop Observing", fg_color="red")
            self.summary_button.configure(state="disabled")
            self.status_label.configure(text="Status: OBSERVING", text_color="green")
            self.log_msg("System: Observer started (2s snapshots).")
            threading.Thread(target=self.observation_loop, daemon=True).start()
        else:
            self.is_observing = False
            self.start_button.configure(text="Start Observing", fg_color=["#3B8ED0", "#1F6AA5"])
            self.summary_button.configure(state="normal")
            self.status_label.configure(text="Status: IDLE", text_color="gray")
            self.log_msg("System: Observer stopped.")

    def generate_summary(self):
        if not self.session_insights:
            self.log_msg("System: No data to summarize yet.")
            return

        self.log_msg("System: Generating session summary...")
        threading.Thread(target=self._summary_thread, daemon=True).start()

    def _summary_thread(self):
        try:
            summary = self.collector.summarize_session(self.session_insights)
            self.log_msg("\n--- SESSION SUMMARY ---")
            self.log_msg(summary)
            self.log_msg("-----------------------\n")
        except Exception as e:
            self.log_msg(f"Error: {str(e)}")

    def log_msg(self, msg):
        timestamp = time.strftime("[%H:%M:%S] ")
        self.log_textbox.insert("end", timestamp + msg + "\n")
        self.log_textbox.see("end")

    def observation_loop(self):
        while self.is_observing:
            try:
                insight = self.collector.analyze_behavior()
                self.session_insights.append(insight)
                self.log_msg(f"AI: {insight}")
            except Exception as e:
                self.log_msg(f"Error: {str(e)}")

            # Wait for 2 seconds
            for _ in range(2):
                if not self.is_observing:
                    break
                time.sleep(1)


if __name__ == "__main__":
    app = AdaptixApp()
    app.mainloop()

import customtkinter as ctk
import threading
import time
import json
from collector import AdaptixCollector

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AdaptixApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Adaptix AI - Hyper-Fast Behavior Study")
        self.geometry("900x700")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Load Preferences
        self.config = self.load_config()
        default_provider = self.config.get("default_provider", "Gemini").capitalize()

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ADAPTIX", font=ctk.CTkFont(size=28, weight="bold", family="Outfit"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.status_card = ctk.CTkFrame(self.sidebar_frame, corner_radius=10, fg_color="#2b2b2b")
        self.status_card.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.status_label = ctk.CTkLabel(self.status_card, text="● IDLE", text_color="#888888", font=ctk.CTkFont(size=14, weight="bold"))
        self.status_label.pack(padx=10, pady=10)

        # Provider Selection
        self.provider_label = ctk.CTkLabel(self.sidebar_frame, text="AI PROVIDER", font=ctk.CTkFont(size=11, weight="bold", family="Outfit"))
        self.provider_label.grid(row=2, column=0, padx=20, pady=(20, 0))

        self.provider_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Gemini", "OpenAI", "DeepSeek"], fg_color="#333333", button_color="#444444")
        self.provider_menu.set(default_provider)
        self.provider_menu.grid(row=3, column=0, padx=20, pady=(5, 20))

        self.start_button = ctk.CTkButton(self.sidebar_frame, text="START OBSERVING", font=ctk.CTkFont(size=13, weight="bold"), height=40, corner_radius=20, command=self.toggle_observing)
        self.start_button.grid(row=4, column=0, padx=20, pady=10)

        self.summary_button = ctk.CTkButton(self.sidebar_frame, text="GENERATE REPORT", font=ctk.CTkFont(size=13, weight="bold"), height=40, corner_radius=20, fg_color="transparent", border_width=2, command=self.generate_summary, state="disabled")
        self.summary_button.grid(row=5, column=0, padx=20, pady=10)

        self.info_label = ctk.CTkLabel(self.sidebar_frame, text="Privacy Active: Local Analysis", font=ctk.CTkFont(size=10), text_color="gray")
        self.info_label.grid(row=6, column=0, padx=20, pady=(50, 10))

        # Main Content
        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#121212")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.header_label = ctk.CTkLabel(self.main_frame, text="BEHAVIOR TIMELINE", font=ctk.CTkFont(size=18, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=30, pady=(30, 20), sticky="w")

        self.log_textbox = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(size=13, family="Consolas"), fg_color="#1a1a1a", border_width=1, border_color="#333333")
        self.log_textbox.grid(row=1, column=0, padx=30, pady=(0, 30), sticky="nsew")

        self.is_observing = False
        self.collector = None
        self.session_insights = []

    def load_config(self):
        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def toggle_observing(self):
        if not self.is_observing:
            provider = self.provider_menu.get().lower()

            self.collector = AdaptixCollector(provider=provider)
            self.is_observing = True
            self.session_insights = []
            self.start_button.configure(text="STOP OBSERVING", fg_color="#d9534f", hover_color="#c9302c")
            self.summary_button.configure(state="disabled")
            self.status_label.configure(text="● OBSERVING", text_color="#5cb85c")
            self.log_msg("System: Adaptive observation started (2s snapshots).")
            threading.Thread(target=self.observation_loop, daemon=True).start()
        else:
            self.is_observing = False
            self.start_button.configure(text="START OBSERVING", fg_color=["#3B8ED0", "#1F6AA5"], hover_color=["#2B7EB0", "#0F5A95"])
            self.summary_button.configure(state="normal")
            self.status_label.configure(text="● IDLE", text_color="#888888")
            self.log_msg("System: Observation stopped. Summary available.")

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
                if insight.startswith("SKIP:"):
                    # Log skip to UI but don't add to AI session insights
                    self.log_msg(f"System: {insight} (API Saved)")
                else:
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
